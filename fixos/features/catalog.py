"""
Package catalog - loads and manages package database from YAML.
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Any
import yaml


@dataclass
class PackageInfo:
    """Information about a single package."""
    id: str
    description: str
    category: str
    distros: Dict[str, str] = field(default_factory=dict)
    flatpak: str = ""
    pip: str = ""
    npm: str = ""
    cargo: str = ""
    install_script: str = ""
    binary_check: str = ""
    condition: str = ""  # e.g., "gpu_vendor == 'nvidia'"

    def get_distro_name(self, distro: str) -> str:
        """Get package name for specific distro."""
        # Direct match
        if distro in self.distros:
            return self.distros[distro]
        # Try ID_LIKE matching (e.g., fedora → rhel)
        return ""

    def is_available_on(self, distro: str) -> bool:
        """Check if package is available on given distro."""
        return bool(self.get_distro_name(distro)) or self.flatpak or self.pip or self.npm or self.cargo or self.install_script


@dataclass
class PackageCategory:
    """A category of packages (e.g., core_utils, dev_tools)."""
    id: str
    description: str
    category: str
    packages: List[PackageInfo] = field(default_factory=list)


class PackageCatalog:
    """Manages the package database."""

    def __init__(self):
        self.categories: Dict[str, PackageCategory] = {}
        self.packages: Dict[str, PackageInfo] = {}

    @classmethod
    def load(cls, data_dir: Optional[Path] = None) -> "PackageCatalog":
        """Load package catalog from YAML files."""
        if data_dir is None:
            data_dir = Path(__file__).parent / "data"
        
        catalog = cls()
        packages_file = data_dir / "packages.yaml"
        
        if not packages_file.exists():
            # Create empty catalog if file doesn't exist
            return catalog
        
        with open(packages_file) as f:
            data = yaml.safe_load(f)
        
        if not data:
            return catalog
        
        for cat_id, cat_data in data.items():
            if cat_id.startswith("_"):
                continue
            
            category = PackageCategory(
                id=cat_id,
                description=cat_data.get("description", ""),
                category=cat_data.get("category", "misc"),
            )
            
            for pkg_data in cat_data.get("packages", []):
                pkg = PackageInfo(
                    id=pkg_data.get("id", ""),
                    description=pkg_data.get("desc", ""),
                    category=cat_data.get("category", "misc"),
                    distros=pkg_data.get("distros", {}),
                    flatpak=pkg_data.get("flatpak", ""),
                    pip=pkg_data.get("pip", ""),
                    npm=pkg_data.get("npm", ""),
                    cargo=pkg_data.get("cargo", ""),
                    install_script=pkg_data.get("install_script", ""),
                    binary_check=pkg_data.get("binary_check", ""),
                    condition=pkg_data.get("condition", ""),
                )
                category.packages.append(pkg)
                catalog.packages[pkg.id] = pkg
            
            catalog.categories[cat_id] = category
        
        return catalog

    def get_package(self, pkg_id: str) -> Optional[PackageInfo]:
        """Get package by ID."""
        return self.packages.get(pkg_id)

    def get_packages_by_category(self, category: str) -> List[PackageInfo]:
        """Get all packages in a category."""
        result = []
        for cat in self.categories.values():
            if cat.category == category:
                result.extend(cat.packages)
        return result

    def list_categories(self) -> List[str]:
        """List all category IDs."""
        return list(self.categories.keys())
