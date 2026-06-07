"""Auth service — registration, login, token management."""
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.models.user import User
from app.repositories.user_repo import UserRepository
from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse, UserResponse
from app.utils.security import create_access_token, create_refresh_token, hash_password, verify_password


class AuthService:
    """Handles authentication business logic."""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_repo = UserRepository(db)
        self.settings = get_settings()

    async def register(self, data: RegisterRequest) -> TokenResponse:
        """Register a new user and return tokens."""
        # Check if email already exists
        existing = await self.user_repo.get_by_email(data.email)
        if existing:
            raise ValueError("An account with this email already exists")

        # Create user
        user = User(
            email=data.email,
            password_hash=hash_password(data.password),
            full_name=data.full_name,
        )
        created_user = await self.user_repo.create(user)

        # Generate tokens
        access_token = create_access_token(user_id=created_user.id)
        refresh_token = create_refresh_token(user_id=created_user.id)

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            user=UserResponse.model_validate(created_user),
        )

    async def login(self, data: LoginRequest) -> TokenResponse:
        """Authenticate user and return tokens."""
        user = await self.user_repo.get_by_email(data.email)
        if not user:
            raise ValueError("Invalid email or password")

        if not verify_password(data.password, user.password_hash):
            raise ValueError("Invalid email or password")

        access_token = create_access_token(user_id=user.id)
        refresh_token = create_refresh_token(user_id=user.id)

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            user=UserResponse.model_validate(user),
        )

    async def refresh(self, user_id: UUID) -> dict:
        """Generate new access token for authenticated user."""
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")

        access_token = create_access_token(user_id=user.id)
        refresh_token = create_refresh_token(user_id=user.id)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }
