from __future__ import annotations

import secrets
from functools import lru_cache

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


_INSECURE_JWT_SECRETS = {
    "",
    "dev-secret-change-in-production",
    "your-secret-key-change-this",
    "change-this-to-a-secure-random-string-at-least-32-chars",
}


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    app_name: str = "Finance Buddy"
    app_version: str = "1.0.0"
    debug: bool = False

    database_url: str = "sqlite+aiosqlite:///./finance_buddy.db"
    database_echo: bool = False
    redis_url: str = "redis://localhost:6379/0"

    jwt_secret_key: str = Field(default_factory=lambda: secrets.token_urlsafe(48))
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7

    gemini_api_key: str = ""

    cors_origins: list[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:8081",
        "http://localhost:19006",
    ]

    currency: str = "INR"

    @field_validator("jwt_secret_key")
    @classmethod
    def reject_insecure_secret_in_production(cls, value: str) -> str:
        if value in _INSECURE_JWT_SECRETS:
            import logging

            logging.getLogger(__name__).warning(
                "JWT_SECRET_KEY is using an insecure development value."
            )
        return value


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()

