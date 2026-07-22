# backend/app/services/ai/openai_client.py
import httpx
from app.config.settings import settings


class OpenAIClient:
    """Thin client for OpenAI chat completions (fallback provider)."""

    def __init__(self):
        if not settings.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is not configured.")
        self.api_key = settings.OPENAI_API_KEY
        self.base_url = settings.OPENAI_BASE_URL  # https://api.openai.com/v1
        self.model = settings.OPENAI_MODEL          # gpt-4o-mini
        self.timeout = settings.AI_REQUEST_TIMEOUT

    def generate(self, system_prompt: str, history: list[dict], user_message: str) -> dict:
        endpoint = f"{self.base_url}/chat/completions"

        messages = [{"role": "system", "content": system_prompt}]
        messages += [{"role": m["role"], "content": m["content"]} for m in history]
        messages.append({"role": "user", "content": user_message})

        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.4,
            "max_tokens": 512,
        }

        headers = {"Authorization": f"Bearer {self.api_key}"}

        with httpx.Client(timeout=self.timeout) as client:
            response = client.post(endpoint, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()

        text = data["choices"][0]["message"]["content"]
        tokens = data.get("usage", {}).get("total_tokens", 0)

        return {"text": text, "tokens": tokens}