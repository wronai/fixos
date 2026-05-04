"""
Ujednolicony klient LLM obsługujący wiele providerów przez OpenAI-compatible API.
Gemini, OpenAI, xAI, OpenRouter, Ollama – wszystkie przez ten sam interfejs.
"""

from __future__ import annotations

import json
import time
from typing import Optional, Iterator, Type

try:
    import openai
    _HAS_OPENAI = True
except ImportError:
    _HAS_OPENAI = False

from ..config import FixOsConfig


class LLMError(Exception):
    """Błąd komunikacji z LLM."""
    pass


class LLMClient:
    """
    Wrapper nad openai.OpenAI kompatybilny z wieloma providerami.
    Obsługuje retry, streaming i zbieranie tokenu zużycia.
    """

    def __init__(self, config: FixOsConfig):
        if not _HAS_OPENAI:
            raise LLMError("Zainstaluj openai: pip install openai")

        self.config = config
        self._client = openai.OpenAI(
            api_key=config.api_key or "ollama",  # ollama nie wymaga klucza
            base_url=config.base_url,
            timeout=120.0,
            max_retries=2,
        )
        self._total_tokens = 0

    def _handle_api_error(self, e: Exception, attempt: int) -> bool:
        """
        Handle a known openai API error.
        Returns True if the caller should retry, False never (raises on fatal errors).
        Raises LLMError for fatal conditions.
        """
        _type = type(e).__name__
        _mod = type(e).__module__
        if not (_mod.startswith("openai") or _type in (
            "AuthenticationError", "RateLimitError", "NotFoundError",
            "APIConnectionError", "APITimeoutError",
        )):
            raise LLMError(f"Nieoczekiwany błąd API: {e}") from e

        if _type == "AuthenticationError":
            raise LLMError(f"Błąd autoryzacji – sprawdź klucz API: {e}") from e
        if _type == "RateLimitError":
            wait = 10 * (attempt + 1)
            print(f"\n  ⚠️  Rate limit – czekam {wait}s...")
            time.sleep(wait)
            if attempt == 2:
                raise LLMError("Rate limit – przekroczono liczbę prób")
            return True
        if _type == "NotFoundError":
            raise LLMError(
                f"Model '{self.config.model}' nie istnieje dla providera "
                f"'{self.config.provider}': {e}"
            ) from e
        if _type in ("APIConnectionError", "APITimeoutError"):
            if attempt == 2:
                raise LLMError(
                    f"Błąd połączenia z {self.config.base_url}: {e}" if _type == "APIConnectionError"
                    else "Timeout połączenia z API"
                )
            time.sleep(5)
            return True
        raise LLMError(f"Nieoczekiwany błąd API: {e}") from e

    def chat(
        self,
        messages: list[dict],
        *,
        max_tokens: int = 3000,
        temperature: float = 0.3,
        stream: bool = False,
    ) -> str:
        """
        Wysyła wiadomości do LLM i zwraca odpowiedź jako string.
        Automatycznie retry przy rate limit / timeout.
        """
        for attempt in range(3):
            try:
                response = self._client.chat.completions.create(
                    model=self.config.model,
                    messages=messages,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    stream=False,
                )
                if response.usage:
                    self._total_tokens += response.usage.total_tokens
                return response.choices[0].message.content or ""
            except Exception as e:
                self._handle_api_error(e, attempt)

        raise LLMError("Nie udało się uzyskać odpowiedzi po 3 próbach")

    def chat_stream(
        self,
        messages: list[dict],
        *,
        max_tokens: int = 3000,
        temperature: float = 0.3,
    ) -> Iterator[str]:
        """Generator streamujący tokeny odpowiedzi."""
        try:
            stream = self._client.chat.completions.create(
                model=self.config.model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature,
                stream=True,
            )
            for chunk in stream:
                delta = chunk.choices[0].delta
                if delta and delta.content:
                    yield delta.content
        except Exception as e:
            raise LLMError(f"Błąd streamingu: {e}") from e

    @property
    def total_tokens(self) -> int:
        return self._total_tokens

    def chat_structured(
        self,
        messages: list[dict],
        response_model: Type,
        *,
        max_retries: int = 2,
        max_tokens: int = 3000,
        temperature: float = 0.1,
    ):
        """Wywołanie LLM z wymuszonym schematem JSON (Pydantic model).

        Args:
            messages: Lista wiadomości do LLM.
            response_model: Klasa Pydantic BaseModel definiująca schemat.
            max_retries: Ile razy ponowić przy błędzie parsowania.

        Returns:
            Instancja response_model z walidowanymi danymi.
        """
        schema = response_model.model_json_schema()
        schema_prompt = (
            "\n\n---\n"
            "CRITICAL: Respond ONLY with a valid JSON object matching "
            f"this schema:\n```json\n{json.dumps(schema, indent=2)}\n```\n"
            "No markdown, no explanation, no preamble. ONLY the JSON object."
        )

        augmented = [m.copy() for m in messages]
        augmented[-1] = {
            **augmented[-1],
            "content": augmented[-1]["content"] + schema_prompt,
        }

        for attempt in range(max_retries + 1):
            raw = self.chat(augmented, max_tokens=max_tokens, temperature=temperature)
            cleaned = self._extract_json(raw)
            try:
                return response_model.model_validate_json(cleaned)
            except Exception as e:
                if attempt < max_retries:
                    augmented.append({"role": "assistant", "content": raw})
                    augmented.append({
                        "role": "user",
                        "content": f"Invalid JSON. Error: {e}. "
                                   f"Please output ONLY valid JSON.",
                    })
                else:
                    raise ValueError(
                        f"LLM failed to produce valid schema after "
                        f"{max_retries + 1} attempts: {e}"
                    )

    @staticmethod
    def _extract_json(text: str) -> str:
        """Wyciągnij JSON z odpowiedzi LLM (obsługa markdown fences)."""
        text = text.strip()
        if text.startswith("```"):
            lines = text.split("\n")
            text = "\n".join(
                lines[1:-1] if lines[-1].startswith("```") else lines[1:]
            )
        return text.strip()

    def ping(self) -> bool:
        """Sprawdza czy API odpowiada (krótki test)."""
        try:
            self.chat(
                [{"role": "user", "content": "ping"}],
                max_tokens=5,
            )
            return True
        except LLMError:
            return False
