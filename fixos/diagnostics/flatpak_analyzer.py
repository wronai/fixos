"""
Advanced Flatpak analyzer for fixOS

Analyzes Flatpak installations to find:
- Unused runtimes (not referenced by any installed app)
- Orphaned applications (no longer in remote)
- Leftover data from uninstalled apps
- Old versions of runtimes/apps
- Large individual applications
"""

from __future__ import annotations

import json
import subprocess
from dataclasses import dataclass
from typing import Dict, List, Optional, Any
from enum import Enum


class FlatpakItemType(Enum):
    APP = "app"
    RUNTIME = "runtime"
    DATA = "data"  # Leftover data directory


@dataclass
class FlatpakItemInfo:
    """Detailed info about a Flatpak item (app, runtime, or data)"""
    ref: str  # Full ref (e.g., com.discordapp.Discord/stable)
    name: str  # Short name
    item_type: FlatpakItemType
    size_bytes: int
    size_human: str
    is_used: bool  # Is referenced by installed apps
    description: str = ""
    install_date: Optional[str] = None
    origin: Optional[str] = None  # Remote origin
    arch: Optional[str] = None
    branch: Optional[str] = None
    can_cleanup: bool = True
    cleanup_command: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "ref": self.ref,
            "name": self.name,
            "type": self.item_type.value,
            "size_bytes": self.size_bytes,
            "size_human": self.size_human,
            "is_used": self.is_used,
            "description": self.description,
            "install_date": self.install_date,
            "origin": self.origin,
            "arch": self.arch,
            "branch": self.branch,
            "can_cleanup": self.can_cleanup,
            "cleanup_command": self.cleanup_command,
        }


class FlatpakAnalyzer:
    """Advanced analyzer for Flatpak cleanup decisions"""
    
    def __init__(self):
        self.installed_apps: List[FlatpakItemInfo] = []
        self.installed_runtimes: List[FlatpakItemInfo] = []
        self.unused_runtimes: List[FlatpakItemInfo] = []
        self.leftover_data: List[FlatpakItemInfo] = []
        self.orphaned_apps: List[FlatpakItemInfo] = []
        
    def analyze(self) -> Dict[str, Any]:
        """Run full Flatpak analysis"""
        self._load_installed_refs()
        self._find_unused_runtimes()
        self._find_leftover_data()
        self._find_orphaned_apps()
        
        return {
            "installed_apps": [a.to_dict() for a in self.installed_apps],
            "installed_runtimes": [r.to_dict() for r in self.installed_runtimes],
            "unused_runtimes": [r.to_dict() for r in self.unused_runtimes],
            "leftover_data": [d.to_dict() for d in self.leftover_data],
            "orphaned_apps": [a.to_dict() for a in self.orphaned_apps],
            "total_size_unused": sum(r.size_bytes for r in self.unused_runtimes),
            "total_size_leftover": sum(d.size_bytes for d in self.leftover_data),
            "total_size_orphaned": sum(a.size_bytes for a in self.orphaned_apps),
        }
    
    def _run_flatpak_command(self, args: List[str]) -> Optional[str]:
        """Run flatpak command and return output"""
        try:
            result = subprocess.run(
                ["flatpak"] + args,
                capture_output=True,
                text=True,
                timeout=30,
            )
            if result.returncode == 0:
                return result.stdout
            return None
        except (subprocess.TimeoutExpired, FileNotFoundError, Exception):
            return None
    
    def _parse_size(self, size_str: str) -> int:
        """Parse human-readable size to bytes"""
        size_str = size_str.strip().upper()
        multipliers = {
            'B': 1,
            'KB': 1024,
            'MB': 1024 ** 2,
            'GB': 1024 ** 3,
            'TB': 1024 ** 4,
        }
        
        for suffix, mult in sorted(multipliers.items(), key=lambda x: -len(x[0])):
            if size_str.endswith(suffix):
                try:
                    return int(float(size_str[:-len(suffix)].strip()) * mult)
                except ValueError:
                    return 0
        
        # Try plain bytes
        try:
            return int(size_str)
        except ValueError:
            return 0
    
    def _format_size(self, size_bytes: int) -> str:
        """Format bytes to human-readable string"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024
        return f"{size_bytes:.1f} PB"
    
    def _load_installed_refs(self):
        """Load all installed apps and runtimes with metadata"""
        # Get installed apps with details
        apps_json = self._run_flatpak_command(["list", "--app", "--columns=all", "--json"])
        if apps_json:
            try:
                apps_data = json.loads(apps_json)
                for app in apps_data:
                    info = FlatpakItemInfo(
                        ref=app.get("ref", ""),
                        name=app.get("name", ""),
                        item_type=FlatpakItemType.APP,
                        size_bytes=0,  # Will be filled later
                        size_human=app.get("size", "0"),
                        is_used=True,  # Apps are always "used"
                        description=f"Application: {app.get('name', '')}",
                        install_date=app.get("install_date"),
                        origin=app.get("origin"),
                        arch=app.get("arch"),
                        branch=app.get("branch"),
                        cleanup_command=f"flatpak uninstall {app.get('ref', '')} -y",
                    )
                    info.size_bytes = self._parse_size(info.size_human)
                    self.installed_apps.append(info)
            except json.JSONDecodeError:
                pass
        
        # Get installed runtimes with details
        runtimes_json = self._run_flatpak_command(["list", "--runtime", "--columns=all", "--json"])
        if runtimes_json:
            try:
                runtimes_data = json.loads(runtimes_json)
                for runtime in runtimes_data:
                    info = FlatpakItemInfo(
                        ref=runtime.get("ref", ""),
                        name=runtime.get("name", ""),
                        item_type=FlatpakItemType.RUNTIME,
                        size_bytes=0,
                        size_human=runtime.get("size", "0"),
                        is_used=True,  # Assume used until proven otherwise
                        description=f"Runtime: {runtime.get('name', '')}",
                        install_date=runtime.get("install_date"),
                        origin=runtime.get("origin"),
                        arch=runtime.get("arch"),
                        branch=runtime.get("branch"),
                        cleanup_command=f"flatpak uninstall {runtime.get('ref', '')} -y",
                    )
                    info.size_bytes = self._parse_size(info.size_human)
                    self.installed_runtimes.append(info)
            except json.JSONDecodeError:
                pass
    
    def _find_unused_runtimes(self):
        """Find runtimes not referenced by any installed app"""
        # Get required runtimes for installed apps
        required_refs = set()
        
        for app in self.installed_apps:
            # Get app info to find required runtimes
            info_output = self._run_flatpak_command(["info", "--show-runtime", app.ref])
            if info_output:
                runtime_ref = info_output.strip()
                if runtime_ref:
                    required_refs.add(runtime_ref)
            
            # Also get full info to find SDK and other dependencies
            info_full = self._run_flatpak_command(["info", app.ref])
            if info_full:
                # Parse for runtime references
                for line in info_full.splitlines():
                    if "Runtime:" in line or "Sdk:" in line:
                        runtime_name = line.split(":", 1)[-1].strip()
                        if runtime_name:
                            # Find matching runtime ref
                            for rt in self.installed_runtimes:
                                if runtime_name in rt.ref or rt.name == runtime_name:
                                    required_refs.add(rt.ref)
        
        # Mark runtimes as unused if not required
        for runtime in self.installed_runtimes:
            if runtime.ref not in required_refs:
                runtime.is_used = False
                runtime.description = f"Unused runtime: {runtime.name} (not required by any app)"
                self.unused_runtimes.append(runtime)
    
    def _find_leftover_data(self):
        """Find data directories for uninstalled apps"""
        # Check for data directories in ~/.var/app
        try:
            import os
            import glob
            
            var_app_path = os.path.expanduser("~/.var/app")
            if os.path.exists(var_app_path):
                data_dirs = glob.glob(f"{var_app_path}/*")
                
                installed_refs = {app.ref for app in self.installed_apps}
                installed_names = {app.name for app in self.installed_apps}
                
                for data_dir in data_dirs:
                    if not os.path.isdir(data_dir):
                        continue
                    
                    app_name = os.path.basename(data_dir)
                    
                    # Check if this app is still installed
                    is_installed = any(
                        app_name in ref or app_name == name
                        for ref in installed_refs
                        for name in installed_names
                    )
                    
                    if not is_installed:
                        # Calculate size
                        total_size = 0
                        for root, dirs, files in os.walk(data_dir):
                            for f in files:
                                try:
                                    fp = os.path.join(root, f)
                                    total_size += os.path.getsize(fp)
                                except (OSError, FileNotFoundError):
                                    continue
                        
                        if total_size > 0:
                            info = FlatpakItemInfo(
                                ref=f"{app_name}/data",
                                name=app_name,
                                item_type=FlatpakItemType.DATA,
                                size_bytes=total_size,
                                size_human=self._format_size(total_size),
                                is_used=False,
                                description=f"Leftover data from uninstalled app: {app_name}",
                                cleanup_command=f"rm -rf {data_dir}",
                            )
                            self.leftover_data.append(info)
        except Exception:
            pass
    
    def _find_orphaned_apps(self):
        """Find apps whose remote is no longer available"""
        # Get list of configured remotes
        remotes_output = self._run_flatpak_command(["remotes", "--columns=name"])
        if not remotes_output:
            return
        
        available_remotes = set(remotes_output.strip().splitlines())
        
        for app in self.installed_apps:
            if app.origin and app.origin not in available_remotes:
                app.is_used = False
                app.description = f"Orphaned app: {app.name} (origin '{app.origin}' not available)"
                self.orphaned_apps.append(app)
    
    def get_cleanup_summary(self) -> str:
        """Get human-readable summary of cleanup opportunities"""
        analysis = self.analyze()
        
        lines = [
            "=== Flatpak Cleanup Analysis ===",
            "",
        ]
        
        if self.unused_runtimes:
            lines.append(f"Unused Runtimes ({len(self.unused_runtimes)} items, {self._format_size(analysis['total_size_unused'])}):")
            for rt in sorted(self.unused_runtimes, key=lambda x: -x.size_bytes):
                lines.append(f"  - {rt.name} ({rt.size_human})")
            lines.append("")
        
        if self.leftover_data:
            lines.append(f"Leftover App Data ({len(self.leftover_data)} items, {self._format_size(analysis['total_size_leftover'])}):")
            for data in sorted(self.leftover_data, key=lambda x: -x.size_bytes)[:10]:
                lines.append(f"  - {data.name} ({data.size_human})")
            if len(self.leftover_data) > 10:
                lines.append(f"  ... and {len(self.leftover_data) - 10} more")
            lines.append("")
        
        if self.orphaned_apps:
            lines.append(f"Orphaned Apps ({len(self.orphaned_apps)} items, {self._format_size(analysis['total_size_orphaned'])}):")
            for app in sorted(self.orphaned_apps, key=lambda x: -x.size_bytes):
                lines.append(f"  - {app.name} ({app.size_human}) - origin: {app.origin}")
            lines.append("")
        
        total_reclaimable = (
            analysis['total_size_unused'] + 
            analysis['total_size_leftover'] + 
            analysis['total_size_orphaned']
        )
        lines.append(f"Total reclaimable space: {self._format_size(total_reclaimable)}")
        
        return "\n".join(lines)


def analyze_flatpak_for_cleanup() -> Dict[str, Any]:
    """Convenience function to run full Flatpak analysis"""
    analyzer = FlatpakAnalyzer()
    return analyzer.analyze()
