"""
System diagnostics aggregator.
Delegates to specialized check modules.
"""

from __future__ import annotations

from typing import Any

from .checks import (
    diagnose_audio,
    diagnose_thumbnails,
    diagnose_hardware,
    diagnose_system,
    diagnose_security,
    diagnose_resources,
)

# Module registry for diagnostic orchestration
DIAGNOSTIC_MODULES = {
    "system": ("🖥️  System (CPU/RAM/dyski/usługi)", diagnose_system),
    "audio": ("🔊 Dźwięk (ALSA/PipeWire/SOF/mikrofon)", diagnose_audio),
    "thumbnails": ("🖼️  Podglądy plików (thumbnails)", diagnose_thumbnails),
    "hardware": ("🔧 Sprzęt (kamera/touchpad/ACPI/DMI)", diagnose_hardware),
    "security": ("🔒 Bezpieczeństwo (firewall/porty/SELinux/SSH)", diagnose_security),
    "resources": ("📊 Zasoby (dysk/pamięć/procesy/autostart)", diagnose_resources),
}


def get_full_diagnostics(
    modules: list[str] | None = None,
    progress_callback=None,
) -> dict[str, Any]:
    """
    Zbiera diagnostykę z wybranych modułów.
    
    Args:
        modules: Lista modułów do uruchomienia (None = wszystkie)
        progress_callback: Funkcja (name, description) -> None do aktualizacji UI
    """
    selected = modules or list(DIAGNOSTIC_MODULES.keys())
    result = {}

    for key in selected:
        if key not in DIAGNOSTIC_MODULES:
            continue
        desc, fn = DIAGNOSTIC_MODULES[key]
        if progress_callback:
            progress_callback(key, desc)
        else:
            print(f"  → {desc}...", end="\r", flush=True)
        try:
            result[key] = fn()
        except Exception as e:
            result[key] = {"error": str(e)}

    if not progress_callback:
        print("  → Diagnostyka zakończona.  ")

    return result


# Re-export all diagnostic functions for backward compatibility
__all__ = [
    "get_full_diagnostics",
    "diagnose_audio",
    "diagnose_thumbnails",
    "diagnose_hardware",
    "diagnose_system",
    "diagnose_security",
    "diagnose_resources",
    "DIAGNOSTIC_MODULES",
]
