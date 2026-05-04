"""
Shared utilities for diagnostic check modules.
"""

import subprocess
from typing import Any

try:
    import psutil
except ModuleNotFoundError:  # pragma: no cover
    psutil = None

from ...platform_utils import IS_LINUX as _IS_LINUX, IS_WINDOWS as _IS_WINDOWS, IS_MAC as _IS_MAC, SYSTEM as _SYSTEM
from ...constants import DIAGNOSTIC_CMD_TIMEOUT


def _psutil_required() -> bool:
    """Check if psutil is available."""
    return psutil is not None


def _cmd(cmd: str, timeout: int = DIAGNOSTIC_CMD_TIMEOUT) -> str:
    """Run a command and return output as string."""
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, timeout=timeout
        )
        out = result.stdout.strip()
        err = result.stderr.strip()
        combined = out
        if result.returncode != 0 and err:
            combined = f"{out}\n[ERR]: {err}" if out else f"[ERR]: {err}"
        return combined or "(brak outputu)"
    except subprocess.TimeoutExpired:
        return f"[TIMEOUT po {timeout}s]"
    except Exception as e:
        return f"[WYJĄTEK: {e}]"


# Export platform constants
IS_LINUX = _IS_LINUX
IS_WINDOWS = _IS_WINDOWS
IS_MAC = _IS_MAC
SYSTEM = _SYSTEM
psutil_module = psutil
