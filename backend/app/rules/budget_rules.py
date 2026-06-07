"""Budget rules — deterministic budget generation using modified 50/30/20 rule.

This module contains PURE FUNCTIONS only.
No database access. No AI calls. No side effects.
Fully unit-testable.
"""
from dataclasses import dataclass, field
from decimal import Decimal, ROUND_HALF_UP


@dataclass
class BudgetInput:
    monthly_income: Decimal
    fixed_expenses: list[dict]  # [{"category": str, "amount": Decimal}]
    goals: list[dict]           # [{"name": str, "monthly_contribution": Decimal}]
    spending_history: dict = field(default_factory=dict)  # {category: avg_monthly_spend}
    spending_style: list[str] = field(default_factory=list)  # self-reported overspending categories


@dataclass
class BudgetAllocation:
    category: str
    allocated: Decimal
    reasoning: str


# Default discretionary categories with suggested weights
DISCRETIONARY_CATEGORIES = {
    "Eating Out": Decimal("0.15"),
    "Groceries/Kirana": Decimal("0.20"),
    "Auto/Riksha": Decimal("0.10"),
    "Cab/Uber/Ola": Decimal("0.05"),
    "Shopping": Decimal("0.10"),
    "Entertainment": Decimal("0.08"),
    "Chai/Coffee": Decimal("0.05"),
    "Swiggy/Zomato": Decimal("0.07"),
    "Health/Medical": Decimal("0.05"),
    "Personal Care": Decimal("0.05"),
    "Other": Decimal("0.10"),
}


def generate_budget(input: BudgetInput) -> list[BudgetAllocation]:
    """Generate a budget using a modified 50/30/20 approach.

    Strategy:
    1. Fixed expenses are allocated first (non-negotiable)
    2. Goal contributions come next (up to 30% of remaining)
    3. Emergency buffer (10% of remaining after goals)
    4. Discretionary spending distributed by weighted categories
    5. Overspending categories get reduced allocations (-20%)
    """
    allocations: list[BudgetAllocation] = []
    remaining = input.monthly_income

    if remaining <= 0:
        return [BudgetAllocation(
            category="Error",
            allocated=Decimal("0"),
            reasoning="Monthly income must be positive",
        )]

    # === Step 1: Fixed expenses (non-negotiable) ===
    total_fixed = Decimal("0")
    for expense in input.fixed_expenses:
        amount = Decimal(str(expense["amount"]))
        allocations.append(BudgetAllocation(
            category=expense["category"],
            allocated=amount,
            reasoning="Fixed recurring expense — non-negotiable",
        ))
        total_fixed += amount
        remaining -= amount

    if remaining <= 0:
        allocations.append(BudgetAllocation(
            category="⚠️ Warning",
            allocated=Decimal("0"),
            reasoning="Fixed expenses exceed income. Review your commitments.",
        ))
        return allocations

    # === Step 2: Goal contributions (max 30% of post-fixed remaining) ===
    max_goal_budget = remaining * Decimal("0.30")
    total_goals = Decimal("0")
    for goal in input.goals:
        contribution = Decimal(str(goal.get("monthly_contribution", 0)))
        if contribution <= 0:
            continue
        # Cap individual goal at remaining goal budget
        actual = min(contribution, max_goal_budget - total_goals)
        if actual <= 0:
            break
        allocations.append(BudgetAllocation(
            category=f"🎯 Goal: {goal['name']}",
            allocated=actual,
            reasoning=f"Monthly savings toward \"{goal['name']}\"",
        ))
        total_goals += actual
        remaining -= actual

    # === Step 3: Emergency buffer (10% of remaining) ===
    buffer = (remaining * Decimal("0.10")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    allocations.append(BudgetAllocation(
        category="🛡️ Emergency Buffer",
        allocated=buffer,
        reasoning="Safety margin for unexpected expenses (10% of discretionary)",
    ))
    remaining -= buffer

    # === Step 4: Savings (20% of remaining if possible) ===
    savings = (remaining * Decimal("0.20")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    allocations.append(BudgetAllocation(
        category="💰 Savings",
        allocated=savings,
        reasoning="General savings — building financial resilience",
    ))
    remaining -= savings

    # === Step 5: Discretionary spending ===
    if remaining > 0:
        # Adjust weights based on spending history and self-reported style
        weights = dict(DISCRETIONARY_CATEGORIES)

        # Reduce allocation for self-reported overspending categories
        for cat in input.spending_style:
            if cat in weights:
                weights[cat] = weights[cat] * Decimal("0.80")  # 20% reduction

        # Normalize weights
        total_weight = sum(weights.values())
        for cat, weight in weights.items():
            amount = (remaining * weight / total_weight).quantize(
                Decimal("0.01"), rounding=ROUND_HALF_UP
            )
            overspend_note = " (reduced — you tend to overspend here)" if cat in input.spending_style else ""
            allocations.append(BudgetAllocation(
                category=cat,
                allocated=amount,
                reasoning=f"Discretionary spending{overspend_note}",
            ))

    return allocations
