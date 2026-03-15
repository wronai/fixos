"""
Feature auditor - compares system state with desired profile.
"""

from dataclasses import dataclass, field
from typing import List, Set
import shutil

from .catalog import PackageCatalog, PackageInfo
from .profiles import UserProfile
from . import SystemInfo


@dataclass
class AuditResult:
    """Result of feature audit - what's installed, what's missing."""
    profile_name: str
    system: SystemInfo
    installed: List[PackageInfo] = field(default_factory=list)
    missing: List[PackageInfo] = field(default_factory=list)
    skipped: List[PackageInfo] = field(default_factory=list)
    repos_needed: List[PackageInfo] = field(default_factory=list)

    @property
    def completion_pct(self) -> float:
        total = len(self.installed) + len(self.missing)
        return (len(self.installed) / total * 100) if total > 0 else 100.0

    @property
    def total_packages(self) -> int:
        return len(self.installed) + len(self.missing) + len(self.skipped)

    def to_dict(self) -> dict:
        return {
            "profile_name": self.profile_name,
            "system": {
                "distro": self.system.distro,
                "desktop_env": self.system.desktop_env,
                "gpu_vendor": self.system.gpu_vendor,
            },
            "completion_pct": self.completion_pct,
            "total": self.total_packages,
            "installed_count": len(self.installed),
            "missing_count": len(self.missing),
            "skipped_count": len(self.skipped),
            "installed": [p.id for p in self.installed],
            "missing": [p.id for p in self.missing],
            "skipped": [p.id for p in self.skipped],
        }


class FeatureAuditor:
    """Compares installed packages with profile requirements."""

    def __init__(self, catalog: PackageCatalog, system: SystemInfo):
        self.catalog = catalog
        self.system = system

    def audit(self, profile: UserProfile) -> AuditResult:
        """Perform audit comparing system with profile."""
        result = AuditResult(profile_name=profile.name, system=self.system)

        for pkg in profile.resolve_packages(self.catalog, self.system):
            # Check conditions (e.g., gpu_vendor, desktop_env)
            if not self._check_conditions(pkg):
                result.skipped.append(pkg)
                continue

            if self._is_installed(pkg):
                result.installed.append(pkg)
            else:
                if pkg.category == "repos":
                    result.repos_needed.append(pkg)
                else:
                    result.missing.append(pkg)

        return result

    def _check_conditions(self, pkg: PackageInfo) -> bool:
        """Check if package conditions are met."""
        if not pkg.condition:
            return True

        # Simple condition evaluation
        # Format: "gpu_vendor == 'nvidia'" or "desktop_env == 'gnome'" or "has_battery"
        condition = pkg.condition.strip()

        # Handle 'has_battery' condition
        if condition == "has_battery":
            return self.system.has_battery

        # Parse key == 'value' conditions
        if "==" in condition:
            parts = condition.split("==")
            if len(parts) == 2:
                key = parts[0].strip()
                value = parts[1].strip().strip("'\"")
                system_value = getattr(self.system, key, None)
                return str(system_value).lower() == value.lower()

        return True

    def _is_installed(self, pkg: PackageInfo) -> bool:
        """Check if package is installed."""
        # Native package
        distro_name = pkg.get_distro_name(self.system.distro)
        if distro_name:
            # Handle space-separated package lists
            for name in distro_name.split():
                name = name.strip()
                if name in self.system.installed_packages:
                    return True

        # Flatpak
        if pkg.flatpak and pkg.flatpak in self.system.installed_flatpaks:
            return True

        # Binary in PATH
        if pkg.binary_check and shutil.which(pkg.binary_check):
            return True

        # Check via pip list (if applicable)
        if pkg.pip and self.system.has_pip:
            # Could check pip list, but expensive - skip for now
            pass

        return False
