"""
Testy jednostkowe – config, anonimizacja, web search.
"""

from __future__ import annotations

import os
from unittest.mock import patch


class TestConfig:
    def test_default_provider_is_gemini(self):
        from fixos.config import FixOsConfig

        with patch.dict(os.environ, {"LLM_PROVIDER": "gemini"}, clear=False):
            cfg = FixOsConfig.load()
        assert cfg.provider == "gemini"

    def test_model_default_gemini(self):
        from fixos.config import FixOsConfig

        cfg = FixOsConfig.load(provider="gemini")
        assert "gemini" in cfg.model.lower()

    def test_invalid_provider_fallback(self):
        from fixos.config import FixOsConfig

        with patch.dict(os.environ, {"LLM_PROVIDER": "nonexistent"}, clear=False):
            cfg = FixOsConfig.load()
        assert cfg.provider == "gemini"

    def test_validate_missing_key(self):
        from fixos.config import FixOsConfig

        cfg = FixOsConfig(provider="openai", api_key=None)
        errors = cfg.validate()
        assert len(errors) > 0
        assert "API" in errors[0]

    def test_validate_ollama_no_key_needed(self):
        from fixos.config import FixOsConfig

        cfg = FixOsConfig(provider="ollama", api_key=None)
        errors = cfg.validate()
        assert len(errors) == 0

    def test_agent_mode_from_env(self):
        from fixos.config import FixOsConfig

        with patch.dict(os.environ, {"AGENT_MODE": "autonomous"}, clear=False):
            cfg = FixOsConfig.load()
        assert cfg.agent_mode == "autonomous"

    def test_summary_masks_key(self):
        from fixos.config import FixOsConfig

        cfg = FixOsConfig(api_key="AIzaSyABCDEFGHIJKLMNOPQRSTUVWXYZ12345")
        summary = cfg.summary()
        assert "AIzaSyAB" in summary
        assert "ABCDEFGHIJKLMNOPQRSTUVWXYZ12345" not in summary


class TestAnonymizer:
    def test_empty_string(self):
        from fixos.utils.anonymizer import anonymize

        anon, report = anonymize("")
        assert anon == ""
        assert len(report.replacements) == 0

    def test_non_string_input(self):
        from fixos.utils.anonymizer import anonymize

        anon, report = anonymize({"key": "value"})
        assert isinstance(anon, str)

    def test_no_sensitive_data(self):
        from fixos.utils.anonymizer import anonymize

        data = "systemctl status pipewire -- Active: running"
        anon, report = anonymize(data)
        # Brak IP ani ścieżek → brak lub minimalne zastąpienia
        sensitive_replacements = {
            k: v
            for k, v in report.replacements.items()
            if k not in ("Hostname", "Username")
        }
        assert len(sensitive_replacements) == 0

    def test_ipv6_not_mangled(self):
        """IPv6 adresy nie powinny być uszkodzone (nie obsługujemy)."""
        from fixos.utils.anonymizer import anonymize

        data = "IPv6 address: 2001:db8::1"
        anon, _ = anonymize(data)
        # Nie crashuje
        assert isinstance(anon, str)

    def test_multiple_ips_all_masked(self):
        from fixos.utils.anonymizer import anonymize

        data = "from 192.168.1.1 to 10.0.0.50 via 172.16.0.1"
        anon, report = anonymize(data)
        assert report.replacements.get("Adresy IPv4", 0) == 3
        assert "192.168.1.1" not in anon
        assert "10.0.0.50" not in anon

    def test_password_in_env_masked(self):
        from fixos.utils.anonymizer import anonymize

        data = "DB_PASSWORD=mysecretpassword123 API_KEY=abc123def456"
        anon, report = anonymize(data)
        assert "mysecretpassword123" not in anon
        assert report.replacements.get("Hasła/sekrety", 0) > 0


class TestWebSearch:
    def test_format_empty_results(self):
        from fixos.utils.web_search import format_results_for_llm

        result = format_results_for_llm([])
        assert "Brak" in result

    def test_format_single_result(self):
        from fixos.utils.web_search import SearchResult, format_results_for_llm

        r = SearchResult(
            title="Fix Lenovo audio",
            url="https://example.com",
            snippet="Install sof-firmware",
            source="Test",
        )
        formatted = format_results_for_llm([r])
        assert "Fix Lenovo audio" in formatted
        assert "https://example.com" in formatted
        assert "[1]" in formatted

    def test_http_get_timeout(self):
        """_http_get powinien obsłużyć timeout gracefully."""
        from fixos.utils.web_search import _http_get

        result = _http_get("http://240.0.0.1/nonexistent", timeout=1)
        assert result is None


class TestSortFixesByPriority:
    def test_cleanup_before_upgrade(self):
        from fixos.agent.session_handlers import _sort_fixes_by_priority

        fixes = [
            ("sudo dnf upgrade -y", "upgrade"),
            ("sudo journalctl --vacuum-size=200M", "clean logs"),
        ]
        result = _sort_fixes_by_priority(fixes)
        assert result[0][0] == "sudo journalctl --vacuum-size=200M"
        assert result[1][0] == "sudo dnf upgrade -y"

    def test_disk_hungry_sorted_to_end(self):
        from fixos.agent.session_handlers import _sort_fixes_by_priority

        fixes = [
            ("sudo dnf upgrade -y", "upgrade"),
            ("sudo apt full-upgrade -y", "upgrade"),
            ("sudo dnf remove oldkernel", "remove"),
            ("sudo rm -rf /var/cache", "clean cache"),
        ]
        result = _sort_fixes_by_priority(fixes)
        # Both remove and rm are cleanup (score 0), upgrades are score 2.
        # Stable sort preserves original order among equal scores.
        assert result[0][0] == "sudo dnf remove oldkernel"
        assert result[1][0] == "sudo rm -rf /var/cache"
        assert result[2][0] == "sudo dnf upgrade -y"
        assert result[3][0] == "sudo apt full-upgrade -y"

    def test_unknown_commands_mid_priority(self):
        from fixos.agent.session_handlers import _sort_fixes_by_priority

        fixes = [
            ("sudo dnf upgrade -y", "upgrade"),
            ("echo 'restart service'", "info"),
        ]
        result = _sort_fixes_by_priority(fixes)
        assert result[0][0] == "echo 'restart service'"
        assert result[1][0] == "sudo dnf upgrade -y"


class TestDiagnosticOnlyCommand:
    def test_simple_diagnostic_is_filtered(self):
        from fixos.agent.session_core import _is_diagnostic_only_command

        assert _is_diagnostic_only_command("df -h") is True
        assert _is_diagnostic_only_command("free -h") is True
        assert _is_diagnostic_only_command("systemctl status auditd") is True

    def test_repair_command_is_not_diagnostic(self):
        from fixos.agent.session_core import _is_diagnostic_only_command

        assert _is_diagnostic_only_command("sudo systemctl restart auditd") is False
        assert _is_diagnostic_only_command("dnf upgrade -y") is False
        assert _is_diagnostic_only_command("rm -rf /var/cache") is False

    def test_journalctl_vacuum_is_not_diagnostic(self):
        from fixos.agent.session_core import _is_diagnostic_only_command

        assert _is_diagnostic_only_command("journalctl --vacuum-size=200M") is False
        assert _is_diagnostic_only_command("journalctl --flush") is False

    def test_compound_command_any_repair_keeps_all(self):
        from fixos.agent.session_core import _is_diagnostic_only_command

        # Compound with both diagnostic and repair → not filtered
        assert _is_diagnostic_only_command("df -h && sudo dnf remove kernel") is False
        assert (
            _is_diagnostic_only_command("cat /etc/fstab || systemctl restart auditd")
            is False
        )

    def test_compound_all_diagnostic_is_filtered(self):
        from fixos.agent.session_core import _is_diagnostic_only_command

        assert _is_diagnostic_only_command("df -h && free -h") is True


class TestExtractFixes:
    """Regression tests for extract_fixes – covers multiple LLM output formats."""

    def test_strict_bold_backticks(self):
        """Pattern 1: **Komenda:** `command` **Co robi:** explanation"""
        from fixos.agent.session_core import extract_fixes

        reply = (
            "🔴 **Problem 1: disk full**\n"
            "   **Komenda:** `sudo dnf autoremove -y`\n"
            "   **Co robi:** removes unused packages\n"
        )
        fixes = extract_fixes(reply)
        assert len(fixes) == 1
        assert fixes[0][0] == "sudo dnf autoremove -y"

    def test_backticks_no_bold(self):
        """Pattern 2: Komenda: `command` (backticks, no bold)"""
        from fixos.agent.session_core import extract_fixes

        reply = (
            "🔴 Problem 1: disk full\n"
            "Komenda: `sudo dnf autoremove -y`\n"
            "Co robi: removes unused packages\n"
        )
        fixes = extract_fixes(reply)
        assert len(fixes) == 1
        assert fixes[0][0] == "sudo dnf autoremove -y"

    def test_no_backticks_no_bold(self):
        """Pattern 3: Komenda: command (plain text – deepseek bug scenario)"""
        from fixos.agent.session_core import extract_fixes

        reply = (
            "🔴 **Problem 1: Krytyczne zapełnienie dysku.**\n"
            "Komenda: sudo journalctl --vacuum-size=200M && sudo dnf autoremove -y\n"
            "Co robi: Oczyszcza logi i pakiety.\n"
            "🟡 **Problem 2: swap failed.**\n"
            "Komenda: sudo systemctl restart swapfile.swap\n"
            "Co robi: Restartuje swap.\n"
        )
        fixes = extract_fixes(reply)
        assert len(fixes) == 2
        assert "journalctl" in fixes[0][0]
        assert "swapfile" in fixes[1][0]

    def test_multiline_command_collapsed(self):
        """Pattern 3 with multiline command – should be collapsed to single line."""
        from fixos.agent.session_core import extract_fixes

        reply = (
            "🔴 **Problem 1: disk full.**\n"
            "Komenda: sudo journalctl --vacuum-size=200M && sudo rm -rf\n"
            "/var/cache/abrt-diag/* && sudo dnf autoremove -y\n"
            "Co robi: cleanup\n"
        )
        fixes = extract_fixes(reply)
        assert len(fixes) >= 1
        cmd = fixes[0][0]
        assert "\n" not in cmd
        assert "journalctl" in cmd
        assert "dnf autoremove" in cmd

    def test_co_robi_extracted_as_comment(self):
        from fixos.agent.session_core import extract_fixes

        reply = (
            "🔴 Problem 1: disk\n"
            "Komenda: `sudo dnf autoremove -y`\n"
            "Co robi: removes unused packages\n"
        )
        fixes = extract_fixes(reply)
        assert len(fixes) == 1
        assert "removes" in fixes[0][1]

    def test_diagnostic_only_filtered(self):
        """Read-only commands should be filtered out."""
        from fixos.agent.session_core import extract_fixes

        reply = (
            "🔴 Problem 1: check disk\n"
            "   **Komenda:** `df -h`\n"
            "   **Co robi:** shows disk usage\n"
        )
        fixes = extract_fixes(reply)
        assert len(fixes) == 0

    def test_duplicate_commands_deduplicated(self):
        """Same command for multiple problems should appear only once."""
        from fixos.agent.session_core import extract_fixes

        reply = (
            "🟡 Problem 3: pending updates\n"
            "Komenda: sudo dnf upgrade -y\n"
            "Co robi: updates packages\n"
            "🟡 Problem 4: security patches\n"
            "Komenda: sudo dnf upgrade -y\n"
            "Co robi: same\n"
        )
        fixes = extract_fixes(reply)
        cmds = [cmd for cmd, _ in fixes]
        assert cmds.count("sudo dnf upgrade -y") == 1

    def test_empty_reply(self):
        from fixos.agent.session_core import extract_fixes

        assert extract_fixes("") == []
        assert extract_fixes("No problems found.") == []


class TestAllModulesRegistered:
    """Verify all 9 diagnostic modules are registered."""

    def test_all_nine_modules_present(self):
        from fixos.diagnostics.system_checks import DIAGNOSTIC_MODULES

        expected = {
            "system",
            "audio",
            "thumbnails",
            "hardware",
            "security",
            "resources",
            "packages",
            "storage",
            "files",
        }
        assert set(DIAGNOSTIC_MODULES.keys()) == expected

    def test_all_modules_callable(self):
        from fixos.diagnostics.system_checks import DIAGNOSTIC_MODULES

        for key, (desc, fn) in DIAGNOSTIC_MODULES.items():
            assert callable(fn), f"Module {key} function is not callable"
            assert isinstance(desc, str) and len(desc) > 0, (
                f"Module {key} has empty description"
            )


class TestInteractiveBlocker:
    def test_newgrp_blocked(self):
        from fixos.platform_utils import is_interactive_blocker

        assert (
            is_interactive_blocker("sudo usermod -aG video $USER && newgrp video")
            is not None
        )

    def test_su_dash_blocked(self):
        from fixos.platform_utils import is_interactive_blocker

        assert is_interactive_blocker("su - tom") is not None

    def test_top_not_blocked_if_batch(self):
        from fixos.platform_utils import is_interactive_blocker

        assert is_interactive_blocker("top -b -n1") is None

    def test_regular_command_not_blocked(self):
        from fixos.platform_utils import is_interactive_blocker

        assert is_interactive_blocker("dnf upgrade -y") is None
