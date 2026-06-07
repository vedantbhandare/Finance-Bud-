"""User repository."""

from __future__ import annotations

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.models.user import User
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(User, session)

    async def get_by_email(self, email: str) -> User | None:
        result = await self.session.execute(
            select(User).where(User.email == email),
        )
        return result.scalar_one_or_none()

    async def get_with_profile(self, user_id: uuid.UUID) -> User | None:
        return await self.get_by_id(user_id)

    async def email_exists(self, email: str) -> bool:
        result = await self.session.execute(
            select(User.id).where(User.email == email),
        )
        return result.scalar_one_or_none() is not None

    async def set_onboarded(self, user_id: uuid.UUID) -> None:
        await self.update_by_id(user_id, {"is_onboarded": True})



