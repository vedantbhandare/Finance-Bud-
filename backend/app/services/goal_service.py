"""Goal service — business logic for financial goals."""
from datetime import date
from decimal import Decimal
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.goal import Goal, GoalContribution, GoalStatus
from app.repositories.goal_repo import GoalRepository
from app.schemas.goal import ContributionCreate, GoalCreate, GoalUpdate


class GoalService:
    """Business logic for goal management."""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = GoalRepository(db)

    async def create_goal(self, user_id: UUID, data: GoalCreate) -> Goal:
        """Create a new financial goal."""
        goal = Goal(
            user_id=user_id,
            name=data.name,
            target_amount=data.target_amount,
            target_date=data.target_date,
        )
        return await self.repo.create(goal)

    async def get_goals(self, user_id: UUID, status: str | None = None) -> list[Goal]:
        """Get all goals for a user."""
        return await self.repo.get_user_goals(user_id, status=status)

    async def get_goal(self, user_id: UUID, goal_id: UUID) -> Goal | None:
        """Get a single goal."""
        goal = await self.repo.get_by_id(goal_id)
        if goal and goal.user_id == user_id:
            return goal
        return None

    async def update_goal(self, user_id: UUID, goal_id: UUID, data: GoalUpdate) -> Goal | None:
        """Update a goal."""
        goal = await self.get_goal(user_id, goal_id)
        if not goal:
            return None
        update_data = data.model_dump(exclude_unset=True)
        return await self.repo.update_by_id(goal_id, update_data)

    async def delete_goal(self, user_id: UUID, goal_id: UUID) -> bool:
        """Delete a goal."""
        goal = await self.get_goal(user_id, goal_id)
        if not goal:
            return False
        await self.repo.delete_by_id(goal_id)
        return True

    async def contribute(self, user_id: UUID, goal_id: UUID, data: ContributionCreate) -> Goal:
        """Add a contribution to a goal."""
        goal = await self.get_goal(user_id, goal_id)
        if not goal:
            raise ValueError("Goal not found")
        if goal.status != GoalStatus.ACTIVE:
            raise ValueError("Cannot contribute to a non-active goal")

        contribution = GoalContribution(
            goal_id=goal_id,
            amount=data.amount,
            contribution_date=date.today(),
            notes=data.notes,
        )
        self.db.add(contribution)

        goal.current_amount += data.amount
        if goal.current_amount >= goal.target_amount:
            goal.status = "completed"

        await self.db.flush()
        return goal

    async def get_active_goals_summary(self, user_id: UUID) -> list[dict]:
        """Get summary of active goals with progress."""
        goals = await self.get_goals(user_id, status="active")
        return [
            {
                "id": str(g.id),
                "name": g.name,
                "target": float(g.target_amount),
                "current": float(g.current_amount),
                "progress_pct": round(
                    float(g.current_amount / g.target_amount * 100), 1
                ) if g.target_amount > 0 else 0,
                "target_date": str(g.target_date) if g.target_date else None,
            }
            for g in goals
        ]
