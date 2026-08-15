from __future__ import annotations

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.auth import AuthService
from app.application.budgets import BudgetService
from app.application.chat import ChatService
from app.application.goals import GoalService
from app.application.health import HealthService
from app.application.onboarding import OnboardingService
from app.application.transactions import TransactionService
from app.core.database import db_session
from app.core.errors import AuthenticationError
from app.core.security import decode_token
from app.infrastructure.orm.models import User

bearer = HTTPBearer(auto_error=True)


async def current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer),
    session: AsyncSession = Depends(db_session),
) -> User:
    try:
        user_id = decode_token(credentials.credentials, "access")
    except (JWTError, ValueError) as exc:
        raise AuthenticationError("Invalid or expired token") from exc

    user = await session.scalar(select(User).where(User.id == user_id))
    if not user or not user.is_active:
        raise AuthenticationError("User not found or inactive")
    return user


async def auth_service(session: AsyncSession = Depends(db_session)) -> AuthService:
    return AuthService(session)


async def transaction_service(session: AsyncSession = Depends(db_session)) -> TransactionService:
    return TransactionService(session)


async def onboarding_service(session: AsyncSession = Depends(db_session)) -> OnboardingService:
    return OnboardingService(session)


async def budget_service(session: AsyncSession = Depends(db_session)) -> BudgetService:
    return BudgetService(session)


async def goal_service(session: AsyncSession = Depends(db_session)) -> GoalService:
    return GoalService(session)


async def health_service(session: AsyncSession = Depends(db_session)) -> HealthService:
    return HealthService(session)


async def chat_service(session: AsyncSession = Depends(db_session)) -> ChatService:
    return ChatService(session)

