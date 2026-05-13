"""
Integration tests for diagnostic modules.

These tests run real system commands (subprocess) so they are slow.
Moved from tests/unit/test_core.py to keep unit tests fast.
"""

from __future__ import annotations

import platform

import pytest


pytestmark = [
    pytest.mark.slow,
    pytest.mark.skipif(
        platform.system() != "Linux",
        reason="Diagnostic checks require Linux",
    ),
]


class TestDiagnosePackages:
    """Tests for the packages diagnostic module."""

    def test_module_loads_and_returns_dict(self):
        from fixos.diagnostics.checks.packages import diagnose_packages

        result = diagnose_packages()
        assert isinstance(result, dict)

    def test_rpm_keys_present_on_linux(self):
        from fixos.diagnostics.checks.packages import diagnose_packages

        result = diagnose_packages()
        # On Linux, RPM/DNF keys should be present
        assert "total_rpm_count" in result
        assert "large_packages" in result
        assert "orphaned_packages" in result

    def test_flatpak_keys_present_on_linux(self):
        from fixos.diagnostics.checks.packages import diagnose_packages

        result = diagnose_packages()
        assert "flatpak_list" in result
        assert "flatpak_app_count" in result

    def test_desktop_apps_keys_present_on_linux(self):
        from fixos.diagnostics.checks.packages import diagnose_packages

        result = diagnose_packages()
        assert "desktop_apps_count" in result

    def test_registered_in_diagnostic_modules(self):
        from fixos.diagnostics.system_checks import DIAGNOSTIC_MODULES

        assert "packages" in DIAGNOSTIC_MODULES
        desc, fn = DIAGNOSTIC_MODULES["packages"]
        assert callable(fn)
        assert "Pakiety" in desc


class TestDiagnoseStorage:
    """Tests for the storage optimization diagnostic module."""

    def test_module_loads_and_returns_dict(self):
        from fixos.diagnostics.checks.storage_optimization import diagnose_storage

        result = diagnose_storage()
        assert isinstance(result, dict)

    def test_partition_keys_present_on_linux(self):
        from fixos.diagnostics.checks.storage_optimization import diagnose_storage

        result = diagnose_storage()
        assert "partition_table" in result
        assert "disk_info" in result

    def test_swap_keys_present_on_linux(self):
        from fixos.diagnostics.checks.storage_optimization import diagnose_storage

        result = diagnose_storage()
        assert "swap_devices" in result
        assert "swappiness" in result

    def test_filesystem_keys_present_on_linux(self):
        from fixos.diagnostics.checks.storage_optimization import diagnose_storage

        result = diagnose_storage()
        assert "mount_options" in result
        assert "fstab" in result
        assert "inode_usage" in result

    def test_registered_in_diagnostic_modules(self):
        from fixos.diagnostics.system_checks import DIAGNOSTIC_MODULES

        assert "storage" in DIAGNOSTIC_MODULES
        desc, fn = DIAGNOSTIC_MODULES["storage"]
        assert callable(fn)
        assert "Dyski" in desc


@pytest.mark.timeout(300)
class TestDiagnoseFiles:
    """Tests for the file analysis diagnostic module."""

    def test_module_loads_and_returns_dict(self):
        from fixos.diagnostics.checks.file_analysis import diagnose_files

        result = diagnose_files()
        assert isinstance(result, dict)

    def test_large_files_keys_present_on_linux(self):
        from fixos.diagnostics.checks.file_analysis import diagnose_files

        result = diagnose_files()
        assert "large_files_all" in result
        assert "large_files_summary" in result

    def test_media_keys_present_on_linux(self):
        from fixos.diagnostics.checks.file_analysis import diagnose_files

        result = diagnose_files()
        assert "ebooks" in result
        assert "music_files" in result
        assert "video_summary" in result
        assert "images_summary" in result

    def test_archive_candidates_keys_present_on_linux(self):
        from fixos.diagnostics.checks.file_analysis import diagnose_files

        result = diagnose_files()
        assert "stale_large_files" in result
        assert "old_downloads" in result
        assert "trash_size" in result

    def test_downloads_keys_present_on_linux(self):
        from fixos.diagnostics.checks.file_analysis import diagnose_files

        result = diagnose_files()
        assert "downloads_total_size" in result
        assert "downloads_by_type" in result

    def test_registered_in_diagnostic_modules(self):
        from fixos.diagnostics.system_checks import DIAGNOSTIC_MODULES

        assert "files" in DIAGNOSTIC_MODULES
        desc, fn = DIAGNOSTIC_MODULES["files"]
        assert callable(fn)
        assert "Pliki" in desc
