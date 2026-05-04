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

CONSTANT_1 = 1.5
MAX_2 = 2.5
CONSTANT_3 = 3
CONSTANT_4 = 4
CONSTANT_5 = 5
TIMEOUT_30 = 30
CONSTANT_50 = 50
TIMEOUT_60 = 60
TIMEOUT_300 = 300
CONSTANT_500 = 500
TIMEOUT_600 = 600
CONSTANT_1024 = 1024

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
        self.duplicate_apps: List[Dict[str, Any]] = []
        self.repo_bloat: Dict[str, Any] = {}
        
    def analyze(self) -> Dict[str, Any]:
        """Run full Flatpak analysis"""
        self._load_installed_refs()
        self._find_unused_runtimes()
        self._find_leftover_data()
        self._find_orphaned_apps()
        self._find_duplicate_apps()
        self._analyze_repo_size()
        
        return {
            "installed_apps": [a.to_dict() for a in self.installed_apps],
            "installed_runtimes": [r.to_dict() for r in self.installed_runtimes],
            "unused_runtimes": [r.to_dict() for r in self.unused_runtimes],
            "leftover_data": [d.to_dict() for d in self.leftover_data],
            "orphaned_apps": [a.to_dict() for a in self.orphaned_apps],
            "duplicate_apps": self.duplicate_apps,
            "repo_bloat": self.repo_bloat,
            "total_size_unused": sum(r.size_bytes for r in self.unused_runtimes),
            "total_size_leftover": sum(d.size_bytes for d in self.leftover_data),
            "total_size_orphaned": sum(a.size_bytes for a in self.orphaned_apps),
            "total_size_duplicates": sum(d.get('total_size', 0) for d in self.duplicate_apps),
            "repo_bloat_size": self.repo_bloat.get('wasted_size', 0),
        }
    
    def _run_flatpak_command(self, args: List[str]) -> Optional[str]:
        """Run flatpak command and return output"""
        try:
            result = subprocess.run(
                ["flatpak"] + args,
                capture_output=True,
                text=True,
                timeout=TIMEOUT_30,
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
            'KB': CONSTANT_1024,
            'MB': CONSTANT_1024 ** 2,
            'GB': CONSTANT_1024 ** CONSTANT_3,
            'TB': CONSTANT_1024 ** CONSTANT_4,
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
            if size_bytes < CONSTANT_1024:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= CONSTANT_1024
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
    
    @staticmethod
    def _dir_total_size(path: str) -> int:
        """Return total byte size of all files under *path*."""
        total = 0
        try:
            for root, _dirs, files in os.walk(path):
                for f in files:
                    try:
                        total += os.path.getsize(os.path.join(root, f))
                    except (OSError, FileNotFoundError):
                        continue
        except Exception:
            pass
        return total

    def _find_leftover_data(self):
        """Find data directories for uninstalled apps"""
        try:
            import glob
            var_app_path = os.path.expanduser("~/.var/app")
            if not os.path.exists(var_app_path):
                return

            installed_refs = {app.ref for app in self.installed_apps}
            installed_names = {app.name for app in self.installed_apps}

            for data_dir in glob.glob(f"{var_app_path}/*"):
                if not os.path.isdir(data_dir):
                    continue
                app_name = os.path.basename(data_dir)
                is_installed = any(
                    app_name in ref or app_name == name
                    for ref in installed_refs
                    for name in installed_names
                )
                if is_installed:
                    continue
                total_size = self._dir_total_size(data_dir)
                if total_size > 0:
                    self.leftover_data.append(FlatpakItemInfo(
                        ref=f"{app_name}/data",
                        name=app_name,
                        item_type=FlatpakItemType.DATA,
                        size_bytes=total_size,
                        size_human=self._format_size(total_size),
                        is_used=False,
                        description=f"Leftover data from uninstalled app: {app_name}",
                        cleanup_command=f"rm -rf {data_dir}",
                    ))
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
    
    def _find_duplicate_apps(self):
        """Find duplicate apps (same app installed multiple times, e.g., stable + dev)"""
        # Group apps by base name (without branch/channel)
        app_groups: Dict[str, List[FlatpakItemInfo]] = {}
        
        for app in self.installed_apps:
            # Extract base name (e.g., "com.microsoft.Edge" from "com.microsoft.Edge/stable")
            base_name = app.ref.split('/')[0] if '/' in app.ref else app.ref
            
            if base_name not in app_groups:
                app_groups[base_name] = []
            app_groups[base_name].append(app)
        
        # Find groups with multiple versions
        for base_name, apps in app_groups.items():
            if len(apps) > 1:
                # Found duplicates
                total_size = sum(a.size_bytes for a in apps)
                versions = [a.branch or 'unknown' for a in apps]
                
                self.duplicate_apps.append({
                    "name": base_name,
                    "count": len(apps),
                    "versions": versions,
                    "total_size": total_size,
                    "apps": [a.to_dict() for a in apps],
                    "cleanup_hint": f"Możesz usunąć starsze wersje: flatpak uninstall {base_name}",
                })
    
    @staticmethod
    def _get_dir_size_du(path: str) -> int:
        """Get actual disk usage via du command."""
        try:
            result = subprocess.run(
                ["du", "-sb", path],
                capture_output=True, text=True, timeout=TIMEOUT_60,
            )
            if result.returncode == 0:
                return int(result.stdout.split()[0])
        except Exception:
            pass
        return 0

    @staticmethod
    def _get_dir_size_walk(path: str) -> int:
        """Fallback: calculate size by walking directory."""
        total = 0
        try:
            for root, _dirs, files in os.walk(path):
                for f in files:
                    try:
                        total += os.path.getsize(os.path.join(root, f))
                    except (OSError, FileNotFoundError):
                        continue
        except Exception:
            pass
        return total

    def _measure_path_size(self, path: str) -> int:
        """Return disk usage of *path* using du, falling back to os.walk."""
        size = self._get_dir_size_du(path)
        return size if size else self._get_dir_size_walk(path)

    def _analyze_repo_size(self):
        """Analyze Flatpak repo size vs apps+runtimes to detect REAL bloat.

        Używa rzeczywistego użycia dysku (du) zamiast sum logicznych,
        aby uniknąć fałszywych alarmów o "śmieciach".
        """
        # Calculate total size of installed apps and runtimes (from flatpak list)
        apps_size = sum(a.size_bytes for a in self.installed_apps)
        runtimes_size = sum(r.size_bytes for r in self.installed_runtimes)
        total_reported_size = apps_size + runtimes_size
        
        # Check FLATPAK ROOT directory size (actual disk usage)
        flatpak_paths = [
            "/var/lib/flatpak",  # System-wide (includes repo, app, runtime)
            os.path.expanduser("~/.local/share/flatpak"),  # User
        ]
        
        actual_disk_usage = 0
        repo_disk_usage = 0

        for flatpak_path in flatpak_paths:
            if os.path.exists(flatpak_path):
                actual_disk_usage += self._measure_path_size(flatpak_path)
                repo_path = os.path.join(flatpak_path, "repo")
                if os.path.exists(repo_path):
                    repo_disk_usage += self._measure_path_size(repo_path)
        
        # Calculate REAL bloat (actual usage vs reported by flatpak list)
        # Note: Some difference is NORMAL due to:
        # - OSTree metadata and indexes
        # - Deduplication (shared objects between apps)
        # - Staging/portal directories
        # 
        # REAL bloat = actual usage significantly > reported + overhead
        # Normal overhead: ~1.5-2x for OSTree structure
        
        normal_overhead = CONSTANT_1  # OSTree can have 50% overhead for metadata
        expected_max_size = total_reported_size * normal_overhead
        
        # Only flag as bloat if actual > expected by significant margin
        # AND after running prune (check if prune was run recently)
        bloat_detected = False
        wasted_size = 0
        ratio = 0.0  # Initialize before conditional
        
        if actual_disk_usage > 0 and total_reported_size > 0:
            ratio = actual_disk_usage / total_reported_size
            
            # Only flag if ratio > 2.5x (significant bloat beyond normal overhead)
            # AND the absolute difference is > 1GB (avoid false positives)
            if ratio > MAX_2 and (actual_disk_usage - expected_max_size) > CONSTANT_1024**CONSTANT_3:
                bloat_detected = True
                wasted_size = actual_disk_usage - expected_max_size
            elif ratio > 2.0:
                # Moderate bloat - warn but don't recommend vacuum as critical
                bloat_detected = False  # Don't flag as critical
                wasted_size = max(0, actual_disk_usage - expected_max_size)
        
        self.repo_bloat = {
            "actual_disk_usage": actual_disk_usage,
            "actual_disk_usage_human": self._format_size(actual_disk_usage),
            "reported_size": total_reported_size,
            "reported_size_human": self._format_size(total_reported_size),
            "repo_disk_usage": repo_disk_usage,
            "repo_disk_usage_human": self._format_size(repo_disk_usage),
            "ratio": ratio if actual_disk_usage > 0 else 0,
            "normal_overhead": normal_overhead,
            "expected_max_size": expected_max_size,
            "expected_max_size_human": self._format_size(expected_max_size),
            "bloat_detected": bloat_detected,
            "wasted_size": wasted_size,
            "wasted_size_human": self._format_size(wasted_size),
            "recommendation": "flatpak repair --vacuum" if bloat_detected else None,
            "note": self._get_flatpak_size_note(ratio, actual_disk_usage, total_reported_size),
        }
    
    def _get_flatpak_size_note(self, ratio: float, actual: int, reported: int) -> str:
        """Get explanation note about Flatpak size"""
        if ratio < CONSTANT_1:
            return "Flatpak jest dobrze zarządzany - minimalny overhead."
        elif ratio < 2.0:
            return "Normalny overhead OSTree - brak potrzeby czyszczenia."
        elif ratio < MAX_2:
            return (
                "Umiarkowany overhead - prawdopodobnie normalne dla dużej instalacji.\n"
                "Możesz uruchomić 'flatpak repair --vacuum' ale oszczędność będzie mała."
            )
        else:
            return (
                "Znaczny overhead - warto rozważyć 'flatpak repair --vacuum'.\n"
                "Jednak jeśli już to robiłeś, to po prostu masz dużo aplikacji."
            )
    
    def get_largest_apps(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get list of largest installed apps (for removal recommendations)"""
        sorted_apps = sorted(self.installed_apps, key=lambda x: -x.size_bytes)
        
        return [
            {
                "name": app.name,
                "ref": app.ref,
                "size": app.size_bytes,
                "size_human": app.size_human,
                "cleanup_command": f"flatpak uninstall {app.ref} -y",
            }
            for app in sorted_apps[:limit]
        ]
    
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
    
    def _rec_repo_bloat(self) -> List[Dict[str, Any]]:
        """Recommendations for repo bloat status."""
        recs: List[Dict[str, Any]] = []
        if self.repo_bloat.get('actual_disk_usage', 0) <= 0:
            return recs
        ratio = self.repo_bloat.get('ratio', 0)
        note = self.repo_bloat.get('note', '')
        if self.repo_bloat.get('bloat_detected'):
            if self.repo_bloat.get('wasted_size', 0) > CONSTANT_1024 ** CONSTANT_3:
                recs.append({
                    "priority": "medium",
                    "action": "flatpak repair --vacuum",
                    "description": "💣 Wyczyść repo Flatpak (potencjalne śmieci)",
                    "explanation": (
                        f"Rzeczywiste użycie dysku: {self.repo_bloat.get('actual_disk_usage_human', '?')}\n"
                        f"Rozmiar raportowany przez flatpak: {self.repo_bloat.get('reported_size_human', '?')}\n"
                        f"Ratio: {ratio:.1f}x (normalne: 1-1.5x)\n\n{note}\n\n"
                        "⚠️ UWAGA: Jeśli już uruchamiałeś 'flatpak repair --vacuum',\n"
                        "to po prostu masz dużo aplikacji - to normalne."
                    ),
                    "estimated_savings": self.repo_bloat.get('wasted_size_human', '?'),
                    "risk": "low",
                    "requires_confirmation": True,
                })
        elif ratio > CONSTANT_1:
            recs.append({
                "priority": "info",
                "action": "# Brak potrzeby czyszczenia",
                "description": f"📊 Flatpak: {self.repo_bloat.get('actual_disk_usage_human', '?')} (normalne dla {len(self.installed_apps)} aplikacji)",
                "explanation": (
                    f"Rzeczywiste użycie: {self.repo_bloat.get('actual_disk_usage_human', '?')}\n"
                    f"Rozmiar aplikacji: {self.repo_bloat.get('reported_size_human', '?')}\n"
                    f"Ratio: {ratio:.1f}x - {note}\n\n"
                    "✅ Twój Flatpak jest w dobrym stanie.\nOverhead jest normalny dla OSTree."
                ),
                "estimated_savings": "0 B",
                "risk": "none",
                "requires_confirmation": False,
            })
        return recs

    def _rec_duplicates(self) -> List[Dict[str, Any]]:
        """Recommendations for duplicate apps."""
        recs: List[Dict[str, Any]] = []
        if not self.duplicate_apps:
            return recs
        total_dup_size = sum(d.get('total_size', 0) for d in self.duplicate_apps)
        if total_dup_size > CONSTANT_50 * CONSTANT_1024 * CONSTANT_1024:
            dup_names = [d['name'] for d in self.duplicate_apps[:CONSTANT_3]]
            recs.append({
                "priority": "high",
                "action": "flatpak uninstall <duplicate_app>",
                "description": f"🔄 Usuń duplikaty aplikacji ({len(self.duplicate_apps)} znalezionych)",
                "explanation": (
                    f"Masz zainstalowane wielokrotne wersje tych samych aplikacji:\n"
                    f"  {', '.join(dup_names)}\n\n"
                    "Możesz bezpiecznie usunąć starsze wersje:\n"
                    "  flatpak uninstall com.microsoft.EdgeDev\n"
                    "  flatpak uninstall synergy\n\n"
                    f"💰 Realne odzyskanie: {self._format_size(total_dup_size)}"
                ),
                "estimated_savings": self._format_size(total_dup_size),
                "risk": "low",
                "requires_confirmation": True,
                "items": self.duplicate_apps,
            })
        return recs

    def _rec_unused_runtimes(self) -> List[Dict[str, Any]]:
        """Recommendations for unused runtimes."""
        recs: List[Dict[str, Any]] = []
        total_unused = sum(r.size_bytes for r in self.unused_runtimes)
        if total_unused > CONSTANT_50 * CONSTANT_1024 * CONSTANT_1024:
            recs.append({
                "priority": "high",
                "action": "flatpak uninstall --unused -y",
                "description": "Usuń nieużywane runtime'y i stare wersje",
                "explanation": (
                    "Ta komenda jest BEZPIECZNA - nie usuwa używanych aplikacji.\n"
                    "Usuwa:\n  - runtime'y nie wymagane przez żadną aplikację\n"
                    "  - stare wersje aplikacji\n  - nieużywane SDK\n\n"
                    f"💰 Realne odzyskanie: {self._format_size(total_unused)}"
                ),
                "estimated_savings": self._format_size(total_unused),
                "risk": "low",
                "requires_confirmation": True,
            })
        return recs

    def _rec_large_apps(self) -> List[Dict[str, Any]]:
        """Recommendations for large apps."""
        recs: List[Dict[str, Any]] = []
        largest_apps = self.get_largest_apps(CONSTANT_5)
        if not largest_apps:
            return recs
        total_large = sum(a['size'] for a in largest_apps)
        if total_large > CONSTANT_500 * CONSTANT_1024 * CONSTANT_1024:
            recs.append({
                "priority": "medium",
                "action": "flatpak uninstall <app>",
                "description": "📱 Usuń duże aplikacje (opcjonalnie)",
                "explanation": (
                    "Największe aplikacje w Twoim systemie:\n"
                    + "\n".join(f"  • {a['name']} - {a['size_human']}" for a in largest_apps[:CONSTANT_5])
                    + f"\n\n💡 Jeśli nie używasz którejś, możesz ją usunąć:\n"
                    + f"  flatpak uninstall {largest_apps[0]['ref']}\n\n"
                    + f"💰 Potencjalne odzyskanie: do {self._format_size(total_large)}"
                ),
                "estimated_savings": f"do {self._format_size(total_large)}",
                "risk": "medium",
                "requires_confirmation": True,
                "items": largest_apps,
            })
        return recs

    def _rec_leftover_and_orphaned(self) -> List[Dict[str, Any]]:
        """Recommendations for leftover data and orphaned apps."""
        recs: List[Dict[str, Any]] = []
        total_leftover = sum(d.size_bytes for d in self.leftover_data)
        if total_leftover > CONSTANT_50 * CONSTANT_1024 * CONSTANT_1024:
            recs.append({
                "priority": "medium",
                "action": "rm -rf ~/.var/app/<unused_app>",
                "description": "Usuń dane po odinstalowanych aplikacjach",
                "explanation": (
                    "Katalog ~/.var/app zawiera dane aplikacji.\n"
                    "Niektóre aplikacje zostały usunięte, ale dane zostały."
                ),
                "estimated_savings": self._format_size(total_leftover),
                "risk": "medium",
                "requires_confirmation": True,
                "items": [d.to_dict() for d in sorted(self.leftover_data, key=lambda x: -x.size_bytes)[:10]],
            })
        if self.orphaned_apps:
            recs.append({
                "priority": "low",
                "action": "flatpak uninstall <orphaned_app>",
                "description": "Usuń aplikacje z niedostępnymi remotes",
                "explanation": (
                    "Te aplikacje pochodzą z remotes, które już nie istnieją.\n"
                    "Nie można ich zaktualizować."
                ),
                "estimated_savings": self._format_size(sum(a.size_bytes for a in self.orphaned_apps)),
                "risk": "medium",
                "requires_confirmation": True,
                "items": [a.to_dict() for a in self.orphaned_apps],
            })
        return recs

    def _rec_hard_reset(self) -> List[Dict[str, Any]]:
        """Recommendation for full hard reset (only if > 50 GB)."""
        total = (
            sum(a.size_bytes for a in self.installed_apps)
            + sum(r.size_bytes for r in self.installed_runtimes)
        )
        if total > CONSTANT_50 * CONSTANT_1024 * CONSTANT_1024 * CONSTANT_1024:
            return [{
                "priority": "low",
                "action": "flatpak uninstall --all",
                "description": "Hard reset - usuń WSZYSTKIE Flatpaki",
                "explanation": (
                    "⚠️ OSTRZEŻENIE: To usuwa WSZYSTKIE aplikacje Flatpak!\n"
                    "Użyj tylko jeśli:\n  - masz mało ważnych aplikacji\n"
                    "  - chcesz zacząć od zera\nPotem instalujesz tylko to, czego potrzebujesz."
                ),
                "estimated_savings": self._format_size(total),
                "risk": "high",
                "requires_confirmation": True,
            }]
        return []

    def get_cleanup_recommendations(self) -> List[Dict[str, Any]]:
        """Get list of cleanup recommendations with explanations"""
        recs: List[Dict[str, Any]] = []
        recs.extend(self._rec_repo_bloat())
        recs.extend(self._rec_duplicates())
        recs.extend(self._rec_unused_runtimes())
        recs.extend(self._rec_large_apps())
        if self.unused_runtimes or self.repo_bloat.get('bloat_detected'):
            recs.append({
                "priority": "low",
                "action": "flatpak repair",
                "description": "Napraw instalację Flatpak (opcjonalnie)",
                "explanation": "Weryfikuje integralność instalacji.\nNie odzyskuje miejsca, ale naprawia błędy.",
                "estimated_savings": "0 B",
                "risk": "none",
                "requires_confirmation": False,
            })
        recs.extend(self._rec_leftover_and_orphaned())
        recs.extend(self._rec_hard_reset())
        return recs
    
    def ask_user_and_cleanup(self, auto_confirm_low_risk: bool = False) -> Dict[str, Any]:
        """
        Pytaj użytkownika o zgodę i wykonaj czyszczenie.
        
        Args:
            auto_confirm_low_risk: Jeśli True, automatycznie wykonuje operacje niskiego ryzyka
        
        Returns:
            Dict z wynikami wykonanych operacji
        """
        results = {
            "executed": [],
            "skipped": [],
            "failed": [],
            "space_reclaimed": 0,
        }
        
        recommendations = self.get_cleanup_recommendations()
        
        if not recommendations:
            print("✅ Brak rekomendacji czyszczenia - Flatpak jest w dobrym stanie.")
            return results
        
        print("\n" + "="*TIMEOUT_60)
        print("🔧 FLATPAK CLEANUP RECOMMENDATIONS")
        print("="*TIMEOUT_60 + "\n")
        
        for i, rec in enumerate(recommendations, 1):
            print(f"\n[{i}/{len(recommendations)}] {rec['description']}")
            print(f"   Komenda: {rec['action']}")
            print(f"   Szacowane odzyskanie: {rec['estimated_savings']}")
            print(f"   Ryzyko: {rec['risk'].upper()}")
            print(f"\n   {rec['explanation']}")
            
            # Decyzja o wykonaniu
            should_execute = False
            
            if rec['risk'] == 'none':
                should_execute = True
                print(f"\n   ▶️ Wykonuję automatycznie (brak ryzyka)...")
            elif rec['risk'] == 'low' and auto_confirm_low_risk:
                should_execute = True
                print(f"\n   ▶️ Wykonuję automatycznie (niskie ryzyko, auto-confirm)...")
            else:
                print(f"\n   ❓ Czy wykonać? [y/N] ", end="")
                try:
                    response = input().strip().lower()
                    should_execute = response in ['y', 'yes', 't', 'tak']
                except (EOFError, KeyboardInterrupt):
                    print("\n   ⏭️ Pomijam...")
                    should_execute = False
            
            if should_execute:
                print(f"\n   🚀 Wykonuję: {rec['action']}")
                result = self._execute_cleanup_action(rec)
                
                if result['success']:
                    results['executed'].append({
                        "action": rec['action'],
                        "output": result.get('output', ''),
                    })
                    results['space_reclaimed'] += result.get('bytes_reclaimed', 0)
                    print(f"   ✅ Sukces")
                else:
                    results['failed'].append({
                        "action": rec['action'],
                        "error": result.get('error', 'Unknown error'),
                    })
                    print(f"   ❌ Błąd: {result.get('error', 'Unknown error')}")
            else:
                results['skipped'].append(rec['action'])
                print(f"   ⏭️ Pominięto")
        
        print("\n" + "="*TIMEOUT_60)
        print("📊 PODSUMOWANIE")
        print("="*TIMEOUT_60)
        print(f"   Wykonano: {len(results['executed'])}")
        print(f"   Pominięto: {len(results['skipped'])}")
        print(f"   Błędy: {len(results['failed'])}")
        print(f"   Odzyskano: {self._format_size(results['space_reclaimed'])}")
        print("="*TIMEOUT_60 + "\n")
        
        return results
    
    def _execute_cleanup_action(self, rec: Dict[str, Any]) -> Dict[str, Any]:
        """Wykonaj pojedynczą akcję czyszczenia"""
        action = rec['action']
        
        try:
            # Specjalne przypadki
            if action == "flatpak uninstall --unused -y":
                return self._execute_flatpak_uninstall_unused()
            elif action == "flatpak repair --vacuum":
                return self._execute_flatpak_vacuum()
            elif action == "flatpak repair":
                return self._execute_flatpak_repair()
            elif action.startswith("flatpak uninstall --all"):
                return self._execute_flatpak_uninstall_all()
            elif "rm -rf" in action and ".var/app" in action:
                # Leftover data - obsługiwane indywidualnie
                return self._execute_leftover_data_cleanup(rec.get('items', []))
            else:
                # Ogólne wykonanie komendy
                result = subprocess.run(
                    action.split(),
                    capture_output=True,
                    text=True,
                    timeout=TIMEOUT_300,
                )
                return {
                    "success": result.returncode == 0,
                    "output": result.stdout,
                    "error": result.stderr if result.returncode != 0 else None,
                    "bytes_reclaimed": 0,
                }
        except subprocess.TimeoutExpired:
            return {"success": False, "error": "Timeout (300s)"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _execute_flatpak_uninstall_unused(self) -> Dict[str, Any]:
        """Wykonaj flatpak uninstall --unused"""
        # Najpierw sprawdź ile odzyskamy
        analysis = self.analyze()
        bytes_before = analysis['total_size_unused']
        
        result = subprocess.run(
            ["flatpak", "uninstall", "--unused", "-y"],
            capture_output=True,
            text=True,
            timeout=TIMEOUT_300,
        )
        
        return {
            "success": result.returncode == 0,
            "output": result.stdout,
            "error": result.stderr if result.returncode != 0 else None,
            "bytes_reclaimed": bytes_before,  # Szacunek
        }
    
    def _execute_flatpak_repair(self) -> Dict[str, Any]:
        """Wykonaj flatpak repair"""
        result = subprocess.run(
            ["flatpak", "repair"],
            capture_output=True,
            text=True,
            timeout=TIMEOUT_300,
        )
        
        return {
            "success": result.returncode == 0,
            "output": result.stdout,
            "error": result.stderr if result.returncode != 0 else None,
            "bytes_reclaimed": 0,
        }
    
    def _execute_flatpak_vacuum(self) -> Dict[str, Any]:
        """Wykonaj flatpak repair --vacuum (czyści repo ze starych obiektów)"""
        # Zapisz rozmiar przed czyszczeniem
        bytes_before = self.repo_bloat.get('wasted_size', 0)
        
        result = subprocess.run(
            ["flatpak", "repair", "--vacuum"],
            capture_output=True,
            text=True,
            timeout=TIMEOUT_600,  # Vacuum może trwać dłużej
        )
        
        return {
            "success": result.returncode == 0,
            "output": result.stdout,
            "error": result.stderr if result.returncode != 0 else None,
            "bytes_reclaimed": bytes_before,  # Szacunek z przed vacuum
        }
    
    def _execute_flatpak_uninstall_all(self) -> Dict[str, Any]:
        """Wykonaj flatpak uninstall --all (hard reset)"""
        analysis = self.analyze()
        bytes_before = (
            sum(a.size_bytes for a in self.installed_apps) +
            sum(r.size_bytes for r in self.installed_runtimes)
        )
        
        result = subprocess.run(
            ["flatpak", "uninstall", "--all", "-y"],
            capture_output=True,
            text=True,
            timeout=TIMEOUT_300,
        )
        
        return {
            "success": result.returncode == 0,
            "output": result.stdout,
            "error": result.stderr if result.returncode != 0 else None,
            "bytes_reclaimed": bytes_before,
        }
    
    def _execute_leftover_data_cleanup(self, items: List[Dict]) -> Dict[str, Any]:
        """Usuń leftover data directories"""
        import os
        import shutil
        
        total_bytes = 0
        errors = []
        
        for item in items:
            # Wyciągnij ścieżkę z cleanup_command
            cleanup_cmd = item.get('cleanup_command', '')
            if 'rm -rf' in cleanup_cmd:
                path = cleanup_cmd.replace('rm -rf ', '').strip()
                if path.startswith('~/.var/app/') or path.startswith('/home/'):
                    try:
                        expanded_path = os.path.expanduser(path) if path.startswith('~') else path
                        if os.path.exists(expanded_path):
                            shutil.rmtree(expanded_path)
                            total_bytes += item.get('size_bytes', 0)
                    except Exception as e:
                        errors.append(f"{path}: {e}")
        
        return {
            "success": len(errors) == 0,
            "output": f"Removed {len(items)} directories",
            "error": "; ".join(errors) if errors else None,
            "bytes_reclaimed": total_bytes,
        }


def analyze_flatpak_for_cleanup() -> Dict[str, Any]:
    """Convenience function to run full Flatpak analysis"""
    analyzer = FlatpakAnalyzer()
    return analyzer.analyze()
