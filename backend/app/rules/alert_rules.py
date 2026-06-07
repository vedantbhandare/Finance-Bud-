"""Alert rules — overspending detection and velocity alerts.

Pure functions. No DB, no AI, no side effects.
"""
from dataclasses import dataclass
from decimal import Decimal


@dataclass
class SpendingAlert:
    category: str
    alert_type: str  # "velocity", "exceeded", "approaching"
    message: str
    severity: str  # "info", "warning", "critical"


def check_budget_velocity(
    category: str,
    spent: Decimal,
    allocated: Decimal,
    day_of_month: int,
    days_in_month: int,
) -> SpendingAlert | None:
    """Check if spending velocity suggests overspending risk.

    If you've spent >X% of budget but the month is only Y% done,
    you're on track to overspend.
    """
    if allocated <= 0:
        return None

    utilization = spent / allocated * 100
    month_progress = Decimal(str(day_of_month / days_in_month * 100))

    # Already exceeded budget
    if utilization >= 100:
        return SpendingAlert(
            category=category,
            alert_type="exceeded",
            message=f"You've exceeded your {category} budget (₹{spent:,.0f} of ₹{allocated:,.0f}).",
            severity="critical",
        )

    # Spending faster than time passing (e.g., 60% spent but only 40% through month)
    if utilization > month_progress + 20:
        remaining = allocated - spent
        return SpendingAlert(
            category=category,
            alert_type="velocity",
            message=f"You've used {utilization:.0f}% of your {category} budget and the month is only {month_progress:.0f}% done. ₹{remaining:,.0f} remaining.",
            severity="warning",
        )

    # Approaching limit (>80% used)
    if utilization >= 80:
        remaining = allocated - spent
        return SpendingAlert(
            category=category,
            alert_type="approaching",
            message=f"Heads up: {category} budget is {utilization:.0f}% used. ₹{remaining:,.0f} left.",
            severity="info",
        )

    return None


def check_all_budgets(
    budget_status: list[dict],  # [{"category", "spent", "allocated"}]
    day_of_month: int,
    days_in_month: int,
) -> list[SpendingAlert]:
    """Check all budget categories for alerts."""
    alerts: list[SpendingAlert] = []
    for item in budget_status:
        alert = check_budget_velocity(
            category=item["category"],
            spent=Decimal(str(item["spent"])),
            allocated=Decimal(str(item["allocated"])),
            day_of_month=day_of_month,
            days_in_month=days_in_month,
        )
        if alert:
            alerts.append(alert)
    return alerts
