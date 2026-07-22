# backend/app/services/ai/ai_provider_manager.py
"""
AI Provider Manager

Coordinates AI providers with automatic fallback.
Providers are instantiated lazily — only when actually
invoked — so a missing API key for one provider doesn't
break the whole feature if the other is configured, and
so unit tests can mock generate_response() without ever
touching real credentials.

Module:
Phase 1 → Module 7 → AI Chat Assistant
"""

import time
import httpx

from app.enums.chat import AIProviderEnum
from app.services.ai.gemini_client import GeminiClient
from app.services.ai.openai_client import OpenAIClient


class AIProviderManager:
    def __init__(self):
        self._gemini: GeminiClient | None = None
        self._openai: OpenAIClient | None = None
        self.primary = AIProviderEnum.GEMINI
        self.fallback = AIProviderEnum.OPENAI

    @property
    def gemini(self) -> GeminiClient:
        """Lazily construct on first real use — not at manager init."""
        if self._gemini is None:
            self._gemini = GeminiClient()
        return self._gemini

    @property
    def openai(self) -> OpenAIClient:
        if self._openai is None:
            self._openai = OpenAIClient()
        return self._openai

    def generate_response(
        self,
        system_prompt: str,
        history: list[dict],
        user_message: str,
    ) -> dict:
        start = time.perf_counter()

        try:
            result = self.gemini.generate(system_prompt, history, user_message)
            return self._build_result(result, self.primary, start)

        except (httpx.TimeoutException, httpx.ConnectError, httpx.HTTPStatusError):
            result = self.openai.generate(system_prompt, history, user_message)
            return self._build_result(result, self.fallback, start)

    @staticmethod
    def _build_result(result: dict, provider: AIProviderEnum, start: float) -> dict:
        return {
            "text": result["text"],
            "tokens": result["tokens"],
            "provider": provider,
            "response_time_ms": int((time.perf_counter() - start) * 1000),
        }