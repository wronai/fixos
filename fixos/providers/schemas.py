"""
Pydantic schemas for structured LLM output.

Replaces fragile regex parsing of LLM responses with validated JSON schemas.
"""

from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class RiskLevel(str, Enum):
    SAFE = "safe"
    MODERATE = "moderate"
    DANGEROUS = "dangerous"


class FixSuggestion(BaseModel):
    """Pojedyncza sugestia naprawy od LLM."""

    command: str = Field(description="Komenda shell do wykonania")
    description: str = Field(description="Co robi ta komenda — po polsku")
    risk_level: RiskLevel = Field(description="Poziom ryzyka")
    requires_sudo: bool = Field(default=False)
    idempotent: bool = Field(
        default=False,
        description="Czy ponowne wykonanie jest bezpieczne",
    )
    check_command: Optional[str] = Field(
        default=None,
        description="Komenda sprawdzająca czy naprawa jest potrzebna",
    )
    rollback_command: Optional[str] = Field(
        default=None,
        description="Komenda cofająca zmianę",
    )


class LLMDiagnosticResponse(BaseModel):
    """Strukturalna odpowiedź LLM na dane diagnostyczne."""

    summary: str = Field(description="Podsumowanie problemów — 2-3 zdania")
    root_causes: list[str] = Field(description="Główne przyczyny problemów")
    suggestions: list[FixSuggestion] = Field(
        description="Lista sugestii napraw, od najbezpieczniejszej",
    )
    confidence: float = Field(
        ge=0.0,
        le=1.0,
        description="Pewność diagnozy (0.0 — zgadywanie, 1.0 — pewność)",
    )
    needs_more_info: list[str] = Field(
        default_factory=list,
        description="Jakie dodatkowe dane byłyby pomocne",
    )


class NLPIntent(BaseModel):
    """Rozpoznana intencja z polecenia NLP."""

    intent_type: str = Field(
        description="Typ intencji: scan, fix, cleanup, status, help, unknown"
    )
    target: Optional[str] = Field(
        default=None, description="Cel polecenia, np. 'docker', 'audio'"
    )
    parameters: dict = Field(default_factory=dict, description="Dodatkowe parametry")
    confidence: float = Field(ge=0.0, le=1.0, default=0.5)


class CommandValidation(BaseModel):
    """Wynik walidacji komendy przez LLM."""

    success: bool = Field(description="Czy komenda osiągnęła cel")
    interpretation: str = Field(description="Krótka interpretacja wyniku")
    user_intent_met: bool = Field(description="Czy oczekiwania użytkownika spełnione")
    suggestion: Optional[str] = Field(default=None, description="Opcjonalna sugestia")
