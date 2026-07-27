"""
Groq Vision Client

Free-tier vision provider — replaces Gemini Vision, which has
zero free quota allocated on this Google Cloud project (confirmed
via 429 RESOURCE_EXHAUSTED with limit: 0 on all free-tier metrics,
2026-07-27). Groq's Llama-4 Scout model supports multimodal input
on the free tier via the same OpenAI-compatible chat/completions
endpoint GroqClient already uses for text chat.

Module: Phase 1 → Module 8 → Disease Detection
Author: VerdiGO Backend Team
"""

import base64
import json

import httpx

from app.config.settings import settings


DISEASE_ANALYSIS_PROMPT = """You are an expert plant pathologist analyzing a crop image for an Indian smallholder farmer.

Look at the image carefully and respond with ONLY a JSON object (no markdown, no prose, no code fences) matching exactly this schema:

{
  "is_healthy": boolean,
  "disease_name": string | null,
  "confidence": number,
  "severity": "none" | "low" | "moderate" | "high" | "critical",
  "treatment": string[],
  "prevention_tips": string[],
  "crop_identified": string | null
}

Rules:
- If the image is not a plant/crop/leaf at all, set is_healthy=false, disease_name="Not a plant image", confidence=0, severity="none".
- Never recommend specific chemical dosages — say "consult your local Krishi Vigyan Kendra (KVK) for exact dosage" instead.
- Be conservative with confidence: only go above 80 if visual symptoms are unambiguous.
- Keep each treatment/prevention string under 15 words, farmer-friendly language, no jargon.
- Return ONLY the JSON object. No other text.
"""


class GroqVisionClient:
    """
    Client for Groq's OpenAI-compatible multimodal chat completions API.
    """

    def __init__(self):
        if not settings.GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY is not configured.")

        self.api_key = settings.GROQ_API_KEY
        self.base_url = "https://api.groq.com/openai/v1"
        # llama-4-scout-17b-16e-instruct was deprecated by Groq (June 2026).
        # qwen/qwen3.6-27b is the current multimodal (vision) model on
        # Groq's free/dev tier as of July 2026. Groq's vision lineup
        # changes frequently — if this breaks again, check
        # https://console.groq.com/docs/vision for the current model.
        self.model = settings.GROQ_VISION_MODEL
        self.timeout = settings.AI_REQUEST_TIMEOUT

    def analyze_image(self, image_bytes: bytes, mime_type: str) -> dict:
        """
        Send an image to Groq Vision and return the parsed
        structured diagnosis. Signature matches GeminiVisionClient
        exactly so it's a drop-in replacement in
        disease_detection_service.py.

        Raises:
            httpx.HTTPStatusError / httpx.TimeoutException / httpx.ConnectError
            ValueError — if the model didn't return valid JSON.
        """

        endpoint = f"{self.base_url}/chat/completions"

        encoded_image = base64.b64encode(image_bytes).decode("utf-8")
        data_url = f"data:{mime_type};base64,{encoded_image}"

        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": DISEASE_ANALYSIS_PROMPT},
                        {"type": "image_url", "image_url": {"url": data_url}},
                    ],
                }
            ],
            "temperature": 0.2,
            "max_tokens": 512,
            "response_format": {"type": "json_object"},
        }

        headers = {"Authorization": f"Bearer {self.api_key}"}

        with httpx.Client(timeout=self.timeout) as client:
            response = client.post(endpoint, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()

        raw_text = data["choices"][0]["message"]["content"]

        try:
            parsed = json.loads(raw_text)
        except json.JSONDecodeError as exc:
            raise ValueError(
                f"Groq Vision returned non-JSON output: {raw_text[:200]}"
            ) from exc

        tokens = data.get("usage", {}).get("total_tokens", 0)

        return {"result": parsed, "tokens": tokens}



    # ⚠️ MODEL STATUS: preview tier as of 2026-07-27. Groq's vision lineup
# changes frequently without long notice. If this starts 404ing again,
# check https://console.groq.com/docs/vision for the replacement and
# update self.model above — do NOT hardcode a model name elsewhere.