"""
Core session types and constants for HITL agent.
"""

import re
import time
from dataclasses import dataclass, field
from typing import List, Tuple

from ..constants import (
    COMMAND_PREFIX_LENGTH,
    MAX_OUTPUT_LINES,
    CLEANUP_TIMEOUT_ESTIMATE,
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
2. SOLUTIONS – for each problem provide a CONCRETE command with a brief explanation
3. FORMAT – always use this exact format:

━━━ DIAGNOZA ━━━
🔴 Problem 1: [description]
   **Komenda:** `command to run`
   **Co robi:** one-sentence explanation

🟡 Problem 2: [description]
   **Komenda:** `command`
   **Co robi:** explanation

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
    return fixes


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
