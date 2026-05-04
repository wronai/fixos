"""
Storage Analyzer for FixOS - comprehensive disk space analysis.

Analizuje cały system i pokazuje REALNE możliwości odzyskania miejsca,
bez fałszywych alarmów.
"""
import subprocess
import os
import re
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

CONSTANT_3 = 3
CONSTANT_4 = 4
CONSTANT_5 = 5
CONSTANT_30 = 30
CONSTANT_50 = 50
CONSTANT_60 = 60
CONSTANT_120 = 120
CONSTANT_200 = 200
CONSTANT_500 = 500
CONSTANT_1024 = 1024

@dataclass
class StorageItem:
    """Represents a storage item that can be cleaned"""
    name: str
    path: str
    size_bytes: int
    category: str
    risk: str  # none, low, medium, high
    cleanup_command: str
    description: str
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "path": self.path,
            "size_bytes": self.size_bytes,
            "size_human": self._format_size(self.size_bytes),
            "category": self.category,
            "risk": self.risk,
            "cleanup_command": self.cleanup_command,
            "description": self.description,
        }
    
    @staticmethod
    def _format_size(size_bytes: int) -> str:
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < CONSTANT_1024:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= CONSTANT_1024
        return f"{size_bytes:.1f} PB"


class StorageAnalyzer:
    """
    Comprehensive storage analyzer for Linux systems.
    
    Analizuje:
    - DNF/RPM cache i stare kernele
    - Journal logs
    - Docker/Podman
    - Flatpak (już zaimplementowane)
    - Snap
    - User cache
    - Btrfs snapshots
    - Duże pliki użytkownika
    """
    
    def __init__(self):
        self.items: List[StorageItem] = []
        self.total_reclaimable = 0
        self.system_info: Dict[str, Any] = {}
        
    def analyze_full(self) -> Dict[str, Any]:
        """Run full system storage analysis"""
        self.items = []
        
        # System packages
        self._analyze_dnf_cache()
        self._analyze_old_kernels()
        self._analyze_journal_logs()
        self._analyze_orphaned_packages()
        
        # Containers
        self._analyze_docker()
        self._analyze_podman()
        
        # User data
        self._analyze_user_cache()
        self._analyze_browser_cache()
        self._analyze_browser_profiles()
        
        # Flatpak deep
        self._analyze_flatpak_user_data()
        self._analyze_ostree_repo()
        
        # Dev projects (node_modules, venv, target, etc.)
        self._analyze_dev_projects()
        
        # Home directory analysis (large files and folders)
        self._analyze_home_directory()
        
        # System
        self._analyze_snap()
        self._analyze_btrfs_snapshots()
        self._analyze_var_cache()
        self._analyze_coredumps()
        self._analyze_system_logs()
        
        # Sort by size
        self.items.sort(key=lambda x: -x.size_bytes)
        
        # Calculate totals
        self.total_reclaimable = sum(item.size_bytes for item in self.items)
        
        # Group by category
        categories = {}
        for item in self.items:
            if item.category not in categories:
                categories[item.category] = []
            categories[item.category].append(item.to_dict())
        
        return {
            "items": [item.to_dict() for item in self.items],
            "categories": categories,
            "total_reclaimable": self.total_reclaimable,
            "total_reclaimable_human": StorageItem._format_size(self.total_reclaimable),
            "system_info": self.system_info,
            "recommendations": self._get_recommendations(),
        }
    
    def _get_dir_size(self, path: str) -> int:
        """Get directory size using du"""
        if not os.path.exists(path):
            return 0
        
        try:
            result = subprocess.run(
                ["du", "-sb", path],
                capture_output=True,
                text=True,
                timeout=CONSTANT_60,
            )
            if result.returncode == 0:
                return int(result.stdout.split()[0])
        except Exception:
            pass
        return 0
    
    def _get_file_size(self, path: str) -> int:
        """Get file size"""
        if not os.path.exists(path):
            return 0
        try:
            return os.path.getsize(path)
        except Exception:
            return 0
    
    def _run_command(self, cmd: List[str]) -> Optional[str]:
        """Run command and return output"""
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=CONSTANT_30,
            )
            if result.returncode == 0:
                return result.stdout
        except Exception:
            pass
        return None
    
    def _analyze_dnf_cache(self):
        """Analyze DNF package cache"""
        cache_paths = [
            "/var/cache/dnf",
        ]
        
        total_size = 0
        for path in cache_paths:
            if os.path.exists(path):
                size = self._get_dir_size(path)
                if size > 10 * CONSTANT_1024 * CONSTANT_1024:  # > 10 MB
                    total_size += size
        
        if total_size > 10 * CONSTANT_1024 * CONSTANT_1024:
            self.items.append(StorageItem(
                name="DNF Cache",
                path="/var/cache/dnf",
                size_bytes=total_size,
                category="packages",
                risk="none",
                cleanup_command="sudo dnf clean all",
                description="Cache pobranych pakietów DNF - bezpieczne do usunięcia",
            ))
    
    def _analyze_old_kernels(self):
        """Analyze old kernel versions"""
        output = self._run_command(["rpm", "-q", "kernel"])
        if not output:
            return
        
        kernels = output.strip().split('\n')
        if len(kernels) <= 2:
            return  # Keep at least 2 kernels
        
        # Get current kernel
        current = self._run_command(["uname", "-r"])
        if not current:
            return
        
        current_version = current.strip()
        old_kernels = [k for k in kernels if current_version not in k]
        
        if old_kernels:
            # Estimate size: ~200MB per kernel
            estimated_size = len(old_kernels) * CONSTANT_200 * CONSTANT_1024 * CONSTANT_1024
            
            self.items.append(StorageItem(
                name=f"Stare kernele ({len(old_kernels)})",
                path="/boot",
                size_bytes=estimated_size,
                category="packages",
                risk="low",
                cleanup_command="sudo dnf remove --oldinstallonly",
                description=f"Masz {len(kernels)} kerneli, używasz {current_version}. "
                           f"Bezpiecznie usuń {len(old_kernels)} starych.",
            ))
    
    def _analyze_journal_logs(self):
        """Analyze systemd journal logs"""
        output = self._run_command(["journalctl", "--disk-usage"])
        if not output:
            return
        
        # Parse: "Archived and active journals take up 1.2G on disk."
        match = re.search(r'take up (\d+\.?\d*[KMG]?)', output)
        if not match:
            return
        
        size_str = match.group(1)
        size_bytes = self._parse_size(size_str)
        
        if size_bytes > 100 * CONSTANT_1024 * CONSTANT_1024:  # > 100 MB
            self.items.append(StorageItem(
                name="Journal logs",
                path="/var/log/journal",
                size_bytes=size_bytes,
                category="logs",
                risk="low",
                cleanup_command="sudo journalctl --vacuum-time=7d",
                description=f"Logi systemowe zajmują {size_str}. "
                           "Bezpiecznie ogranicz do 7 dni.",
            ))
    
    @staticmethod
    def _parse_size_static(size_str: str) -> int:
        """Parse size string like '1.2G' to bytes (static version for use in classmethods)."""
        size_str = size_str.strip().upper()
        multipliers = {
            'K': CONSTANT_1024,
            'M': CONSTANT_1024**2,
            'G': CONSTANT_1024**CONSTANT_3,
            'T': CONSTANT_1024**CONSTANT_4,
        }
        for suffix, mult in multipliers.items():
            if size_str.endswith(suffix):
                try:
                    return int(float(size_str[:-1]) * mult)
                except ValueError:
                    return 0
        try:
            return int(float(size_str))
        except ValueError:
            return 0

    @staticmethod
    def _parse_docker_df_output(output: str) -> dict:
        """Parse 'docker system df -v' output into image/cache stats."""
        total_images = 0
        dangling_images = 0
        dangling_size = 0
        build_cache = 0
        current_section = None

        for line in output.split('\n'):
            line = line.strip()
            if line.startswith("Images space usage:"):
                current_section = "images"
            elif line.startswith("Containers space usage:"):
                current_section = "containers"
            elif line.startswith("Local Volumes space usage:"):
                current_section = "volumes"
            elif line.startswith("Build Cache"):
                current_section = "build_cache"
            elif current_section == "images" and line and not line.startswith("REPOSITORY"):
                parts = line.split()
                if len(parts) >= CONSTANT_4:
                    if parts[0] == "<none>" or parts[1] == "<none>":
                        dangling_images += 1
                        dangling_size += StorageAnalyzer._parse_size_static(parts[CONSTANT_3])
                    total_images += 1
            elif current_section == "build_cache" and line and not line.startswith("CACHE ID"):
                parts = line.split()
                if len(parts) >= 2:
                    build_cache += StorageAnalyzer._parse_size_static(parts[-2])

        return {
            "total_images": total_images,
            "dangling_images": dangling_images,
            "dangling_size": dangling_size,
            "build_cache": build_cache,
        }

    def _add_dangling_images_item(self, dangling_images: int, dangling_size: int) -> None:
        """Append a StorageItem for dangling Docker images if threshold exceeded."""
        if dangling_size > CONSTANT_50 * CONSTANT_1024 * CONSTANT_1024:
            self.items.append(StorageItem(
                name=f"Dangling Docker Images ({dangling_images})",
                path="/var/lib/docker",
                size_bytes=dangling_size,
                category="containers",
                risk="low",
                cleanup_command="docker image prune -f",
                description=(
                    f"Dangling images (bez tagu): {StorageItem._format_size(dangling_size)}. "
                    "Bezpieczne do usunięcia - to nieużywane obrazy."
                ),
            ))

    def _add_build_cache_item(self, build_cache: int) -> None:
        """Append a StorageItem for Docker build cache if threshold exceeded."""
        if build_cache > 100 * CONSTANT_1024 * CONSTANT_1024:
            self.items.append(StorageItem(
                name="Docker Build Cache",
                path="/var/lib/docker",
                size_bytes=build_cache,
                category="containers",
                risk="low",
                cleanup_command="docker builder prune -f",
                description=(
                    f"Build cache Dockera: {StorageItem._format_size(build_cache)}. "
                    "Bezpieczne do usunięcia."
                ),
            ))

    def _add_docker_total_item(self, total_images: int, dangling_images: int) -> None:
        """Append a StorageItem for total Docker usage if threshold exceeded."""
        total_docker = self._get_dir_size("/var/lib/docker")
        if total_docker > CONSTANT_1024**CONSTANT_3:
            self.items.append(StorageItem(
                name="Docker Total",
                path="/var/lib/docker",
                size_bytes=total_docker,
                category="containers",
                risk="medium",
                cleanup_command="docker system prune -a --volumes",
                description=(
                    f"Docker łącznie: {StorageItem._format_size(total_docker)}. "
                    f"Obrazy: {total_images}, dangling: {dangling_images}. "
                    "Uwaga: usunie wszystkie nieużywane zasoby."
                ),
            ))

    def _analyze_docker(self):
        """Analyze Docker storage - images, containers, volumes, build cache"""
        if not os.path.exists("/var/lib/docker"):
            return

        output = self._run_command(["docker", "system", "df", "-v"])
        if not output:
            size = self._get_dir_size("/var/lib/docker")
            if size > CONSTANT_500 * CONSTANT_1024 * CONSTANT_1024:
                self.items.append(StorageItem(
                    name="Docker",
                    path="/var/lib/docker",
                    size_bytes=size,
                    category="containers",
                    risk="medium",
                    cleanup_command="docker system prune -a",
                    description=f"Docker zajmuje {StorageItem._format_size(size)}. "
                               "Uwaga: usunie nieużywane obrazy i kontenery.",
                ))
            return

        stats = self._parse_docker_df_output(output)
        self._add_dangling_images_item(stats["dangling_images"], stats["dangling_size"])
        self._add_build_cache_item(stats["build_cache"])
        self._add_docker_total_item(stats["total_images"], stats["dangling_images"])
    
    def _analyze_podman(self):
        """Analyze Podman storage"""
        if not os.path.exists("/var/lib/containers"):
            return
        
        size = self._get_dir_size("/var/lib/containers")
        if size > CONSTANT_500 * CONSTANT_1024 * CONSTANT_1024:  # > CONSTANT_500 MB
            self.items.append(StorageItem(
                name="Podman",
                path="/var/lib/containers",
                size_bytes=size,
                category="containers",
                risk="medium",
                cleanup_command="podman system prune -a",
                description=f"Podman zajmuje {StorageItem._format_size(size)}.",
            ))
    
    def _analyze_user_cache(self):
        """Analyze user cache directories"""
        cache_paths = [
            ("~/.cache/pip", "Python pip cache"),
            ("~/.cache/npm", "npm cache"),
            ("~/.cache/yarn", "Yarn cache"),
            ("~/.cache/go-build", "Go build cache"),
            ("~/.cache/gradle", "Gradle cache"),
            ("~/.cargo/registry", "Cargo registry"),
        ]
        
        for path, name in cache_paths:
            expanded = os.path.expanduser(path)
            if os.path.exists(expanded):
                size = self._get_dir_size(expanded)
                if size > CONSTANT_50 * CONSTANT_1024 * CONSTANT_1024:  # > CONSTANT_50 MB
                    self.items.append(StorageItem(
                        name=name,
                        path=expanded,
                        size_bytes=size,
                        category="user_cache",
                        risk="low",
                        cleanup_command=f"rm -rf {expanded}",
                        description=f"{name} zajmuje {StorageItem._format_size(size)}.",
                    ))
    
    def _analyze_browser_cache(self):
        """Analyze browser cache"""
        browsers = [
            ("~/.cache/google-chrome", "Google Chrome cache"),
            ("~/.cache/mozilla", "Firefox cache"),
            ("~/.cache/brave", "Brave cache"),
            ("~/.cache/microsoft-edge", "Edge cache"),
        ]
        
        for path, name in browsers:
            expanded = os.path.expanduser(path)
            if os.path.exists(expanded):
                size = self._get_dir_size(expanded)
                if size > 100 * CONSTANT_1024 * CONSTANT_1024:  # > 100 MB
                    self.items.append(StorageItem(
                        name=name,
                        path=expanded,
                        size_bytes=size,
                        category="browser_cache",
                        risk="low",
                        cleanup_command=f"rm -rf {expanded}",
                        description=f"{name} zajmuje {StorageItem._format_size(size)}. "
                                   "Uwaga: wyczyści dane sesji.",
                    ))
    
    def _analyze_btrfs_snapshots(self):
        """Analyze Btrfs snapshots (major space consumer on Fedora)"""
        # Check if Btrfs is used
        output = self._run_command(["btrfs", "filesystem", "df", "/"])
        if not output:
            return
        
        # Check snapper snapshots
        if os.path.exists("/.snapshots"):
            size = self._get_dir_size("/.snapshots")
            if size > CONSTANT_1024**CONSTANT_3:  # > 1 GB
                # Count snapshots
                output = self._run_command(["snapper", "list"])
                snapshot_count = 0
                if output:
                    lines = output.strip().split('\n')[1:]  # Skip header
                    snapshot_count = len(lines)
                
                self.items.append(StorageItem(
                    name=f"Btrfs Snapshots ({snapshot_count})",
                    path="/.snapshots",
                    size_bytes=size,
                    category="snapshots",
                    risk="medium",
                    cleanup_command="sudo snapper delete <old-id>",
                    description=f"Snapshoty Btrfs zajmują {StorageItem._format_size(size)}. "
                               f"Masz {snapshot_count} snapshotów. Usuń stare, zachowaj 3-5 ostatnich.",
                ))
        
        # Check Timeshift
        if os.path.exists("/timeshift"):
            size = self._get_dir_size("/timeshift")
            if size > CONSTANT_500 * CONSTANT_1024 * CONSTANT_1024:  # > CONSTANT_500 MB
                self.items.append(StorageItem(
                    name="Timeshift Backups",
                    path="/timeshift",
                    size_bytes=size,
                    category="snapshots",
                    risk="medium",
                    cleanup_command="sudo timeshift --delete-all",
                    description=f"Kopie Timeshift zajmują {StorageItem._format_size(size)}.",
                ))
    
    def _analyze_coredumps(self):
        """Analyze systemd coredumps"""
        coredump_path = "/var/lib/systemd/coredump"
        if not os.path.exists(coredump_path):
            return
        
        size = self._get_dir_size(coredump_path)
        if size > 100 * CONSTANT_1024 * CONSTANT_1024:  # > 100 MB
            self.items.append(StorageItem(
                name="Coredumps",
                path=coredump_path,
                size_bytes=size,
                category="system",
                risk="none",
                cleanup_command="sudo rm -rf /var/lib/systemd/coredump/*",
                description=f"Coredumpy (crash dumps) zajmują {StorageItem._format_size(size)}. "
                           "Bezpieczne do usunięcia.",
            ))
    
    def _analyze_orphaned_packages(self):
        """Analyze orphaned packages and debug symbols"""
        # Check for debuginfo packages
        output = self._run_command(["dnf", "repoquery", "--installed", "*debuginfo*"])
        if output and output.strip():
            debug_packages = output.strip().split('\n')
            # Estimate: ~500MB per debug package
            estimated_size = len(debug_packages) * CONSTANT_500 * CONSTANT_1024 * CONSTANT_1024
            
            if estimated_size > CONSTANT_500 * CONSTANT_1024 * CONSTANT_1024:  # > CONSTANT_500 MB
                self.items.append(StorageItem(
                    name=f"Debug symbols ({len(debug_packages)})",
                    path="/usr/lib/debug",
                    size_bytes=estimated_size,
                    category="packages",
                    risk="low",
                    cleanup_command="sudo dnf remove '*debuginfo*'",
                    description=f"Pakiety debuginfo zajmują ~{StorageItem._format_size(estimated_size)}. "
                               "Usuń jeśli nie rozwijasz aplikacji.",
                ))
        
        # Check for orphaned packages (leaves)
        output = self._run_command(["package-cleanup", "--leaves"])
        if output and output.strip():
            orphaned = output.strip().split('\n')
            if len(orphaned) > CONSTANT_5:  # Only report if significant
                estimated_size = len(orphaned) * CONSTANT_50 * CONSTANT_1024 * CONSTANT_1024  # ~50MB each
                
                self.items.append(StorageItem(
                    name=f"Orphaned packages ({len(orphaned)})",
                    path="/var/lib/rpm",
                    size_bytes=estimated_size,
                    category="packages",
                    risk="low",
                    cleanup_command="sudo dnf remove $(package-cleanup --leaves)",
                    description=f"Osierocone pakiety (leaves): {len(orphaned)}. "
                               "Biblioteki nie wymagane przez żaden pakiet.",
                ))
    
    def _analyze_browser_profiles(self):
        """Analyze browser profile bloat (not just cache)"""
        # Firefox profiles
        firefox_path = os.path.expanduser("~/.mozilla/firefox")
        if os.path.exists(firefox_path):
            size = self._get_dir_size(firefox_path)
            if size > CONSTANT_500 * CONSTANT_1024 * CONSTANT_1024:  # > CONSTANT_500 MB
                self.items.append(StorageItem(
                    name="Firefox Profile",
                    path=firefox_path,
                    size_bytes=size,
                    category="browser_data",
                    risk="medium",
                    cleanup_command="about:support → Clear Profile Data",
                    description=f"Profil Firefox zajmuje {StorageItem._format_size(size)}. "
                               "Możesz wyczyścić dane w przeglądarce.",
                ))
        
        # Chrome profile
        chrome_path = os.path.expanduser("~/.config/google-chrome")
        if os.path.exists(chrome_path):
            size = self._get_dir_size(chrome_path)
            if size > CONSTANT_500 * CONSTANT_1024 * CONSTANT_1024:  # > CONSTANT_500 MB
                self.items.append(StorageItem(
                    name="Chrome Profile",
                    path=chrome_path,
                    size_bytes=size,
                    category="browser_data",
                    risk="medium",
                    cleanup_command="chrome://settings/clearBrowserData",
                    description=f"Profil Chrome zajmuje {StorageItem._format_size(size)}.",
                ))
    
    def _analyze_flatpak_user_data(self):
        """Analyze Flatpak user app data (~/.var/app)"""
        var_app_path = os.path.expanduser("~/.var/app")
        if not os.path.exists(var_app_path):
            return
        
        # Get total size
        total_size = self._get_dir_size(var_app_path)
        if total_size < CONSTANT_500 * CONSTANT_1024 * CONSTANT_1024:  # < CONSTANT_500 MB
            return
        
        # Find largest apps
        app_sizes = []
        for app_dir in os.listdir(var_app_path):
            app_path = os.path.join(var_app_path, app_dir)
            if os.path.isdir(app_path):
                size = self._get_dir_size(app_path)
                if size > CONSTANT_50 * CONSTANT_1024 * CONSTANT_1024:  # > CONSTANT_50 MB
                    app_sizes.append((app_dir, size))
        
        if app_sizes:
            app_sizes.sort(key=lambda x: -x[1])
            largest = app_sizes[:CONSTANT_5]
            
            self.items.append(StorageItem(
                name=f"Flatpak App Data ({len(app_sizes)} apps)",
                path=var_app_path,
                size_bytes=total_size,
                category="flatpak",
                risk="low",
                cleanup_command="rm -rf ~/.var/app/*/cache",
                description=f"Dane aplikacji Flatpak: {StorageItem._format_size(total_size)}. "
                           f"Największe: {', '.join(f'{a} ({StorageItem._format_size(s)})' for a, s in largest[:CONSTANT_3])}. "
                           "Możesz bezpiecznie usunąć cache.",
            ))
    
    def _analyze_ostree_repo(self):
        """Analyze OSTree repo (Flatpak backend) for hidden bloat"""
        repo_path = "/var/lib/flatpak/repo/objects"
        if not os.path.exists(repo_path):
            return
        
        size = self._get_dir_size(repo_path)
        if size > 10 * CONSTANT_1024**CONSTANT_3:  # > 10 GB
            self.items.append(StorageItem(
                name="OSTree Objects DB",
                path=repo_path,
                size_bytes=size,
                category="flatpak",
                risk="low",
                cleanup_command="sudo ostree prune --repo=/var/lib/flatpak/repo --depth=0",
                description=f"OSTree objects DB zajmuje {StorageItem._format_size(size)}. "
                           "Możesz bezpiecznie przeprowadzić głębokie prune.",
            ))
    
    def _analyze_dev_projects(self):
        """Analyze developer project dependencies (node_modules, venv, target, etc.)"""
        from fixos.diagnostics.dev_project_analyzer import DevProjectAnalyzer
        
        try:
            dev_analyzer = DevProjectAnalyzer()
            analysis = dev_analyzer.analyze(max_depth=CONSTANT_5)
            
            # Add each dependency as a StorageItem
            for dep in dev_analyzer.dependencies:
                # Determine risk based on can_recreate and age
                risk = "low" if dep.can_recreate else "medium"
                
                self.items.append(StorageItem(
                    name=f"{dep.dep_type} ({dep.project_name})",
                    path=dep.path,
                    size_bytes=dep.size_bytes,
                    category="dev_projects",
                    risk=risk,
                    cleanup_command=f"rm -rf {dep.path}",
                    description=f"{dep.dep_type} w projekcie {dep.project_name}: "
                               f"{StorageItem._format_size(dep.size_bytes)}. "
                               f"Odtworzenie: {dep.recreate_command}",
                ))
        except Exception:
            pass  # Silently fail if dev analyzer not available
    
    def _analyze_system_logs(self):
        """Analyze /var/log beyond journal"""
        log_path = "/var/log"
        if not os.path.exists(log_path):
            return
        
        size = self._get_dir_size(log_path)
        journal_size = self._get_dir_size("/var/log/journal")
        other_logs = size - journal_size
        
        if other_logs > CONSTANT_500 * CONSTANT_1024 * CONSTANT_1024:  # > CONSTANT_500 MB
            self.items.append(StorageItem(
                name="Other System Logs",
                path=log_path,
                size_bytes=other_logs,
                category="logs",
                risk="low",
                cleanup_command="sudo logrotate -f /etc/logrotate.conf",
                description=f"Inne logi systemowe zajmują {StorageItem._format_size(other_logs)}.",
            ))
    
    def _analyze_home_directory(self):
        """Analyze home directory for large files and folders"""
        home_path = os.path.expanduser("~")
        if not os.path.exists(home_path):
            return
        
        # Find large files (>200MB)
        large_files = self._find_large_files(home_path, min_size_mb=CONSTANT_200)
        
        # Find large directories (>500MB) not already analyzed
        large_dirs = self._find_large_home_dirs(home_path, min_size_mb=CONSTANT_500)
        
        # Store for interactive selection
        self.home_large_files = large_files
        self.home_large_dirs = large_dirs
        
        # Add summary item
        if large_files or large_dirs:
            total_size = sum(f['size'] for f in large_files) + sum(d['size'] for d in large_dirs)
            self.items.append(StorageItem(
                name=f"Duże pliki w home ({len(large_files) + len(large_dirs)})",
                path=home_path,
                size_bytes=total_size,
                category="home_analysis",
                risk="medium",
                cleanup_command="home:interactive",  # Special marker
                description=f"Znaleziono {len(large_files)} dużych plików i {len(large_dirs)} folderów. "
                           f"Użyj 'home' w menu aby zarządzać.",
            ))
    
    def _find_large_files(self, path: str, min_size_mb: int = CONSTANT_200) -> List[Dict[str, Any]]:
        """Find files larger than min_size_mb in path"""
        large_files = []
        min_size = min_size_mb * CONSTANT_1024 * CONSTANT_1024
        
        # Skip certain directories
        skip_dirs = {'.git', '.venv', 'venv', 'node_modules', '__pycache__', 
                     '.cache', '.local', '.config', '.cargo', '.rustup',
                     'target', 'build', 'dist', '.tox'}
        
        try:
            for root, dirs, files in os.walk(path):
                # Skip certain directories
                dirs[:] = [d for d in dirs if d not in skip_dirs]
                
                for file in files:
                    try:
                        file_path = os.path.join(root, file)
                        size = os.path.getsize(file_path)
                        
                        if size > min_size:
                            large_files.append({
                                'path': file_path,
                                'size': size,
                                'size_human': StorageItem._format_size(size),
                                'type': 'file',
                            })
                    except (OSError, PermissionError):
                        continue
                
                # Limit to prevent long scans
                if len(large_files) > 100:
                    break
        except Exception:
            pass
        
        # Sort by size
        large_files.sort(key=lambda x: -x['size'])
        return large_files[:CONSTANT_50]  # Return top CONSTANT_50
    
    def _find_large_home_dirs(self, path: str, min_size_mb: int = CONSTANT_500) -> List[Dict[str, Any]]:
        """Find directories larger than min_size_mb in home"""
        large_dirs = []
        min_size = min_size_mb * CONSTANT_1024 * CONSTANT_1024
        
        # Skip certain directories
        skip_names = {'.git', '.cache', '.local', '.config', '.cargo', '.rustup'}
        skip_paths = {os.path.expanduser('~/github'), os.path.expanduser('~/projects')}
        
        try:
            for root, dirs, files in os.walk(path):
                # Skip certain directories
                dirs[:] = [d for d in dirs if d not in skip_names]
                
                # Skip deep scans in known large paths
                if any(root.startswith(p) for p in skip_paths):
                    dirs[:] = []
                    continue
                
                for d in dirs:
                    try:
                        dir_path = os.path.join(root, d)
                        
                        # Skip if already in items
                        if any(item.path == dir_path for item in self.items):
                            continue
                        
                        size = self._get_dir_size(dir_path)
                        
                        if size > min_size:
                            large_dirs.append({
                                'path': dir_path,
                                'size': size,
                                'size_human': StorageItem._format_size(size),
                                'type': 'directory',
                            })
                    except (OSError, PermissionError):
                        continue
                
                # Limit to prevent long scans
                if len(large_dirs) > CONSTANT_50:
                    break
        except Exception:
            pass
        
        # Sort by size
        large_dirs.sort(key=lambda x: -x['size'])
        return large_dirs[:CONSTANT_30]
    
    def get_large_directories(self, min_size_mb: int = 100) -> List[Dict[str, Any]]:
        """
        Find all directories larger than min_size_mb.
        
        Returns a full storage map - every directory >100MB.
        """
        large_dirs = []
        
        # Scan common locations
        scan_paths = [
            "/var",
            "/usr",
            "/opt",
            "/home",
            "/root",
        ]
        
        for scan_path in scan_paths:
            if not os.path.exists(scan_path):
                continue
            
            try:
                # Use du to find large directories
                result = subprocess.run(
                    ["du", "-h", "--threshold", f"{min_size_mb}M", scan_path],
                    capture_output=True,
                    text=True,
                    timeout=CONSTANT_120,
                )
                
                if result.returncode == 0:
                    for line in result.stdout.strip().split('\n'):
                        parts = line.split('\t')
                        if len(parts) == 2:
                            size_str, path = parts
                            size_bytes = self._parse_size(size_str)
                            
                            # Skip if already in items
                            if any(item.path == path for item in self.items):
                                continue
                            
                            large_dirs.append({
                                "path": path,
                                "size": size_bytes,
                                "size_human": StorageItem._format_size(size_bytes),
                            })
            except Exception:
                continue
        
        # Sort by size
        large_dirs.sort(key=lambda x: -x['size'])
        
        return large_dirs
    
    def _parse_snap_line(self, line: str) -> dict | None:
        """Parse a single line from 'snap list --all' output. Returns None if invalid."""
        parts = line.split()
        if len(parts) < CONSTANT_4:
            return None
        name, version, rev = parts[0], parts[1], parts[2]
        status = parts[CONSTANT_3] if len(parts) > CONSTANT_3 else ""
        is_disabled = 'disabled' in status.lower()
        snap_path = f"/var/lib/snapd/snaps/{name}_{rev}.snap"
        size = self._get_file_size(snap_path) if os.path.exists(snap_path) else 0
        return {'name': name, 'version': version, 'rev': rev, 'size': size, 'disabled': is_disabled}

    def _add_snap_items(self, snap_packages: list, old_count: int) -> None:
        """Append StorageItems for old snap versions and active snap total."""
        if old_count > 0:
            estimated_size = old_count * 100 * CONSTANT_1024 * CONSTANT_1024
            self.items.append(StorageItem(
                name=f"Stare wersje Snap ({old_count})",
                path="/var/lib/snapd",
                size_bytes=estimated_size,
                category="packages",
                risk="low",
                cleanup_command="sudo snap set system refresh.retain=2",
                description=f"Masz {old_count} starych wersji pakietów Snap. Ogranicz do 2 wersji.",
            ))
        if snap_packages:
            active = [p for p in snap_packages if not p['disabled']]
            total_snap_size = sum(p['size'] for p in active)
            if total_snap_size > CONSTANT_500 * CONSTANT_1024 * CONSTANT_1024:
                self.items.append(StorageItem(
                    name=f"Zainstalowane Snap ({len(active)})",
                    path="/var/lib/snapd/snaps",
                    size_bytes=total_snap_size,
                    category="packages",
                    risk="medium",
                    cleanup_command="snap:interactive",
                    description=f"Masz {len(snap_packages)} pakietów Snap. Użyj 'snap' w menu aby zarządzać.",
                ))

    def _analyze_snap(self):
        """Analyze Snap packages - old versions and installed packages"""
        if not os.path.exists("/var/lib/snapd"):
            return

        output = self._run_command(["snap", "list", "--all"])
        if not output:
            return

        snap_packages = []
        old_count = 0
        for line in output.strip().split('\n')[1:]:
            pkg = self._parse_snap_line(line)
            if pkg:
                snap_packages.append(pkg)
                if pkg['disabled']:
                    old_count += 1

        self.snap_packages = snap_packages
        self._add_snap_items(snap_packages, old_count)
    
    def _analyze_btrfs_snapshots(self):
        """Analyze Btrfs snapshots"""
        output = self._run_command(["btrfs", "subvolume", "list", "/"])
        if not output:
            return
        
        # Check for snapper
        output = self._run_command(["snapper", "list"])
        if not output:
            return
        
        lines = output.strip().split('\n')[1:]  # Skip header
        snapshot_count = len(lines)
        
        if snapshot_count > CONSTANT_5:
            # Estimate: ~500MB per snapshot (rough)
            estimated_size = snapshot_count * CONSTANT_500 * CONSTANT_1024 * CONSTANT_1024
            
            self.items.append(StorageItem(
                name=f"Btrfs Snapshots ({snapshot_count})",
                path="/.snapshots",
                size_bytes=estimated_size,
                category="snapshots",
                risk="medium",
                cleanup_command="sudo snapper delete <old-id>",
                description=f"Masz {snapshot_count} snapshotów. "
                           "Możesz usunąć stare, ale zachowaj kilka ostatnich.",
            ))
    
    def _analyze_var_cache(self):
        """Analyze /var/cache"""
        if not os.path.exists("/var/cache"):
            return
        
        # Skip if already analyzed DNF
        size = self._get_dir_size("/var/cache")
        dnf_size = self._get_dir_size("/var/cache/dnf")
        other_size = size - dnf_size
        
        if other_size > CONSTANT_200 * CONSTANT_1024 * CONSTANT_1024:  # > CONSTANT_200 MB
            self.items.append(StorageItem(
                name="Inne cache systemowe",
                path="/var/cache",
                size_bytes=other_size,
                category="system_cache",
                risk="low",
                cleanup_command="sudo rm -rf /var/cache/*",
                description=f"Cache systemowe (poza DNF) zajmują "
                          f"{StorageItem._format_size(other_size)}.",
            ))
    
    def _parse_size(self, size_str: str) -> int:
        """Parse size string like '1.2G' to bytes"""
        size_str = size_str.strip().upper()
        multipliers = {
            'K': CONSTANT_1024,
            'M': CONSTANT_1024**2,
            'G': CONSTANT_1024**CONSTANT_3,
            'T': CONSTANT_1024**CONSTANT_4,
        }
        
        for suffix, mult in multipliers.items():
            if size_str.endswith(suffix):
                try:
                    return int(float(size_str[:-1]) * mult)
                except ValueError:
                    return 0
        
        try:
            return int(float(size_str))
        except ValueError:
            return 0
    
    def _get_recommendations(self) -> List[Dict[str, Any]]:
        """Get prioritized cleanup recommendations"""
        recommendations = []
        
        # Group by risk and size
        safe_items = [item for item in self.items if item.risk in ['none', 'low']]
        medium_items = [item for item in self.items if item.risk == 'medium']
        high_items = [item for item in self.items if item.risk == 'high']
        
        # Safe cleanup (can be done automatically)
        if safe_items:
            total_safe = sum(item.size_bytes for item in safe_items)
            recommendations.append({
                "priority": "high",
                "description": f"Bezpieczne czyszczenie ({len(safe_items)} elementów)",
                "items": [item.to_dict() for item in safe_items[:CONSTANT_5]],
                "estimated_savings": StorageItem._format_size(total_safe),
                "risk": "low",
                "action": "auto",
            })
        
        # Medium risk (requires confirmation)
        if medium_items:
            total_medium = sum(item.size_bytes for item in medium_items)
            recommendations.append({
                "priority": "medium",
                "description": f"Wymaga potwierdzenia ({len(medium_items)} elementów)",
                "items": [item.to_dict() for item in medium_items[:CONSTANT_5]],
                "estimated_savings": StorageItem._format_size(total_medium),
                "risk": "medium",
                "action": "confirm",
            })
        
        return recommendations
    
    def get_summary(self) -> str:
        """Get human-readable summary"""
        analysis = self.analyze_full()
        
        lines = [
            "=" * CONSTANT_60,
            "📊 STORAGE ANALYSIS",
            "=" * CONSTANT_60,
            "",
        ]
        
        if not self.items:
            lines.append("✅ System jest czysty - brak dużych śmieci.")
            return "\n".join(lines)
        
        # Group by category
        categories = {}
        for item in self.items:
            if item.category not in categories:
                categories[item.category] = []
            categories[item.category].append(item)
        
        for category, items in categories.items():
            total = sum(item.size_bytes for item in items)
            lines.append(f"\n{category.upper()} ({StorageItem._format_size(total)})")
            for item in items[:CONSTANT_5]:
                risk_icon = {"none": "✅", "low": "🟢", "medium": "🟡", "high": "🔴"}.get(item.risk, "•")
                lines.append(f"  {risk_icon} {item.name}: {StorageItem._format_size(item.size_bytes)}")
            if len(items) > CONSTANT_5:
                lines.append(f"  ... i {len(items) - CONSTANT_5} więcej")
        
        lines.append(f"\n{'=' * CONSTANT_60}")
        lines.append(f"💰 ŁĄCZNIE DO ODZYSKANIA: {analysis['total_reclaimable_human']}")
        lines.append("=" * CONSTANT_60)
        
        return "\n".join(lines)
