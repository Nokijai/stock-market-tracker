from pydantic_settings import BaseSettings
from functools import lru_cache
import secrets


class Settings(BaseSettings):
    # Generate a random default so the app never silently uses a known-weak key.
    # In production this MUST be overridden via the .env file.
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours

    DATABASE_URL: str = "sqlite:///./stock_tracker.db"
    REDIS_URL: str = "redis://localhost:6379/0"

    # --- Alert Notification Settings ---

    # ntfy.sh topic for push notifications.
    # Sign up at https://ntfy.sh, pick a topic name, and set it here.
    # Example: "my-stock-alerts" sends notifications to https://ntfy.sh/my-stock-alerts
    NTFY_TOPIC: str | None = None

    # Optional SMTP settings for email fallback notifications.
    # SMTP_HOST: str = ""
    # SMTP_PORT: int = 587
    # SMTP_USER: str = ""
    # SMTP_PASSWORD: str = ""
    # SMTP_FROM: str = "alerts@example.com"
    # NOTIFY_EMAIL: str = ""

    FINNHUB_API_KEY: str = ""   # deprecated -- kept for backward compat
    MARKETAUX_API_KEY: str = ""
    LITELLM_BASE_URL: str = "https://yuanyuaicloud.cn/v1"
    LITELLM_API_KEY: str = ""
    LITELLM_MODEL: str = "glm-5.2"

    # SMTP / Email
    SMTP_HOST: str = ""
    SMTP_PORT: int = 587
    SMTP_USERNAME: str = ""
    SMTP_PASSWORD: str = ""
    SMTP_FROM: str = "alerts@stock-tracker"
    ENV: str = "development"
    CORS_ORIGINS: str = "https://stock.worldofnoki.com"

    class Config:
        env_file = ".env"
        extra = "ignore"


@lru_cache()
def get_settings() -> Settings:
    return Settings()