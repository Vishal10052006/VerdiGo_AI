from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    # =========================
    # Application
    # =========================
    APP_NAME: str = "VerdiGO AI"
    APP_ENV: str = "development"
    DEBUG: bool = True

    # =========================
    # Database
    # =========================
    DATABASE_URL: str

    # =========================
    # JWT
    # =========================
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int

    # =========================
    # OTP
    # =========================
    OTP_LENGTH: int
    OTP_EXPIRE_MINUTES: int
    OTP_MAX_ATTEMPTS: int
    SMS_PROVIDER_URL: str = ""
    SMS_PROVIDER_API_KEY: str = ""
    SMS_SENDER_ID: str = ""

    # =========================
    # Weather
    # =========================

    WEATHERAPI_API_KEY: str
    WEATHERAPI_BASE_URL: str
    OPENMETEO_BASE_URL: str
    PRIMARY_WEATHER_PROVIDER: str
    FALLBACK_WEATHER_PROVIDER: str
    WEATHER_REQUEST_TIMEOUT: int
    WEATHER_CACHE_MINUTES: int


    # Add to backend/app/config/settings.py

    # =========================
    # AI Chat Assistant
    # =========================
    GEMINI_API_KEY: str = ""
    GEMINI_BASE_URL: str = "https://generativelanguage.googleapis.com/v1beta"
    GEMINI_MODEL: str = "gemini-1.5-flash"

    OPENAI_API_KEY: str = ""
    OPENAI_BASE_URL: str = "https://api.openai.com/v1"
    OPENAI_MODEL: str = "gpt-4o-mini"

    AI_REQUEST_TIMEOUT: int = 15
    AI_DAILY_MESSAGE_LIMIT: int = 100  # per-farmer rate limit — cost control

    # =========================
    # CORS
    # =========================
    ALLOWED_ORIGINS: str
    
    # ===========================
    # File Upload
    # ===========================

    UPLOAD_DIR: str = "uploads"

    PROFILE_UPLOAD_DIR: str = "uploads/profile"

    MAX_IMAGE_SIZE: int = 5 * 1024 * 1024  # 5 MB

    ALLOWED_IMAGE_EXTENSIONS: tuple[str, ...] = (
        ".jpg",
        ".jpeg",
        ".png",
        ".webp",
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()
