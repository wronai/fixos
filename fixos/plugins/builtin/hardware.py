"""Hardware diagnostic plugin — DMI, GPU, touchpad, camera, battery."""

from __future__ import annotations

from fixos.plugins.base import DiagnosticPlugin, DiagnosticResult, Finding, Severity
from fixos.platform_utils import run_command


class Plugin(DiagnosticPlugin):
    name = "hardware"
    description = "Diagnostyka sprzętu (DMI, GPU, touchpad, kamera, bateria)"
    platforms = ["linux"]

    def diagnose(self) -> DiagnosticResult:
        findings = []
        raw_data = {}

        # GPU info
        gpu = self._check_gpu()
        raw_data["gpu"] = gpu
        if gpu.get("error"):
            findings.append(
                Finding(
                    title="Nie wykryto GPU",
                    severity=Severity.WARNING,
                    description="Nie udało się odczytać informacji o GPU.",
                    suggestion="Sprawdź sterowniki graficzne.",
                )
            )

        # Battery
        battery = self._check_battery()
        raw_data["battery"] = battery
        if battery.get("capacity") is not None and battery["capacity"] < 30:
            findings.append(
                Finding(
                    title="Niski poziom baterii",
                    severity=Severity.WARNING,
                    description=f"Bateria na poziomie {battery['capacity']}%.",
                )
            )
        if battery.get("health") and battery["health"] < 50:
            findings.append(
                Finding(
                    title="Zużyta bateria",
                    severity=Severity.CRITICAL,
                    description=f"Zdrowie baterii: {battery['health']}%.",
                    suggestion="Rozważ wymianę baterii.",
                )
            )

        # Touchpad
        touchpad = self._check_touchpad()
        raw_data["touchpad"] = touchpad
        if touchpad.get("missing"):
            findings.append(
                Finding(
                    title="Nie wykryto touchpada",
                    severity=Severity.INFO,
                    description="System nie wykrył urządzenia touchpad.",
                )
            )

        # Camera
        camera = self._check_camera()
        raw_data["camera"] = camera
        if camera.get("missing"):
            findings.append(
                Finding(
                    title="Nie wykryto kamery",
                    severity=Severity.INFO,
                    description="Nie znaleziono urządzenia /dev/video*.",
                )
            )

        # DMI info
        dmi = self._check_dmi()
        raw_data["dmi"] = dmi

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

    def _check_gpu(self) -> dict:
        ok, stdout, stderr, rc = run_command("lspci | grep -i vga", timeout=5)
        if ok and stdout:
            return {"devices": stdout.splitlines(), "error": None}
        return {"devices": [], "error": "lspci failed or no VGA device"}

    def _check_battery(self) -> dict:
        ok, stdout, stderr, rc = run_command(
            "cat /sys/class/power_supply/BAT0/capacity 2>/dev/null", timeout=5
        )
        capacity = None
        if ok and stdout.strip().isdigit():
            capacity = int(stdout.strip())

        health = None
        ok2, full, _, _ = run_command(
            "cat /sys/class/power_supply/BAT0/energy_full 2>/dev/null", timeout=5
        )
        ok3, design, _, _ = run_command(
            "cat /sys/class/power_supply/BAT0/energy_full_design 2>/dev/null", timeout=5
        )
        if ok2 and ok3 and full.strip().isdigit() and design.strip().isdigit():
            design_val = int(design.strip())
            if design_val > 0:
                health = round(int(full.strip()) / design_val * 100)

        return {"capacity": capacity, "health": health}

    def _check_touchpad(self) -> dict:
        ok, stdout, stderr, rc = run_command(
            "grep -i touchpad /proc/bus/input/devices 2>/dev/null", timeout=5
        )
        return {"missing": not ok or not stdout.strip()}

    def _check_camera(self) -> dict:
        ok, stdout, stderr, rc = run_command("ls /dev/video* 2>/dev/null", timeout=5)
        return {
            "missing": not ok or not stdout.strip(),
            "devices": stdout.splitlines() if ok else [],
        }

    def _check_dmi(self) -> dict:
        ok, stdout, stderr, rc = run_command(
            "cat /sys/class/dmi/id/product_name 2>/dev/null", timeout=5
        )
        product = stdout.strip() if ok else "unknown"
        ok2, vendor, _, _ = run_command(
            "cat /sys/class/dmi/id/sys_vendor 2>/dev/null", timeout=5
        )
        return {"product": product, "vendor": vendor.strip() if ok2 else "unknown"}
