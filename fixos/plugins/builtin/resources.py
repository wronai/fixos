"""Resources diagnostic plugin — CPU, RAM, processes, autostart."""

from __future__ import annotations

from fixos.plugins.base import DiagnosticPlugin, DiagnosticResult, Finding, Severity
from fixos.platform_utils import run_command


class Plugin(DiagnosticPlugin):
    name = "resources"
    description = "Diagnostyka zasobów (CPU, RAM, procesy, autostart)"
    platforms = ["linux", "macos"]

    def diagnose(self) -> DiagnosticResult:
        findings = []
        raw_data = {}

        # CPU load
        cpu = self._check_cpu()
        raw_data["cpu"] = cpu
        if cpu.get("load_1m") and cpu["load_1m"] > cpu.get("cores", 1) * 2:
            findings.append(
                Finding(
                    title="Wysokie obciążenie CPU",
                    severity=Severity.WARNING,
                    description=f"Load average 1m: {cpu['load_1m']:.1f} (rdzenie: {cpu.get('cores', '?')}).",
                    suggestion="Sprawdź procesy zużywające CPU: top lub htop.",
                )
            )

        # RAM usage
        ram = self._check_ram()
        raw_data["ram"] = ram
        if ram.get("percent") and ram["percent"] > 90:
            findings.append(
                Finding(
                    title="Krytycznie wysokie zużycie RAM",
                    severity=Severity.CRITICAL,
                    description=f"RAM: {ram['percent']:.0f}% ({ram.get('used_gb', '?')}GB / {ram.get('total_gb', '?')}GB).",
                    suggestion="Zamknij niepotrzebne aplikacje lub zwiększ swap.",
                )
            )
        elif ram.get("percent") and ram["percent"] > 80:
            findings.append(
                Finding(
                    title="Wysokie zużycie RAM",
                    severity=Severity.WARNING,
                    description=f"RAM: {ram['percent']:.0f}% ({ram.get('used_gb', '?')}GB / {ram.get('total_gb', '?')}GB).",
                )
            )

        # Top processes
        procs = self._check_top_processes()
        raw_data["top_processes"] = procs

        # Zombie processes
        zombies = self._check_zombies()
        raw_data["zombies"] = zombies
        if zombies.get("count", 0) > 5:
            findings.append(
                Finding(
                    title=f"{zombies['count']} procesów zombie",
                    severity=Severity.WARNING,
                    description="Duża liczba procesów zombie może wskazywać na problem z parent process.",
                )
            )

        # Swap usage
        swap = self._check_swap()
        raw_data["swap"] = swap
        if swap.get("percent") and swap["percent"] > 80:
            findings.append(
                Finding(
                    title="Wysokie zużycie swap",
                    severity=Severity.WARNING,
                    description=f"Swap: {swap['percent']:.0f}% wykorzystany.",
                    suggestion="System intensywnie korzysta ze swap — może być wolny.",
                )
            )

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

    def _check_cpu(self) -> dict:
        try:
            import psutil

            load = psutil.getloadavg()
            return {
                "load_1m": load[0],
                "load_5m": load[1],
                "load_15m": load[2],
                "cores": psutil.cpu_count(),
            }
        except Exception:
            ok, stdout, _, _ = run_command("cat /proc/loadavg 2>/dev/null", timeout=5)
            if ok and stdout:
                parts = stdout.split()
                return {"load_1m": float(parts[0]) if parts else 0, "cores": None}
            return {}

    def _check_ram(self) -> dict:
        try:
            import psutil

            mem = psutil.virtual_memory()
            return {
                "total_gb": round(mem.total / (1024**3), 1),
                "used_gb": round(mem.used / (1024**3), 1),
                "available_gb": round(mem.available / (1024**3), 1),
                "percent": mem.percent,
            }
        except Exception:
            return {}

    def _check_top_processes(self) -> dict:
        ok, stdout, _, _ = run_command("ps aux --sort=-%mem | head -6", timeout=5)
        return {"raw": stdout if ok else ""}

    def _check_zombies(self) -> dict:
        ok, stdout, _, _ = run_command(
            "ps aux | awk '$8 ~ /Z/ {count++} END {print count+0}'", timeout=5
        )
        count = int(stdout.strip()) if ok and stdout.strip().isdigit() else 0
        return {"count": count}

    def _check_swap(self) -> dict:
        try:
            import psutil

            swap = psutil.swap_memory()
            return {
                "total_gb": round(swap.total / (1024**3), 1),
                "used_gb": round(swap.used / (1024**3), 1),
                "percent": swap.percent,
            }
        except Exception:
            return {}
