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
    REDIS_URL: str = "redis://localhost:6380/0"

    FINNHUB_API_KEY: str = ""   # deprecated -- kept for backward compat
    MARKETAUX_API_KEY: str = ""
    LITELLM_BASE_URL: str = ""
    LITELLM_API_KEY: str = "dummy"
    LITELLM_MODEL: str = "claude-sonnet-4-6"
    ENV: str = "development"
    CORS_ORIGINS: str = "https://stock.worldofnoki.com"

    class Config:
        env_file = ".env"
        extra = "ignore"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
