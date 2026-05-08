"""
File analysis diagnostics module.
Finds duplicate files, large files >200MB, media grouping,
and archive candidates for cleanup/organization.
"""

from typing import Any
from ._shared import _cmd, IS_LINUX, IS_WINDOWS, IS_MAC
from ...constants import (
    MAX_FILE_ANALYSIS_LARGE,
    MAX_FILE_ANALYSIS_DUPES,
    MAX_FILE_ANALYSIS_MEDIA,
    MIN_LARGE_FILE_ANALYSIS_MB,
)


def diagnose_files() -> dict[str, Any]:
    """
    Diagnostyka plików użytkownika.
    Znajduje:
    - Duże pliki (>200MB) z podziałem na kategorie
    - Duplikaty plików (ten sam hash/rozmiar)
    - Pliki medialne (ebooki, mp3, mp4, obrazy) do archiwizacji
    - Stare pliki nieużywane >90 dni
    - Propozycje organizacji i archiwizacji
    """
    result: dict[str, Any] = {}

    if IS_LINUX:
        result.update(_find_large_files())
        result.update(_find_duplicates())
        result.update(_find_media_files())
        result.update(_find_archive_candidates())
        result.update(_find_downloads_cleanup())

    elif IS_WINDOWS:
        result.update({
            "large_files": _cmd(
                'powershell -Command "Get-ChildItem -Path $HOME -Recurse '
                '-ErrorAction SilentlyContinue | Where-Object {$_.Length -gt 200MB} | '
                'Sort-Object Length -Descending | Select-Object FullName,'
                '@{N=\'SizeMB\';E={[math]::Round($_.Length/1MB,1)}} | '
                'Format-Table -AutoSize | Out-String -Width 200" 2>nul'
            ),
        })

    elif IS_MAC:
        result.update({
            "large_files": _cmd(
                f"find ~ -xdev -size +{MIN_LARGE_FILE_ANALYSIS_MB}M "
                "-not -path '*/Library/*' -not -path '*/.Trash/*' "
                f"2>/dev/null | head -{MAX_FILE_ANALYSIS_LARGE}"
            ),
        })

    return result


def _find_large_files() -> dict[str, Any]:
    """Find large files >200MB grouped by type."""
    return {
        # All large files sorted by size
        "large_files_all": _cmd(
            f"find ~ -xdev -size +{MIN_LARGE_FILE_ANALYSIS_MB}M "
            "-not -path '*/.cache/*' -not -path '*/.local/share/Trash/*' "
            "-not -path '*/node_modules/*' -not -path '*/.git/*' "
            "-not -path '*/.cargo/*' -not -path '*/.rustup/*' "
            "-not -path '*/.var/app/*' "
            "-printf '%s %T@ %p\\n' 2>/dev/null | "
            "sort -rn | "
            "awk '{size=$1/1048576; split($3,a,\"/\"); "
            "ext=substr(a[length(a)],index(a[length(a)],\".\")+1); "
            "printf \"%.0f MB | %s | %s\\n\", size, ext, $3}' | "
            f"head -{MAX_FILE_ANALYSIS_LARGE}"
        ),

        # Large videos (mp4, mkv, avi, mov, wmv, webm)
        "large_videos": _cmd(
            "find ~ -xdev \\( -iname '*.mp4' -o -iname '*.mkv' -o -iname '*.avi' "
            "-o -iname '*.mov' -o -iname '*.wmv' -o -iname '*.webm' "
            "-o -iname '*.flv' -o -iname '*.m4v' \\) "
            f"-size +{MIN_LARGE_FILE_ANALYSIS_MB}M "
            "-not -path '*/.cache/*' -not -path '*/.local/share/Trash/*' "
            "-printf '%s %p\\n' 2>/dev/null | sort -rn | "
            "awk '{printf \"%.0f MB | %s\\n\", $1/1048576, $2}' | "
            f"head -{MAX_FILE_ANALYSIS_MEDIA}"
        ),

        # Large archives (zip, tar.gz, rar, 7z, iso)
        "large_archives": _cmd(
            "find ~ -xdev \\( -iname '*.zip' -o -iname '*.tar.gz' -o -iname '*.tar.bz2' "
            "-o -iname '*.tar.xz' -o -iname '*.rar' -o -iname '*.7z' "
            "-o -iname '*.iso' -o -iname '*.img' \\) "
            "-size +100M "
            "-not -path '*/.cache/*' -not -path '*/.local/share/Trash/*' "
            "-printf '%s %p\\n' 2>/dev/null | sort -rn | "
            "awk '{printf \"%.0f MB | %s\\n\", $1/1048576, $2}' | "
            f"head -{MAX_FILE_ANALYSIS_MEDIA}"
        ),

        # Large disk images (vmdk, qcow2, vdi, vhd, raw)
        "large_disk_images": _cmd(
            "find ~ -xdev \\( -iname '*.vmdk' -o -iname '*.qcow2' -o -iname '*.vdi' "
            "-o -iname '*.vhd' -o -iname '*.raw' -o -iname '*.img' \\) "
            "-size +500M "
            "-not -path '*/.cache/*' "
            "-printf '%s %p\\n' 2>/dev/null | sort -rn | "
            "awk '{printf \"%.0f MB | %s\\n\", $1/1048576, $2}' | head -10"
        ),

        # Summary: total large files by category
        "large_files_summary": _cmd(
            "find ~ -xdev -size +200M "
            "-not -path '*/.cache/*' -not -path '*/.local/share/Trash/*' "
            "-not -path '*/node_modules/*' -not -path '*/.git/*' "
            "-not -path '*/.cargo/*' -not -path '*/.var/app/*' "
            "-printf '%s %f\\n' 2>/dev/null | "
            "awk '{"
            "ext=tolower(substr($2,index($2,\".\")+1)); "
            "size[ext]+=$1; count[ext]++} "
            "END {for(e in size) printf \"%d MB | %d plików | .%s\\n\", "
            "size[e]/1048576, count[e], e}' | sort -rn | head -15"
        ),
    }


def _find_duplicates() -> dict[str, Any]:
    """Find duplicate files by size+partial hash."""
    return {
        # Find potential duplicates by exact size match (fast pre-filter)
        "duplicate_candidates": _cmd(
            "find ~ -xdev -size +10M "
            "-not -path '*/.cache/*' -not -path '*/.local/share/Trash/*' "
            "-not -path '*/node_modules/*' -not -path '*/.git/*' "
            "-not -path '*/.cargo/*' -not -path '*/.var/app/*' "
            "-printf '%s %p\\n' 2>/dev/null | "
            "sort -n | "
            "awk '{if(prev_size==$1) {"
            "if(!printed_prev) {print prev_line; printed_prev=1}; "
            "printf \"%s %s\\n\", $1, $2} "
            "else {printed_prev=0}; "
            "prev_size=$1; prev_line=$0}' | "
            "awk '{printf \"%.1f MB | %s\\n\", $1/1048576, $2}' | "
            f"head -{MAX_FILE_ANALYSIS_DUPES}"
        ),

        # Verify with partial MD5 (first 4KB) for top candidates
        "duplicate_verified": _cmd(
            "find ~ -xdev -size +50M "
            "-not -path '*/.cache/*' -not -path '*/.local/share/Trash/*' "
            "-not -path '*/node_modules/*' -not -path '*/.git/*' "
            "-not -path '*/.cargo/*' -not -path '*/.var/app/*' "
            "-printf '%s %p\\n' 2>/dev/null | "
            "sort -n | "
            "awk '{if(prev==$1) arr[$1]=arr[$1]\"\\n\"$2; "
            "else if(arr[prev]) arr[prev]=prev_f\"\\n\"arr[prev]; "
            "prev=$1; prev_f=$2}' | "
            "head -20 || echo 'N/A'"
        ),

        # Use fdupes if available (most accurate)
        "fdupes_summary": _cmd(
            "fdupes -r -S ~/Documents ~/Downloads ~/Desktop 2>/dev/null | "
            "head -40 || echo 'fdupes niedostępny (dnf install fdupes)'"
        ),

        # rdfind summary
        "rdfind_summary": _cmd(
            "rdfind -dryrun true ~/Documents ~/Downloads 2>/dev/null | "
            "tail -5 || echo 'rdfind niedostępny (dnf install rdfind)'"
        ),
    }


def _find_media_files() -> dict[str, Any]:
    """Group media files for potential archival or cleanup."""
    return {
        # Ebooks (epub, pdf, mobi, azw3, djvu)
        "ebooks": _cmd(
            "find ~ -xdev \\( -iname '*.epub' -o -iname '*.mobi' "
            "-o -iname '*.azw3' -o -iname '*.djvu' -o -iname '*.fb2' \\) "
            "-not -path '*/.cache/*' -not -path '*/.local/share/Trash/*' "
            "-printf '%s %p\\n' 2>/dev/null | sort -rn | "
            "awk '{printf \"%.1f MB | %s\\n\", $1/1048576, $2}' | "
            f"head -{MAX_FILE_ANALYSIS_MEDIA}"
        ),
        "ebooks_summary": _cmd(
            "find ~ -xdev \\( -iname '*.epub' -o -iname '*.mobi' "
            "-o -iname '*.azw3' -o -iname '*.djvu' -o -iname '*.fb2' \\) "
            "-not -path '*/.cache/*' -not -path '*/.local/share/Trash/*' "
            "-printf '%s\\n' 2>/dev/null | "
            "awk '{s+=$1; c++} END {printf \"%d plików, %.1f MB łącznie\\n\", c, s/1048576}'"
        ),

        # PDF documents (separate from ebooks, often larger)
        "pdf_documents": _cmd(
            "find ~ -xdev -iname '*.pdf' "
            "-not -path '*/.cache/*' -not -path '*/.local/share/Trash/*' "
            "-printf '%s %p\\n' 2>/dev/null | sort -rn | "
            "awk '{printf \"%.1f MB | %s\\n\", $1/1048576, $2}' | head -20"
        ),
        "pdf_summary": _cmd(
            "find ~ -xdev -iname '*.pdf' "
            "-not -path '*/.cache/*' "
            "-printf '%s\\n' 2>/dev/null | "
            "awk '{s+=$1; c++} END {printf \"%d plików, %.1f MB łącznie\\n\", c, s/1048576}'"
        ),

        # Music (mp3, flac, ogg, m4a, wav, wma, aac)
        "music_files": _cmd(
            "find ~ -xdev \\( -iname '*.mp3' -o -iname '*.flac' -o -iname '*.ogg' "
            "-o -iname '*.m4a' -o -iname '*.wav' -o -iname '*.wma' -o -iname '*.aac' \\) "
            "-not -path '*/.cache/*' -not -path '*/.local/share/Trash/*' "
            "-printf '%s\\n' 2>/dev/null | "
            "awk '{s+=$1; c++} END {printf \"%d plików, %.1f MB łącznie\\n\", c, s/1048576}'"
        ),
        "music_locations": _cmd(
            "find ~ -xdev \\( -iname '*.mp3' -o -iname '*.flac' -o -iname '*.ogg' "
            "-o -iname '*.m4a' \\) "
            "-not -path '*/.cache/*' "
            "-printf '%h\\n' 2>/dev/null | sort | uniq -c | sort -rn | head -10"
        ),

        # Video files summary
        "video_summary": _cmd(
            "find ~ -xdev \\( -iname '*.mp4' -o -iname '*.mkv' -o -iname '*.avi' "
            "-o -iname '*.mov' -o -iname '*.wmv' -o -iname '*.webm' \\) "
            "-not -path '*/.cache/*' -not -path '*/.local/share/Trash/*' "
            "-printf '%s\\n' 2>/dev/null | "
            "awk '{s+=$1; c++} END {printf \"%d plików, %.1f MB łącznie\\n\", c, s/1048576}'"
        ),
        "video_locations": _cmd(
            "find ~ -xdev \\( -iname '*.mp4' -o -iname '*.mkv' -o -iname '*.avi' "
            "-o -iname '*.mov' \\) "
            "-not -path '*/.cache/*' "
            "-printf '%h\\n' 2>/dev/null | sort | uniq -c | sort -rn | head -10"
        ),

        # Images summary (large collections)
        "images_summary": _cmd(
            "find ~ -xdev \\( -iname '*.jpg' -o -iname '*.jpeg' -o -iname '*.png' "
            "-o -iname '*.gif' -o -iname '*.bmp' -o -iname '*.tiff' -o -iname '*.raw' "
            "-o -iname '*.cr2' -o -iname '*.nef' -o -iname '*.heic' \\) "
            "-not -path '*/.cache/*' -not -path '*/.local/share/Trash/*' "
            "-printf '%s\\n' 2>/dev/null | "
            "awk '{s+=$1; c++} END {printf \"%d plików, %.1f MB łącznie\\n\", c, s/1048576}'"
        ),
        "images_locations": _cmd(
            "find ~ -xdev \\( -iname '*.jpg' -o -iname '*.jpeg' -o -iname '*.png' "
            "-o -iname '*.raw' -o -iname '*.cr2' \\) "
            "-not -path '*/.cache/*' "
            "-printf '%h\\n' 2>/dev/null | sort | uniq -c | sort -rn | head -10"
        ),
    }


def _find_archive_candidates() -> dict[str, Any]:
    """Find files/directories that are good candidates for archival."""
    return {
        # Old files not accessed in 90+ days (large ones only)
        "stale_large_files": _cmd(
            "find ~ -xdev -size +100M -atime +90 "
            "-not -path '*/.cache/*' -not -path '*/.local/*' "
            "-not -path '*/.config/*' -not -path '*/node_modules/*' "
            "-not -path '*/.git/*' -not -path '*/.cargo/*' "
            "-not -path '*/.var/app/*' "
            "-printf '%Ab %Ad %AY | %s | %p\\n' 2>/dev/null | "
            "awk -F'|' '{gsub(/^[ ]+|[ ]+$/,\"\",$2); "
            "printf \"%s | %.0f MB | %s\\n\", $1, $2/1048576, $3}' | "
            f"head -{MAX_FILE_ANALYSIS_LARGE}"
        ),

        # Directories with media that could be archived to external drive
        "media_dirs_to_archive": _cmd(
            "du -sh ~/Videos ~/Music ~/Pictures ~/Documents/ebooks "
            "~/Audiobooks ~/Podcasts ~/Recordings "
            "2>/dev/null | sort -rh | head -10"
        ),

        # Old downloads (>30 days in Downloads folder)
        "old_downloads": _cmd(
            "find ~/Downloads -maxdepth 1 -mtime +30 "
            "-printf '%s %Td/%Tm/%TY %p\\n' 2>/dev/null | "
            "sort -rn | "
            "awk '{printf \"%.1f MB | %s | %s\\n\", $1/1048576, $2, $3}' | "
            "head -20"
        ),
        "old_downloads_total": _cmd(
            "find ~/Downloads -maxdepth 1 -mtime +30 "
            "-printf '%s\\n' 2>/dev/null | "
            "awk '{s+=$1; c++} END {printf \"%d plików, %.1f MB łącznie\\n\", c, s/1048576}'"
        ),

        # Trash size
        "trash_size": _cmd(
            "du -sh ~/.local/share/Trash/files 2>/dev/null || echo 'Kosz pusty'"
        ),
        "trash_count": _cmd(
            "find ~/.local/share/Trash/files -maxdepth 1 2>/dev/null | wc -l"
        ),
    }


def _find_downloads_cleanup() -> dict[str, Any]:
    """Analyze Downloads folder specifically."""
    return {
        # Downloads folder size
        "downloads_total_size": _cmd(
            "du -sh ~/Downloads 2>/dev/null || echo 'N/A'"
        ),

        # Downloads grouped by extension
        "downloads_by_type": _cmd(
            "find ~/Downloads -maxdepth 2 -type f "
            "-printf '%s %f\\n' 2>/dev/null | "
            "awk '{"
            "ext=tolower(substr($2,index($2,\".\")+1)); "
            "if(ext==$2) ext=\"brak\"; "
            "size[ext]+=$1; count[ext]++} "
            "END {for(e in size) printf \"%d MB | %d plików | .%s\\n\", "
            "size[e]/1048576, count[e], e}' | sort -rn | head -15"
        ),

        # Installer/package files that can be removed
        "installer_files": _cmd(
            "find ~/Downloads -maxdepth 2 \\( "
            "-iname '*.rpm' -o -iname '*.deb' -o -iname '*.AppImage' "
            "-o -iname '*.flatpakref' -o -iname '*.exe' -o -iname '*.msi' "
            "-o -iname '*.dmg' -o -iname '*.pkg' -o -iname '*.snap' "
            "-o -iname '*.run' -o -iname '*.sh' \\) "
            "-printf '%s %p\\n' 2>/dev/null | sort -rn | "
            "awk '{printf \"%.1f MB | %s\\n\", $1/1048576, $2}' | head -15"
        ),
    }
