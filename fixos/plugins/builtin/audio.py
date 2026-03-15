"""Audio diagnostic plugin — ALSA, PipeWire, PulseAudio, SOF firmware."""

from __future__ import annotations

from fixos.plugins.base import DiagnosticPlugin, DiagnosticResult, Finding, Severity
from fixos.platform_utils import run_command


class Plugin(DiagnosticPlugin):
    name = "audio"
    description = "Diagnostyka dźwięku (ALSA/PipeWire/PulseAudio/SOF)"
    platforms = ["linux"]

    def diagnose(self) -> DiagnosticResult:
        findings = []
        raw_data = {}

        # ALSA cards
        alsa = self._check_alsa()
        raw_data["alsa"] = alsa
        if not alsa.get("cards"):
            findings.append(Finding(
                title="Brak kart ALSA",
                severity=Severity.CRITICAL,
                description="System nie wykrył żadnych kart dźwiękowych ALSA.",
                suggestion="Sprawdź czy moduły jądra snd_* są załadowane.",
                command="sudo modprobe snd_hda_intel",
            ))

        # PipeWire status
        pw = self._check_pipewire()
        raw_data["pipewire"] = pw
        if pw.get("status") == "failed":
            findings.append(Finding(
                title="PipeWire nie działa",
                severity=Severity.CRITICAL,
                description="Usługa PipeWire nie jest aktywna.",
                command="systemctl --user restart pipewire pipewire-pulse",
            ))
        elif pw.get("status") == "inactive":
            findings.append(Finding(
                title="PipeWire nieaktywny",
                severity=Severity.WARNING,
                description="Usługa PipeWire jest nieaktywna.",
                command="systemctl --user start pipewire pipewire-pulse",
            ))

        # WirePlumber
        wp = self._check_wireplumber()
        raw_data["wireplumber"] = wp
        if wp.get("status") == "failed":
            findings.append(Finding(
                title="WirePlumber nie działa",
                severity=Severity.WARNING,
                description="WirePlumber (session manager) nie jest aktywny.",
                command="systemctl --user restart wireplumber",
            ))

        # SOF firmware
        sof = self._check_sof()
        raw_data["sof"] = sof
        if sof.get("missing"):
            findings.append(Finding(
                title="Brak firmware SOF",
                severity=Severity.WARNING,
                description="Firmware Sound Open Firmware nie jest zainstalowany.",
                suggestion="Zainstaluj pakiet sof-firmware.",
                command="sudo dnf install -y sof-firmware",
            ))

        status = Severity.OK
        if any(f.severity == Severity.CRITICAL for f in findings):
            status = Severity.CRITICAL
        elif any(f.severity == Severity.WARNING for f in findings):
            status = Severity.WARNING

        return DiagnosticResult(
            plugin_name=self.name,
            status=status,
            findings=findings,
            raw_data=raw_data,
        )

    def _check_alsa(self) -> dict:
        ok, stdout, stderr, rc = run_command("cat /proc/asound/cards", timeout=5)
        cards = []
        if ok and stdout and "no soundcards" not in stdout.lower():
            cards = [line.strip() for line in stdout.splitlines() if line.strip()]
        return {"cards": cards, "raw": stdout}

    def _check_pipewire(self) -> dict:
        ok, stdout, stderr, rc = run_command(
            "systemctl --user is-active pipewire", timeout=5
        )
        return {"status": stdout.strip() if stdout else "unknown"}

    def _check_wireplumber(self) -> dict:
        ok, stdout, stderr, rc = run_command(
            "systemctl --user is-active wireplumber", timeout=5
        )
        return {"status": stdout.strip() if stdout else "unknown"}

    def _check_sof(self) -> dict:
        ok, stdout, stderr, rc = run_command(
            "ls /lib/firmware/intel/sof 2>/dev/null", timeout=5
        )
        return {"missing": not ok or not stdout.strip()}
