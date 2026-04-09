"""
Hardware diagnostics module.
Checks laptop/desktop hardware: ACPI, camera, touchpad, DMI.
"""

from typing import Any
from ._shared import _cmd


def diagnose_hardware() -> dict[str, Any]:
    """Diagnostyka sprzętu laptopa/desktopa (ACPI, kamera, touchpad, DMI)."""
    return {
        # Identyfikacja
        "dmi_product": _cmd("cat /sys/class/dmi/id/product_name 2>/dev/null"),
        "dmi_vendor": _cmd("cat /sys/class/dmi/id/sys_vendor 2>/dev/null"),
        "dmi_board": _cmd("cat /sys/class/dmi/id/board_name 2>/dev/null"),
        "bios_version": _cmd("cat /sys/class/dmi/id/bios_version 2>/dev/null"),
        "bios_date": _cmd("cat /sys/class/dmi/id/bios_date 2>/dev/null"),
        "cpu_model": _cmd("grep 'model name' /proc/cpuinfo | head -1 | cut -d: -f2 | xargs"),

        # Grafika
        "gpu_info": _cmd("lspci -nn 2>/dev/null | grep -iE '(vga|3d|display)'"),
        "drm_drivers": _cmd("ls /sys/class/drm/ 2>/dev/null"),
        "wayland_display": _cmd("echo $WAYLAND_DISPLAY $XDG_SESSION_TYPE 2>/dev/null"),

        # Touchpad / Input
        "input_devices": _cmd("cat /proc/bus/input/devices 2>/dev/null | grep -E '(Name|Handlers)' | head -20"),
        "touchpad_driver": _cmd("lsmod | grep -E '(i2c_hid|hid_multitouch|psmouse|libinput)'"),

        # Kamera
        "camera_devices": _cmd("ls /dev/video* 2>/dev/null"),
        "camera_v4l": _cmd("v4l2-ctl --list-devices 2>/dev/null | head -10"),

        # ACPI / Power
        "acpi_events": _cmd("acpi -a -b -t 2>/dev/null"),
        "battery_status": _cmd("upower -i $(upower -e | grep battery) 2>/dev/null | grep -E '(state|percentage|time|energy)'"),
        "power_profile": _cmd("powerprofilesctl get 2>/dev/null || echo 'power-profiles-daemon niedostępny'"),
        "tlp_status": _cmd("tlp-stat -s 2>/dev/null | head -5 || echo 'TLP nie zainstalowany'"),

        # Czujniki temperatury
        "sensors": _cmd("sensors 2>/dev/null || echo 'lm_sensors niedostępny (dnf install lm_sensors)'"),
    }
