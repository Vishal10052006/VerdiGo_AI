"""
Groq Client

Free-tier dev/testing provider. OpenAI-compatible API format,
so this mirrors OpenAIClient exactly — just a different base_url
and model. Swap GROQ_API_KEY in for real testing without billing.
"""

import httpx
from app.config.settings import settings


class GroqClient:
    def __init__(self):
        if not settings.GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY is not configured.")
        self.api_key = settings.GROQ_API_KEY
        self.base_url = "https://api.groq.com/openai/v1"
        self.model = "llama-3.3-70b-versatile"
        self.timeout = settings.AI_REQUEST_TIMEOUT

    def generate(self, system_prompt: str, history: list[dict], user_message: str) -> dict:
        endpoint = f"{self.base_url}/chat/completions"

        messages = [{"role": "system", "content": system_prompt}]
        messages += [{"role": m["role"], "content": m["content"]} for m in history]
        messages.append({"role": "user", "content": user_message})

        payload = {"model": self.model, "messages": messages, "temperature": 0.4, "max_tokens": 512}
        headers = {"Authorization": f"Bearer {self.api_key}"}

        with httpx.Client(timeout=self.timeout) as client:
            response = client.post(endpoint, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()

        text = data["choices"][0]["message"]["content"]
        tokens = data.get("usage", {}).get("total_tokens", 0)
        return {"text": text, "tokens": tokens}