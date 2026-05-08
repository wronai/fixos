"""
Storage Analyzer for FixOS - comprehensive disk space analysis.

Analizuje cały system i pokazuje REALNE możliwości odzyskania miejsca,
bez fałszywych alarmów.

Sub-modules (split from the original monolith):
  _storage_system_mixin.py    – DNF, kernels, journal, orphaned, coredumps, snap, …
  _storage_container_mixin.py – Docker, Podman
  _storage_user_mixin.py      – user cache, browsers, flatpak, dev projects, home, btrfs
"""
import subprocess
import os
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from fixos.diagnostics.utils import format_size as _format_size
from ..constants import (
    FAST_COMMAND_TIMEOUT,
    DIAGNOSTIC_CMD_TIMEOUT,
)


@dataclass
class StorageItem:
    """Represents a storage item that can be cleaned"""
    name: str
    path: str
    size_bytes: int
    category: str
    risk: str  # none, low, medium, high
    cleanup_command: str
    description: str
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "path": self.path,
            "size_bytes": self.size_bytes,
            "size_human": self._format_size(self.size_bytes),
            "category": self.category,
            "risk": self.risk,
            "cleanup_command": self.cleanup_command,
            "description": self.description,
        }
    
    @staticmethod
    def _format_size(size_bytes: int) -> str:
        return _format_size(size_bytes)


# Import mixins *after* StorageItem is defined (they reference it).
from fixos.diagnostics._storage_system_mixin import _SystemAnalyzerMixin  # noqa: E402
from fixos.diagnostics._storage_container_mixin import _ContainerAnalyzerMixin  # noqa: E402
from fixos.diagnostics._storage_user_mixin import _UserAnalyzerMixin  # noqa: E402


class StorageAnalyzer(
    _SystemAnalyzerMixin,
    _ContainerAnalyzerMixin,
    _UserAnalyzerMixin,
):
    """
    Comprehensive storage analyzer for Linux systems.
    
    Analizuje:
    - DNF/RPM cache i stare kernele
    - Journal logs
    - Docker/Podman
    - Flatpak (już zaimplementowane)
    - Snap
    - User cache
    - Btrfs snapshots
    - Duże pliki użytkownika
    """
    
    def __init__(self):
        self.items: List[StorageItem] = []
        self.total_reclaimable = 0
        self.system_info: Dict[str, Any] = {}
        
    def analyze_full(self) -> Dict[str, Any]:
        """Run full system storage analysis"""
        self.items = []
        
        # System packages
        self._analyze_dnf_cache()
        self._analyze_old_kernels()
        self._analyze_journal_logs()
        self._analyze_orphaned_packages()
        
        # Containers
        self._analyze_docker()
        self._analyze_podman()
        
        # User data
        self._analyze_user_cache()
        self._analyze_browser_cache()
        self._analyze_browser_profiles()
        
        # Flatpak deep
        self._analyze_flatpak_user_data()
        self._analyze_ostree_repo()
        
        # Dev projects (node_modules, venv, target, etc.)
        self._analyze_dev_projects()
        
        # Home directory analysis (large files and folders)
        self._analyze_home_directory()
        
        # System
        self._analyze_snap()
        self._analyze_btrfs_snapshots()
        self._analyze_var_cache()
        self._analyze_coredumps()
        self._analyze_system_logs()
        
        # Sort by size
        self.items.sort(key=lambda x: -x.size_bytes)
        
        # Calculate totals
        self.total_reclaimable = sum(item.size_bytes for item in self.items)
        
        # Group by category
        categories = {}
        for item in self.items:
            if item.category not in categories:
                categories[item.category] = []
            categories[item.category].append(item.to_dict())
        
        return {
            "items": [item.to_dict() for item in self.items],
            "categories": categories,
            "total_reclaimable": self.total_reclaimable,
            "total_reclaimable_human": StorageItem._format_size(self.total_reclaimable),
            "system_info": self.system_info,
            "recommendations": self._get_recommendations(),
        }

    # ── Shared utility methods (used by all mixins) ───────────────────────

    def _get_dir_size(self, path: str) -> int:
        """Get directory size using du"""
        if not os.path.exists(path):
            return 0
        try:
            result = subprocess.run(
                ["du", "-sb", path],
                capture_output=True,
                text=True,
                timeout=FAST_COMMAND_TIMEOUT,
            )
            if result.returncode == 0:
                return int(result.stdout.split()[0])
        except Exception:
            pass
        return 0
    
    def _get_file_size(self, path: str) -> int:
        """Get file size"""
        if not os.path.exists(path):
            return 0
        try:
            return os.path.getsize(path)
        except Exception:
            return 0
    
    def _run_command(self, cmd: List[str]) -> Optional[str]:
        """Run command and return output"""
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=DIAGNOSTIC_CMD_TIMEOUT,
            )
            if result.returncode == 0:
                return result.stdout
        except Exception:
            pass
        return None

    @staticmethod
    def _parse_size_static(size_str: str) -> int:
        """Parse size string like '1.2G' to bytes (static version for use in classmethods)."""
        size_str = size_str.strip().upper()
        multipliers = {
            'K': 1024,
            'M': 1024**2,
            'G': 1024**3,
            'T': 1024**4,
        }
        for suffix, mult in multipliers.items():
            if size_str.endswith(suffix):
                try:
                    return int(float(size_str[:-1]) * mult)
                except ValueError:
                    return 0
        try:
            return int(float(size_str))
        except ValueError:
            return 0

    def _parse_size(self, size_str: str) -> int:
        """Parse size string like '1.2G' to bytes"""
        return self._parse_size_static(size_str)

    # ── Recommendations and summary ───────────────────────────────────────

    def _get_recommendations(self) -> List[Dict[str, Any]]:
        """Get prioritized cleanup recommendations"""
        recommendations = []
        
        safe_items = [item for item in self.items if item.risk in ['none', 'low']]
        medium_items = [item for item in self.items if item.risk == 'medium']
        
        if safe_items:
            total_safe = sum(item.size_bytes for item in safe_items)
            recommendations.append({
                "priority": "high",
                "description": f"Bezpieczne czyszczenie ({len(safe_items)} elementów)",
                "items": [item.to_dict() for item in safe_items[:5]],
                "estimated_savings": StorageItem._format_size(total_safe),
                "risk": "low",
                "action": "auto",
            })
        
        if medium_items:
            total_medium = sum(item.size_bytes for item in medium_items)
            recommendations.append({
                "priority": "medium",
                "description": f"Wymaga potwierdzenia ({len(medium_items)} elementów)",
                "items": [item.to_dict() for item in medium_items[:5]],
                "estimated_savings": StorageItem._format_size(total_medium),
                "risk": "medium",
                "action": "confirm",
            })
        
        return recommendations
    
    def get_summary(self) -> str:
        """Get human-readable summary"""
        analysis = self.analyze_full()
        
        lines = [
            "=" * 60,
            "📊 STORAGE ANALYSIS",
            "=" * 60,
            "",
        ]
        
        if not self.items:
            lines.append("✅ System jest czysty - brak dużych śmieci.")
            return "\n".join(lines)
        
        categories = {}
        for item in self.items:
            if item.category not in categories:
                categories[item.category] = []
            categories[item.category].append(item)
        
        for category, items in categories.items():
            total = sum(item.size_bytes for item in items)
            lines.append(f"\n{category.upper()} ({StorageItem._format_size(total)})")
            for item in items[:5]:
                risk_icon = {"none": "✅", "low": "🟢", "medium": "🟡", "high": "🔴"}.get(item.risk, "•")
                lines.append(f"  {risk_icon} {item.name}: {StorageItem._format_size(item.size_bytes)}")
            if len(items) > 5:
                lines.append(f"  ... i {len(items) - 5} więcej")
        
        lines.append(f"\n{'=' * 60}")
        lines.append(f"💰 ŁĄCZNIE DO ODZYSKANIA: {analysis['total_reclaimable_human']}")
        lines.append("=" * 60)
        
        return "\n".join(lines)
