"""
Cross-platform utilities for fixos.
Handles differences between Linux, macOS, and Windows.
"""

from __future__ import annotations

import os
import platform
import subprocess
import sys
from pathlib import Path
from typing import Optional

SYSTEM = platform.system()  # "Linux", "Darwin", "Windows"
IS_LINUX = SYSTEM == "Linux"
IS_WINDOWS = SYSTEM == "Windows"
IS_MAC = SYSTEM == "Darwin"
IS_POSIX = IS_LINUX or IS_MAC


def get_os_info() -> dict:
    """Returns basic OS information."""
    info = {
        "system": SYSTEM,
        "release": platform.release(),
        "version": platform.version(),
        "machine": platform.machine(),
        "python": sys.version.split()[0],
    }
    if IS_LINUX:
        try:
            info["distro"] = Path("/etc/os-release").read_text(errors="replace")[:300]
        except Exception:
            info["distro"] = "unknown"
    if IS_WINDOWS:
        info["edition"] = platform.win32_edition() if hasattr(platform, "win32_edition") else "unknown"
    return info


def needs_elevation(cmd: str) -> bool:
    """Returns True if command likely needs admin/sudo."""
    cmd = cmd.strip()
    if IS_WINDOWS:
        elevated_prefixes = [
            "sc ", "net ", "netsh ", "reg ", "bcdedit", "diskpart",
            "sfc ", "dism ", "wmic ", "powercfg", "icacls",
        ]
        return any(cmd.lower().startswith(p) for p in elevated_prefixes)
    else:
        sudo_prefixes = [
            "dnf", "apt", "apt-get", "yum", "pacman", "zypper",
            "rpm", "systemctl", "firewall-cmd", "setenforce",
            "modprobe", "rmmod", "alsactl", "grub2-", "update-grub",
            "chmod 0", "chown", "mount", "umount", "useradd", "usermod",
            "snap install", "flatpak install",
        ]
        return any(cmd.startswith(p) for p in sudo_prefixes) and not cmd.startswith("sudo")


def elevate_cmd(cmd: str) -> str:
    """Adds sudo (Linux/Mac) or wraps in PowerShell -Verb RunAs (Windows)."""
    if IS_WINDOWS:
        # On Windows, we can't auto-elevate inline; just return as-is with a note
        return cmd
    else:
        if needs_elevation(cmd):
            return "sudo " + cmd.strip()
        return cmd


def is_dangerous(cmd: str) -> Optional[str]:
    """Returns reason string if command is dangerous, None if safe."""
    import re
    patterns = [
        (r"rm\s+-rf\s+/(?!\w)", "rm -rf / destroys root filesystem"),
        (r"rm\s+-rf\s+/(?:boot|etc|usr|lib|bin|sbin)\b", "deletes critical system directory"),
        (r"dd\s+if=.*of=/dev/(?:sd|nvme|vd|hd)[a-z](?!\d)", "overwrites disk with dd"),
        (r"mkfs\.", "formats filesystem"),
        (r":\(\)\{.*\};:", "fork bomb"),
        (r">\s*/dev/(?:sd|nvme|vd)", "writes directly to block device"),
        (r"format\s+[a-z]:", "Windows format command"),
        (r"del\s+/[sf]\s+[a-z]:\\windows", "deletes Windows system files"),
    ]
    for pat, reason in patterns:
        if re.search(pat, cmd, re.IGNORECASE):
            return reason
    return None


def run_command(
    cmd: str,
    timeout: int = 120,
    shell: bool = True,
) -> tuple[bool, str, str, int]:
    """
    Runs a command cross-platform.
    Returns (success, stdout, stderr, returncode).
    """
    try:
        if IS_WINDOWS and not shell:
            import shlex
            args = shlex.split(cmd)
        else:
            args = cmd

        proc = subprocess.run(
            args,
            shell=shell,
            capture_output=True,
            text=True,
            timeout=timeout,
            encoding="utf-8",
            errors="replace",
        )
        return proc.returncode == 0, proc.stdout.strip(), proc.stderr.strip(), proc.returncode
    except subprocess.TimeoutExpired:
        return False, "", f"[TIMEOUT {timeout}s]", -2
    except Exception as e:
        return False, "", f"[ERROR: {e}]", -3


def get_package_manager() -> Optional[str]:
    """Detects the system package manager."""
    if IS_WINDOWS:
        for pm in ["winget", "choco", "scoop"]:
            if _cmd_exists(pm):
                return pm
        return None
    elif IS_MAC:
        if _cmd_exists("brew"):
            return "brew"
        return None
    else:
        for pm in ["dnf", "apt-get", "apt", "pacman", "zypper", "yum", "apk"]:
            if _cmd_exists(pm):
                return pm
        return None


def install_package_cmd(package: str) -> str:
    """Returns the install command for the detected package manager."""
    pm = get_package_manager()
    if not pm:
        return f"# No package manager detected. Install {package} manually."
    cmds = {
        "dnf": f"dnf install -y {package}",
        "apt-get": f"apt-get install -y {package}",
        "apt": f"apt install -y {package}",
        "pacman": f"pacman -S --noconfirm {package}",
        "zypper": f"zypper install -y {package}",
        "yum": f"yum install -y {package}",
        "apk": f"apk add {package}",
        "brew": f"brew install {package}",
        "winget": f"winget install {package}",
        "choco": f"choco install -y {package}",
        "scoop": f"scoop install {package}",
    }
    return cmds.get(pm, f"# install {package}")


def _cmd_exists(cmd: str) -> bool:
    import shutil
    return shutil.which(cmd) is not None


def setup_signal_timeout(seconds: int, handler) -> bool:
    """
    Sets up a timeout signal. Returns True if supported (POSIX only).
    Windows does not support SIGALRM.
    """
    if IS_POSIX:
        import signal
        signal.signal(signal.SIGALRM, handler)
        signal.alarm(seconds)
        return True
    return False


def cancel_signal_timeout():
    """Cancels the timeout signal (POSIX only)."""
    if IS_POSIX:
        import signal
        signal.alarm(0)
