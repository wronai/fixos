"""
Audio diagnostics module.
Checks ALSA, PipeWire, PulseAudio, SOF firmware.
"""

from typing import Any
from ._shared import _cmd
from ...constants import MAX_AUDIO_STATUS_LINES, MAX_AUDIO_RESULTS


def diagnose_audio() -> dict[str, Any]:
    """
    Diagnostyka dźwięku (ALSA/PipeWire/PulseAudio/SOF).
    Typowe problemy po aktualizacji system:
    - SOF (Sound Open Firmware) - brak karty dźwiękowej
    - PipeWire nie startuje / błędna konfiguracja
    - ALSA: brak urządzeń / mute
    - Intel HDA vs SOF konflikt sterowników
    """
    return {
        # System audio
        "pipewire_version": _cmd("pipewire --version 2>/dev/null | head -1"),
        "pipewire_status": _cmd(
            f"systemctl --user status pipewire.service --no-pager -l 2>/dev/null | head -{MAX_AUDIO_STATUS_LINES}"
        ),
        "pipewire_pulse_status": _cmd(
            f"systemctl --user status pipewire-pulse.service --no-pager -l 2>/dev/null | head -{MAX_AUDIO_STATUS_LINES}"
        ),
        "wireplumber_status": _cmd(
            f"systemctl --user status wireplumber.service --no-pager -l 2>/dev/null | head -{MAX_AUDIO_STATUS_LINES}"
        ),
        "pulseaudio_status": _cmd(
            "systemctl --user status pulseaudio.service --no-pager 2>/dev/null | head -10"
        ),
        # ALSA
        "alsa_cards": _cmd("cat /proc/asound/cards 2>/dev/null"),
        "alsa_devices": _cmd("aplay -l 2>/dev/null"),
        "alsa_capture": _cmd("arecord -l 2>/dev/null"),
        "alsa_mixer_controls": _cmd("amixer -c 0 scontents 2>/dev/null | head -40"),
        # PipeWire objects
        "pw_dump_audio": _cmd(
            f"pw-dump 2>/dev/null | python3 -c \"import sys,json; d=json.load(sys.stdin); [print(n.get('info',{{}}).get('props',{{}}).get('node.name','?'), '->', n.get('info',{{}}).get('props',{{}}).get('object.path','?')) for n in d if n.get('type','') == 'PipeWire:Interface:Node']\" 2>/dev/null | head -{MAX_AUDIO_RESULTS}"
        ),
        "pactl_info": _cmd("pactl info 2>/dev/null"),
        "pactl_sinks": _cmd(
            f"pactl list sinks 2>/dev/null | grep -E '(Name|State|Volume|Mute|Description)' | head -{MAX_AUDIO_RESULTS}"
        ),
        "pactl_sources": _cmd(
            f"pactl list sources 2>/dev/null | grep -E '(Name|State|Volume|Mute|Description)' | head -{MAX_AUDIO_RESULTS}"
        ),
        # Kernel / SOF (Sound Open Firmware) - kluczowy dla Lenovo/Intel
        "sof_firmware": _cmd("ls /lib/firmware/intel/sof* 2>/dev/null | head -10"),
        "sof_modules": _cmd(
            "lsmod | grep -E '(sof|snd_hda|intel_sst|avs)' 2>/dev/null"
        ),
        "kernel_audio_dmesg": _cmd(
            f"dmesg | grep -iE '(snd|audio|alsa|hda|sof|codec|speaker|mic|hdmi)' | tail -{MAX_AUDIO_RESULTS}"
        ),
        "hdaudio_codec": _cmd(
            f"cat /proc/asound/card*/codec* 2>/dev/null | grep -E '(Codec|Address|Vendor)' | head -{MAX_AUDIO_STATUS_LINES}"
        ),
        # Lenovo-specific
        "lenovo_ideapad": _cmd("lsmod | grep -i ideapad 2>/dev/null"),
        "thinkpad_acpi": _cmd("lsmod | grep -i thinkpad_acpi 2>/dev/null"),
        "yoga_udev": _cmd("udevadm info /sys/class/sound/card0 2>/dev/null | head -20"),
        # Mikrofon
        "mic_privacy_switch": _cmd(
            "cat /sys/bus/platform/devices/*/PNP0C14*/wmi_bus/*/mic_mute 2>/dev/null || echo 'N/A'"
        ),
        "mic_input_mute": _cmd("amixer get Capture 2>/dev/null | tail -3"),
        # Pakiety audio
        "audio_packages": _cmd(
            "rpm -qa 2>/dev/null | grep -E '(alsa|pipewire|pulseaudio|sof-firmware|wireplumber|jack)' | sort"
        ),
        "sof_firmware_pkg": _cmd("rpm -q sof-firmware 2>/dev/null"),
        "alsa_firmware_pkg": _cmd("rpm -q alsa-firmware alsa-ucm-utils 2>/dev/null"),
    }
