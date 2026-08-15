from __future__ import annotations

from datetime import date
from decimal import Decimal

from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas import HealthScoreResponse
from app.domain.health import health_label, health_score, recommendations
from app.infrastructure.orm.repositories import BudgetRepository, GoalRepository
from app.application.transactions import TransactionService


class HealthService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.transactions = TransactionService(session)
        self.budgets = BudgetRepository(session)
        self.goals = GoalRepository(session)

    async def current(self, user_id: str) -> HealthScoreResponse:
        today = date.today()
        summary = await self.transactions.monthly_summary(user_id, today.year, today.month)
        income = summary.total_income
        expenses = summary.total_expenses
        savings_rate = ((income - expenses) / income * 100) if income > 0 else Decimal("0")

        budget_adherence = Decimal("50")
        budget = await self.budgets.current(user_id)
        if budget and budget.allocations:
            total_allocated = sum((allocation.allocated_amount for allocation in budget.allocations), Decimal("0.00"))
            if total_allocated > 0:
                budget_adherence = Decimal("100") - min(Decimal("100"), max(Decimal("0"), (expenses - total_allocated) / total_allocated * 100))

        goals = await self.goals.active_for_user(user_id)
        if goals:
            goal_progress = sum(
                ((goal.current_amount / goal.target_amount * 100) if goal.target_amount > 0 else Decimal("0"))
                for goal in goals
            ) / Decimal(len(goals))
        else:
            goal_progress = Decimal("0")

        score = health_score(savings_rate, budget_adherence, goal_progress)
        return HealthScoreResponse(
            overall_score=score,
            label=health_label(score),
            savings_rate=round(float(savings_rate), 2),
            budget_adherence=round(float(budget_adherence), 2),
            goal_progress=round(float(goal_progress), 2),
            spending_trend="stable",
            recommendations=recommendations(savings_rate, budget_adherence, goal_progress),
        )

