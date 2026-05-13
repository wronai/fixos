"""
Base classes for fixOS diagnostic plugins.

Provides ABC for creating diagnostic plugins and data classes for results.
External plugins can inherit from DiagnosticPlugin and register via entry_points.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class Severity(Enum):
    """Severity level for diagnostic findings."""

    OK = "ok"
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


@dataclass
class Finding:
    """Single finding from a diagnostic plugin."""

    title: str
    severity: Severity
    description: str
    suggestion: str | None = None
    command: str | None = None
    data: dict[str, Any] = field(default_factory=dict)


@dataclass
class DiagnosticResult:
    """Result of a diagnostic plugin run."""

    plugin_name: str
    status: Severity
    findings: list[Finding] = field(default_factory=list)
    raw_data: dict[str, Any] = field(default_factory=dict)
    duration_ms: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        return {
            "plugin_name": self.plugin_name,
            "status": self.status.value,
            "findings": [
                {
                    "title": f.title,
                    "severity": f.severity.value,
                    "description": f.description,
                    "suggestion": f.suggestion,
                    "command": f.command,
                    "data": f.data,
                }
                for f in self.findings
            ],
            "raw_data": self.raw_data,
            "duration_ms": self.duration_ms,
        }


class DiagnosticPlugin(ABC):
    """Bazowa klasa dla pluginów diagnostycznych fixOS.

    Aby stworzyć plugin:
    1. Dziedzicz po DiagnosticPlugin
    2. Ustaw name, description, version, platforms
    3. Zaimplementuj diagnose() -> DiagnosticResult
    4. Zarejestruj jako entry_point w pyproject.toml:
       [project.entry-points."fixos.diagnostics"]
       myplugin = "my_package:MyPlugin"
    """

    name: str = "unnamed"
    description: str = ""
    version: str = "0.1.0"
    platforms: list[str] = ["linux", "windows", "macos"]

    @abstractmethod
    def diagnose(self) -> DiagnosticResult:
        """Wykonaj diagnostykę i zwróć wynik."""
        ...

    def can_run(self) -> bool:
        """Czy plugin może działać na aktualnej platformie?"""
        import platform

        current = platform.system().lower()
        platform_map = {"linux": "linux", "darwin": "macos", "windows": "windows"}
        return platform_map.get(current, current) in self.platforms

    def get_metadata(self) -> dict:
        return {
            "name": self.name,
            "description": self.description,
            "version": self.version,
            "platforms": self.platforms,
        }
