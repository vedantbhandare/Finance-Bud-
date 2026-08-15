from __future__ import annotations

from fastapi import APIRouter, Depends
from jose import JWTError

from app.api.deps import auth_service, current_user
from app.api.schemas import LoginRequest, RefreshRequest, RegisterRequest, TokenResponse, UserResponse
from app.application.auth import AuthService
from app.core.errors import AuthenticationError
from app.core.security import decode_token
from app.infrastructure.orm.models import User

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=TokenResponse, status_code=201)
async def register(data: RegisterRequest, service: AuthService = Depends(auth_service)):
    return await service.register(data)


@router.post("/login", response_model=TokenResponse)
async def login(data: LoginRequest, service: AuthService = Depends(auth_service)):
    return await service.login(data)


@router.post("/refresh", response_model=TokenResponse)
async def refresh(data: RefreshRequest, service: AuthService = Depends(auth_service)):
    try:
        user_id = decode_token(data.refresh_token, "refresh")
    except (JWTError, ValueError) as exc:
        raise AuthenticationError("Invalid or expired refresh token") from exc
    return await service.refresh(user_id)


@router.get("/me", response_model=UserResponse)
async def me(user: User = Depends(current_user)):
    return UserResponse.model_validate(user)

