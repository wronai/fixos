"""
Testy e2e – scenariusz uszkodzonych podglądów plików (thumbnails).
"""

from __future__ import annotations

import os
from unittest.mock import MagicMock, patch

import pytest

from fixos.utils.anonymizer import anonymize


class TestThumbnailsDetection:
    """Testy wykrywania problemów z thumbnails."""

    def test_detect_missing_ffmpegthumbnailer(self, broken_thumbnails_diagnostics):
        thumb = broken_thumbnails_diagnostics["thumbnails"]
        assert "nie zainstalowany" in thumb.get("ffmpegthumbnailer", "").lower()

    def test_detect_missing_totem_thumbnailer(self, broken_thumbnails_diagnostics):
        thumb = broken_thumbnails_diagnostics["thumbnails"]
        assert "nie znaleziony" in thumb.get("totem_thumb", "").lower()

    def test_detect_empty_thumbnail_cache(self, broken_thumbnails_diagnostics):
        thumb = broken_thumbnails_diagnostics["thumbnails"]
        cache_count = int(thumb.get("thumbnail_cache_count", "0"))
        assert cache_count == 0

    def test_detect_high_fail_count(self, broken_thumbnails_diagnostics):
        """Duża liczba failed thumbnails wskazuje na problem."""
        thumb = broken_thumbnails_diagnostics["thumbnails"]
        fail_count = int(thumb.get("thumbnail_fail_files", "0"))
        assert fail_count > 10, "Powinno być dużo failed thumbnails"

    def test_detect_missing_thumbnailer_packages(self, broken_thumbnails_diagnostics):
        thumb = broken_thumbnails_diagnostics["thumbnails"]
        packages = thumb.get("thumbnailer_packages", "")
        assert packages.strip() == "" or "ffmpeg" not in packages.lower()

    def test_detect_missing_thumbnailer_configs(self, broken_thumbnails_diagnostics):
        thumb = broken_thumbnails_diagnostics["thumbnails"]
        configs = thumb.get("thumbnailer_configs", "")
        # Pusty katalog thumbnailerów
        assert configs.strip() == "" or "total 0" in configs


class TestThumbnailsAnonymization:
    """Testy anonimizacji danych thumbnails."""

    def test_home_path_in_cache_anonymized(self, broken_thumbnails_diagnostics):
        """Ścieżka ~/.cache powinna być zanonimizowana."""
        import getpass

        username = getpass.getuser()
        data = str(broken_thumbnails_diagnostics)
        data += f" /home/{username}/.cache/thumbnails"

        anon, report = anonymize(data)
        assert username not in anon or "[USER]" in anon

    def test_xdg_cache_path_anonymized(self):
        """Ścieżka XDG_CACHE_HOME powinna być zanonimizowana."""
        data = "XDG_CACHE_HOME=/home/testuser/.cache"
        anon, _ = anonymize(data)
        assert "testuser" not in anon


class TestThumbnailsMockLLM:
    """Testy z mock LLM dla scenariusza thumbnails."""

    @patch("fixos.providers.llm.openai")
    def test_llm_suggests_ffmpegthumbnailer(
        self, mock_openai, broken_thumbnails_diagnostics, mock_config
    ):
        """LLM powinien sugerować instalację ffmpegthumbnailer."""
        from fixos.providers.llm import LLMClient

        mock_resp = MagicMock()
        mock_resp.choices[0].message.content = (
            "🟡 Problem: Brak thumbnailerów\n"
            "→ Fix: `sudo dnf install ffmpegthumbnailer`\n"
            "→ Fix: `sudo dnf install totem-nautilus`\n"
            "→ Fix: `nautilus -q && rm -rf ~/.cache/thumbnails/*`"
        )
        mock_resp.usage.total_tokens = 80
        mock_openai.OpenAI.return_value.chat.completions.create.return_value = mock_resp

        client = LLMClient(mock_config)
        anon_str, _ = anonymize(str(broken_thumbnails_diagnostics))
        messages = [
            {"role": "system", "content": "Diagnozuj Fedora Linux."},
            {"role": "user", "content": anon_str},
        ]
        reply = client.chat(messages)

        assert "ffmpegthumbnailer" in reply.lower()
        assert "dnf install" in reply.lower()

    @patch("fixos.providers.llm.openai")
    def test_llm_suggests_cache_clear(
        self, mock_openai, broken_thumbnails_diagnostics, mock_config
    ):
        """LLM powinien sugerować wyczyszczenie cache thumbnails."""
        from fixos.providers.llm import LLMClient

        mock_resp = MagicMock()
        mock_resp.choices[0].message.content = (
            "Wyczyść cache: rm -rf ~/.cache/thumbnails/fail/*\n"
            "Zainstaluj: dnf install ffmpegthumbnailer gstreamer1-plugins-good"
        )
        mock_resp.usage.total_tokens = 60
        mock_openai.OpenAI.return_value.chat.completions.create.return_value = mock_resp

        client = LLMClient(mock_config)
        anon_str, _ = anonymize(str(broken_thumbnails_diagnostics))
        reply = client.chat([{"role": "user", "content": anon_str}])

        assert "thumbnail" in reply.lower() or "cache" in reply.lower()


class TestWebSearchFallback:
    """Testy wyszukiwania zewnętrznego jako fallback."""

    def test_search_arch_wiki_thumbnails(self):
        """Arch Wiki powinno zwrócić wyniki dla 'thumbnails'."""
        from fixos.utils.web_search import search_arch_wiki

        results = search_arch_wiki("file manager thumbnails")
        # Wyniki mogą być puste gdy brak internetu w Docker
        assert isinstance(results, list)

    def test_search_fedora_bugzilla_audio(self):
        """Bugzilla może zwrócić wyniki dla problemów audio SOF."""
        from fixos.utils.web_search import search_fedora_bugzilla

        results = search_fedora_bugzilla("sof-firmware audio Lenovo")
        assert isinstance(results, list)

    def test_format_results_for_llm(self):
        """Wyniki powinny być poprawnie sformatowane dla LLM."""
        from fixos.utils.web_search import SearchResult, format_results_for_llm

        results = [
            SearchResult(
                title="Fix audio Fedora 40",
                url="https://ask.fedoraproject.org/t/fix/123",
                snippet="Zainstaluj sof-firmware i zrestartuj.",
                source="ask.fedoraproject.org",
            )
        ]
        formatted = format_results_for_llm(results)
        assert "Fix audio Fedora 40" in formatted
        assert "sof-firmware" in formatted
        assert "[1]" in formatted

    def test_empty_results_handled(self):
        """Puste wyniki powinny zwrócić sensowny komunikat."""
        from fixos.utils.web_search import format_results_for_llm

        formatted = format_results_for_llm([])
        assert "Brak wyników" in formatted


class TestFullBrokenScenario:
    """Testy pełnego scenariusza (audio + thumbnails + inne problemy)."""

    def test_all_modules_detected(self, full_broken_diagnostics):
        """Powinny być dane ze wszystkich modułów diagnostycznych."""
        assert "audio" in full_broken_diagnostics
        assert "thumbnails" in full_broken_diagnostics
        assert "hardware" in full_broken_diagnostics
        assert "system" in full_broken_diagnostics

    def test_combined_issues_anonymized(self, full_broken_diagnostics):
        """Dane z wielu modułów powinny być anonimizowane razem."""
        import socket
        import getpass

        data = str(full_broken_diagnostics)
        data += f" {socket.gethostname()} {getpass.getuser()} 192.168.100.200"

        anon, report = anonymize(data)
        assert socket.gethostname() not in anon
        assert "192.168.100.200" not in anon
        assert len(report.replacements) >= 2

    @patch("fixos.providers.llm.openai")
    def test_full_scenario_llm_comprehensive(
        self, mock_openai, full_broken_diagnostics, mock_config
    ):
        """LLM powinien wykryć wiele problemów naraz."""
        from fixos.providers.llm import LLMClient

        mock_resp = MagicMock()
        mock_resp.choices[0].message.content = """
━━━ DIAGNOZA ━━━
🔴 Problem 1: Brak dźwięku – sof-firmware nie zainstalowany
   → Fix: `sudo dnf install sof-firmware`
🔴 Problem 2: PipeWire failed
   → Fix: `systemctl --user restart pipewire wireplumber`
🟡 Problem 3: Brak thumbnailerów
   → Fix: `sudo dnf install ffmpegthumbnailer totem-nautilus`
🟡 Problem 4: 15 pakietów do aktualizacji
   → Fix: `sudo dnf upgrade -y`
🟢 Problem 5: Pusty cache miniaturek
   → Fix: `rm -rf ~/.cache/thumbnails/*`
"""
        mock_resp.usage.total_tokens = 400
        mock_openai.OpenAI.return_value.chat.completions.create.return_value = mock_resp

        client = LLMClient(mock_config)
        anon_str, _ = anonymize(str(full_broken_diagnostics))
        messages = [
            {"role": "system", "content": "Diagnostyk Fedora."},
            {"role": "user", "content": anon_str},
        ]
        reply = client.chat(messages)

        # Sprawdź wykrycie wielu problemów
        assert "sof-firmware" in reply.lower()
        assert "ffmpegthumbnailer" in reply.lower() or "thumbnail" in reply.lower()
        assert "dnf" in reply.lower()

    @pytest.mark.skipif(
        not os.environ.get("GEMINI_API_KEY")
        or "TWOJ" in os.environ.get("GEMINI_API_KEY", ""),
        reason="Wymaga GEMINI_API_KEY w .env",
    )
    def test_real_llm_full_scenario(self, full_broken_diagnostics, test_config):
        """Prawdziwy LLM analizuje pełny scenariusz uszkodzeń."""
        from fixos.providers.llm import LLMClient
        from fixos.utils.anonymizer import anonymize

        client = LLMClient(test_config)
        anon_str, _ = anonymize(str(full_broken_diagnostics))

        messages = [
            {
                "role": "system",
                "content": (
                    "Jesteś diagnostą Fedora Linux. "
                    "Wymień TYLKO główne problemy jako numerowaną listę (max 5 punktów). "
                    "Dla każdego podaj komendę fix."
                ),
            },
            {"role": "user", "content": f"Dane:\n{anon_str[:3000]}"},
        ]

        reply = client.chat(messages, max_tokens=500)

        # Sprawdź czy wykryto kluczowe problemy
        audio_found = any(
            t in reply.lower() for t in ["audio", "sof", "dźwięk", "alsa", "pipewire"]
        )
        thumb_found = any(
            t in reply.lower()
            for t in ["thumbnail", "thumbnailer", "podgląd", "ffmpeg"]
        )

        assert audio_found or thumb_found, (
            f"LLM nie wykrył żadnego z oczekiwanych problemów.\nOdpowiedź: {reply[:400]}"
        )
        print(f"\n✅ Odpowiedź LLM:\n{reply[:600]}")
