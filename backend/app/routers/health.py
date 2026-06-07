"""Health router — financial health score and history."""
from datetime import date
from decimal import Decimal

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db_session
from app.dependencies import get_current_user
from app.models.user import User
from app.rules.health_rules import compute_health_score, get_health_label, get_health_recommendations

router = APIRouter()


@router.get("/score")
async def get_health_score(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
):
    """Get current financial health score using real user data."""
    from app.services.transaction_service import TransactionService

    txn_service = TransactionService(db)
    today = date.today()

    try:
        monthly = await txn_service.get_monthly_summary(
            current_user.id, today.year, today.month
        )
        total_income = monthly.get("total_income", 0)
        total_expenses = monthly.get("total_expenses", 0)
    except Exception:
        total_income = 0
        total_expenses = 0

    # Compute savings rate
    if total_income > 0:
        savings_rate = Decimal(str(((total_income - total_expenses) / total_income) * 100))
    else:
        savings_rate = Decimal("0")

    # Simple budget adherence (% of income not overspent)
    budget_adherence = Decimal("70") if total_expenses <= total_income else Decimal("30")

    # Goal progress placeholder
    goal_progress = Decimal("50")

    score = compute_health_score(
        savings_rate=savings_rate,
        budget_adherence=budget_adherence,
        goal_progress=goal_progress,
    )

    return {
        "overall_score": score,
        "label": get_health_label(score),
        "savings_rate": float(savings_rate),
        "budget_adherence": float(budget_adherence),
        "goal_progress": float(goal_progress),
        "spending_trend": "stable" if total_expenses <= total_income else "overspending",
        "recommendations": get_health_recommendations(savings_rate, budget_adherence, goal_progress),
    }


@router.get("/history")
async def get_health_history(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
):
    """Get health score history."""
    return {"snapshots": []}
