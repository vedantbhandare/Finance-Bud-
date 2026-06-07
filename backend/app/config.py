"""Application configuration loaded from environment variables."""

from __future__ import annotations

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Centralised application settings backed by .env / env vars."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ── Database ────────────────────────────────────────────────────────
    database_url: str = Field(
        default="postgresql+asyncpg://postgres:postgres@localhost:5432/finance_buddy",
        description="Async SQLAlchemy database URL",
    )
    database_echo: bool = Field(default=False)

    # ── Redis ───────────────────────────────────────────────────────────
    redis_url: str = Field(default="redis://localhost:6379/0")

    # ── JWT ──────────────────────────────────────────────────────────────
    jwt_secret_key: str = Field(
        default="change-this-to-a-secure-random-string-at-least-32-chars",
    )
    jwt_algorithm: str = Field(default="HS256")
    access_token_expire_minutes: int = Field(default=30)
    refresh_token_expire_days: int = Field(default=7)

    # ── Google Gemini ────────────────────────────────────────────────────
    gemini_api_key: str = Field(default="")

    # ── App ──────────────────────────────────────────────────────────────
    app_name: str = Field(default="Finance Buddy")
    app_version: str = Field(default="0.1.0")
    debug: bool = Field(default=False)
    cors_origins: list[str] = Field(
        default=["http://localhost:3000", "http://localhost:5173"],
    )

    # ── Hardcoded for MVP ────────────────────────────────────────────────
    currency: str = "INR"


def get_settings() -> Settings:
    """Return a cached Settings instance."""
    return _settings


_settings = Settings()
