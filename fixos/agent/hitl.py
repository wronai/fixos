"""
Tryb Human-in-the-Loop (HITL) – użytkownik zatwierdza każdą akcję.
LLM proponuje, człowiek decyduje, skrypt wykonuje.

Refactored: Now uses HITLSession class for better modularity.
"""

from __future__ import annotations

from .hitl_session import (
    HITLSession,
    CmdResult,
    SYSTEM_PROMPT,
)

__all__ = [
    "run_hitl_session",
    "HITLSession",
    "CmdResult",
    "SYSTEM_PROMPT",
]


def run_hitl_session(diagnostics: dict, config, show_data: bool = True) -> None:
    """
    Run interactive HITL session with full transparency.
    
    This is a backward-compatible wrapper around HITLSession.
    For new code, use HITLSession directly.
    """
    session = HITLSession(
        diagnostics=diagnostics,
        config=config,
        show_data=show_data,
    )
    session.run()
