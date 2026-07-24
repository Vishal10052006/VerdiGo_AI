# backend/app/services/ai/ai_provider_manager.py
"""
AI Provider Manager

Coordinates AI providers with automatic 3-tier fallback:
Gemini (primary) → OpenAI (secondary) → Groq (free-tier tertiary).

Providers are instantiated lazily — only when actually invoked —
so a missing/unfunded key for one tier doesn't break the whole
feature if a later tier is configured, and so unit tests can mock
generate_response() without ever touching real credentials.

Groq is kept as a permanent tertiary fallback (not just a dev
workaround): it's free, hosted, OpenAI-compatible, and gives
resilience if both paid providers are ever rate-limited or
unfunded — costs nothing to leave wired in for production.

Module:
Phase 1 → Module 7 → AI Chat Assistant
"""

import time
import httpx

from app.enums.chat import AIProviderEnum
from app.services.ai.gemini_client import GeminiClient
from app.services.ai.openai_client import OpenAIClient
from app.services.ai.groq_client import GroqClient


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

        # ------------------------------------------------------------
        # Tier 1 — Gemini
        # ------------------------------------------------------------
        try:
            result = self.gemini.generate(system_prompt, history, user_message)
            return self._build_result(result, self.primary, start)
        except (httpx.TimeoutException, httpx.ConnectError, httpx.HTTPStatusError, ValueError):
            pass  # ValueError covers "API key not configured" — fall through

        # ------------------------------------------------------------
        # Tier 2 — OpenAI
        # ------------------------------------------------------------
        try:
            result = self.openai.generate(system_prompt, history, user_message)
            return self._build_result(result, self.secondary, start)
        except (httpx.TimeoutException, httpx.ConnectError, httpx.HTTPStatusError, ValueError):
            pass

        # ------------------------------------------------------------
        # Tier 3 — Groq (free-tier fallback)
        # ------------------------------------------------------------
        result = self.groq.generate(system_prompt, history, user_message)
        return self._build_result(result, self.tertiary, start)

    @staticmethod
    def _build_result(result: dict, provider: AIProviderEnum, start: float) -> dict:
        return {
            "text": result["text"],
            "tokens": result["tokens"],
            "provider": provider,
            "response_time_ms": int((time.perf_counter() - start) * 1000),
        }