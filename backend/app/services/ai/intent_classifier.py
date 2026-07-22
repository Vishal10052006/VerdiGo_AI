# backend/app/services/ai/intent_classifier.py
"""
Intent Classifier

Lightweight keyword-based classification. Avoids an extra
LLM call per message (cost + latency). Upgrade to a small
classifier model only if keyword accuracy proves insufficient.
"""

from app.enums.chat import ChatIntentEnum

_KEYWORDS = {
    ChatIntentEnum.FERTILIZER_ADVICE: ["fertilizer", "urea", "npk", "nutrient", "khad"],
    ChatIntentEnum.IRRIGATION_ADVICE: ["water", "irrigation", "irrigate", "sinchai"],
    ChatIntentEnum.PEST_ADVICE: ["pest", "insect", "disease", "fungus", "keeda"],
    ChatIntentEnum.CROP_GUIDANCE: ["crop", "sow", "plant", "seed", "variety"],
    ChatIntentEnum.WEATHER_QUERY: ["weather", "rain", "temperature", "forecast"],
}


def classify_intent(message: str) -> ChatIntentEnum:
    lowered = message.lower()

    for intent, keywords in _KEYWORDS.items():
        if any(keyword in lowered for keyword in keywords):
            return intent

    return ChatIntentEnum.GENERAL