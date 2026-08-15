"""FastAPI dependencies — authentication helpers and service providers.

All services are injected via Depends() so routers never instantiate
them directly.  This enables clean testing with dependency overrides.
"""

from __future__ import annotations

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db_session
from app.exceptions import AuthenticationError
from app.models.user import User
from app.utils.security import decode_access_token

_bearer = HTTPBearer(auto_error=True)
_bearer_optional = HTTPBearer(auto_error=False)


# ── Auth dependencies ──────────────────────────────────────────────────────


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(_bearer),
    session: AsyncSession = Depends(get_db_session),
) -> User:
    """Resolve the authenticated user from the Authorization header.

    Raises AuthenticationError (401) if the token is missing, invalid,
    or the user doesn't exist.
    """
    try:
        user_id = decode_access_token(credentials.credentials)
    except (JWTError, ValueError) as exc:
        raise AuthenticationError("Invalid or expired token") from exc

    result = await session.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if user is None or not user.is_active:
        raise AuthenticationError("User not found or inactive")
    return user


async def get_optional_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(_bearer_optional),
    session: AsyncSession = Depends(get_db_session),
) -> User | None:
    """Optionally resolve the user.  Returns None for unauthenticated requests."""
    if credentials is None:
        return None
    try:
        user_id = decode_access_token(credentials.credentials)
    except (JWTError, ValueError):
        return None

    result = await session.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if user is None or not user.is_active:
        return None
    return user


# ── Service providers ──────────────────────────────────────────────────────
# Each service gets the DB session via Depends, so routers never
# create services manually.


async def get_auth_service(
    db: AsyncSession = Depends(get_db_session),
):
    """Provide AuthService instance."""
    from app.services.auth import AuthService

    return AuthService(db)


async def get_transaction_service(
    db: AsyncSession = Depends(get_db_session),
):
    """Provide TransactionService instance."""
    from app.services.transaction import TransactionService

    return TransactionService(db)


async def get_budget_service(
    db: AsyncSession = Depends(get_db_session),
):
    """Provide BudgetService instance."""
    from app.services.budget import BudgetService

    return BudgetService(db)


async def get_goal_service(
    db: AsyncSession = Depends(get_db_session),
):
    """Provide GoalService instance."""
    from app.services.goal import GoalService

    return GoalService(db)


async def get_health_service(
    db: AsyncSession = Depends(get_db_session),
):
    """Provide HealthService instance."""
    from app.services.health import HealthService

    return HealthService(db)


async def get_onboarding_service(
    db: AsyncSession = Depends(get_db_session),
):
    """Provide OnboardingService instance."""
    from app.services.onboarding import OnboardingService

    return OnboardingService(db)


async def get_ai_orchestrator(
    db: AsyncSession = Depends(get_db_session),
):
    """Provide AIOrchestrator instance."""
    from app.ai.orchestrator import AIOrchestrator

    return AIOrchestrator(db)
