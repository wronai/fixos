"""Testy jednostkowe dla ServiceDataScanner."""

from __future__ import annotations

from fixos.diagnostics.service_scanner import ServiceDataScanner, ServiceType


class TestChromeSafetyClassification:
    def test_chrome_profile_is_marked_for_review(self, monkeypatch):
        scanner = ServiceDataScanner(threshold_mb=1)
        profile_path = "/home/tom/.config/google-chrome"

        monkeypatch.setattr(scanner, "_get_path_size_mb", lambda path: 537.0)
        monkeypatch.setattr(scanner._details_provider, "get_details", lambda service_type, path: {})

        info = scanner._analyze_service_path(ServiceType.CHROME, profile_path)

        assert info is not None
        assert info.safe_to_cleanup is False
        assert profile_path in info.cleanup_command

    def test_chrome_cache_path_is_marked_safe(self, monkeypatch):
        scanner = ServiceDataScanner(threshold_mb=1)
        cache_path = "/home/tom/.cache/google-chrome"

        monkeypatch.setattr(scanner, "_get_path_size_mb", lambda path: 40.0)
        monkeypatch.setattr(scanner._details_provider, "get_details", lambda service_type, path: {})

        info = scanner._analyze_service_path(ServiceType.CHROME, cache_path)

        assert info is not None
        assert info.safe_to_cleanup is True
        assert cache_path in info.cleanup_command
