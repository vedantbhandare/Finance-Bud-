"""Health scorer — computes financial health score from deterministic rules."""
from decimal import Decimal
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.health import HealthSnapshot
from app.rules.health_rules import compute_health_score


class HealthScorer:
    """Computes and stores financial health scores."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def compute_and_store(
        self,
        user_id: UUID,
        savings_rate: Decimal,
        budget_adherence: Decimal,
        goal_progress: Decimal,
        emergency_fund_months: Decimal = Decimal("0"),
        debt_to_income: Decimal = Decimal("0"),
    ) -> HealthSnapshot:
        """Compute health score using deterministic rules and persist."""
        from datetime import date

        score = compute_health_score(
            savings_rate=savings_rate,
            budget_adherence=budget_adherence,
            goal_progress=goal_progress,
            emergency_fund_months=emergency_fund_months,
            debt_to_income=debt_to_income,
        )

        # Determine trend based on last snapshot
        trend = "stable"

        # Convert Decimal metrics to int scores clamped 0-100
        _sav = max(0, min(100, int(savings_rate)))
        _adh = max(0, min(100, int(budget_adherence)))
        _goal = max(0, min(100, int(goal_progress)))
        # Map trend label to a numeric consistency score (stable → 50)
        _consistency = 50  # default for "stable"

        breakdown_dict = {
            "savings_rate": float(savings_rate),
            "budget_adherence": float(budget_adherence),
            "goal_progress": float(goal_progress),
            "emergency_fund_months": float(emergency_fund_months),
            "debt_to_income": float(debt_to_income),
        }

        import json
        snapshot = HealthSnapshot(
            user_id=user_id,
            snapshot_date=date.today(),
            overall_score=score,
            savings_score=_sav,
            budget_adherence_score=_adh,
            goal_progress_score=_goal,
            spending_consistency_score=_consistency,
            summary=json.dumps(breakdown_dict),
        )
        self.db.add(snapshot)
        await self.db.flush()
        return snapshot
