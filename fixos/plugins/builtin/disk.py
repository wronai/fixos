"""Disk diagnostic plugin — usage, partitions, SMART health."""

from __future__ import annotations

from fixos.plugins.base import DiagnosticPlugin, DiagnosticResult, Finding, Severity
from fixos.platform_utils import run_command


class Plugin(DiagnosticPlugin):
    name = "disk"
    description = "Diagnostyka dysku (zajętość, partycje, SMART)"
    platforms = ["linux", "macos"]

    def diagnose(self) -> DiagnosticResult:
        findings = []
        raw_data = {}

        # Disk usage
        usage = self._check_usage()
        raw_data["usage"] = usage
        for mount in usage.get("mounts", []):
            pct = mount.get("percent", 0)
            if pct >= 95:
                findings.append(Finding(
                    title=f"Dysk {mount['mount']} prawie pełny ({pct}%)",
                    severity=Severity.CRITICAL,
                    description=f"Partycja {mount['mount']} ma {pct}% zajętości ({mount.get('used', '?')}/{mount.get('total', '?')}).",
                    suggestion="Zwolnij miejsce lub rozszerz partycję.",
                ))
            elif pct >= 85:
                findings.append(Finding(
                    title=f"Dysk {mount['mount']} wysoko zajęty ({pct}%)",
                    severity=Severity.WARNING,
                    description=f"Partycja {mount['mount']} ma {pct}% zajętości.",
                ))

        # Inodes
        inodes = self._check_inodes()
        raw_data["inodes"] = inodes
        for mount in inodes.get("mounts", []):
            pct = mount.get("percent", 0)
            if pct >= 90:
                findings.append(Finding(
                    title=f"Mało i-node na {mount['mount']} ({pct}%)",
                    severity=Severity.WARNING,
                    description="Wyczerpanie i-node blokuje tworzenie nowych plików.",
                ))

        # Read-only mounts
        ro = self._check_readonly()
        raw_data["readonly"] = ro
        if ro.get("readonly_mounts"):
            for m in ro["readonly_mounts"]:
                findings.append(Finding(
                    title=f"Partycja {m} jest read-only",
                    severity=Severity.CRITICAL,
                    description=f"Partycja {m} jest zamontowana w trybie tylko do odczytu.",
                    suggestion="Sprawdź system plików: fsck lub remount.",
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

    def _check_usage(self) -> dict:
        ok, stdout, _, _ = run_command("df -h --output=target,size,used,avail,pcent -x tmpfs -x devtmpfs 2>/dev/null", timeout=10)
        mounts = []
        if ok and stdout:
            for line in stdout.splitlines()[1:]:
                parts = line.split()
                if len(parts) >= 5:
                    pct_str = parts[4].rstrip("%")
                    mounts.append({
                        "mount": parts[0],
                        "total": parts[1],
                        "used": parts[2],
                        "available": parts[3],
                        "percent": int(pct_str) if pct_str.isdigit() else 0,
                    })
        return {"mounts": mounts}

    def _check_inodes(self) -> dict:
        ok, stdout, _, _ = run_command("df -i --output=target,iused,iavail,ipcent -x tmpfs -x devtmpfs 2>/dev/null", timeout=10)
        mounts = []
        if ok and stdout:
            for line in stdout.splitlines()[1:]:
                parts = line.split()
                if len(parts) >= 4:
                    pct_str = parts[3].rstrip("%")
                    mounts.append({
                        "mount": parts[0],
                        "percent": int(pct_str) if pct_str.isdigit() else 0,
                    })
        return {"mounts": mounts}

    def _check_readonly(self) -> dict:
        ok, stdout, _, _ = run_command("mount | grep 'ro,' | grep -v 'snap\\|loop'", timeout=5)
        ro_mounts = []
        if ok and stdout:
            for line in stdout.splitlines():
                parts = line.split()
                if len(parts) >= 3:
                    ro_mounts.append(parts[2])
        return {"readonly_mounts": ro_mounts}
