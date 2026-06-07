"""Health score rules — deterministic financial health computation.

Pure functions. No DB, no AI, no side effects.
"""
from decimal import Decimal


def compute_health_score(
    savings_rate: Decimal,
    budget_adherence: Decimal,
    goal_progress: Decimal,
    emergency_fund_months: Decimal = Decimal("0"),
    debt_to_income: Decimal = Decimal("0"),
) -> int:
    """Compute financial health score (0-100).

    Weights:
    - Savings rate: 25% (20%+ is excellent)
    - Budget adherence: 25% (% of categories within limit)
    - Goal progress: 20% (on-track percentage)
    - Emergency fund: 15% (6 months is excellent)
    - Debt-to-income: 15% (lower is better)
    """
    score = Decimal("0")

    # Savings rate: 20%+ = 100 score
    savings_score = min(savings_rate / Decimal("20") * 100, Decimal("100"))
    score += savings_score * Decimal("0.25")

    # Budget adherence: direct percentage (0-100)
    adherence_score = min(max(budget_adherence, Decimal("0")), Decimal("100"))
    score += adherence_score * Decimal("0.25")

    # Goal progress: on-track percentage (0-100)
    goal_score = min(max(goal_progress, Decimal("0")), Decimal("100"))
    score += goal_score * Decimal("0.20")

    # Emergency fund: 6 months = 100 score
    ef_score = min(emergency_fund_months / Decimal("6") * 100, Decimal("100"))
    score += ef_score * Decimal("0.15")

    # Debt-to-income: 0% = 100, 40%+ = 0
    dti_score = max(Decimal("100") - (debt_to_income * Decimal("2.5")), Decimal("0"))
    score += dti_score * Decimal("0.15")

    return max(0, min(100, int(score)))


def get_health_label(score: int) -> str:
    """Human-readable label for a health score."""
    if score >= 80:
        return "Excellent"
    elif score >= 65:
        return "Good"
    elif score >= 50:
        return "Fair"
    elif score >= 35:
        return "Needs Attention"
    else:
        return "Critical"


def get_health_recommendations(
    savings_rate: Decimal,
    budget_adherence: Decimal,
    goal_progress: Decimal,
) -> list[str]:
    """Generate actionable recommendations based on health metrics."""
    recs: list[str] = []

    if savings_rate < Decimal("10"):
        recs.append("Your savings rate is below 10%. Try to save at least 20% of income.")
    elif savings_rate < Decimal("20"):
        recs.append("Good start on saving! Push toward 20% for long-term financial health.")

    if budget_adherence < Decimal("60"):
        recs.append("You're overspending in multiple budget categories. Focus on the top 2-3 areas.")
    elif budget_adherence < Decimal("80"):
        recs.append("Most budget categories are on track. A few need attention.")

    if goal_progress < Decimal("50"):
        recs.append("You're behind on your financial goals. Consider increasing monthly contributions.")

    if not recs:
        recs.append("You're doing great! Keep up the financial discipline. 💪")

    return recs
