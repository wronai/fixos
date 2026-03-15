"""Plugin system for fixOS diagnostics."""
from .base import DiagnosticPlugin, DiagnosticResult, Finding, Severity
from .registry import PluginRegistry

__all__ = [
    "DiagnosticPlugin",
    "DiagnosticResult",
    "Finding",
    "Severity",
    "PluginRegistry",
]
