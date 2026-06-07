"""Budgets router — view and generate budgets."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db_session
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.budget import BudgetPlanResponse
from app.services.budget_engine import BudgetEngine

router = APIRouter()


@router.get("/current")
async def get_current_budget(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
):
    """Get the current active budget plan."""
    engine = BudgetEngine(db)
    budget = await engine.get_current_budget(current_user.id)
    if not budget:
        return {"message": "No active budget. Generate one to get started.", "budget": None}
    return BudgetPlanResponse.model_validate(budget)


@router.post("/generate")
async def generate_budget(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
):
    """Generate a new AI-powered budget plan based on user data."""
    from decimal import Decimal
    from app.repositories.user_repo import UserRepository

    user_repo = UserRepository(db)
    # Get user's income — use monthly_salary from onboarding, fall back to default
    income = Decimal(str(current_user.monthly_salary)) if current_user.monthly_salary else Decimal("50000")

    from sqlalchemy import select
    from app.models.health import UserPreference

    # Load spending style from user preferences
    spending_style = []
    pref_result = await db.execute(select(UserPreference).where(UserPreference.user_id == current_user.id))
    pref = pref_result.scalar_one_or_none()
    
    if pref and pref.spending_style:
        spending_style = [pref.spending_style]

    engine = BudgetEngine(db)
    plan = await engine.generate_budget_plan(
        user_id=current_user.id,
        monthly_income=income,
        fixed_expenses=[],
        goals=[],
        spending_style=spending_style,
    )
    return {"budget_plan": plan, "message": "Budget generated successfully"}
