"""
System core diagnostics module.
Checks CPU, RAM, disks, processes - cross-platform.
"""

from datetime import datetime
from typing import Any
import platform

from ._shared import _cmd, _psutil_required, IS_LINUX, IS_WINDOWS, IS_MAC, psutil_module as psutil


def _collect_os_info() -> tuple[str, str, str]:
    """Return (os_release, kernel, uptime) for the current platform."""
    if IS_LINUX:
        return (
            _cmd("cat /etc/os-release | grep -E '^(NAME|VERSION|ID)='"),
            _cmd("uname -r"),
            _cmd("uptime -p"),
        )
    if IS_WINDOWS:
        return (
            _cmd('powershell -Command "(Get-WmiObject Win32_OperatingSystem).Caption"'),
            _cmd('powershell -Command "(Get-WmiObject Win32_OperatingSystem).Version"'),
            _cmd('powershell -Command "((Get-Date)-(gcim Win32_OperatingSystem).LastBootUpTime).ToString()"'),
        )
    return (
        _cmd("sw_vers 2>/dev/null"),
        _cmd("uname -r"),
        _cmd("uptime 2>/dev/null"),
    )


def _collect_platform_details() -> dict[str, Any]:
    """Return platform-specific diagnostic fields (updates, logs, firewall, etc.)."""
    if IS_LINUX:
        return {
            "updates_pending": _cmd(
                "dnf check-update -q 2>/dev/null | grep -c '^[A-Za-z]' || "
                "apt list --upgradable 2>/dev/null | grep -c upgradable || echo '0'"
            ),
            "pkg_history": _cmd("dnf history list --last=5 2>/dev/null || true"),
            "systemctl_failed": _cmd("systemctl --failed --no-legend 2>/dev/null"),
            "journal_errors_24h": _cmd("journalctl -p err -n 20 --no-pager --since '24 hours ago' 2>/dev/null"),
            "dmesg_errors": _cmd("dmesg --level=err,crit,emerg --notime 2>/dev/null | tail -15"),
            "selinux": _cmd("getenforce 2>/dev/null || echo 'N/A'"),
            "firewall": _cmd("firewall-cmd --state 2>/dev/null || echo 'N/A'"),
        }
    if IS_WINDOWS:
        return {
            "updates_pending": _cmd('powershell -Command "(New-Object -ComObject Microsoft.Update.Session).CreateUpdateSearcher().Search(\"IsInstalled=0\").Updates.Count" 2>nul || echo "N/A"'),
            "services_failed": _cmd('powershell -Command "Get-Service | Where-Object{$_.Status -eq \"Stopped\" -and $_.StartType -eq \"Automatic\"} | Select-Object Name | Format-List"'),
            "event_errors": _cmd('powershell -Command "Get-EventLog -LogName System -EntryType Error -Newest 10 2>$null | Select-Object TimeGenerated,Source,Message | Format-List"'),
            "firewall": _cmd("netsh advfirewall show allprofiles state 2>nul"),
        }
    return {
        "updates_pending": _cmd("softwareupdate -l 2>/dev/null | grep -c '\\*' || echo '0'"),
        "launchd_failed": _cmd("launchctl list 2>/dev/null | grep -v '^-' | awk '$1 != 0 {print}' | head -10"),
        "firewall": _cmd("defaults read /Library/Preferences/com.apple.alf globalstate 2>/dev/null"),
    }


def diagnose_system() -> dict[str, Any]:
    """System metrics – cross-platform: CPU, RAM, disks, processes."""
    if not _psutil_required():
        return {"error": "psutil is required for system diagnostics but is not installed"}

    vm = psutil.virtual_memory()
    sw = psutil.swap_memory()

    disks = {}
    for p in psutil.disk_partitions(all=False):
        try:
            u = psutil.disk_usage(p.mountpoint)
            disks[p.mountpoint] = {
                "device": p.device, "fstype": p.fstype,
                "total_gb": round(u.total / 1024**3, 2),
                "used_gb": round(u.used / 1024**3, 2),
                "free_gb": round(u.free / 1024**3, 2),
                "percent": u.percent,
            }
        except PermissionError:
            pass

    procs = []
    for p in psutil.process_iter(["pid", "name", "cpu_percent", "memory_percent"]):
        try:
            procs.append(p.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    procs.sort(key=lambda x: x.get("cpu_percent", 0), reverse=True)

    os_release, kernel, uptime = _collect_os_info()

    result: dict[str, Any] = {
        "timestamp": datetime.now().isoformat(),
        "platform": platform.platform(),
        "os": "Linux" if IS_LINUX else ("Windows" if IS_WINDOWS else "Darwin"),
        "kernel": kernel,
        "os_release": os_release,
        "uptime": uptime,
        "cpu_percent": psutil.cpu_percent(interval=1),
        "cpu_count": psutil.cpu_count(),
        "ram_total_gb": round(vm.total / 1024**3, 2),
        "ram_used_percent": vm.percent,
        "swap_used_percent": sw.percent,
        "disks": disks,
        "top_processes": procs[:8],
    }

    if IS_LINUX or IS_MAC:
        try:
            result["load_avg"] = list(psutil.getloadavg())
        except AttributeError:
            pass

    result.update(_collect_platform_details())
    return result
