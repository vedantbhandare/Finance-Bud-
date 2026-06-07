"""Onboarding router — multi-step setup flow."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db_session
from app.dependencies import get_current_user
from app.models.user import User
from app.models.transaction import RecurringRule
from app.models.goal import Goal
from app.models.health import UserPreference
from app.schemas.onboarding import ExpenseSetup, GoalSetup, IncomeSetup, SpendingStyleSetup

router = APIRouter()


@router.post("/income")
async def setup_income(
    data: IncomeSetup,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
):
    """Step 1: Set up income profile."""
    current_user.monthly_salary = data.amount
    current_user.pay_cycle_day = data.pay_day
    await db.flush()
    return {"message": "Income profile saved"}


@router.post("/expenses")
async def setup_expenses(
    data: ExpenseSetup,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
):
    """Step 2: Set up recurring expenses."""
    from app.models.transaction import RecurrenceFrequency, TransactionType as TxnType
    rules = []
    for expense in data.expenses:
        freq_str = expense.frequency if expense.frequency else "monthly"
        try:
            freq = RecurrenceFrequency(freq_str)
        except ValueError:
            freq = RecurrenceFrequency.MONTHLY
        rule = RecurringRule(
            user_id=current_user.id,
            description=expense.description,
            amount=expense.amount,
            frequency=freq,
            start_date=expense.start_date,
            transaction_type=TxnType.EXPENSE,
            is_active=True,
        )
        db.add(rule)
        rules.append(rule)
    await db.flush()
    return {"message": f"{len(rules)} recurring expenses saved"}


@router.post("/goals")
async def setup_goals(
    data: GoalSetup,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
):
    """Step 3: Set up financial goals."""
    goals = []
    for g in data.goals:
        goal = Goal(
            user_id=current_user.id,
            name=g.name,
            target_amount=g.target_amount,
            target_date=g.target_date,
        )
        db.add(goal)
        goals.append(goal)
    await db.flush()
    return {"message": f"{len(goals)} goals created"}


@router.post("/spending-style")
async def setup_spending_style(
    data: SpendingStyleSetup,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
):
    """Step 4: Set spending behavior preferences."""
    import json
    from sqlalchemy import select

    # Upsert: check if preference already exists for this user
    result = await db.execute(
        select(UserPreference).where(UserPreference.user_id == current_user.id)
    )
    pref = result.scalars().first()

    categories_json = json.dumps(data.overspending_categories) if data.overspending_categories else None

    if pref:
        # Update existing preference
        pref.top_expense_categories = categories_json
        pref.spending_style = "moderate"
    else:
        # Create new preference
        pref = UserPreference(
            user_id=current_user.id,
            top_expense_categories=categories_json,
            spending_style="moderate",
        )
        db.add(pref)

    await db.flush()
    return {"message": "Preferences saved"}


@router.post("/complete")
async def complete_onboarding(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
):
    """Finalize onboarding — mark complete."""
    current_user.is_onboarded = True
    await db.flush()

    return {
        "message": "Welcome to Finance Buddy! 🎉",
        "onboarding_completed": True,
    }
