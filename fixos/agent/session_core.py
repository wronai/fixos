"""
Core session types and constants for HITL agent.
"""

import re
import time
from dataclasses import dataclass, field
from typing import List, Tuple

from ..constants import (
    MAX_SUMMARY_LENGTH,
    MAX_TECH_TERMS,
)


@dataclass
class CmdResult:
    """Result of executed command."""

    cmd: str
    comment: str
    ok: bool
    stdout: str
    stderr: str
    returncode: int
    skipped: bool = False
    timestamp: float = field(default_factory=time.time)


SYSTEM_PROMPT = """You are an expert Linux/Windows/macOS system diagnostics assistant.

You receive anonymized diagnostic data OR a user-described problem. Your tasks:

1. DIAGNOSE – identify ALL problems (🔴 critical → 🟡 important → 🟢 minor)
2. SOLUTIONS – for each problem provide an ACTIONABLE repair command with a brief explanation
3. FORMAT – always use this exact format:

━━━ DIAGNOZA ━━━
🔴 Problem 1: [description]
   **Komenda:** `command to run`
   **Co robi:** one-sentence explanation

🟡 Problem 2: [description]
   **Komenda:** `command`
   **Co robi:** explanation

IMPORTANT RULES:
- Commands in the action list must change/fix something, not only inspect state.
- Do NOT use read-only diagnostics as fixes (e.g. `df -h`, `free -h`, `ls`, `cat`, `grep`, `systemctl status`).
- If needed, mention diagnostics in explanation, but propose executable repair steps in `Komenda`.
- For package upgrades and heavy operations, provide the real fix command (e.g. `dnf upgrade -y`).
- When disk usage is critically high (>90%), ALWAYS propose cleanup commands FIRST.
- NEVER suggest package upgrades or installations BEFORE cleanup has freed sufficient space and been verified.

PACKAGE ANALYSIS rules (when "packages" data is present):
- For orphaned packages: propose `sudo dnf autoremove` or specific `sudo dnf remove <pkg>`.
- For debug/devel packages on desktop: propose `sudo dnf remove '*-debuginfo*'` or specific removals.
- For duplicate RPM+Flatpak apps: propose removing one version (prefer Flatpak for GUI apps).
- For unused Flatpak runtimes: propose `flatpak uninstall --unused`.
- For leaf packages not used in 90+ days: propose specific `sudo dnf remove <pkg>`.
- Always warn user about dependencies that will be removed.

STORAGE OPTIMIZATION rules (when "storage" data is present):
- If unallocated disk space exists: propose `sudo growpart` or `sudo lvextend + resize2fs/xfs_growfs`.
- For btrfs without compression: propose adding `compress=zstd:1` to fstab.
- For old btrfs snapshots: propose `sudo snapper delete <id>` for specific old snapshots.
- For swap/zram optimization: propose tuning swappiness or enabling zram.
- If fstrim.timer is disabled on SSD: propose `sudo systemctl enable --now fstrim.timer`.

FILE ANALYSIS rules (when "files" data is present):
- For large files >200MB: list them and propose review/deletion commands.
- For duplicate files: propose `fdupes -d` or `rdfind` commands for interactive dedup.
- For media files (ebooks, mp3, mp4, images): propose organizing/archiving commands:
  - `mkdir -p ~/Archive/{ebooks,muzyka,wideo,obrazy}` + `mv` commands.
  - For compression: `tar czf ~/Archive/ebooks.tar.gz ~/path/to/ebooks/`.
- For old downloads (>30 days): propose cleanup of ~/Downloads.
- For trash: propose `rm -rf ~/.local/share/Trash/files/*`.
- Always group suggestions by category (video, music, ebooks, archives, etc.).

Always end with:
━━━ DOSTĘPNE AKCJE ━━━
[1] Fix problem 1 – `command`
[2] Fix problem 2 – `command`
[A] Fix all automatically
[S] Skip all
[D] Describe a new problem
[Q] End session

IMPORTANT: Adapt commands to the detected OS (Linux/Windows/macOS).
"""


def _is_diagnostic_only_command(cmd: str) -> bool:
    """Return True if command is read-only and not a repair action."""
    # Split by common shell delimiters to check each part
    parts = re.split(r" && | \|\| |; ", cmd)

    # If any part of a compound command looks like a repair, the whole thing is actionable
    for part in parts:
        if not _is_part_diagnostic_only(part):
            return False
    return True


def _is_part_diagnostic_only(part: str) -> bool:
    """Helper for _is_diagnostic_only_command to check a single command part."""
    normalized = part.strip().lower()
    if normalized.startswith("sudo "):
        normalized = normalized[5:].strip()

    # Special case: diagnostic tools used for cleanup/repair
    if normalized.startswith("journalctl"):
        if (
            "--vacuum-" in normalized
            or "--flush" in normalized
            or "--rotate" in normalized
        ):
            return False

    diagnostic_prefixes = (
        "df ",
        "free ",
        "ls ",
        "cat ",
        "grep ",
        "find ",
        "which ",
        "whereis ",
        "journalctl",
        "dmesg",
        "uptime",
        "top ",
        "ps ",
        "systemctl status",
        "dnf check-update",
        "apt list --upgradable",
        "pacman -qu",
        "flatpak list",
        "snap list",
    )
    return normalized.startswith(diagnostic_prefixes)


def _extract_co_robi(text: str) -> str:
    """Extract 'Co robi:' comment from text following a command match."""
    m = re.search(r"\s*\*{0,2}Co robi:\*{0,2}\s*(.+?)(?:\n|$)", text, re.IGNORECASE)
    return m.group(1).strip() if m else ""


def _pattern_strict_bold(reply: str) -> List[Tuple[str, str]]:
    """Pattern 1: **Komenda:** `command` (strict: bold + backticks)."""
    fixes: List[Tuple[str, str]] = []
    for m in re.finditer(
        r"\*\*Komenda:\*\*\s*`([^`]+)`(?:[^\n]*?\*\*Co robi:\*\*\s*(.+?))?(?=\n|$)",
        reply,
        re.IGNORECASE,
    ):
        cmd = m.group(1).strip()
        if cmd:
            fixes.append((cmd, (m.group(2) or "").strip()))
    return fixes


def _pattern_backticks(reply: str) -> List[Tuple[str, str]]:
    """Pattern 2: Komenda: `command` (backticks, optional bold)."""
    fixes: List[Tuple[str, str]] = []
    for m in re.finditer(
        r"\*{0,2}Komenda:\*{0,2}\s*`([^`]+)`",
        reply,
        re.IGNORECASE,
    ):
        cmd = m.group(1).strip()
        if cmd:
            fixes.append((cmd, _extract_co_robi(reply[m.end() :])))
    return fixes


def _pattern_no_backticks(reply: str) -> List[Tuple[str, str]]:
    """Pattern 3: Komenda: command (no backticks — until next section)."""
    fixes: List[Tuple[str, str]] = []
    for m in re.finditer(
        r"\*{0,2}Komenda:\*{0,2}\s*"
        r"(.+?)"
        r"(?=\n\s*\*{0,2}Co robi:|\n[🔴🟡🟢]|\n━|\n─|\n\[[\dA-Z]|\Z)",
        reply,
        re.IGNORECASE | re.DOTALL,
    ):
        cmd = re.sub(r"\s*\n\s*", " ", m.group(1)).strip()
        if cmd:
            fixes.append((cmd, _extract_co_robi(reply[m.end() :])))
    return fixes


def _pattern_fallbacks(reply: str) -> List[Tuple[str, str]]:
    """Fallback patterns: → Fix, [N] command, EXEC."""
    fixes: List[Tuple[str, str]] = []
    for m in re.finditer(r"→\s*Fix:\s*`([^`]+)`", reply, re.IGNORECASE):
        fixes.append((m.group(1).strip(), ""))
    if not fixes:
        for m in re.finditer(r"\[(\d+)\][^`\n]+`([^`]+)`", reply):
            fixes.append((m.group(2).strip(), f"Fix #{m.group(1)}"))
    if not fixes:
        for m in re.finditer(r"EXEC:\s*`([^`]+)`", reply, re.IGNORECASE):
            fixes.append((m.group(1).strip(), ""))
    return fixes


def _deduplicate(fixes: List[Tuple[str, str]]) -> List[Tuple[str, str]]:
    """Remove diagnostic-only commands and deduplicate."""
    filtered = [
        (cmd, comment) for cmd, comment in fixes if not _is_diagnostic_only_command(cmd)
    ]
    seen: set[str] = set()
    unique: List[Tuple[str, str]] = []
    for cmd, comment in filtered:
        if cmd not in seen:
            seen.add(cmd)
            unique.append((cmd, comment))
    return unique


def extract_fixes(reply: str) -> List[Tuple[str, str]]:
    """Extract (command, comment) pairs from LLM reply."""
    fixes = (
        _pattern_strict_bold(reply)
        or _pattern_backticks(reply)
        or _pattern_no_backticks(reply)
        or _pattern_fallbacks(reply)
    )
    return _deduplicate(fixes)


def extract_search_topic(llm_reply: str) -> str:
    """Extract search keywords from LLM reply."""
    tech_terms = re.findall(
        r"\b(sof-firmware|pipewire|alsa|thumbnails?|nautilus|"
        r"dnf|apt|systemctl|journalctl|codec|driver|nvidia|amd|"
        r"snd_hda|intel_sst|avs|wireplumber|pulseaudio|bluetooth|wifi)\b",
        llm_reply,
        re.IGNORECASE,
    )
    if tech_terms:
        return " ".join(dict.fromkeys(tech_terms[:MAX_TECH_TERMS]))
    first_sentence = llm_reply.split(".")[0][:MAX_SUMMARY_LENGTH]
    return first_sentence or "linux system diagnostics"
