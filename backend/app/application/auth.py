from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas import LoginRequest, RegisterRequest, TokenResponse, UserResponse
from app.core.errors import AuthenticationError, ConflictError
from app.core.security import create_access_token, create_refresh_token, hash_password, verify_password
from app.infrastructure.orm.models import User
from app.infrastructure.orm.repositories import CategoryRepository, UserRepository


class AuthService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.users = UserRepository(session)
        self.categories = CategoryRepository(session)

    def _tokens(self, user: User) -> TokenResponse:
        return TokenResponse(
            access_token=create_access_token(user.id),
            refresh_token=create_refresh_token(user.id),
            user=UserResponse.model_validate(user),
        )

    async def register(self, data: RegisterRequest) -> TokenResponse:
        if await self.users.by_email(data.email):
            raise ConflictError("User with this email already exists")
        user = User(
            email=data.email.lower(),
            full_name=data.full_name.strip(),
            password_hash=hash_password(data.password),
        )
        await self.users.add(user)
        await self.categories.ensure_system_categories()
        return self._tokens(user)

    async def login(self, data: LoginRequest) -> TokenResponse:
        user = await self.users.by_email(data.email)
        if not user or not user.is_active or not verify_password(data.password, user.password_hash):
            raise AuthenticationError("Invalid email or password")
        return self._tokens(user)

    async def refresh(self, user_id: str) -> TokenResponse:
        user = await self.users.get(user_id)
        if not user or not user.is_active:
            raise AuthenticationError("Invalid refresh token")
        return self._tokens(user)

