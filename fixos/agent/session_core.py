"""
Core session types and constants for HITL agent.
"""

import re
import time
from dataclasses import dataclass, field
from typing import List, Tuple

from ..constants import (
    MAX_SUMMARY_LENGTH,
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
    parts = re.split(r' && | \|\| |; ', cmd)
    
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
        if "--vacuum-" in normalized or "--flush" in normalized or "--rotate" in normalized:
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


def extract_fixes(reply: str) -> List[Tuple[str, str]]:
    """Extract (command, comment) pairs from LLM reply."""
    fixes: List[Tuple[str, str]] = []
    for m in re.finditer(
        r"\*\*Komenda:\*\*\s*`([^`]+)`(?:[^\n]*?\*\*Co robi:\*\*\s*(.+?))?(?=\n|$)",
        reply, re.IGNORECASE,
    ):
        cmd = m.group(1).strip()
        if cmd:
            fixes.append((cmd, (m.group(2) or "").strip()))
    if not fixes:
        for m in re.finditer(r"→\s*Fix:\s*`([^`]+)`", reply, re.IGNORECASE):
            fixes.append((m.group(1).strip(), ""))
    if not fixes:
        for m in re.finditer(r"\[(\d+)\][^`\n]+`([^`]+)`", reply):
            fixes.append((m.group(2).strip(), f"Fix #{m.group(1)}"))
    if not fixes:
        for m in re.finditer(r"EXEC:\s*`([^`]+)`", reply, re.IGNORECASE):
            fixes.append((m.group(1).strip(), ""))

    # Keep only actionable commands in menu; diagnostic-only commands are noise.
    filtered = [(cmd, comment) for cmd, comment in fixes if not _is_diagnostic_only_command(cmd)]
    return filtered


def extract_search_topic(llm_reply: str) -> str:
    """Extract search keywords from LLM reply."""
    tech_terms = re.findall(
        r"\b(sof-firmware|pipewire|alsa|thumbnails?|nautilus|"
        r"dnf|apt|systemctl|journalctl|codec|driver|nvidia|amd|"
        r"snd_hda|intel_sst|avs|wireplumber|pulseaudio|bluetooth|wifi)\b",
        llm_reply, re.IGNORECASE
    )
    if tech_terms:
        return " ".join(dict.fromkeys(tech_terms[:4]))
    first_sentence = llm_reply.split(".")[0][:MAX_SUMMARY_LENGTH]
    return first_sentence or "linux system diagnostics"
