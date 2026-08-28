from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import Decimal

from app.domain.money import money


def monthly_goal_contribution(
    target: Decimal,
    current: Decimal,
    target_date: date | None,
    today: date | None = None,
) -> Decimal:
    """Compute the monthly contribution needed to hit a goal by its target date.

    If no target_date is set, defaults to spreading over 12 months.
    Never returns a negative or zero-division result.
    """
    remaining = max(Decimal("0"), target - current)
    if remaining <= 0:
        return Decimal("0.00")
    if not target_date:
        return money(remaining / Decimal("12"))
    ref = today or date.today()
    months_left = max(1, (target_date.year - ref.year) * 12 + (target_date.month - ref.month))
    return money(remaining / Decimal(str(months_left)))


@dataclass(frozen=True)
class BudgetInput:
    monthly_income: Decimal
    fixed_expenses: tuple[tuple[str, Decimal], ...]
    monthly_goal_need: Decimal
    overspending_categories: tuple[str, ...] = ()


@dataclass(frozen=True)
class BudgetLine:
    category_name: str
    amount: Decimal
    reasoning: str


BASE_DISCRETIONARY_WEIGHTS: dict[str, Decimal] = {
    "Groceries/Kirana": Decimal("0.30"),
    "Eating Out": Decimal("0.18"),
    "Swiggy/Zomato": Decimal("0.12"),
    "Auto/Riksha": Decimal("0.12"),
    "Cab/Uber/Ola": Decimal("0.08"),
    "Shopping": Decimal("0.10"),
    "Entertainment": Decimal("0.06"),
    "Other": Decimal("0.04"),
}


def generate_budget(input_data: BudgetInput) -> tuple[BudgetLine, ...]:
    income = money(input_data.monthly_income)
    if income <= 0:
        return ()

    lines: list[BudgetLine] = []
    fixed_total = Decimal("0.00")
    for category_name, amount in input_data.fixed_expenses:
        clean_amount = money(amount)
        if clean_amount <= 0:
            continue
        fixed_total += clean_amount
        lines.append(BudgetLine(category_name, clean_amount, "Recurring fixed expense."))

    if fixed_total >= income:
        return tuple(lines)

    remaining = income - fixed_total

    goal_cap = remaining * Decimal("0.30")
    goal_amount = min(money(input_data.monthly_goal_need), money(goal_cap))
    if goal_amount > 0:
        lines.append(BudgetLine("Goals", goal_amount, "Goal contribution capped at 30% after fixed expenses."))
        remaining -= goal_amount

    emergency = money(remaining * Decimal("0.10"))
    if emergency > 0:
        lines.append(BudgetLine("Emergency Fund", emergency, "Emergency buffer from flexible money."))
        remaining -= emergency

    savings = money(remaining * Decimal("0.20"))
    if savings > 0:
        lines.append(BudgetLine("Savings", savings, "Baseline monthly savings allocation."))
        remaining -= savings

    overspending = {name.lower() for name in input_data.overspending_categories}
    weights: dict[str, Decimal] = {}
    total_weight = Decimal("0")
    for category_name, weight in BASE_DISCRETIONARY_WEIGHTS.items():
        adjusted = weight * (Decimal("0.80") if category_name.lower() in overspending else Decimal("1"))
        weights[category_name] = adjusted
        total_weight += adjusted

    if remaining > 0 and total_weight > 0:
        allocated = Decimal("0")
        for category_name, weight in weights.items():
            allocation = money(remaining * (weight / total_weight))
            
            # Prevent allocating more than what is left
            if allocated + allocation > remaining:
                allocation = remaining - allocated
                
            if allocation > 0:
                lines.append(BudgetLine(category_name, allocation, "Weighted flexible spending allocation."))
                allocated += allocation

    return tuple(lines)

