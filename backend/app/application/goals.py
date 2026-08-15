from __future__ import annotations

from datetime import date

from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas import ContributionCreate, GoalCreate, GoalResponse, GoalUpdate
from app.application.serializers import goal_response
from app.core.errors import NotFoundError, ValidationError
from app.infrastructure.orm.models import Goal, GoalContribution
from app.infrastructure.orm.repositories import GoalContributionRepository, GoalRepository


class GoalService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.goals = GoalRepository(session)
        self.contributions = GoalContributionRepository(session)

    async def create(self, user_id: str, data: GoalCreate) -> GoalResponse:
        goal = Goal(
            user_id=user_id,
            name=data.name,
            description=data.description,
            target_amount=data.target_amount,
            target_date=data.target_date,
            icon=data.icon,
            status="active",
        )
        await self.goals.add(goal)
        return goal_response(goal)

    async def list(self, user_id: str, status: str | None = None) -> list[GoalResponse]:
        return [goal_response(goal) for goal in await self.goals.list_for_user(user_id, status)]

    async def get_entity(self, user_id: str, goal_id: str) -> Goal:
        goal = await self.goals.get(goal_id)
        if not goal or goal.user_id != user_id:
            raise NotFoundError("Goal not found")
        return goal

    async def get(self, user_id: str, goal_id: str) -> GoalResponse:
        return goal_response(await self.get_entity(user_id, goal_id))

    async def update(self, user_id: str, goal_id: str, data: GoalUpdate) -> GoalResponse:
        goal = await self.get_entity(user_id, goal_id)
        for field_name, value in data.model_dump(exclude_unset=True).items():
            setattr(goal, field_name, value)
        await self.session.flush()
        return goal_response(goal)

    async def delete(self, user_id: str, goal_id: str) -> None:
        goal = await self.get_entity(user_id, goal_id)
        await self.goals.delete(goal)

    async def contribute(self, user_id: str, goal_id: str, data: ContributionCreate) -> GoalResponse:
        goal = await self.get_entity(user_id, goal_id)
        if goal.status != "active":
            raise ValidationError("Cannot contribute to an inactive goal")
        contribution = GoalContribution(
            goal_id=goal.id,
            amount=data.amount,
            contribution_date=date.today(),
            notes=data.notes,
        )
        await self.contributions.add(contribution)
        goal.current_amount += data.amount
        if goal.current_amount >= goal.target_amount:
            goal.status = "completed"
        await self.session.flush()
        return goal_response(goal)

