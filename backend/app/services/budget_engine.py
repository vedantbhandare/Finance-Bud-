"""Budget engine — orchestrates deterministic budget rules with AI explanation."""
from __future__ import annotations

from datetime import date
from decimal import Decimal
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.budget import BudgetAllocation, BudgetPlan
from app.repositories.budget_repo import BudgetPlanRepository
from app.repositories.transaction_repo import TransactionRepository


class BudgetEngine:
    """Orchestrates budget generation using deterministic rules."""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.budget_repo = BudgetPlanRepository(db)
        self.txn_repo = TransactionRepository(db)

    async def generate_budget_plan(
        self,
        user_id: UUID,
        monthly_income: Decimal,
        fixed_expenses: list[dict] | None = None,
        goals: list[dict] | None = None,
        spending_style: list[str] | None = None,
    ) -> BudgetPlan:
        """Generate a new budget plan using the 50/30/20 rule."""
        today = date.today()
        period_start = today.replace(day=1)
        if today.month == 12:
            period_end = today.replace(year=today.year + 1, month=1, day=1)
        else:
            period_end = today.replace(month=today.month + 1, day=1)

        # Simple 50/30/20 allocation
        needs = monthly_income * Decimal("0.50")
        wants = monthly_income * Decimal("0.30")
        savings = monthly_income * Decimal("0.20")

        reasoning = (
            f"• Needs (50%): ₹{needs:,.2f} — Rent, groceries, utilities, transport\n"
            f"• Wants (30%): ₹{wants:,.2f} — Dining, shopping, entertainment\n"
            f"• Savings (20%): ₹{savings:,.2f} — Emergency fund, investments, goals"
        )

        # Deactivate any existing active budget
        existing = await self.budget_repo.get_active_plan(user_id)
        if existing:
            existing.status = "expired"

        # Create budget plan
        plan = BudgetPlan(
            user_id=user_id,
            month_start=period_start,
            month_end=period_end,
            total_income=monthly_income,
            needs_pct=Decimal("50"),
            wants_pct=Decimal("30"),
            savings_pct=Decimal("20"),
            status="active",
            ai_reasoning=reasoning,
            is_ai_generated=True,
        )
        self.db.add(plan)
        await self.db.flush()

        return plan

    async def get_current_budget(self, user_id: UUID) -> BudgetPlan | None:
        """Get the active budget plan."""
        return await self.budget_repo.get_active_plan(user_id)
