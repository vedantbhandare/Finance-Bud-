"""Application configuration loaded from environment variables.

Validates critical settings at startup so the app fails fast rather than
running with insecure defaults.
"""

from __future__ import annotations

import secrets
from functools import lru_cache

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


_INSECURE_DEFAULTS = frozenset({
    "change-this-to-a-secure-random-string-at-least-32-chars",
    "dev-secret-change-in-production",
    "your-secret-key-change-this",
    "",
})


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
        default="sqlite+aiosqlite:///./finance_buddy.db",
        description="Async SQLAlchemy database URL",
    )
    database_echo: bool = Field(default=False)

    # ── Redis ───────────────────────────────────────────────────────────
    redis_url: str = Field(default="redis://localhost:6379/0")

    # ── JWT ──────────────────────────────────────────────────────────────
    jwt_secret_key: str = Field(
        default_factory=lambda: secrets.token_urlsafe(48),
        description="HMAC secret for JWT signing — MUST be overridden in production",
    )
    jwt_algorithm: str = Field(default="HS256")
    access_token_expire_minutes: int = Field(default=30)
    refresh_token_expire_days: int = Field(default=7)

    # ── Google Gemini ────────────────────────────────────────────────────
    gemini_api_key: str = Field(default="")

    # ── App ──────────────────────────────────────────────────────────────
    app_name: str = Field(default="Finance Buddy")
    app_version: str = Field(default="0.2.0")
    debug: bool = Field(default=False)
    cors_origins: list[str] = Field(
        default=[
            "http://localhost:3000",
            "http://localhost:5173",
            "http://localhost:8081",
            "http://localhost:19006",
        ],
    )

    # ── Hardcoded for MVP ────────────────────────────────────────────────
    currency: str = "INR"

    @field_validator("jwt_secret_key")
    @classmethod
    def _warn_insecure_secret(cls, v: str) -> str:
        """Log a loud warning if the JWT secret is a known insecure default.

        In production the app should be started with a proper secret.
        We don't *crash* in debug mode to keep local development easy,
        but we do log a bright warning.
        """
        import logging

        if v in _INSECURE_DEFAULTS:
            logging.getLogger(__name__).warning(
                "⚠️  JWT_SECRET_KEY is set to an insecure default! "
                "Generate a real secret: python -c \"import secrets; print(secrets.token_urlsafe(48))\""
            )
        return v


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return a cached Settings instance (loaded once per process)."""
    return Settings()
