"""
Diagnostic profiles for fixOS.

Profiles define presets of diagnostic modules and thresholds for different scenarios.
Built-in profiles: server, desktop, developer, minimal.
User profiles stored in ~/.fixos/profiles/.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

import yaml

PROFILES_DIR = Path(__file__).parent


@dataclass
class Profile:
    """Profil diagnostyczny z zestawem modułów i progów."""
    name: str
    description: str
    modules: list[str]
    thresholds: dict[str, int | float] = field(default_factory=dict)

    @classmethod
    def load(cls, name: str) -> Profile:
        """Załaduj profil — najpierw user, potem builtin."""
        user_path = Path.home() / ".fixos" / "profiles" / f"{name}.yaml"
        if user_path.exists():
            path = user_path
        else:
            path = PROFILES_DIR / f"{name}.yaml"

        if not path.exists():
            raise FileNotFoundError(
                f"Profile '{name}' not found. "
                f"Available: {', '.join(cls.list_available())}"
            )

        data = yaml.safe_load(path.read_text())
        return cls(
            name=data.get("name", name),
            description=data.get("description", ""),
            modules=data.get("modules", []),
            thresholds=data.get("thresholds", {}),
        )

    @classmethod
    def list_available(cls) -> list[str]:
        """Lista dostępnych profili (builtin + user)."""
        builtin = [f.stem for f in PROFILES_DIR.glob("*.yaml")]
        user_dir = Path.home() / ".fixos" / "profiles"
        user = [f.stem for f in user_dir.glob("*.yaml")] if user_dir.exists() else []
        return sorted(set(builtin + user))

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "description": self.description,
            "modules": self.modules,
            "thresholds": self.thresholds,
        }
