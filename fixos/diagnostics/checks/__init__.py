"""
Diagnostic check modules for system analysis.
Each module focuses on a specific system aspect.
"""

from .audio import diagnose_audio
from .thumbnails import diagnose_thumbnails
from .hardware import diagnose_hardware
from .system_core import diagnose_system
from .security import diagnose_security
from .resources import diagnose_resources
from .packages import diagnose_packages
from .storage_optimization import diagnose_storage
from .file_analysis import diagnose_files

__all__ = [
    "diagnose_audio",
    "diagnose_thumbnails",
    "diagnose_hardware",
    "diagnose_system",
    "diagnose_security",
    "diagnose_resources",
    "diagnose_packages",
    "diagnose_storage",
    "diagnose_files",
]
