"""Security utilities — Argon2 password hashing and JWT token management."""

from __future__ import annotations

import uuid
from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt
from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher

from app.config import get_settings

_settings = get_settings()

# ── Password hashing (Argon2) ─────────────────────────────────────────────
_password_hash = PasswordHash((Argon2Hasher(),))


def hash_password(plain: str) -> str:
    """Return an Argon2id hash of *plain*."""
    return _password_hash.hash(plain)


def verify_password(plain: str, hashed: str) -> bool:
    """Verify *plain* against an existing *hashed* value."""
    return _password_hash.verify(plain, hashed)


# ── JWT tokens ─────────────────────────────────────────────────────────────

def _create_token(data: dict, expires_delta: timedelta) -> str:
    payload = data.copy()
    payload["exp"] = datetime.now(timezone.utc) + expires_delta
    payload["iat"] = datetime.now(timezone.utc)
    return jwt.encode(payload, _settings.jwt_secret_key, algorithm=_settings.jwt_algorithm)


def create_access_token(user_id: uuid.UUID) -> str:
    """Create a short-lived access token."""
    return _create_token(
        {"sub": str(user_id), "type": "access"},
        timedelta(minutes=_settings.access_token_expire_minutes),
    )


def create_refresh_token(user_id: uuid.UUID) -> str:
    """Create a long-lived refresh token."""
    return _create_token(
        {"sub": str(user_id), "type": "refresh"},
        timedelta(days=_settings.refresh_token_expire_days),
    )


def decode_token(token: str) -> dict:
    """Decode and validate a JWT. Raises JWTError on failure."""
    return jwt.decode(
        token,
        _settings.jwt_secret_key,
        algorithms=[_settings.jwt_algorithm],
    )


def decode_access_token(token: str) -> uuid.UUID:
    """Decode an access token and return the user UUID.

    Raises
    ------
    JWTError
        If the token is invalid, expired, or not an access token.
    """
    payload = decode_token(token)
    if payload.get("type") != "access":
        raise JWTError("Token is not an access token")
    sub = payload.get("sub")
    if sub is None:
        raise JWTError("Token has no subject")
    return uuid.UUID(sub)


def decode_refresh_token(token: str) -> uuid.UUID:
    """Decode a refresh token and return the user UUID.

    Raises
    ------
    JWTError
        If the token is invalid, expired, or not a refresh token.
    """
    payload = decode_token(token)
    if payload.get("type") != "refresh":
        raise JWTError("Token is not a refresh token")
    sub = payload.get("sub")
    if sub is None:
        raise JWTError("Token has no subject")
    return uuid.UUID(sub)
