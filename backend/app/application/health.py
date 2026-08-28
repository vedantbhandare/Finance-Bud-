from __future__ import annotations

from datetime import date
from decimal import Decimal

from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas import HealthScoreResponse
from app.core.time import month_range
from app.domain.health import health_label, health_score, recommendations, spending_trend
from app.application.transactions import TransactionService
from app.infrastructure.orm.repositories import BudgetRepository, GoalRepository


class HealthService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.transactions = TransactionService(session)
        self.budgets = BudgetRepository(session)
        self.goals = GoalRepository(session)

    async def current(self, user_id: str) -> HealthScoreResponse:
        today = date.today()

        # Current month summary (uses SQL aggregation)
        summary = await self.transactions.monthly_summary(user_id, today.year, today.month)
        income = summary.total_income
        expenses = summary.total_expenses
        savings_rate = ((income - expenses) / income * 100) if income > 0 else Decimal("0")

        # --- Budget adherence + overspent categories ---
        budget_adherence = Decimal("50")
        overspent_categories: list[str] = []
        budget = await self.budgets.current(user_id)
        if budget and budget.allocations:
            total_allocated = sum(
                (a.allocated_amount for a in budget.allocations), Decimal("0")
            )
            if total_allocated > 0:
                budget_adherence = Decimal("100") - min(
                    Decimal("100"),
                    max(Decimal("0"), (expenses - total_allocated) / total_allocated * 100),
                )
            for a in budget.allocations:
                if a.spent_amount > a.allocated_amount and a.category:
                    overspent_categories.append(a.category.name)

        # --- Goal progress ---
        goals = await self.goals.active_for_user(user_id)
        if goals:
            goal_progress = sum(
                (
                    (g.current_amount / g.target_amount * 100)
                    if g.target_amount > 0
                    else Decimal("0")
                )
                for g in goals
            ) / Decimal(len(goals))
        else:
            goal_progress = Decimal("0")

        # --- Real spending trend (current vs. previous month) ---
        prev_month = today.month - 1 if today.month > 1 else 12
        prev_year = today.year if today.month > 1 else today.year - 1
        prev_start, prev_end = month_range(prev_year, prev_month)
        prev_totals = await self.transactions.transactions.aggregate_monthly(
            user_id, prev_start, prev_end,
        )
        trend = spending_trend(expenses, prev_totals["total_expenses"])

        # --- Days remaining in month ---
        _, month_end = month_range(today.year, today.month)
        days_remaining = max(0, (month_end - today).days)

        score = health_score(savings_rate, budget_adherence, goal_progress)
        return HealthScoreResponse(
            overall_score=score,
            label=health_label(score),
            savings_rate=round(float(savings_rate), 2),
            budget_adherence=round(float(budget_adherence), 2),
            goal_progress=round(float(goal_progress), 2),
            spending_trend=trend,
            recommendations=recommendations(
                savings_rate,
                budget_adherence,
                goal_progress,
                spending_trend_label=trend,
                days_remaining=days_remaining,
                top_overspent_categories=overspent_categories,
            ),
        )
