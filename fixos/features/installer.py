"""
Feature installer - safely installs missing packages.
"""

import subprocess
import shutil
from typing import List, Optional
from pathlib import Path

from .catalog import PackageInfo
from . import SystemInfo


class FeatureInstaller:
    """Safely installs packages using native package manager or other backends."""

    def __init__(self, system: SystemInfo, dry_run: bool = False):
        self.system = system
        self.dry_run = dry_run
        self.installed: List[str] = []
        self.failed: List[str] = []

    def install(self, packages: List[PackageInfo]) -> dict:
        """Install a list of packages."""
        results = {
            "installed": [],
            "failed": [],
            "skipped": [],
            "commands": [],
        }

        for pkg in packages:
            # Skip repos (they need special handling)
            if pkg.category == "repos":
                result = self._install_repo(pkg)
            else:
                result = self._install_package(pkg)

            if result == "installed":
                results["installed"].append(pkg.id)
            elif result == "failed":
                results["failed"].append(pkg.id)
            else:
                results["skipped"].append(pkg.id)

        return results

    def _install_package(self, pkg: PackageInfo) -> str:
        """Install a single package. Returns: installed|failed|skipped"""
        # Determine best installation method
        methods = []

        # 1. Native package manager
        distro_name = pkg.get_distro_name(self.system.distro)
        if distro_name:
            methods.append(("native", distro_name))

        # 2. Flatpak
        if pkg.flatpak and self.system.has_flatpak:
            methods.append(("flatpak", pkg.flatpak))

        # 3. pip
        if pkg.pip and self.system.has_pip:
            methods.append(("pip", pkg.pip))

        # 4. cargo
        if pkg.cargo and self.system.has_cargo:
            methods.append(("cargo", pkg.cargo))

        # 5. npm
        if pkg.npm and self.system.has_npm:
            methods.append(("npm", pkg.npm))

        # 6. Install script
        if pkg.install_script:
            methods.append(("script", pkg.install_script))

        if not methods:
            return "skipped"

        # Try methods in order
        for method, value in methods:
            if self.dry_run:
                print(f"  [DRY-RUN] Would install {pkg.id} via {method}: {value}")
                return "installed"

            try:
                if method == "native":
                    if self._install_native(value):
                        return "installed"
                elif method == "flatpak":
                    if self._install_flatpak(value):
                        return "installed"
                elif method == "pip":
                    if self._install_pip(value):
                        return "installed"
                elif method == "cargo":
                    if self._install_cargo(value):
                        return "installed"
                elif method == "npm":
                    if self._install_npm(value):
                        return "installed"
                elif method == "script":
                    if self._run_script(value):
                        return "installed"
            except Exception as e:
                print(f"  Failed to install {pkg.id} via {method}: {e}")
                continue

        return "failed"

    def _install_repo(self, pkg: PackageInfo) -> str:
        """Install a repository."""
        if not pkg.install_script:
            return "skipped"

        if self.dry_run:
            print(f"  [DRY-RUN] Would setup repo {pkg.id}")
            return "installed"

        try:
            if self._run_script(pkg.install_script):
                return "installed"
        except Exception as e:
            print(f"  Failed to setup repo {pkg.id}: {e}")

        return "failed"

    def _install_native(self, packages: str) -> bool:
        """Install via native package manager."""
        pm = self.system.pkg_manager
        commands = {
            "dnf": ["sudo", "dnf", "install", "-y"] + packages.split(),
            "apt": ["sudo", "apt", "install", "-y"] + packages.split(),
            "pacman": ["sudo", "pacman", "-S", "--noconfirm"] + packages.split(),
            "zypper": ["sudo", "zypper", "install", "-y"] + packages.split(),
            "xbps": ["sudo", "xbps-install", "-y"] + packages.split(),
        }

        cmd = commands.get(pm)
        if not cmd:
            return False

        result = subprocess.run(cmd, capture_output=True, timeout=300)
        return result.returncode == 0

    def _install_flatpak(self, app_id: str) -> bool:
        """Install via Flatpak."""
        cmd = ["flatpak", "install", "-y", "flathub", app_id]
        result = subprocess.run(cmd, capture_output=True, timeout=300)
        return result.returncode == 0

    def _install_pip(self, package: str) -> bool:
        """Install via pip."""
        pip_cmd = "pip3" if shutil.which("pip3") else "pip"
        cmd = [pip_cmd, "install", "--user", package]
        result = subprocess.run(cmd, capture_output=True, timeout=120)
        return result.returncode == 0

    def _install_cargo(self, package: str) -> bool:
        """Install via cargo."""
        cmd = ["cargo", "install", package]
        result = subprocess.run(cmd, capture_output=True, timeout=300)
        return result.returncode == 0

    def _install_npm(self, package: str) -> bool:
        """Install via npm."""
        cmd = ["npm", "install", "-g", package]
        result = subprocess.run(cmd, capture_output=True, timeout=120)
        return result.returncode == 0

    def _run_script(self, script: str) -> bool:
        """Run install script."""
        result = subprocess.run(
            script, shell=True, capture_output=True, timeout=300
        )
        return result.returncode == 0

    def get_rollback_commands(self, installed_packages: List[str]) -> List[str]:
        """Generate rollback commands for installed packages."""
        commands = []
        pm = self.system.pkg_manager

        for pkg_id in installed_packages:
            pkg = None
            # Find package in catalog (would need catalog reference)
            # For now, use native package removal

        # Generate command based on package manager
        if installed_packages:
            if pm == "dnf":
                commands.append(f"sudo dnf remove {' '.join(installed_packages)}")
            elif pm == "apt":
                commands.append(f"sudo apt remove {' '.join(installed_packages)}")
            elif pm == "pacman":
                commands.append(f"sudo pacman -R {' '.join(installed_packages)}")
            elif pm == "zypper":
                commands.append(f"sudo zypper remove {' '.join(installed_packages)}")
            elif pm == "xbps":
                commands.append(f"sudo xbps-remove {' '.join(installed_packages)}")

        return commands
