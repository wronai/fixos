"""
Tryb autonomiczny – agent sam diagnozuje i naprawia system.
Wymaga jawnego włączenia: --mode autonomous lub AGENT_MODE=autonomous
Posiada mechanizmy bezpieczeństwa i limity.

Refactored: Now uses AutonomousSession class for better modularity.
"""

from __future__ import annotations

from .autonomous_session import (
    AutonomousSession,
    AgentReport,
    FixAction,
    SYSTEM_PROMPT_AUTONOMOUS,
    FORBIDDEN_COMMANDS,
    SUDO_PREFIXES,
)

__all__ = [
    "run_autonomous_session",
    "AutonomousSession",
    "AgentReport",
    "FixAction",
    "SYSTEM_PROMPT_AUTONOMOUS",
    "FORBIDDEN_COMMANDS",
    "SUDO_PREFIXES",
]


def run_autonomous_session(
    diagnostics: dict,
    config,
    show_data: bool = True,
    max_fixes: int = 10,
):
    """
    Uruchamia autonomiczny tryb agenta.

    This is a backward-compatible wrapper around AutonomousSession.
    For new code, use AutonomousSession directly.
    """
    session = AutonomousSession(
        diagnostics=diagnostics,
        config=config,
        show_data=show_data,
        max_fixes=max_fixes,
    )
    return session.run()
