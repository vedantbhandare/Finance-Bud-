from __future__ import annotations

import json
from datetime import date

from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas import ExpenseSetup, GoalSetup, IncomeSetup, SpendingStyleSetup, StatusResponse
from app.infrastructure.orm.models import Goal, RecurringRule, User, UserPreference
from app.infrastructure.orm.repositories import CategoryRepository, PreferenceRepository


class OnboardingService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.categories = CategoryRepository(session)
        self.preferences = PreferenceRepository(session)

    async def income(self, user: User, data: IncomeSetup) -> StatusResponse:
        user.monthly_salary = data.amount
        user.pay_cycle_day = data.pay_day
        await self.session.flush()
        return StatusResponse(message="Income details saved")

    async def expenses(self, user: User, data: ExpenseSetup) -> StatusResponse:
        for expense in data.expenses:
            category = None
            if expense.category_name:
                category = await self.categories.by_name(expense.category_name, user.id)
            rule = RecurringRule(
                user_id=user.id,
                category_id=category.id if category else None,
                amount=expense.amount,
                description=expense.description,
                frequency=expense.frequency,
                start_date=expense.start_date or date.today(),
                next_due_date=expense.start_date or date.today(),
                transaction_type="expense",
            )
            self.session.add(rule)
        await self.session.flush()
        return StatusResponse(message=f"Saved {len(data.expenses)} recurring expenses")

    async def goals(self, user: User, data: GoalSetup) -> StatusResponse:
        for goal in data.goals:
            self.session.add(
                Goal(
                    user_id=user.id,
                    name=goal.name,
                    target_amount=goal.target_amount,
                    target_date=goal.target_date,
                    status="active",
                )
            )
        await self.session.flush()
        return StatusResponse(message=f"Saved {len(data.goals)} goals")

    async def spending_style(self, user: User, data: SpendingStyleSetup) -> StatusResponse:
        preference = await self.preferences.for_user(user.id)
        if not preference:
            preference = UserPreference(user_id=user.id)
            self.session.add(preference)
        preference.spending_style = data.ai_personality
        preference.top_expense_categories = json.dumps(data.overspending_categories)
        await self.session.flush()
        return StatusResponse(message="Spending style saved")

    async def complete(self, user: User) -> StatusResponse:
        user.is_onboarded = True
        await self.session.flush()
        return StatusResponse(message="Onboarding completed")

