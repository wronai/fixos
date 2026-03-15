"""
System detection module for fixOS features.
Detects OS, DE, GPU, package manager, and installed packages.
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, Set, List
import platform
import subprocess
import shutil
import os


@dataclass
class SystemInfo:
    """Complete system information snapshot."""
    # OS
    os_family: str = "linux"
    distro: str = "unknown"
    distro_version: str = ""
    distro_id_like: List[str] = field(default_factory=list)
    kernel: str = ""

    # Desktop
    desktop_env: str = "none"
    display_server: str = "none"
    session_type: str = "tty"

    # Hardware
    gpu_vendor: str = "unknown"
    gpu_model: str = ""
    has_battery: bool = False
    cpu_arch: str = ""

    # Package Manager
    pkg_manager: str = "unknown"
    has_flatpak: bool = False
    has_snap: bool = False
    has_brew: bool = False
    has_pip: bool = False
    has_cargo: bool = False
    has_npm: bool = False

    # Installed packages cache
    installed_packages: Set[str] = field(default_factory=set)
    installed_flatpaks: Set[str] = field(default_factory=set)


class SystemDetector:
    """Detects system parameters."""

    def detect(self) -> SystemInfo:
        """Detect complete system information."""
        info = SystemInfo(
            os_family=self._detect_os_family(),
            distro=self._detect_distro(),
            distro_version=self._detect_distro_version(),
            kernel=platform.release(),
            cpu_arch=platform.machine(),
        )
        info.distro_id_like = self._detect_id_like()
        info.desktop_env = self._detect_de()
        info.display_server = self._detect_display_server()
        info.gpu_vendor = self._detect_gpu_vendor()
        info.gpu_model = self._detect_gpu_model()
        info.has_battery = Path("/sys/class/power_supply/BAT0").exists()
        info.pkg_manager = self._detect_pkg_manager()
        info.has_flatpak = shutil.which("flatpak") is not None
        info.has_snap = shutil.which("snap") is not None
        info.has_brew = shutil.which("brew") is not None
        info.has_pip = shutil.which("pip3") is not None or shutil.which("pip") is not None
        info.has_cargo = shutil.which("cargo") is not None
        info.has_npm = shutil.which("npm") is not None
        info.installed_packages = self._get_installed_packages(info.pkg_manager)
        if info.has_flatpak:
            info.installed_flatpaks = self._get_installed_flatpaks()
        return info

    def _detect_os_family(self) -> str:
        """Detect OS family."""
        system = platform.system().lower()
        if system == "linux":
            return "linux"
        elif system == "darwin":
            return "macos"
        elif system == "windows":
            return "windows"
        return "unknown"

    def _detect_distro(self) -> str:
        """Detect Linux distribution."""
        try:
            with open("/etc/os-release") as f:
                for line in f:
                    if line.startswith("ID="):
                        return line.strip().split("=")[1].strip('"').lower()
        except FileNotFoundError:
            pass
        return "unknown"

    def _detect_distro_version(self) -> str:
        """Detect distribution version."""
        try:
            with open("/etc/os-release") as f:
                for line in f:
                    if line.startswith("VERSION_ID="):
                        return line.strip().split("=")[1].strip('"').lower()
        except FileNotFoundError:
            pass
        return ""

    def _detect_id_like(self) -> List[str]:
        """Detect ID_LIKE from os-release."""
        try:
            with open("/etc/os-release") as f:
                for line in f:
                    if line.startswith("ID_LIKE="):
                        value = line.strip().split("=")[1].strip('"').lower()
                        return value.split()
        except FileNotFoundError:
            pass
        return []

    def _detect_de(self) -> str:
        """Detect desktop environment."""
        de = os.environ.get("XDG_CURRENT_DESKTOP", "").lower()
        session = os.environ.get("DESKTOP_SESSION", "").lower()
        wayland_display = os.environ.get("WAYLAND_DISPLAY", "")
        
        if "gnome" in de:
            return "gnome"
        elif "kde" in de or "plasma" in de:
            return "kde"
        elif "xfce" in de:
            return "xfce"
        elif "sway" in de or "sway" in session:
            return "sway"
        elif "hyprland" in de:
            return "hyprland"
        elif "i3" in de or "i3" in session:
            return "i3"
        elif "cinnamon" in de:
            return "cinnamon"
        elif "mate" in de:
            return "mate"
        elif "budgie" in de:
            return "budgie"
        
        # If graphical session but no DE detected
        if self._detect_display_server() != "none":
            return de or "other"
        
        return "none"

    def _detect_display_server(self) -> str:
        """Detect display server (Wayland/X11)."""
        wayland_display = os.environ.get("WAYLAND_DISPLAY", "")
        display = os.environ.get("DISPLAY", "")
        
        if wayland_display:
            return "wayland"
        elif display:
            return "x11"
        return "none"

    def _detect_gpu_vendor(self) -> str:
        """Detect GPU vendor."""
        try:
            # Try lspci first
            result = subprocess.run(
                ["lspci"], capture_output=True, text=True, timeout=5
            )
            lspci_output = result.stdout.lower()
            
            if "nvidia" in lspci_output:
                return "nvidia"
            elif "amd" in lspci_output or "radeon" in lspci_output or "advanced micro devices" in lspci_output:
                return "amd"
            elif "intel" in lspci_output:
                return "intel"
        except Exception:
            pass
        
        # Fallback: check /sys/class/drm
        try:
            for card in Path("/sys/class/drm").glob("card*"):
                vendor_file = card / "device/vendor"
                if vendor_file.exists():
                    vendor = vendor_file.read_text().strip().lower()
                    if "10de" in vendor:
                        return "nvidia"
                    elif "1002" in vendor:
                        return "amd"
                    elif "8086" in vendor:
                        return "intel"
        except Exception:
            pass
        
        return "unknown"

    def _detect_gpu_model(self) -> str:
        """Detect GPU model."""
        try:
            result = subprocess.run(
                ["lspci"], capture_output=True, text=True, timeout=5
            )
            for line in result.stdout.split("\n"):
                if "vga" in line.lower() or "3d" in line.lower():
                    # Extract model name
                    parts = line.split(":")[-1].strip()
                    return parts
        except Exception:
            pass
        return ""

    def _detect_pkg_manager(self) -> str:
        """Detect package manager."""
        for pm, cmd in [
            ("dnf", "dnf"),
            ("apt", "apt"),
            ("pacman", "pacman"),
            ("zypper", "zypper"),
            ("xbps", "xbps-install"),
        ]:
            if shutil.which(cmd):
                return pm
        return "unknown"

    def _get_installed_packages(self, pm: str) -> Set[str]:
        """Get list of installed native packages."""
        commands = {
            "dnf": ["rpm", "-qa", "--queryformat", "%{NAME}\n"],
            "apt": ["dpkg-query", "-W", "-f", "${Package}\n"],
            "pacman": ["pacman", "-Qq"],
            "zypper": ["rpm", "-qa", "--queryformat", "%{NAME}\n"],
            "xbps": ["xbps-query", "-l"],
        }
        cmd = commands.get(pm)
        if not cmd:
            return set()
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            if pm == "xbps":
                # xbps-query -l format: [i] package-version ...
                packages = []
                for line in result.stdout.strip().split("\n"):
                    if line.startswith("[i]"):
                        parts = line.split()
                        if len(parts) >= 2:
                            pkg_name = parts[1].rsplit("-", 1)[0]  # Remove version
                            packages.append(pkg_name)
                return set(packages)
            return set(result.stdout.strip().split("\n"))
        except Exception:
            return set()

    def _get_installed_flatpaks(self) -> Set[str]:
        """Get list of installed Flatpak apps."""
        try:
            result = subprocess.run(
                ["flatpak", "list", "--app", "--columns=application"],
                capture_output=True, text=True, timeout=10
            )
            return set(line.strip() for line in result.stdout.strip().split("\n") if line.strip())
        except Exception:
            return set()
