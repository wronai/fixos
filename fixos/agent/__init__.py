"""Agent module for fixOS - HITL and Autonomous session management."""

import time
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .hitl_session import HITLSession
    from .autonomous_session import AutonomousSession


def get_remaining_time(session: "HITLSession | AutonomousSession") -> int:
    """Calculate remaining session time in seconds."""
    start_time = getattr(session, 'start_ts', None) or getattr(session, 'start_time')
    return session.config.session_timeout - int(time.time() - start_time)


from .hitl import run_hitl_session, HITLSession
from .autonomous import run_autonomous_session
from .autonomous_session import (
    AutonomousSession,
    AgentReport,
    FixAction,
    SYSTEM_PROMPT_AUTONOMOUS,
    FORBIDDEN_COMMANDS,
    SUDO_PREFIXES,
)

__all__ = [
    "run_hitl_session",
    "HITLSession",
    "run_autonomous_session",
    "AutonomousSession",
    "AgentReport",
    "FixAction",
    "SYSTEM_PROMPT_AUTONOMOUS",
    "FORBIDDEN_COMMANDS",
    "SUDO_PREFIXES",
    "get_remaining_time",
]
