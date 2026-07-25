"""
AI Provider Manager

Coordinates AI providers with automatic 3-tier fallback:
Gemini (primary) → OpenAI (secondary) → Groq (free-tier tertiary).

Module:
Phase 1 → Module 7 → AI Chat Assistant
"""

import logging
import time
import httpx

from app.enums.chat import AIProviderEnum
from app.services.ai.gemini_client import GeminiClient
from app.services.ai.openai_client import OpenAIClient
from app.services.ai.groq_client import GroqClient

logger = logging.getLogger(__name__)


class AllAIProvidersUnavailableError(Exception):
    """
    Raised when every configured tier (Gemini -> OpenAI -> Groq) fails.

    Carries `attempts` — a list of (provider_name, error_type, error_message)
    tuples — so the caller (chat_service.py) can log or surface WHICH
    failure mode occurred (all misconfigured vs. all genuinely down vs.
    a mix), instead of collapsing everything into one generic
    "AI assistant unavailable" 503 with no diagnostic trail. Previously
    a bare `except Exception` in chat_service swallowed this distinction
    entirely — you couldn't tell from logs whether a farmer's message
    failed because GEMINI_API_KEY was blank or because Google's API
    was down.
    """

    def __init__(self, attempts: list[tuple[str, str, str]]):
        self.attempts = attempts
        summary = "; ".join(
            f"{provider}: {error_type} - {message}"
            for provider, error_type, message in attempts
        )
        super().__init__(f"All AI providers failed. {summary}")


class AIProviderManager:
    def __init__(self):
        self._gemini: GeminiClient | None = None
        self._openai: OpenAIClient | None = None
        self._groq: GroqClient | None = None

        self.primary = AIProviderEnum.GEMINI
        self.secondary = AIProviderEnum.OPENAI
        self.tertiary = AIProviderEnum.GROQ

    @property
    def gemini(self) -> GeminiClient:
        if self._gemini is None:
            self._gemini = GeminiClient()
        return self._gemini

    @property
    def openai(self) -> OpenAIClient:
        if self._openai is None:
            self._openai = OpenAIClient()
        return self._openai

    @property
    def groq(self) -> GroqClient:
        if self._groq is None:
            self._groq = GroqClient()
        return self._groq

    def generate_response(
        self,
        system_prompt: str,
        history: list[dict],
        user_message: str,
    ) -> dict:
        start = time.perf_counter()
        attempts: list[tuple[str, str, str]] = []

        # ------------------------------------------------------------
        # Tier 1 — Gemini
        # ------------------------------------------------------------
        try:
            result = self.gemini.generate(system_prompt, history, user_message)
            return self._build_result(result, self.primary, start)
        except (httpx.TimeoutException, httpx.ConnectError, httpx.HTTPStatusError, ValueError) as exc:
            attempts.append((self.primary.value, type(exc).__name__, str(exc)))

        # ------------------------------------------------------------
        # Tier 2 — OpenAI
        # ------------------------------------------------------------
        try:
            result = self.openai.generate(system_prompt, history, user_message)
            return self._build_result(result, self.secondary, start)
        except (httpx.TimeoutException, httpx.ConnectError, httpx.HTTPStatusError, ValueError) as exc:
            attempts.append((self.secondary.value, type(exc).__name__, str(exc)))

        # ------------------------------------------------------------
        # Tier 3 — Groq (free-tier fallback)
        #
        # FIX: previously this call was NOT wrapped in try/except at
        # all — if Groq also failed (or wasn't configured, raising
        # ValueError from GroqClient.__init__), the exception propagated
        # as a raw, untyped exception. chat_service.py's bare
        # `except Exception` caught it either way, but with zero
        # information about tiers 1 and 2 having already failed first.
        # ------------------------------------------------------------
        try:
            result = self.groq.generate(system_prompt, history, user_message)
            return self._build_result(result, self.tertiary, start)
        except (httpx.TimeoutException, httpx.ConnectError, httpx.HTTPStatusError, ValueError) as exc:
            attempts.append((self.tertiary.value, type(exc).__name__, str(exc)))

        # ------------------------------------------------------------
        # All three tiers exhausted — raise a typed exception carrying
        # the full attempt trail, and log it server-side at ERROR level
        # (chat_service still turns this into a clean farmer-facing 503,
        # but now you can actually diagnose it from logs/observability).
        # ------------------------------------------------------------
        logger.error(
            "All AI providers failed for a chat request. Attempts: %s",
            attempts,
        )
        raise AllAIProvidersUnavailableError(attempts)

    @staticmethod
    def _build_result(result: dict, provider: AIProviderEnum, start: float) -> dict:
        return {
            "text": result["text"],
            "tokens": result["tokens"],
            "provider": provider,
            "response_time_ms": int((time.perf_counter() - start) * 1000),
        }