from __future__ import annotations

from decimal import Decimal


def clamp(value: Decimal, low: Decimal = Decimal("0"), high: Decimal = Decimal("100")) -> Decimal:
    return max(low, min(high, value))


def health_score(
    savings_rate: Decimal,
    budget_adherence: Decimal,
    goal_progress: Decimal,
    emergency_months: Decimal = Decimal("0"),
    debt_to_income: Decimal = Decimal("0"),
) -> int:
    """Compute a 0-100 financial health score from five weighted components."""
    savings_component = clamp((savings_rate / Decimal("20")) * Decimal("100"))
    adherence_component = clamp(budget_adherence)
    goal_component = clamp(goal_progress)
    emergency_component = clamp((emergency_months / Decimal("6")) * Decimal("100"))
    debt_component = Decimal("100") - clamp((debt_to_income / Decimal("50")) * Decimal("100"))

    weighted = (
        savings_component * Decimal("0.25")
        + adherence_component * Decimal("0.25")
        + goal_component * Decimal("0.20")
        + emergency_component * Decimal("0.15")
        + debt_component * Decimal("0.15")
    )
    return int(weighted.quantize(Decimal("1")))


def health_label(score: int) -> str:
    if score >= 80:
        return "Excellent"
    if score >= 65:
        return "Good"
    if score >= 50:
        return "Fair"
    if score >= 35:
        return "Needs Attention"
    return "Critical"


def spending_trend(current_expenses: Decimal, previous_expenses: Decimal) -> str:
    """Compare current-month expenses to previous month.

    Returns one of: 'decreasing', 'stable', 'increasing', 'insufficient_data'.
    Uses a 15% threshold to filter noise.
    """
    if previous_expenses <= 0:
        return "insufficient_data"
    change_pct = (current_expenses - previous_expenses) / previous_expenses * Decimal("100")
    if change_pct > Decimal("15"):
        return "increasing"
    if change_pct < Decimal("-15"):
        return "decreasing"
    return "stable"


def recommendations(
    savings_rate: Decimal,
    budget_adherence: Decimal,
    goal_progress: Decimal,
    spending_trend_label: str = "stable",
    days_remaining: int = 15,
    top_overspent_categories: list[str] | None = None,
) -> list[str]:
    """Generate contextual, actionable financial recommendations.

    Goes beyond the old 3-recommendation ceiling to provide tiered savings
    advice, spending-trend awareness, category-level callouts, and
    end-of-month urgency alerts.
    """
    output: list[str] = []

    # --- Savings guidance (tiered) ---
    if savings_rate < Decimal("5"):
        output.append(
            "Your savings rate is critically low. Start with even ₹500/month "
            "into a recurring deposit to build the habit."
        )
    elif savings_rate < Decimal("10"):
        output.append(
            "Savings are below 10%. Set up a small auto-transfer to a savings "
            "account on pay day."
        )
    elif savings_rate < Decimal("20"):
        output.append(
            "Good start — push toward 20% by automating an SIP or RD."
        )

    # --- Budget adherence ---
    if budget_adherence < Decimal("50"):
        output.append(
            "Budget adherence is below 50%. Identify the two largest overruns "
            "and set tighter daily spending caps."
        )
    elif budget_adherence < Decimal("75"):
        output.append(
            "You're moderately over budget. Review flexible categories and "
            "trim the biggest outlier."
        )
    elif budget_adherence < Decimal("90"):
        output.append(
            "Almost on track — a small cut in discretionary spending will "
            "bring you in line."
        )

    # --- Goal progress ---
    if goal_progress < Decimal("15"):
        output.append(
            "Goal progress is very low. Add a recurring ₹500–₹1,000/month "
            "contribution to your top goal."
        )
    elif goal_progress < Decimal("40"):
        output.append(
            "Increase goal contributions — even small bumps compound over time."
        )

    # --- Spending trend ---
    if spending_trend_label == "increasing":
        output.append(
            "Spending is trending upward vs. last month. Check dining and "
            "shopping categories for lifestyle creep."
        )
    elif spending_trend_label == "decreasing":
        output.append(
            "Great discipline — spending is trending down. Redirect the "
            "surplus into savings or goals."
        )

    # --- Overspent categories ---
    if top_overspent_categories:
        cats = ", ".join(top_overspent_categories[:3])
        output.append(f"Watch out for {cats} — running ahead of budget pace.")

    # --- End-of-month urgency ---
    if days_remaining <= 5 and budget_adherence < Decimal("85"):
        output.append(
            f"Only {days_remaining} days left this month. Stick to essentials "
            f"to finish on target."
        )
    elif days_remaining <= 10 and budget_adherence < Decimal("75"):
        output.append(
            f"{days_remaining} days left and budget is strained. Postpone "
            f"non-essential purchases."
        )

    if not output:
        output.append(
            "Your financial habits are solid. Keep the current rhythm and "
            "review your goals quarterly."
        )
    return output
