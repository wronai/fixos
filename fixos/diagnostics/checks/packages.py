"""
Package environment diagnostics module.
Analyzes installed applications, finds unused packages,
orphaned dependencies, and proposes cleanup.
"""

from typing import Any
from ._shared import _cmd, IS_LINUX, IS_WINDOWS, IS_MAC
from ...constants import (
    MAX_ORPHANED_PACKAGES,
    MAX_PKG_RECENTLY_INSTALLED,
    MAX_PKG_LARGE_INSTALLED,
    MAX_PKG_LEAF_UNUSED,
    MAX_PKG_FLATPAK_UNUSED,
)


def diagnose_packages() -> dict[str, Any]:
    """
    Diagnostyka zainstalowanych pakietów i środowiska.
    Znajduje:
    - Osierocone pakiety (orphans) – zależności bez rodzica
    - Duże pakiety, które można usunąć
    - Pakiety leaf (liście) – bez zależnych, potencjalnie zbędne
    - Nieużywane flatpaki/snapy
    - Duplikaty (RPM + Flatpak tej samej aplikacji)
    - Ostatnio instalowane pakiety (do przeglądu)
    - Autoremove candidates
    """
    result: dict[str, Any] = {}

    if IS_LINUX:
        result.update(_diagnose_rpm_dnf())
        result.update(_diagnose_flatpak())
        result.update(_diagnose_snap())
        result.update(_diagnose_duplicates())
        result.update(_diagnose_desktop_apps())

    elif IS_WINDOWS:
        result.update(
            {
                "installed_apps": _cmd(
                    'powershell -Command "Get-ItemProperty HKLM:\\Software\\Microsoft\\Windows\\'
                    "CurrentVersion\\Uninstall\\* | Select-Object DisplayName,EstimatedSize,"
                    "InstallDate | Sort-Object EstimatedSize -Descending | Select-Object -First 30 "
                    '| Format-Table -AutoSize" 2>nul'
                ),
            }
        )

    elif IS_MAC:
        result.update(
            {
                "brew_list": _cmd("brew list --formula 2>/dev/null | head -50"),
                "brew_cask_list": _cmd("brew list --cask 2>/dev/null | head -50"),
                "brew_autoremove_dry": _cmd("brew autoremove --dry-run 2>/dev/null"),
                "brew_cleanup_dry": _cmd(
                    "brew cleanup --dry-run 2>/dev/null | tail -20"
                ),
                "applications": _cmd("ls /Applications/ 2>/dev/null"),
            }
        )

    return result


def _diagnose_rpm_dnf() -> dict[str, Any]:
    """RPM/DNF package analysis for Fedora/RHEL."""
    return {
        # Orphaned packages – dependencies with no parent
        "orphaned_packages": _cmd(
            f"dnf repoquery --extras --quiet 2>/dev/null | head -{MAX_ORPHANED_PACKAGES} || "
            f"package-cleanup --orphans 2>/dev/null | head -{MAX_ORPHANED_PACKAGES} || echo 'N/A'"
        ),
        # Autoremove candidates – unneeded dependencies
        "autoremove_candidates": _cmd(
            f"dnf autoremove --assumeno 2>/dev/null | "
            f"grep -E '^ ' | head -{MAX_ORPHANED_PACKAGES} || echo 'N/A'"
        ),
        "autoremove_count": _cmd(
            "dnf autoremove --assumeno 2>/dev/null | grep -cE '^ ' || echo '0'"
        ),
        # Leaf packages – installed but nothing depends on them
        "leaf_packages": _cmd(
            f"dnf repoquery --installed --whatrequires='' 2>/dev/null | head -{MAX_PKG_LEAF_UNUSED} || "
            f"dnf leaves 2>/dev/null | head -{MAX_PKG_LEAF_UNUSED} || echo 'N/A'"
        ),
        # Large installed packages sorted by size
        "large_packages": _cmd(
            f"rpm -qa --queryformat '%{{SIZE}} %{{NAME}}-%{{VERSION}}\\n' 2>/dev/null | "
            f"sort -rn | head -{MAX_PKG_LARGE_INSTALLED}"
        ),
        # Recently installed (last 30 days) – user review
        "recently_installed": _cmd(
            f"dnf history list --reverse 2>/dev/null | tail -{MAX_PKG_RECENTLY_INSTALLED} || echo 'N/A'"
        ),
        "recently_installed_packages": _cmd(
            f"rpm -qa --queryformat '%{{INSTALLTIME:date}} %{{NAME}}\\n' 2>/dev/null | "
            f"sort -r | head -{MAX_PKG_RECENTLY_INSTALLED}"
        ),
        # Old kernels that can be removed
        "installed_kernels": _cmd("rpm -q kernel kernel-core 2>/dev/null | sort -V"),
        "running_kernel": _cmd("uname -r"),
        # Package groups installed
        "installed_groups": _cmd(
            "dnf group list --installed 2>/dev/null | head -20 || echo 'N/A'"
        ),
        # Total package count
        "total_rpm_count": _cmd("rpm -qa 2>/dev/null | wc -l"),
        "total_rpm_size": _cmd(
            "rpm -qa --queryformat '%{SIZE}\\n' 2>/dev/null | "
            "awk '{s+=$1} END {printf \"%.1f GB\\n\", s/1024/1024/1024}'"
        ),
        # Debug/devel packages (often unnecessary on desktop)
        "debug_packages": _cmd(
            "rpm -qa 2>/dev/null | grep -E '(-debug|-debuginfo|-debugsource)' | wc -l"
        ),
        "debug_packages_list": _cmd(
            "rpm -qa 2>/dev/null | grep -E '(-debug|-debuginfo|-debugsource)' | head -20"
        ),
        "devel_packages": _cmd("rpm -qa 2>/dev/null | grep -E '(-devel)$' | head -30"),
        "devel_packages_count": _cmd("rpm -qa 2>/dev/null | grep -cE '(-devel)$'"),
    }


def _diagnose_flatpak() -> dict[str, Any]:
    """Flatpak analysis."""
    return {
        "flatpak_list": _cmd(
            f"flatpak list --app --columns=name,application,size 2>/dev/null | "
            f"head -{MAX_PKG_FLATPAK_UNUSED} || echo 'Flatpak niedostępny'"
        ),
        "flatpak_runtimes": _cmd(
            "flatpak list --runtime --columns=name,application,size 2>/dev/null | head -30 || echo 'N/A'"
        ),
        "flatpak_unused_runtimes": _cmd(
            "flatpak uninstall --unused --assumeyes --dry-run 2>/dev/null || echo 'N/A'"
        ),
        "flatpak_app_count": _cmd("flatpak list --app 2>/dev/null | wc -l || echo '0'"),
        "flatpak_total_size": _cmd("du -sh /var/lib/flatpak 2>/dev/null || echo 'N/A'"),
    }


def _diagnose_snap() -> dict[str, Any]:
    """Snap analysis."""
    return {
        "snap_list": _cmd(
            "snap list 2>/dev/null | head -30 || echo 'Snap niedostępny'"
        ),
        "snap_disabled": _cmd(
            "snap list --all 2>/dev/null | grep 'disabled' | head -20 || echo 'N/A'"
        ),
        "snap_total_size": _cmd("du -sh /snap 2>/dev/null || echo 'N/A'"),
    }


def _diagnose_duplicates() -> dict[str, Any]:
    """Find apps available via both RPM and Flatpak."""
    return {
        "duplicate_rpm_flatpak": _cmd(
            "comm -12 "
            "<(rpm -qa --queryformat '%{NAME}\\n' 2>/dev/null | "
            "sed 's/-[0-9].*//' | sort -u) "
            "<(flatpak list --app --columns=application 2>/dev/null | "
            "awk -F. '{print tolower($NF)}' | sort -u) "
            "2>/dev/null | head -20 || echo 'N/A'"
        ),
    }


def _diagnose_desktop_apps() -> dict[str, Any]:
    """Analyze .desktop files to find GUI apps and their usage."""
    return {
        # All desktop apps with their packages
        "desktop_apps_count": _cmd(
            "find /usr/share/applications -name '*.desktop' 2>/dev/null | wc -l"
        ),
        "desktop_apps_with_packages": _cmd(
            "for f in /usr/share/applications/*.desktop; do "
            "name=$(grep -m1 '^Name=' \"$f\" 2>/dev/null | cut -d= -f2); "
            'pkg=$(rpm -qf "$f" 2>/dev/null | head -1); '
            '[ -n "$name" ] && echo "$pkg | $name"; '
            "done 2>/dev/null | sort | head -50"
        ),
        # Recently used apps (from GNOME tracker / zeitgeist)
        "recently_used_apps": _cmd(
            "find ~/.local/share/recently-used.xbel -newer /dev/null 2>/dev/null && "
            "grep -oP 'exec=\"\\K[^\"]+' ~/.local/share/applications/mimeinfo.cache 2>/dev/null | "
            "sort -u | head -30 || echo 'N/A'"
        ),
        # Apps with no recent activity (based on binary access time)
        "stale_desktop_binaries": _cmd(
            "for f in /usr/share/applications/*.desktop; do "
            "exec=$(grep -m1 '^Exec=' \"$f\" 2>/dev/null | cut -d= -f2 | cut -d' ' -f1); "
            'bin=$(which "$exec" 2>/dev/null); '
            'if [ -n "$bin" ]; then '
            "atime=$(stat -c '%X' \"$bin\" 2>/dev/null); "
            "now=$(date +%s); "
            "days=$(( (now - atime) / 86400 )); "
            '[ $days -gt 90 ] && echo "${days}d | $exec"; '
            "fi; done 2>/dev/null | sort -rn | head -30"
        ),
    }
