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

    # =========================
    # CORS
    # =========================
    ALLOWED_ORIGINS: str

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()