# backend/app/services/ai/gemini_client.py
import httpx
from app.config.settings import settings


class GeminiClient:
    """Thin client for Google Gemini generateContent API."""

    def __init__(self):
        if not settings.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is not configured.")
        self.api_key = settings.GEMINI_API_KEY
        self.base_url = settings.GEMINI_BASE_URL  # e.g. https://generativelanguage.googleapis.com/v1beta
        self.model = settings.GEMINI_MODEL          # e.g. "gemini-1.5-flash"
        self.timeout = settings.AI_REQUEST_TIMEOUT

    def generate(self, system_prompt: str, history: list[dict], user_message: str) -> dict:
        endpoint = f"{self.base_url}/models/{self.model}:generateContent?key={self.api_key}"

        contents = [
            {"role": "user" if m["role"] == "user" else "model", "parts": [{"text": m["content"]}]}
            for m in history
        ]
        contents.append({"role": "user", "parts": [{"text": user_message}]})

        payload = {
            "system_instruction": {"parts": [{"text": system_prompt}]},
            "contents": contents,
            "generationConfig": {
                "temperature": 0.4,
                "maxOutputTokens": 512,
            },
        }

        with httpx.Client(timeout=self.timeout) as client:
            response = client.post(endpoint, json=payload)
            response.raise_for_status()
            data = response.json()

        text = data["candidates"][0]["content"]["parts"][0]["text"]
        tokens = data.get("usageMetadata", {}).get("totalTokenCount", 0)

        return {"text": text, "tokens": tokens}