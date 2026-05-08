"""Analysis methods for FlatpakAnalyzer (load refs, find unused/orphaned/duplicates, repo size)."""
from __future__ import annotations

import json
import os
import subprocess
from typing import Dict, List, Optional, Any

from fixos.constants import (
    FLATPAK_BLOAT_RATIO_CRITICAL,
    FLATPAK_BLOAT_RATIO_NORMAL,
    FAST_COMMAND_TIMEOUT,
)


class _FlatpakAnalysisMixin:
    """Mixin providing analysis methods for FlatpakAnalyzer."""

    def _load_installed_refs(self):
        """Load all installed apps and runtimes with metadata"""
        from fixos.diagnostics.flatpak_analyzer import FlatpakItemInfo, FlatpakItemType

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
        required_refs = set()

        for app in self.installed_apps:
            info_output = self._run_flatpak_command(["info", "--show-runtime", app.ref])
            if info_output:
                runtime_ref = info_output.strip()
                if runtime_ref:
                    required_refs.add(runtime_ref)

            info_full = self._run_flatpak_command(["info", app.ref])
            if info_full:
                for line in info_full.splitlines():
                    if "Runtime:" in line or "Sdk:" in line:
                        runtime_name = line.split(":", 1)[-1].strip()
                        if runtime_name:
                            for rt in self.installed_runtimes:
                                if runtime_name in rt.ref or rt.name == runtime_name:
                                    required_refs.add(rt.ref)

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
        from fixos.diagnostics.flatpak_analyzer import FlatpakItemInfo, FlatpakItemType

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
        app_groups: Dict[str, list] = {}

        for app in self.installed_apps:
            base_name = app.ref.split('/')[0] if '/' in app.ref else app.ref

            if base_name not in app_groups:
                app_groups[base_name] = []
            app_groups[base_name].append(app)

        for base_name, apps in app_groups.items():
            if len(apps) > 1:
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
                capture_output=True, text=True, timeout=FAST_COMMAND_TIMEOUT,
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
        """Analyze Flatpak repo size vs apps+runtimes to detect REAL bloat."""
        apps_size = sum(a.size_bytes for a in self.installed_apps)
        runtimes_size = sum(r.size_bytes for r in self.installed_runtimes)
        total_reported_size = apps_size + runtimes_size

        flatpak_paths = [
            "/var/lib/flatpak",
            os.path.expanduser("~/.local/share/flatpak"),
        ]

        actual_disk_usage = 0
        repo_disk_usage = 0

        for flatpak_path in flatpak_paths:
            if os.path.exists(flatpak_path):
                actual_disk_usage += self._measure_path_size(flatpak_path)
                repo_path = os.path.join(flatpak_path, "repo")
                if os.path.exists(repo_path):
                    repo_disk_usage += self._measure_path_size(repo_path)

        normal_overhead = FLATPAK_BLOAT_RATIO_NORMAL
        expected_max_size = total_reported_size * normal_overhead

        bloat_detected = False
        wasted_size = 0
        ratio = 0.0

        if actual_disk_usage > 0 and total_reported_size > 0:
            ratio = actual_disk_usage / total_reported_size

            if ratio > FLATPAK_BLOAT_RATIO_CRITICAL and (actual_disk_usage - expected_max_size) > 1024**3:
                bloat_detected = True
                wasted_size = actual_disk_usage - expected_max_size
            elif ratio > 2.0:
                bloat_detected = False
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
        if ratio < FLATPAK_BLOAT_RATIO_NORMAL:
            return "Flatpak jest dobrze zarządzany - minimalny overhead."
        elif ratio < 2.0:
            return "Normalny overhead OSTree - brak potrzeby czyszczenia."
        elif ratio < FLATPAK_BLOAT_RATIO_CRITICAL:
            return (
                "Umiarkowany overhead - prawdopodobnie normalne dla dużej instalacji.\n"
                "Możesz uruchomić 'flatpak repair --vacuum' ale oszczędność będzie mała."
            )
        else:
            return (
                "Znaczny overhead - warto rozważyć 'flatpak repair --vacuum'.\n"
                "Jednak jeśli już to robiłeś, to po prostu masz dużo aplikacji."
            )
