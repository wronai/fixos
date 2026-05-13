"""
User profile management for fixOS features.
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional, Set
import yaml

from .catalog import PackageCatalog, PackageInfo


@dataclass
class UserProfile:
    """A user profile defining what packages/features they want."""

    name: str
    description: str
    icon: str = "📦"
    includes: List[str] = field(default_factory=list)  # Category IDs to include
    extra_packages: List[str] = field(default_factory=list)  # Specific package IDs

    @classmethod
    def load(cls, profile_name: str, data_dir: Optional[Path] = None) -> "UserProfile":
        """Load a profile from YAML file."""
        if data_dir is None:
            data_dir = Path(__file__).parent / "data" / "profiles"

        profile_file = data_dir / f"{profile_name}.yaml"

        if not profile_file.exists():
            raise FileNotFoundError(
                f"Profile '{profile_name}' not found at {profile_file}"
            )

        with open(profile_file) as f:
            data = yaml.safe_load(f)

        return cls(
            name=data.get("name", profile_name),
            description=data.get("description", ""),
            icon=data.get("icon", "📦"),
            includes=data.get("includes", []),
            extra_packages=data.get("extra_packages", []),
        )

    @classmethod
    def list_available(cls, data_dir: Optional[Path] = None) -> List[str]:
        """List available profile names."""
        if data_dir is None:
            data_dir = Path(__file__).parent / "data" / "profiles"

        profiles = []
        if data_dir.exists():
            for f in data_dir.glob("*.yaml"):
                profiles.append(f.stem)
        return sorted(profiles)

    def resolve_packages(
        self, catalog: PackageCatalog, system_info
    ) -> List[PackageInfo]:
        """Resolve all packages for this profile based on system."""
        result: List[PackageInfo] = []
        seen: Set[str] = set()

        # Add packages from included categories
        for cat_id in self.includes:
            if cat_id in catalog.categories:
                cat = catalog.categories[cat_id]
                for pkg in cat.packages:
                    if pkg.id not in seen:
                        result.append(pkg)
                        seen.add(pkg.id)

        # Add extra packages
        for pkg_id in self.extra_packages:
            if pkg_id not in seen:
                pkg = catalog.get_package(pkg_id)
                if pkg:
                    result.append(pkg)
                    seen.add(pkg_id)

        return result

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "name": self.name,
            "description": self.description,
            "icon": self.icon,
            "includes": self.includes,
            "extra_packages": self.extra_packages,
        }
