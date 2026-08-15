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


def recommendations(savings_rate: Decimal, budget_adherence: Decimal, goal_progress: Decimal) -> list[str]:
    output: list[str] = []
    if savings_rate < Decimal("20"):
        output.append("Increase your savings rate toward 20% of income.")
    if budget_adherence < Decimal("80"):
        output.append("Review flexible spending and adjust categories that are ahead of pace.")
    if goal_progress < Decimal("50"):
        output.append("Add a small recurring contribution to your highest-priority goal.")
    if not output:
        output.append("Your core money habits look healthy. Keep the current rhythm.")
    return output

