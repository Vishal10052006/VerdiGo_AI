from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    # =========================
    # Application
    # =========================
    APP_NAME: str
    APP_ENV: str
    DEBUG: bool

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
    # CORS
    # =========================
    ALLOWED_ORIGINS: str

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

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
