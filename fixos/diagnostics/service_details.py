"""
Service Details Provider for fixOS
Extracts detailed information about specific services (Docker, Conda, Ollama, etc.)
"""

import subprocess
import os
from typing import Dict, Any

# Import enhanced Flatpak analyzer
try:
    from .flatpak_analyzer import FlatpakAnalyzer

    _HAS_FLATPAK_ANALYZER = True
except ImportError:
    _HAS_FLATPAK_ANALYZER = False


class ServiceDetailsProvider:
    """Provides detailed information about service data."""

    def get_details(self, service_type, path: str) -> Dict[str, Any]:
        """Get details for a specific service type."""
        from .service_scanner import ServiceType

        handlers = {
            ServiceType.DOCKER: self._docker,
            ServiceType.OLLAMA: self._ollama,
            ServiceType.CONDA: self._conda,
            ServiceType.FLATPAK: self._flatpak,
        }

        # Package cache handler for multiple types
        package_cache_types = {
            ServiceType.NPM,
            ServiceType.YARN,
            ServiceType.PNPM,
            ServiceType.PIP,
            ServiceType.POETRY,
            ServiceType.GRADLE,
            ServiceType.MAVEN,
            ServiceType.CARGO,
            ServiceType.GO,
        }

        if service_type in handlers:
            return handlers[service_type]()
        elif service_type in package_cache_types:
            return self._package_cache(path)
        else:
            return {}

    def _parse_docker_system_df(self, details: Dict[str, Any]) -> None:
        """Populate details from 'docker system df -v' output."""
        try:
            result = subprocess.run(
                ["docker", "system", "df", "-v"],
                capture_output=True,
                text=True,
                timeout=10,
            )
            if result.returncode == 0:
                for line in result.stdout.strip().split("\n"):
                    if any(
                        x in line
                        for x in ["Images", "Containers", "Volumes", "Build Cache"]
                    ):
                        parts = line.split()
                        if len(parts) >= 2 and parts[1].isdigit():
                            details["components"][parts[0]] = int(parts[1])
                            details["items_count"] += int(parts[1])
        except Exception:
            pass

    def _get_docker_counts(self, details: Dict[str, Any]) -> None:
        """Add precise image and container counts via docker CLI queries."""
        try:
            r = subprocess.run(
                ["docker", "images", "-q"], capture_output=True, text=True, timeout=5
            )
            if r.returncode == 0:
                details["components"]["images"] = len(
                    [l for l in r.stdout.strip().split("\n") if l]
                )
        except Exception:
            pass
        try:
            r = subprocess.run(
                ["docker", "ps", "-aq"], capture_output=True, text=True, timeout=5
            )
            if r.returncode == 0:
                details["components"]["containers"] = len(
                    [l for l in r.stdout.strip().split("\n") if l]
                )
        except Exception:
            pass

    def _docker(self) -> Dict[str, Any]:
        """Get Docker-specific details - images, containers, volumes."""
        details: Dict[str, Any] = {"items_count": 0, "components": {}}
        self._parse_docker_system_df(details)
        self._get_docker_counts(details)
        return details

    def _ollama(self) -> Dict[str, Any]:
        """Get Ollama-specific details - installed models."""
        details = {"items_count": 0, "models": []}

        try:
            result = subprocess.run(
                ["ollama", "list"], capture_output=True, text=True, timeout=10
            )
            if result.returncode == 0:
                lines = result.stdout.strip().split("\n")
                # Skip header line
                for line in lines[1:]:
                    if line.strip():
                        parts = line.split()
                        if parts:
                            details["models"].append(parts[0])
                details["items_count"] = len(details["models"])
        except Exception:
            pass

        return details

    def _conda(self) -> Dict[str, Any]:
        """Get Conda-specific details - environments."""
        details = {"items_count": 0, "envs": []}

        try:
            result = subprocess.run(
                ["conda", "env", "list"], capture_output=True, text=True, timeout=10
            )
            if result.returncode == 0:
                lines = result.stdout.strip().split("\n")
                # Skip header lines (first 2)
                for line in lines[2:]:
                    if line.strip():
                        parts = line.split()
                        if parts:
                            details["envs"].append(parts[0])
                details["items_count"] = len(details["envs"])
        except Exception:
            pass

        return details

    def _package_cache(self, path: str) -> Dict[str, Any]:
        """Get package cache details - file count."""
        details = {"items_count": 0}

        try:
            count = 0
            for _, _, files in os.walk(path):
                count += len(files)
                if count > 10000:  # Don't count too many
                    break
            details["items_count"] = count if count <= 10000 else "10000+"
        except Exception:
            pass

        return details

    def _flatpak(self) -> Dict[str, Any]:
        """Get detailed Flatpak analysis including unused runtimes and leftover data."""
        details = {
            "items_count": 0,
            "unused_runtimes": [],
            "leftover_data": [],
            "orphaned_apps": [],
            "installed_apps": [],
            "installed_runtimes": [],
            "has_detailed_analysis": True,
        }

        if not _HAS_FLATPAK_ANALYZER:
            return details

        try:
            analyzer = FlatpakAnalyzer()
            analysis = analyzer.analyze()

            # Add detailed breakdown
            details["unused_runtimes"] = analysis.get("unused_runtimes", [])
            details["leftover_data"] = analysis.get("leftover_data", [])
            details["orphaned_apps"] = analysis.get("orphaned_apps", [])
            details["installed_apps"] = analysis.get("installed_apps", [])
            details["installed_runtimes"] = analysis.get("installed_runtimes", [])

            # Calculate totals
            total_unused = sum(
                self._parse_size_bytes(rt.get("size_human", "0"))
                for rt in details["unused_runtimes"]
            )
            total_leftover = sum(
                self._parse_size_bytes(d.get("size_human", "0"))
                for d in details["leftover_data"]
            )
            total_orphaned = sum(
                self._parse_size_bytes(a.get("size_human", "0"))
                for a in details["orphaned_apps"]
            )

            details["total_unused_bytes"] = total_unused
            details["total_leftover_bytes"] = total_leftover
            details["total_orphaned_bytes"] = total_orphaned
            details["total_reclaimable_bytes"] = (
                total_unused + total_leftover + total_orphaned
            )

            # Total items for count
            details["items_count"] = (
                len(details["unused_runtimes"])
                + len(details["leftover_data"])
                + len(details["orphaned_apps"])
            )

            # Summary for display
            details["summary"] = analyzer.get_cleanup_summary()

        except Exception as e:
            details["error"] = str(e)

        return details

    @staticmethod
    def _parse_size_bytes(size_str: str) -> int:
        """Parse human-readable size to bytes."""
        size_str = size_str.strip().upper()
        multipliers = {
            "B": 1,
            "KB": 1024,
            "MB": 1024**2,
            "GB": 1024**3,
            "TB": 1024**4,
        }

        for suffix, mult in sorted(multipliers.items(), key=lambda x: -len(x[0])):
            if size_str.endswith(suffix):
                try:
                    return int(float(size_str[: -len(suffix)].strip()) * mult)
                except ValueError:
                    return 0

        try:
            return int(size_str)
        except ValueError:
            return 0
