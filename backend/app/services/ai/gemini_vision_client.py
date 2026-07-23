"""
Gemini Vision Client

Thin client for Gemini's multimodal generateContent API,
specialized for crop-disease image analysis. Forces a strict
JSON schema response so the service layer never has to parse
free-form text — same "structured output over regex" principle
used nowhere else yet in this codebase, but it's the only safe
way to consume a vision model's output reliably.

Module: Phase 1 → Module 8 → Disease Detection
Author: VerdiGO Backend Team
"""

import base64
import json

import httpx

from app.config.settings import settings


DISEASE_ANALYSIS_PROMPT = """You are an expert plant pathologist analyzing a crop image for an Indian smallholder farmer.

Look at the image carefully and respond with ONLY a JSON object (no markdown, no prose) matching exactly this schema:

{
  "is_healthy": boolean,
  "disease_name": string | null,      // null if healthy
  "confidence": number,                // 0-100, your certainty in this diagnosis
  "severity": "none" | "low" | "moderate" | "high" | "critical",
  "treatment": string[],               // 2-5 short, actionable steps. Empty if healthy.
  "prevention_tips": string[],         // 2-4 short, actionable steps.
  "crop_identified": string | null     // your best guess at the crop/plant type, null if unclear
}

Rules:
- If the image is not a plant/crop/leaf at all, set is_healthy=false, disease_name="Not a plant image", confidence=0, severity="none".
- Never recommend specific chemical dosages — say "consult your local Krishi Vigyan Kendra (KVK) for exact dosage" instead.
- Be conservative with confidence: only go above 80 if visual symptoms are unambiguous (e.g. clear blight lesions, obvious rust pustules).
- Keep each treatment/prevention string under 15 words, farmer-friendly language, no jargon.
"""


class GeminiVisionClient:
    """
    Client for Gemini's multimodal (image + text) generateContent API.
    """

    def __init__(self):
        if not settings.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is not configured.")

        self.api_key = settings.GEMINI_API_KEY
        self.base_url = settings.GEMINI_BASE_URL
        self.model = settings.GEMINI_VISION_MODEL
        self.timeout = settings.AI_REQUEST_TIMEOUT

    def analyze_image(self, image_bytes: bytes, mime_type: str) -> dict:
        """
        Send an image to Gemini Vision and return the parsed
        structured diagnosis.

        Raises:
            httpx.HTTPStatusError / httpx.TimeoutException / httpx.ConnectError
                on transport failure (caller decides fallback/error handling).
            ValueError
                if the model didn't return valid JSON matching the schema.
        """

        endpoint = (
            f"{self.base_url}/models/{self.model}:generateContent"
            f"?key={self.api_key}"
        )

        encoded_image = base64.b64encode(image_bytes).decode("utf-8")

        payload = {
            "contents": [
                {
                    "role": "user",
                    "parts": [
                        {"text": DISEASE_ANALYSIS_PROMPT},
                        {
                            "inline_data": {
                                "mime_type": mime_type,
                                "data": encoded_image,
                            }
                        },
                    ],
                }
            ],
            "generationConfig": {
                "temperature": 0.2,  # low — this is a diagnostic task, not creative
                "maxOutputTokens": 512,
                "response_mime_type": "application/json",
            },
        }

        with httpx.Client(timeout=self.timeout) as client:
            response = client.post(endpoint, json=payload)
            response.raise_for_status()
            data = response.json()

        raw_text = data["candidates"][0]["content"]["parts"][0]["text"]

        try:
            parsed = json.loads(raw_text)
        except json.JSONDecodeError as exc:
            raise ValueError(
                f"Gemini Vision returned non-JSON output: {raw_text[:200]}"
            ) from exc

        return {
            "result": parsed,
            "tokens": data.get("usageMetadata", {}).get("totalTokenCount", 0),
        }