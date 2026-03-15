#!/usr/bin/env python3
"""
Service Data Scanner for fixOS
Scans data from various services (Docker, Ollama, etc.) and allows cleanup
"""

import os
import shutil
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum


class ServiceType(Enum):
    DOCKER = "docker"
    OLLAMA = "ollama"
    CONTAINERD = "containerd"
    PODMAN = "podman"
    NPM = "npm"
    YARN = "yarn"
    PNPM = "pnpm"
    PIP = "pip"
    CONDA = "conda"
    POETRY = "poetry"
    GRADLE = "gradle"
    MAVEN = "maven"
    CARGO = "cargo"
    GO = "go"
    FLUTTER = "flutter"
    DART = "dart"
    ANDROID = "android"
    SNAP = "snap"
    FLATPAK = "flatpak"
    APPIMAGE = "appimage"
    VAGRANT = "vagrant"
    VBOX = "virtualbox"
    VMWARE = "vmware"
    NIX = "nix"
    BREW = "brew"
    APT = "apt"
    DNF = "dnf"
    PACMAN = "pacman"
    YUM = "yum"
    ZYPPER = "zypper"
    CHROME = "chrome"
    FIREFOX = "firefox"
    EDGE = "edge"
    VSCODE = "vscode"
    JETBRAINS = "jetbrains"
    CURSOR = "cursor"
    HUGGINGFACE = "huggingface"
    AWS = "aws"
    GCLOUD = "gcloud"
    AZURE = "azure"
    TERRAFORM = "terraform"
    PULUMI = "pulumi"
    UNITY = "unity"
    UNREAL = "unreal"
    JUPYTER = "jupyter"
    THUMBNAILS = "thumbnails"
    TRASH = "trash"
    LOGS = "logs"
    UNKNOWN = "unknown"


@dataclass
class ServiceDataInfo:
    """Information about service data"""
    service_type: ServiceType
    name: str
    path: str
    size_mb: float
    size_gb: float
    description: str
    can_cleanup: bool
    cleanup_command: str
    preview_command: str
    safe_to_cleanup: bool
    impact: str = "medium"
    items_count: Optional[int] = None
    details: Dict[str, Any] = field(default_factory=dict)


class ServiceDataScanner:
    """Scans for large service data directories and allows cleanup"""
    
    DEFAULT_THRESHOLD_MB = 500  # Default 500MB threshold
    
    # Service paths and detection patterns
    SERVICE_PATHS = {
        # Container runtimes
        ServiceType.DOCKER: [
            "/var/lib/docker",
            "~/.docker",
        ],
        ServiceType.OLLAMA: [
            "~/.ollama",
            "/usr/share/ollama",
        ],
        ServiceType.CONTAINERD: [
            "/var/lib/containerd",
            "/run/containerd",
        ],
        ServiceType.PODMAN: [
            "~/.local/share/containers",
            "~/.config/containers",
        ],
        # JavaScript/Node package managers
        ServiceType.NPM: [
            "~/.npm",
            "~/.cache/npm",
        ],
        ServiceType.YARN: [
            "~/.cache/yarn",
            "~/.yarn",
            "~/.config/yarn",
        ],
        ServiceType.PNPM: [
            "~/.pnpm-store",
            "~/.local/share/pnpm",
            "~/Library/pnpm",  # macOS
        ],
        # Python package managers
        ServiceType.PIP: [
            "~/.cache/pip",
            "~/.local/lib/python*/site-packages",
        ],
        ServiceType.CONDA: [
            "~/anaconda3",
            "~/miniconda3",
            "~/miniforge3",
            "~/.conda",
            "~/opt/anaconda3",
            "~/opt/miniconda3",
        ],
        ServiceType.POETRY: [
            "~/.cache/pypoetry",
            "~/Library/Caches/pypoetry",  # macOS
        ],
        # Java build tools
        ServiceType.GRADLE: [
            "~/.gradle",
            "~/.cache/gradle",
        ],
        ServiceType.MAVEN: [
            "~/.m2",
        ],
        # Rust
        ServiceType.CARGO: [
            "~/.cargo/registry",
            "~/.cargo/git",
        ],
        # Go
        ServiceType.GO: [
            "~/go/pkg",
            "~/.go/pkg",
            "~/go/bin",
        ],
        # Mobile development
        ServiceType.FLUTTER: [
            "~/.flutter-sdk",
            "~/flutter",
            "~/.pub-cache",
        ],
        ServiceType.DART: [
            "~/.pub-cache",
        ],
        ServiceType.ANDROID: [
            "~/Android/Sdk",
            "~/Library/Android/sdk",  # macOS
            "~/.android",
        ],
        # System package managers
        ServiceType.SNAP: [
            "/var/snap",
            "/snap",
        ],
        ServiceType.FLATPAK: [
            "~/.local/share/flatpak",
            "/var/lib/flatpak",
        ],
        ServiceType.APPIMAGE: [
            "~/.local/share/AppImage",
            "~/.cache/AppImage",
        ],
        ServiceType.APT: [
            "/var/cache/apt/archives",
        ],
        ServiceType.DNF: [
            "/var/cache/dnf",
        ],
        ServiceType.YUM: [
            "/var/cache/yum",
        ],
        ServiceType.PACMAN: [
            "/var/cache/pacman/pkg",
        ],
        ServiceType.ZYPPER: [
            "/var/cache/zypp",
        ],
        # Virtualization
        ServiceType.VAGRANT: [
            "~/.vagrant.d",
            "~/VirtualBox VMs",
        ],
        ServiceType.VBOX: [
            "~/VirtualBox VMs",
            "~/.config/VirtualBox",
        ],
        ServiceType.VMWARE: [
            "~/vmware",
            "~/Virtual Machines",
            "~/.vmware",
        ],
        # Package managers (nix, brew)
        ServiceType.NIX: [
            "~/.nix-profile",
            "~/.nix-defexpr",
            "~/.nixpkgs",
            "/nix",
        ],
        ServiceType.BREW: [
            "~/homebrew",
            "/usr/local/Homebrew",
            "/opt/homebrew",
            "~/.homebrew",
        ],
        # Browsers
        ServiceType.CHROME: [
            "~/.cache/google-chrome",
            "~/.config/google-chrome/Default/Service Worker",
            "~/Library/Caches/Google/Chrome",  # macOS
        ],
        ServiceType.FIREFOX: [
            "~/.cache/mozilla",
            "~/.mozilla/firefox/*/cache2",
            "~/Library/Caches/Firefox",  # macOS
        ],
        ServiceType.EDGE: [
            "~/.cache/microsoft-edge",
            "~/Library/Caches/Microsoft Edge",  # macOS
        ],
        # IDEs and editors
        ServiceType.VSCODE: [
            "~/.vscode/extensions",
            "~/.config/Code/Cache",
            "~/.config/Code/CachedData",
            "~/Library/Application Support/Code/Cache",  # macOS
        ],
        ServiceType.CURSOR: [
            "~/.cursor/extensions",
            "~/.config/Cursor/Cache",
            "~/.config/Cursor/CachedData",
        ],
        ServiceType.JETBRAINS: [
            "~/.JetBrains",
            "~/.cache/JetBrains",
            "~/Library/Caches/JetBrains",  # macOS
            "~/.config/JetBrains",
        ],
        # ML/AI caches
        ServiceType.HUGGINGFACE: [
            "~/.cache/huggingface",
            "~/.huggingface",
        ],
        # Cloud CLIs
        ServiceType.AWS: [
            "~/.aws/sso/cache",
            "~/.aws/cli/cache",
        ],
        ServiceType.GCLOUD: [
            "~/.config/gcloud/logs",
            "~/.cache/gcloud",
        ],
        ServiceType.AZURE: [
            "~/.azure/telemetry",
            "~/.azure/logs",
        ],
        # Infrastructure as Code
        ServiceType.TERRAFORM: [
            "~/.terraform.d/plugin-cache",
            "~/.terraform.d/providers",
        ],
        ServiceType.PULUMI: [
            "~/.pulumi/plugins",
        ],
        # Game engines
        ServiceType.UNITY: [
            "~/.config/unity3d",
            "~/.cache/unity3d",
            "~/Library/Unity",  # macOS
        ],
        ServiceType.UNREAL: [
            "~/.config/Epic",
            "~/Library/Application Support/Epic",  # macOS
        ],
        # Jupyter
        ServiceType.JUPYTER: [
            "~/.local/share/jupyter/runtime",
            "~/.local/share/jupyter/kernels",
            "~/Library/Jupyter",  # macOS
        ],
        # System
        ServiceType.THUMBNAILS: [
            "~/.cache/thumbnails",
            "~/.thumbnails",
        ],
        ServiceType.TRASH: [
            "~/.local/share/Trash",
            "~/.trash",
            "~/.Trash",  # macOS
        ],
        ServiceType.LOGS: [
            "~/.cache/log",
            "~/.local/state",
        ],
    }
    
    def __init__(self, threshold_mb: int = None):
        self.threshold_mb = threshold_mb or self.DEFAULT_THRESHOLD_MB
        self.threshold_gb = self.threshold_mb / 1024
        
    def scan_all_services(self) -> List[ServiceDataInfo]:
        """Scan all known services for data above threshold"""
        results = []
        
        for service_type in ServiceType:
            if service_type == ServiceType.UNKNOWN:
                continue
            service_data = self.scan_service(service_type)
            results.extend(service_data)
            
        # Sort by size (largest first)
        results.sort(key=lambda x: x.size_mb, reverse=True)
        return results
    
    def scan_service(self, service_type: ServiceType) -> List[ServiceDataInfo]:
        """Scan specific service type for data"""
        results = []
        paths = self.SERVICE_PATHS.get(service_type, [])
        
        for path_pattern in paths:
            # Expand home directory
            expanded_path = os.path.expanduser(path_pattern)
            
            # Handle glob patterns
            import glob
            matching_paths = glob.glob(expanded_path) or [expanded_path]
            
            for path in matching_paths:
                if os.path.exists(path):
                    info = self._analyze_service_path(service_type, path)
                    if info and info.size_mb >= self.threshold_mb:
                        results.append(info)
                        
        return results
    
    def _analyze_service_path(self, service_type: ServiceType, path: str) -> Optional[ServiceDataInfo]:
        """Analyze a specific service path"""
        try:
            size_mb = self._get_path_size_mb(path)
            size_gb = size_mb / 1024
            
            if size_mb < self.threshold_mb:
                return None
                
            details = self._get_service_details(service_type, path)
            
            return ServiceDataInfo(
                service_type=service_type,
                name=service_type.value.title(),
                path=path,
                size_mb=round(size_mb, 2),
                size_gb=round(size_gb, 3),
                description=self._get_service_description(service_type),
                can_cleanup=True,
                cleanup_command=self._get_cleanup_command(service_type, path),
                preview_command=self._get_preview_command(service_type, path),
                safe_to_cleanup=self._is_safe_cleanup(service_type),
                impact="high" if size_gb > 1.0 else "medium",
                items_count=details.get("items_count"),
                details=details
            )
        except Exception as e:
            return ServiceDataInfo(
                service_type=service_type,
                name=service_type.value.title(),
                path=path,
                size_mb=0,
                size_gb=0,
                description=f"Error analyzing: {str(e)}",
                can_cleanup=False,
                cleanup_command="",
                preview_command="",
                safe_to_cleanup=False,
                impact="none",
                details={"error": str(e)}
            )
    
    def _get_path_size_mb(self, path: str) -> float:
        """Get size of path in MB"""
        total_size = 0
        
        if os.path.isfile(path):
            return os.path.getsize(path) / (1024 * 1024)
            
        try:
            for dirpath, dirnames, filenames in os.walk(path):
                for filename in filenames:
                    filepath = os.path.join(dirpath, filename)
                    try:
                        total_size += os.path.getsize(filepath)
                    except (OSError, FileNotFoundError):
                        continue
        except (OSError, PermissionError):
            pass
            
        return total_size / (1024 * 1024)
    
    def _get_service_details(self, service_type: ServiceType, path: str) -> Dict[str, Any]:
        """Get additional details about service data"""
        details = {}
        
        if service_type == ServiceType.DOCKER:
            details.update(self._get_docker_details())
        elif service_type == ServiceType.OLLAMA:
            details.update(self._get_ollama_details())
        elif service_type in [ServiceType.NPM, ServiceType.YARN, ServiceType.PNPM, 
                             ServiceType.PIP, ServiceType.CONDA, ServiceType.POETRY,
                             ServiceType.GRADLE, ServiceType.MAVEN, ServiceType.CARGO,
                             ServiceType.GO]:
            details.update(self._get_package_cache_details(path))
        elif service_type == ServiceType.CONDA:
            details.update(self._get_conda_details())
            
        return details
    
    def _get_conda_details(self) -> Dict[str, Any]:
        """Get Conda-specific details"""
        details = {"items_count": 0, "envs": []}
        
        try:
            result = subprocess.run(
                ["conda", "env", "list"],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                lines = result.stdout.strip().split("\n")
                for line in lines[2:]:  # Skip header
                    if line.strip():
                        parts = line.split()
                        if parts:
                            details["envs"].append(parts[0])
                details["items_count"] = len(details["envs"])
        except Exception:
            pass
            
        return details
    
    def _get_docker_details(self) -> Dict[str, Any]:
        """Get Docker-specific details"""
        details = {"items_count": 0, "components": {}}
        
        try:
            # Check docker disk usage
            result = subprocess.run(
                ["docker", "system", "df", "-v"],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                lines = result.stdout.strip().split("\n")
                for line in lines:
                    if "Images" in line or "Containers" in line or "Volumes" in line or "Build Cache" in line:
                        parts = line.split()
                        if len(parts) >= 2:
                            component = parts[0]
                            try:
                                count = int(parts[1]) if parts[1].isdigit() else 0
                                details["components"][component] = count
                                details["items_count"] += count
                            except ValueError:
                                pass
        except Exception:
            pass
            
        # Get more detailed info
        try:
            images_result = subprocess.run(
                ["docker", "images", "-q"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if images_result.returncode == 0:
                image_count = len([l for l in images_result.stdout.strip().split("\n") if l])
                details["components"]["images"] = image_count
                
            containers_result = subprocess.run(
                ["docker", "ps", "-aq"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if containers_result.returncode == 0:
                container_count = len([l for l in containers_result.stdout.strip().split("\n") if l])
                details["components"]["containers"] = container_count
        except Exception:
            pass
            
        return details
    
    def _get_ollama_details(self) -> Dict[str, Any]:
        """Get Ollama-specific details"""
        details = {"items_count": 0, "models": []}
        
        try:
            result = subprocess.run(
                ["ollama", "list"],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                lines = result.stdout.strip().split("\n")
                # Skip header
                for line in lines[1:]:
                    if line.strip():
                        parts = line.split()
                        if parts:
                            details["models"].append(parts[0])
                details["items_count"] = len(details["models"])
        except Exception:
            pass
            
        return details
    
    def _get_package_cache_details(self, path: str) -> Dict[str, Any]:
        """Get package cache details"""
        details = {"items_count": 0}
        
        try:
            # Count items in cache
            count = 0
            for _, _, files in os.walk(path):
                count += len(files)
                if count > 10000:  # Don't count too many
                    break
            details["items_count"] = count if count <= 10000 else "10000+"
        except Exception:
            pass
            
        return details
    
    def _get_service_description(self, service_type: ServiceType) -> str:
        """Get description for service type"""
        descriptions = {
            # Containers
            ServiceType.DOCKER: "Docker images, containers, and volumes",
            ServiceType.OLLAMA: "Ollama AI models and cache",
            ServiceType.CONTAINERD: "Containerd container runtime data",
            ServiceType.PODMAN: "Podman containers and images",
            # JS/Node
            ServiceType.NPM: "NPM package cache",
            ServiceType.YARN: "Yarn package cache",
            ServiceType.PNPM: "PNPM store cache",
            # Python
            ServiceType.PIP: "Python pip cache",
            ServiceType.CONDA: "Conda/Anaconda environments and packages",
            ServiceType.POETRY: "Poetry virtual environments and cache",
            # Java
            ServiceType.GRADLE: "Gradle build cache",
            ServiceType.MAVEN: "Maven repository cache",
            # Rust/Go
            ServiceType.CARGO: "Rust Cargo registry cache",
            ServiceType.GO: "Go modules cache",
            # Mobile
            ServiceType.FLUTTER: "Flutter SDK and pub cache",
            ServiceType.DART: "Dart pub cache",
            ServiceType.ANDROID: "Android SDK and build cache",
            # System packages
            ServiceType.SNAP: "Snap packages and cache",
            ServiceType.FLATPAK: "Flatpak applications and runtimes",
            ServiceType.APPIMAGE: "AppImage applications",
            ServiceType.APT: "APT package cache",
            ServiceType.DNF: "DNF package cache",
            ServiceType.PACMAN: "Pacman package cache",
            ServiceType.YUM: "Yum package cache",
            ServiceType.ZYPPER: "Zypper package cache",
            # Virtualization
            ServiceType.VAGRANT: "Vagrant boxes and VMs",
            ServiceType.VBOX: "VirtualBox VMs and cache",
            ServiceType.VMWARE: "VMware virtual machines",
            # Package managers
            ServiceType.NIX: "Nix store and profiles",
            ServiceType.BREW: "Homebrew cache and Cellar",
            # Browsers
            ServiceType.CHROME: "Google Chrome cache and data",
            ServiceType.FIREFOX: "Firefox cache and data",
            ServiceType.EDGE: "Microsoft Edge cache and data",
            # IDEs
            ServiceType.VSCODE: "VS Code extensions and cache",
            ServiceType.CURSOR: "Cursor editor cache",
            ServiceType.JETBRAINS: "JetBrains IDE caches and indexes",
            # Cloud/ML
            ServiceType.HUGGINGFACE: "HuggingFace models cache",
            ServiceType.AWS: "AWS CLI cache and logs",
            ServiceType.GCLOUD: "Google Cloud CLI cache",
            ServiceType.AZURE: "Azure CLI telemetry and logs",
            # IaC
            ServiceType.TERRAFORM: "Terraform provider plugins cache",
            ServiceType.PULUMI: "Pulumi plugins cache",
            # Game engines
            ServiceType.UNITY: "Unity Editor cache and data",
            ServiceType.UNREAL: "Unreal Engine cache",
            # Other
            ServiceType.JUPYTER: "Jupyter runtime and kernels",
            ServiceType.THUMBNAILS: "Thumbnail cache",
            ServiceType.TRASH: "Trash/Recycle Bin",
            ServiceType.LOGS: "Application logs",
        }
        return descriptions.get(service_type, f"{service_type.value} data")
    
    def _get_cleanup_command(self, service_type: ServiceType, path: str) -> str:
        """Get cleanup command for service"""
        commands = {
            # Containers
            ServiceType.DOCKER: "docker system prune -af --volumes",
            ServiceType.OLLAMA: "ollama rm $(ollama list | tail -n +2 | awk '{print $1}') 2>/dev/null || true && rm -rf ~/.ollama/models/*",
            ServiceType.CONTAINERD: "sudo rm -rf /var/lib/containerd",
            ServiceType.PODMAN: "podman system prune -af --volumes",
            # JS/Node
            ServiceType.NPM: "npm cache clean --force",
            ServiceType.YARN: "yarn cache clean --all",
            ServiceType.PNPM: "pnpm store prune",
            # Python
            ServiceType.PIP: "pip cache purge || rm -rf ~/.cache/pip/*",
            ServiceType.CONDA: "conda clean --all -y || rm -rf ~/.conda/envs/*/pkgs",
            ServiceType.POETRY: "poetry cache clear --all pypi || rm -rf ~/.cache/pypoetry",
            # Java
            ServiceType.GRADLE: "rm -rf ~/.gradle/caches ~/.gradle/daemon ~/.gradle/wrapper",
            ServiceType.MAVEN: "rm -rf ~/.m2/repository",
            # Rust/Go
            ServiceType.CARGO: "cargo clean --registry || rm -rf ~/.cargo/registry/cache",
            ServiceType.GO: "go clean -cache -modcache && rm -rf ~/go/pkg",
            # Mobile
            ServiceType.FLUTTER: "flutter pub cache clean && rm -rf ~/.pub-cache",
            ServiceType.DART: "rm -rf ~/.pub-cache",
            ServiceType.ANDROID: "rm -rf ~/.android/build-cache ~/Android/Sdk/build-tools/*/preview",
            # System packages
            ServiceType.SNAP: "snap list --all | awk '/disabled/{print $1, $3}' | while read snapname revision; do sudo snap remove \"$snapname\" --revision=\"$revision\"; done",
            ServiceType.FLATPAK: "flatpak uninstall --unused -y && flatpak repair",
            ServiceType.APPIMAGE: "rm -rf ~/.local/share/AppImage ~/.cache/AppImage",
            ServiceType.APT: "sudo apt-get clean && sudo apt-get autoclean",
            ServiceType.DNF: "sudo dnf clean all",
            ServiceType.PACMAN: "sudo pacman -Scc --noconfirm",
            ServiceType.YUM: "sudo yum clean all",
            ServiceType.ZYPPER: "sudo zypper clean --all",
            # Virtualization
            ServiceType.VAGRANT: "vagrant box prune --force",
            ServiceType.VBOX: "rm -rf ~/VirtualBox\\ VMs/*/Snapshots",
            ServiceType.VMWARE: "rm -rf ~/vmware/*.log ~/vmware/*.vmss",
            # Package managers
            ServiceType.NIX: "nix-collect-garbage -d || nix store gc",
            ServiceType.BREW: "brew cleanup --prune=all && brew autoremove",
            # Browsers
            ServiceType.CHROME: "rm -rf ~/.cache/google-chrome ~/.config/google-chrome/Default/Service\\ Worker",
            ServiceType.FIREFOX: "rm -rf ~/.cache/mozilla ~/.mozilla/firefox/*/cache2",
            ServiceType.EDGE: "rm -rf ~/.cache/microsoft-edge",
            # IDEs
            ServiceType.VSCODE: "rm -rf ~/.config/Code/Cache ~/.config/Code/CachedData ~/.vscode/extensions/*/out",
            ServiceType.CURSOR: "rm -rf ~/.config/Cursor/Cache ~/.config/Cursor/CachedData ~/.cursor/extensions/*/out",
            ServiceType.JETBRAINS: "find ~/.cache/JetBrains -name 'index' -type d -exec rm -rf {} + 2>/dev/null; find ~/.JetBrains -name 'caches' -type d -exec rm -rf {} + 2>/dev/null",
            # Cloud/ML
            ServiceType.HUGGINGFACE: "rm -rf ~/.cache/huggingface/hub/*",
            ServiceType.AWS: "rm -rf ~/.aws/sso/cache ~/.aws/cli/cache",
            ServiceType.GCLOUD: "gcloud auth application-default revoke 2>/dev/null; rm -rf ~/.config/gcloud/logs ~/.cache/gcloud",
            ServiceType.AZURE: "rm -rf ~/.azure/telemetry ~/.azure/logs",
            # IaC
            ServiceType.TERRAFORM: "rm -rf ~/.terraform.d/plugin-cache",
            ServiceType.PULUMI: "pulumi plugin rm --all --yes 2>/dev/null || rm -rf ~/.pulumi/plugins",
            # Game engines
            ServiceType.UNITY: "rm -rf ~/.config/unity3d/Editor/Cache",
            ServiceType.UNREAL: "rm -rf ~/.config/Epic/UnrealEngine/5.*/DerivedDataCache",
            # Other
            ServiceType.JUPYTER: "jupyter kernelspec uninstall -y $(jupyter kernelspec list | tail -n +2 | awk '{print $1}') 2>/dev/null; rm -rf ~/.local/share/jupyter/runtime",
            ServiceType.THUMBNAILS: "rm -rf ~/.cache/thumbnails/* ~/.thumbnails/*",
            ServiceType.TRASH: "rm -rf ~/.local/share/Trash/* ~/.Trash/*",
            ServiceType.LOGS: "find ~/.cache/log ~/.local/state -name '*.log' -mtime +7 -delete 2>/dev/null; journalctl --vacuum-time=7d 2>/dev/null || true",
        }
        return commands.get(service_type, f"rm -rf {path}")
    
    def _get_preview_command(self, service_type: ServiceType, path: str) -> str:
        """Get preview command for service"""
        previews = {
            # Containers
            ServiceType.DOCKER: "docker system df -v",
            ServiceType.OLLAMA: "ollama list",
            ServiceType.CONTAINERD: "sudo ls -la /var/lib/containerd 2>/dev/null || echo 'Requires sudo access'",
            ServiceType.PODMAN: "podman system df -v || podman images",
            # JS/Node
            ServiceType.NPM: "npm cache ls 2>/dev/null || du -sh ~/.npm",
            ServiceType.YARN: "yarn cache list 2>/dev/null || du -sh ~/.cache/yarn",
            ServiceType.PNPM: "pnpm store status 2>/dev/null || du -sh ~/.pnpm-store",
            # Python
            ServiceType.PIP: "pip cache dir && pip cache info 2>/dev/null || du -sh ~/.cache/pip",
            ServiceType.CONDA: "conda info --envs 2>/dev/null && conda list 2>/dev/null | head -20 || du -sh ~/miniconda3",
            ServiceType.POETRY: "poetry config cache-dir 2>/dev/null || du -sh ~/.cache/pypoetry",
            # Java
            ServiceType.GRADLE: "ls -la ~/.gradle/caches 2>/dev/null | head -20 || du -sh ~/.gradle",
            ServiceType.MAVEN: "du -sh ~/.m2/repository/* 2>/dev/null | sort -hr | head -20",
            # Rust/Go
            ServiceType.CARGO: "ls -la ~/.cargo/registry/cache 2>/dev/null | head -20 || du -sh ~/.cargo",
            ServiceType.GO: "go env GOPATH && du -sh ~/go/pkg 2>/dev/null || echo 'Go modules cache'",
            # Mobile
            ServiceType.FLUTTER: "flutter pub cache list 2>/dev/null | head -20 || du -sh ~/.pub-cache",
            ServiceType.DART: "du -sh ~/.pub-cache 2>/dev/null",
            ServiceType.ANDROID: "du -sh ~/Android/Sdk/* 2>/dev/null | sort -hr | head -10 || du -sh ~/.android",
            # System packages
            ServiceType.SNAP: "snap list --all",
            ServiceType.FLATPAK: "flatpak list --app --runtime",
            ServiceType.APPIMAGE: "ls -la ~/.local/share/AppImage 2>/dev/null || echo 'No AppImage data'",
            ServiceType.APT: "apt-cache stats 2>/dev/null || du -sh /var/cache/apt/archives",
            ServiceType.DNF: "dnf repolist && du -sh /var/cache/dnf 2>/dev/null",
            ServiceType.PACMAN: "pacman -Sc --dry-run 2>/dev/null || du -sh /var/cache/pacman/pkg",
            ServiceType.YUM: "yum repolist && du -sh /var/cache/yum 2>/dev/null",
            ServiceType.ZYPPER: "zypper packages --installed-only 2>/dev/null | head -20 || du -sh /var/cache/zypp",
            # Virtualization
            ServiceType.VAGRANT: "vagrant box list",
            ServiceType.VBOX: "vboxmanage list vms 2>/dev/null || ls -la ~/VirtualBox\\ VMs 2>/dev/null || echo 'No VirtualBox VMs'",
            ServiceType.VMWARE: "ls -la ~/vmware 2>/dev/null || ls -la ~/Virtual\\ Machines 2>/dev/null || echo 'No VMware VMs'",
            # Package managers
            ServiceType.NIX: "nix store gc --dry-run 2>/dev/null || du -sh /nix 2>/dev/null || du -sh ~/.nix-profile",
            ServiceType.BREW: "brew list | wc -l && du -sh ~/homebrew 2>/dev/null || du -sh /opt/homebrew 2>/dev/null || du -sh /usr/local/Homebrew",
            # Browsers
            ServiceType.CHROME: "du -sh ~/.cache/google-chrome 2>/dev/null || du -sh ~/.config/google-chrome",
            ServiceType.FIREFOX: "du -sh ~/.cache/mozilla 2>/dev/null || du -sh ~/.mozilla",
            ServiceType.EDGE: "du -sh ~/.cache/microsoft-edge 2>/dev/null || du -sh ~/.config/microsoft-edge",
            # IDEs
            ServiceType.VSCODE: "code --list-extensions 2>/dev/null | wc -l && du -sh ~/.vscode/extensions 2>/dev/null",
            ServiceType.CURSOR: "du -sh ~/.cursor/extensions 2>/dev/null || du -sh ~/.config/Cursor",
            ServiceType.JETBRAINS: "find ~/.cache/JetBrains -maxdepth 1 -type d 2>/dev/null | wc -l && du -sh ~/.cache/JetBrains 2>/dev/null",
            # Cloud/ML
            ServiceType.HUGGINGFACE: "du -sh ~/.cache/huggingface 2>/dev/null && ls ~/.cache/huggingface/hub 2>/dev/null | head -10",
            ServiceType.AWS: "ls -la ~/.aws/sso/cache 2>/dev/null || du -sh ~/.aws",
            ServiceType.GCLOUD: "gcloud config list 2>/dev/null | head -10 || du -sh ~/.config/gcloud",
            ServiceType.AZURE: "az account list 2>/dev/null | head -5 || du -sh ~/.azure",
            # IaC
            ServiceType.TERRAFORM: "ls ~/.terraform.d/providers 2>/dev/null || du -sh ~/.terraform.d",
            ServiceType.PULUMI: "pulumi plugin ls 2>/dev/null || du -sh ~/.pulumi/plugins",
            # Game engines
            ServiceType.UNITY: "du -sh ~/.config/unity3d 2>/dev/null || du -sh ~/Library/Unity",
            ServiceType.UNREAL: "du -sh ~/.config/Epic 2>/dev/null || du -sh ~/Library/Application\\ Support/Epic",
            # Other
            ServiceType.JUPYTER: "jupyter kernelspec list 2>/dev/null || du -sh ~/.local/share/jupyter",
            ServiceType.THUMBNAILS: "du -sh ~/.cache/thumbnails 2>/dev/null && find ~/.cache/thumbnails -type f | wc -l",
            ServiceType.TRASH: "du -sh ~/.local/share/Trash 2>/dev/null || du -sh ~/.Trash",
            ServiceType.LOGS: "find ~/.cache/log ~/.local/state /var/log ~/.var/log 2>/dev/null -name '*.log' | wc -l && du -sh ~/.cache/log 2>/dev/null || du -sh /var/log 2>/dev/null",
        }
        return previews.get(service_type, f"du -sh {path} 2>/dev/null && ls -la {path} | head -20")
    
    def _is_safe_cleanup(self, service_type: ServiceType) -> bool:
        """Determine if cleanup is generally safe (cache-only, not user data)"""
        safe_services = {
            # Package caches (can be re-downloaded)
            ServiceType.NPM, ServiceType.YARN, ServiceType.PNPM,
            ServiceType.PIP, ServiceType.POETRY,
            ServiceType.GRADLE, ServiceType.MAVEN, ServiceType.CARGO,
            ServiceType.GO,
            # System caches
            ServiceType.APT, ServiceType.DNF, ServiceType.PACMAN, 
            ServiceType.YUM, ServiceType.ZYPPER,
            # Browser caches
            ServiceType.CHROME, ServiceType.FIREFOX, ServiceType.EDGE,
            # App caches
            ServiceType.THUMBNAILS, ServiceType.LOGS,
            # Cloud CLI caches
            ServiceType.AWS, ServiceType.GCLOUD, ServiceType.AZURE,
            # IaC caches
            ServiceType.TERRAFORM, ServiceType.PULUMI,
        }
        return service_type in safe_services
    
    def get_cleanup_plan(self, selected_services: List[str] = None) -> Dict[str, Any]:
        """Generate cleanup plan for services"""
        services = self.scan_all_services()
        
        if selected_services:
            services = [s for s in services if s.service_type.value in selected_services]
            
        total_size_gb = sum(s.size_gb for s in services)
        safe_services = [s for s in services if s.safe_to_cleanup]
        unsafe_services = [s for s in services if not s.safe_to_cleanup]
        
        plan = {
            "threshold_mb": self.threshold_mb,
            "services_found": len(services),
            "total_size_gb": round(total_size_gb, 2),
            "safe_cleanup_gb": round(sum(s.size_gb for s in safe_services), 2),
            "requires_review_gb": round(sum(s.size_gb for s in unsafe_services), 2),
            "services": [self._service_to_dict(s) for s in services],
            "safe_to_cleanup": [self._service_to_dict(s) for s in safe_services],
            "requires_review": [self._service_to_dict(s) for s in unsafe_services],
        }
        
        return plan
    
    def _service_to_dict(self, service: ServiceDataInfo) -> Dict[str, Any]:
        """Convert ServiceDataInfo to dictionary"""
        return {
            "service_type": service.service_type.value,
            "name": service.name,
            "path": service.path,
            "size_mb": service.size_mb,
            "size_gb": service.size_gb,
            "description": service.description,
            "can_cleanup": service.can_cleanup,
            "cleanup_command": service.cleanup_command,
            "preview_command": service.preview_command,
            "safe_to_cleanup": service.safe_to_cleanup,
            "impact": service.impact,
            "items_count": service.items_count,
            "details": service.details,
        }
    
    def cleanup_service(self, service_type: str, dry_run: bool = False) -> Dict[str, Any]:
        """Execute cleanup for a specific service"""
        result = {
            "service": service_type,
            "dry_run": dry_run,
            "success": False,
            "space_freed_gb": 0,
            "output": "",
            "error": "",
        }
        
        try:
            service_enum = ServiceType(service_type)
            services = self.scan_service(service_enum)
            
            if not services:
                result["error"] = f"No {service_type} data found above threshold"
                return result
                
            service = services[0]  # Take first (largest)
            initial_size = service.size_gb
            
            if dry_run:
                result["success"] = True
                result["output"] = f"[DRY RUN] Would execute: {service.cleanup_command}"
                result["space_freed_gb"] = initial_size
                return result
            
            # Execute cleanup
            cleanup_result = subprocess.run(
                service.cleanup_command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=300
            )
            
            # Check new size
            new_size_mb = self._get_path_size_mb(service.path)
            new_size_gb = new_size_mb / 1024
            freed_gb = max(0, initial_size - new_size_gb)
            
            result["success"] = cleanup_result.returncode == 0
            result["output"] = cleanup_result.stdout
            result["error"] = cleanup_result.stderr
            result["space_freed_gb"] = round(freed_gb, 3)
            result["initial_size_gb"] = initial_size
            result["remaining_size_gb"] = round(new_size_gb, 3)
            
        except Exception as e:
            result["error"] = str(e)
            
        return result


def main():
    """Test the service data scanner"""
    scanner = ServiceDataScanner(threshold_mb=100)
    plan = scanner.get_cleanup_plan()
    print(json.dumps(plan, indent=2, default=str))


if __name__ == "__main__":
    main()
