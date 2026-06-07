"""Goal and GoalContribution repositories."""

from __future__ import annotations

import uuid
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.models.goal import Goal, GoalContribution, GoalStatus
from app.repositories.base import BaseRepository


class GoalRepository(BaseRepository[Goal]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(Goal, session)

    async def get_user_goals(
        self,
        user_id: uuid.UUID,
        *,
        status: GoalStatus | None = None,
    ) -> Sequence[Goal]:
        stmt = select(Goal).where(Goal.user_id == user_id)
        if status:
            stmt = stmt.where(Goal.status == status)
        stmt = stmt.order_by(Goal.created_at.desc())
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_with_contributions(self, goal_id: uuid.UUID) -> Goal | None:
        result = await self.session.execute(
            select(Goal)
            .options(joinedload(Goal.contributions))
            .where(Goal.id == goal_id),
        )
        return result.unique().scalar_one_or_none()

    async def get_active_goals(self, user_id: uuid.UUID) -> Sequence[Goal]:
        return await self.get_user_goals(user_id, status=GoalStatus.ACTIVE)


class GoalContributionRepository(BaseRepository[GoalContribution]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(GoalContribution, session)

    async def get_goal_contributions(
        self,
        goal_id: uuid.UUID,
        *,
        offset: int = 0,
        limit: int = 50,
    ) -> Sequence[GoalContribution]:
        result = await self.session.execute(
            select(GoalContribution)
            .where(GoalContribution.goal_id == goal_id)
            .order_by(GoalContribution.contribution_date.desc())
            .offset(offset)
            .limit(limit),
        )
        return result.scalars().all()
