"""
Ujednolicony klient LLM obsługujący wiele providerów przez OpenAI-compatible API.
Gemini, OpenAI, xAI, OpenRouter, Ollama – wszystkie przez ten sam interfejs.
"""

from __future__ import annotations

import time
from typing import Optional, Iterator

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

                content = response.choices[0].message.content or ""
                return content

            except Exception as e:
                _type = type(e).__name__
                _mod = type(e).__module__
                if _mod.startswith("openai") or _type in (
                    "AuthenticationError", "RateLimitError", "NotFoundError",
                    "APIConnectionError", "APITimeoutError",
                ):
                    if _type == "AuthenticationError":
                        raise LLMError(f"Błąd autoryzacji – sprawdź klucz API: {e}") from e
                    if _type == "RateLimitError":
                        wait = 10 * (attempt + 1)
                        print(f"\n  ⚠️  Rate limit – czekam {wait}s...")
                        time.sleep(wait)
                        if attempt == 2:
                            raise LLMError("Rate limit – przekroczono liczbę prób")
                        continue
                    if _type == "NotFoundError":
                        raise LLMError(
                            f"Model '{self.config.model}' nie istnieje dla providera "
                            f"'{self.config.provider}': {e}"
                        ) from e
                    if _type == "APIConnectionError":
                        if attempt == 2:
                            raise LLMError(f"Błąd połączenia z {self.config.base_url}: {e}") from e
                        time.sleep(5)
                        continue
                    if _type == "APITimeoutError":
                        if attempt == 2:
                            raise LLMError("Timeout połączenia z API")
                        time.sleep(5)
                        continue
                raise LLMError(f"Nieoczekiwany błąd API: {e}") from e

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
