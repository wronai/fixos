"""Thumbnails diagnostic plugin — cache, GStreamer, thumbnailers."""

from __future__ import annotations

from fixos.plugins.base import DiagnosticPlugin, DiagnosticResult, Finding, Severity
from fixos.platform_utils import run_command


class Plugin(DiagnosticPlugin):
    name = "thumbnails"
    description = "Diagnostyka podglądów plików (cache, GStreamer, thumbnailers)"
    platforms = ["linux"]

    def diagnose(self) -> DiagnosticResult:
        findings = []
        raw_data = {}

        # Thumbnail cache
        cache = self._check_cache()
        raw_data["cache"] = cache
        if cache.get("count", 0) == 0:
            findings.append(Finding(
                title="Pusty cache miniaturek",
                severity=Severity.WARNING,
                description="Brak podglądów plików w cache — miniatury nie będą wyświetlane.",
                suggestion="Sprawdź konfigurację thumbnailerów.",
            ))
        elif cache.get("size_mb", 0) > 500:
            findings.append(Finding(
                title=f"Duży cache miniaturek ({cache['size_mb']:.0f} MB)",
                severity=Severity.INFO,
                description="Cache miniaturek zajmuje dużo miejsca.",
                suggestion="Wyczyść stare miniatury.",
                command="rm -rf ~/.cache/thumbnails/fail ~/.cache/thumbnails/large",
            ))

        # ffmpegthumbnailer
        ffmpeg = self._check_ffmpegthumbnailer()
        raw_data["ffmpegthumbnailer"] = ffmpeg
        if not ffmpeg.get("installed"):
            findings.append(Finding(
                title="ffmpegthumbnailer nie zainstalowany",
                severity=Severity.WARNING,
                description="Bez ffmpegthumbnailer nie będą generowane miniatury filmów.",
                command="sudo dnf install -y ffmpegthumbnailer",
            ))

        # totem-video-thumbnailer
        totem = self._check_totem()
        raw_data["totem"] = totem
        if not totem.get("found"):
            findings.append(Finding(
                title="totem-video-thumbnailer nie znaleziony",
                severity=Severity.INFO,
                description="Alternatywny thumbnailer wideo nie jest dostępny.",
            ))

        # GStreamer plugins
        gst = self._check_gstreamer()
        raw_data["gstreamer"] = gst
        if gst.get("missing_plugins"):
            findings.append(Finding(
                title="Brakujące pluginy GStreamer",
                severity=Severity.WARNING,
                description=f"Brakujące: {', '.join(gst['missing_plugins'])}",
                suggestion="Zainstaluj codec GStreamer.",
                command="sudo dnf install -y gstreamer1-plugins-good gstreamer1-plugins-ugly",
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

    def _check_cache(self) -> dict:
        ok, stdout, _, _ = run_command(
            "find ~/.cache/thumbnails -type f 2>/dev/null | wc -l", timeout=10
        )
        count = int(stdout.strip()) if ok and stdout.strip().isdigit() else 0

        ok2, stdout2, _, _ = run_command(
            "du -sm ~/.cache/thumbnails 2>/dev/null | cut -f1", timeout=10
        )
        size_mb = float(stdout2.strip()) if ok2 and stdout2.strip().replace(".", "").isdigit() else 0

        return {"count": count, "size_mb": size_mb}

    def _check_ffmpegthumbnailer(self) -> dict:
        ok, stdout, _, _ = run_command("which ffmpegthumbnailer 2>/dev/null", timeout=5)
        return {"installed": ok and bool(stdout.strip())}

    def _check_totem(self) -> dict:
        ok, stdout, _, _ = run_command("which totem-video-thumbnailer 2>/dev/null", timeout=5)
        return {"found": ok and bool(stdout.strip())}

    def _check_gstreamer(self) -> dict:
        ok, stdout, _, _ = run_command(
            "gst-inspect-1.0 2>/dev/null | head -1", timeout=5
        )
        missing = []
        if not ok:
            missing.append("gstreamer1-plugins-base")
        else:
            for plugin in ["playback", "videoconvert", "videoscale"]:
                ok2, _, _, _ = run_command(
                    f"gst-inspect-1.0 {plugin} 2>/dev/null", timeout=5
                )
                if not ok2:
                    missing.append(plugin)
        return {"available": ok, "missing_plugins": missing}
