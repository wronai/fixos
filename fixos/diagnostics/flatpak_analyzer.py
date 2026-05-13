"""
Advanced Flatpak analyzer for fixOS

Analyzes Flatpak installations to find:
- Unused runtimes (not referenced by any installed app)
- Orphaned applications (no longer in remote)
- Leftover data from uninstalled apps
- Old versions of runtimes/apps
- Large individual applications

Sub-modules (split from the original monolith):
  _flatpak_analysis_mixin.py        – loading refs, finding unused/orphaned/duplicates, repo analysis
  _flatpak_recommendations_mixin.py – generating cleanup recommendations
  _flatpak_execution_mixin.py       – executing cleanup actions
"""

from __future__ import annotations

import subprocess
from dataclasses import dataclass
from typing import Dict, List, Optional, Any
from enum import Enum
from fixos.diagnostics.utils import format_size as _format_size_shared
from ..constants import FAST_COMMAND_TIMEOUT


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


from fixos.diagnostics._flatpak_analysis_mixin import _FlatpakAnalysisMixin  # noqa: E402
from fixos.diagnostics._flatpak_recommendations_mixin import (
    _FlatpakRecommendationsMixin,
)  # noqa: E402
from fixos.diagnostics._flatpak_execution_mixin import _FlatpakExecutionMixin  # noqa: E402


class FlatpakAnalyzer(
    _FlatpakAnalysisMixin,
    _FlatpakRecommendationsMixin,
    _FlatpakExecutionMixin,
):
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
            "total_size_duplicates": sum(
                d.get("total_size", 0) for d in self.duplicate_apps
            ),
            "repo_bloat_size": self.repo_bloat.get("wasted_size", 0),
        }

    # ── Utility methods (used by all mixins) ──────────────────────────────

    def _run_flatpak_command(self, args: List[str]) -> Optional[str]:
        """Run flatpak command and return output"""
        try:
            result = subprocess.run(
                ["flatpak"] + args,
                capture_output=True,
                text=True,
                timeout=FAST_COMMAND_TIMEOUT,
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
            "B": 1,
            "KB": 1024,
            "MB": 1024**2,
            "GB": 1024**3,
            "TB": 1024**4,
        }

        for suffix, mult in sorted(multipliers.items(), key=lambda x: -len(x[0])):
            if size_str.endswith(suffix):
                try:
                    return int(float(size_str[: -len(suffix)].strip()) * mult)
                except ValueError:
                    return 0

        try:
            return int(size_str)
        except ValueError:
            return 0

    def _format_size(self, size_bytes: int) -> str:
        """Format bytes to human-readable string"""
        return _format_size_shared(size_bytes)


def analyze_flatpak_for_cleanup() -> Dict[str, Any]:
    """Convenience function to run full Flatpak analysis"""
    analyzer = FlatpakAnalyzer()
    return analyzer.analyze()
