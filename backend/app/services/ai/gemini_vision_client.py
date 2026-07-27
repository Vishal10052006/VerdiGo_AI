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

import json
import logging

from google import genai
from google.genai import types

from app.config.settings import settings

logger = logging.getLogger(__name__)


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

        self.client = genai.Client(
            api_key=settings.GEMINI_API_KEY,
        )

        self.model = settings.GEMINI_VISION_MODEL

        logger.info("Gemini Vision initialized")
        logger.info("Model: %s", self.model)

    def analyze_image(self, image_bytes: bytes, mime_type: str) -> dict:
        """
        Analyze a crop image using the Google GenAI SDK.
        Returns a structured diagnosis.
        """

        response = self.client.models.generate_content(
            model=self.model,
            contents=[
                types.Part.from_text(text=DISEASE_ANALYSIS_PROMPT),
                types.Part.from_bytes(
                    data=image_bytes,
                    mime_type=mime_type,
                ),
            ],
            config=types.GenerateContentConfig(
                temperature=0.2,
                response_mime_type="application/json",
                max_output_tokens=512,
            ),
        )

        if not response.text:
            raise ValueError("Gemini returned an empty response.")

        try:
            parsed = json.loads(response.text)
        except json.JSONDecodeError as exc:
            raise ValueError(
                f"Gemini returned invalid JSON:\n{response.text}"
            ) from exc

        tokens = 0

        if (
            hasattr(response, "usage_metadata")
            and response.usage_metadata
            and hasattr(response.usage_metadata, "total_token_count")
        ):
            tokens = response.usage_metadata.total_token_count

        return {
            "result": parsed,
            "tokens": tokens,
        }