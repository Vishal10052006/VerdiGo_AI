from enum import Enum


class ChatRoleEnum(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class ChatIntentEnum(str, Enum):
    CROP_GUIDANCE = "crop_guidance"
    FERTILIZER_ADVICE = "fertilizer_advice"
    IRRIGATION_ADVICE = "irrigation_advice"
    PEST_ADVICE = "pest_advice"
    WEATHER_QUERY = "weather_query"
    GENERAL = "general"


class AIProviderEnum(str, Enum):
    GEMINI = "gemini"
    OPENAI = "openai"
    GROQ = "groq"