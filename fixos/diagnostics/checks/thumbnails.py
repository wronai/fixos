"""
Thumbnails diagnostics module.
Checks file preview functionality in file managers.
"""

from typing import Any
from ._shared import _cmd


def diagnose_thumbnails() -> dict[str, Any]:
    """
    Diagnostyka podglądów plików (thumbnails) w system.
    Typowe problemy po aktualizacji:
    - Brak thumbnailerów (totem-video-thumbnailer, evince-thumbnailer)
    - Uszkodzony cache miniaturek
    - Nautilus/Thunar/Dolphin – wyłączone podglądy
    - Brak codec-ów GStreamer
    - Brakujące uprawnienia ~/.cache/thumbnails
    """
    return {
        # Desktop Environment / File manager
        "desktop_env": _cmd("echo $XDG_CURRENT_DESKTOP 2>/dev/null || echo 'nieznane'"),
        "file_manager": _cmd("ps aux 2>/dev/null | grep -E '(nautilus|thunar|dolphin|nemo|pcmanfm|caja)' | grep -v grep | awk '{print $11}' | head -3"),
        "nautilus_version": _cmd("nautilus --version 2>/dev/null"),
        "thunar_version": _cmd("thunar --version 2>/dev/null | head -1"),
        "dolphin_version": _cmd("dolphin --version 2>/dev/null | head -1"),

        # Thumbnailer binaries
        "thumbnailers_installed": _cmd("ls /usr/bin/*thumb* /usr/lib/*thumb* /usr/lib64/*thumb* 2>/dev/null"),
        "gdk_pixbuf_loaders": _cmd("gdk-pixbuf-query-loaders 2>/dev/null | grep -c 'loader' || echo '0'"),
        "thumbnailer_configs": _cmd("ls /usr/share/thumbnailers/ 2>/dev/null"),
        "local_thumbnailers": _cmd("ls ~/.local/share/thumbnailers/ 2>/dev/null"),

        # Cache stanu
        "thumbnail_cache_size": _cmd("du -sh ~/.cache/thumbnails/ 2>/dev/null || echo 'brak cache'"),
        "thumbnail_cache_count": _cmd("find ~/.cache/thumbnails/ -name '*.png' 2>/dev/null | wc -l"),
        "thumbnail_cache_perms": _cmd("ls -la ~/.cache/ 2>/dev/null | grep thumb"),
        "thumbnail_fail_files": _cmd("find ~/.cache/thumbnails/fail/ -name '*.png' 2>/dev/null | wc -l"),

        # GStreamer (podglądy wideo)
        "gst_plugins": _cmd("gst-inspect-1.0 2>/dev/null | grep -cE '(video|thumbnailer)' || echo '0 (gstreamer brak)'"),
        "gst_bad_good": _cmd("rpm -qa 2>/dev/null | grep -i 'gstreamer1-plugins' | sort"),

        # Pakiety thumbnailerów
        "thumbnailer_packages": _cmd(
            "rpm -qa 2>/dev/null | grep -iE '(thumbnailer|ffmpegthumbnailer|totem-nautilus|evince-thumbnailer|raw-thumbnailer|gnome-epub-thumbnailer)' | sort"
        ),
        "ffmpegthumbnailer": _cmd("ffmpegthumbnailer --version 2>/dev/null || echo 'ffmpegthumbnailer nie zainstalowany'"),
        "totem_thumb": _cmd("which totem-video-thumbnailer 2>/dev/null || echo 'totem-video-thumbnailer nie znaleziony'"),

        # GNOME/GTK ustawienia
        "gsettings_thumbnails": _cmd(
            "gsettings get org.gnome.nautilus.preferences show-image-thumbnails 2>/dev/null; "
            "gsettings get org.gnome.nautilus.preferences thumbnail-limit 2>/dev/null"
        ),
        "gsettings_show_previews": _cmd(
            "gsettings get org.gnome.nautilus.icon-view default-zoom-level 2>/dev/null"
        ),

        # Problemy z uprawnieniami
        "xdg_cache_dir": _cmd("echo $XDG_CACHE_HOME 2>/dev/null || echo '~/.cache (domyślnie)'"),
    }
