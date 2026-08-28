from __future__ import annotations

import json
from decimal import Decimal

from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas import BudgetEnvelope, BudgetGenerateResponse
from app.application.serializers import budget_response
from app.core.errors import AppError
from app.core.time import current_month_range
from app.domain.budgets import BudgetInput, generate_budget, monthly_goal_contribution
from app.infrastructure.orm.models import BudgetAllocation, BudgetPlan, User
from app.infrastructure.orm.repositories import (
    BudgetRepository,
    CategoryRepository,
    GoalRepository,
    PreferenceRepository,
    RecurringRuleRepository,
)


class BudgetService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.budgets = BudgetRepository(session)
        self.categories = CategoryRepository(session)
        self.recurring = RecurringRuleRepository(session)
        self.goals = GoalRepository(session)
        self.preferences = PreferenceRepository(session)

    async def current(self, user_id: str) -> BudgetEnvelope:
        plan = await self.budgets.current(user_id)
        if not plan:
            return BudgetEnvelope(budget=None, message="No active budget. Generate one to get started.")
        return BudgetEnvelope(budget=budget_response(plan))

    async def generate(self, user: User) -> BudgetGenerateResponse:
        # System categories are seeded at app startup — no per-request seeding.
        await self.budgets.expire_active(user.id)

        start, end = current_month_range()
        recurring_rules = await self.recurring.active_for_user(user.id)
        fixed = tuple(
            (rule.category.name if rule.category else rule.description, rule.amount)
            for rule in recurring_rules
        )

        # Date-aware goal allocation: goals due in 2 months get 6x the
        # monthly allocation of goals due in 12 months.
        active_goals = await self.goals.active_for_user(user.id)
        monthly_goal_need = sum(
            (
                monthly_goal_contribution(g.target_amount, g.current_amount, g.target_date)
                for g in active_goals
            ),
            Decimal("0.00"),
        )

        preference = await self.preferences.for_user(user.id)
        overspending_categories: tuple[str, ...] = ()
        if preference and preference.top_expense_categories:
            try:
                overspending_categories = tuple(json.loads(preference.top_expense_categories))
            except json.JSONDecodeError:
                overspending_categories = ()

        income = user.monthly_salary or Decimal("50000.00")
        lines = generate_budget(
            BudgetInput(
                monthly_income=income,
                fixed_expenses=fixed,
                monthly_goal_need=monthly_goal_need,
                overspending_categories=overspending_categories,
            )
        )

        plan = BudgetPlan(
            user_id=user.id,
            month_start=start,
            month_end=end,
            total_income=income,
            needs_pct=Decimal("50.00"),
            wants_pct=Decimal("30.00"),
            savings_pct=Decimal("20.00"),
            status="active",
            is_ai_generated=False,
            ai_reasoning="Generated with deterministic 50/30/20 rules adjusted for fixed bills, goals, and overspending categories.",
        )
        await self.budgets.add(plan)

        for line in lines:
            category = await self.categories.by_name(line.category_name, user.id)
            allocation = BudgetAllocation(
                budget_plan_id=plan.id,
                category_id=category.id if category else None,
                allocated_amount=line.amount,
                spent_amount=Decimal("0.00"),
            )
            self.session.add(allocation)
        await self.session.flush()

        reloaded = await self.budgets.current(user.id)
        if not reloaded:
            raise AppError("Failed to reload generated budget plan")
        return BudgetGenerateResponse(
            budget_plan=budget_response(reloaded),
            message="Budget generated successfully",
        )
