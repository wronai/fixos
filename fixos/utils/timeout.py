"""
Shared SessionTimeout exception and timeout handler for fixOS.

Eliminates duplication of SessionTimeout across autonomous.py, hitl.py, llm_shell.py.
"""

from __future__ import annotations


class SessionTimeout(Exception):
    """Wyjątek rzucany po przekroczeniu limitu czasu sesji."""
    pass


def timeout_handler(signum, frame):
    """Signal handler dla SIGALRM — rzuca SessionTimeout."""
    raise SessionTimeout("Sesja wygasła — przekroczono limit czasu")
