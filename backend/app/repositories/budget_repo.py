"""Budget repositories."""

from __future__ import annotations

import uuid
from datetime import date
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.models.budget import BudgetAllocation, BudgetPlan, BudgetStatus
from app.repositories.base import BaseRepository


class BudgetPlanRepository(BaseRepository[BudgetPlan]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(BudgetPlan, session)

    async def get_active_plan(self, user_id: uuid.UUID) -> BudgetPlan | None:
        result = await self.session.execute(
            select(BudgetPlan)
            .options(joinedload(BudgetPlan.allocations).joinedload(BudgetAllocation.category))
            .where(
                BudgetPlan.user_id == user_id,
                BudgetPlan.status == BudgetStatus.ACTIVE,
            )
            .order_by(BudgetPlan.month_start.desc())
            .limit(1),
        )
        return result.unique().scalar_one_or_none()

    async def get_plan_for_month(
        self,
        user_id: uuid.UUID,
        month_start: date,
    ) -> BudgetPlan | None:
        result = await self.session.execute(
            select(BudgetPlan)
            .options(joinedload(BudgetPlan.allocations))
            .where(
                BudgetPlan.user_id == user_id,
                BudgetPlan.month_start == month_start,
            ),
        )
        return result.unique().scalar_one_or_none()

    async def get_user_plans(
        self,
        user_id: uuid.UUID,
        limit: int = 12,
    ) -> Sequence[BudgetPlan]:
        result = await self.session.execute(
            select(BudgetPlan)
            .where(BudgetPlan.user_id == user_id)
            .order_by(BudgetPlan.month_start.desc())
            .limit(limit),
        )
        return result.scalars().all()


class BudgetAllocationRepository(BaseRepository[BudgetAllocation]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(BudgetAllocation, session)

    async def get_plan_allocations(
        self,
        budget_plan_id: uuid.UUID,
    ) -> Sequence[BudgetAllocation]:
        result = await self.session.execute(
            select(BudgetAllocation)
            .options(joinedload(BudgetAllocation.category))
            .where(BudgetAllocation.budget_plan_id == budget_plan_id),
        )
        return result.unique().scalars().all()
