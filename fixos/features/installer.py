"""
Feature installer - safely installs missing packages.
"""

import subprocess
import shutil
from typing import List

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

    def _build_install_methods(self, pkg: PackageInfo) -> list:
        """Return ordered list of (method, value) pairs available for this package."""
        methods = []
        distro_name = pkg.get_distro_name(self.system.distro)
        if distro_name:
            methods.append(("native", distro_name))
        if pkg.flatpak and self.system.has_flatpak:
            methods.append(("flatpak", pkg.flatpak))
        if pkg.pip and self.system.has_pip:
            methods.append(("pip", pkg.pip))
        if pkg.cargo and self.system.has_cargo:
            methods.append(("cargo", pkg.cargo))
        if pkg.npm and self.system.has_npm:
            methods.append(("npm", pkg.npm))
        if pkg.install_script:
            methods.append(("script", pkg.install_script))
        return methods

    def _install_package(self, pkg: PackageInfo) -> str:
        """Install a single package. Returns: installed|failed|skipped"""
        methods = self._build_install_methods(pkg)
        if not methods:
            return "skipped"

        method_dispatch = {
            "native":  self._install_native,
            "flatpak": self._install_flatpak,
            "pip":     self._install_pip,
            "cargo":   self._install_cargo,
            "npm":     self._install_npm,
            "script":  self._run_script,
        }

        for method, value in methods:
            if self.dry_run:
                print(f"  [DRY-RUN] Would install {pkg.id} via {method}: {value}")
                return "installed"
            try:
                if method_dispatch[method](value):
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
        if not installed_packages:
            return []

        pm = self.system.pkg_manager
        pkg_list = " ".join(installed_packages)

        rollback_map = {
            "dnf": f"sudo dnf remove {pkg_list}",
            "apt": f"sudo apt remove {pkg_list}",
            "pacman": f"sudo pacman -R {pkg_list}",
            "zypper": f"sudo zypper remove {pkg_list}",
            "xbps": f"sudo xbps-remove {pkg_list}",
        }

        if pm in rollback_map:
            return [rollback_map[pm]]
        return []
