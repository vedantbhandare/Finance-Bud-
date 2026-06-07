"""Auth schemas — register, login, tokens, user response."""

from __future__ import annotations

import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class RegisterRequest(BaseModel):
    """Payload for user registration."""

    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    full_name: str = Field(min_length=1, max_length=200)


class LoginRequest(BaseModel):
    """Payload for user login."""

    email: EmailStr
    password: str


class RefreshRequest(BaseModel):
    """Payload for token refresh."""

    refresh_token: str


class UserResponse(BaseModel):
    """Public user representation."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    email: str
    full_name: str
    is_active: bool
    is_onboarded: bool
    created_at: datetime


class TokenResponse(BaseModel):
    """JWT token pair returned after login/register/refresh."""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: UserResponse | None = None
