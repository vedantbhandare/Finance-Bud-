from __future__ import annotations

from decimal import Decimal

from app.domain.budgets import BudgetInput, generate_budget
from app.domain.categories import categorize_text
from app.domain.health import health_label, health_score, recommendations


def test_categorization_is_india_aware():
    assert categorize_text("Paid on Swiggy") == "Swiggy/Zomato"
    assert categorize_text("Namma Yatri ride") == "Auto/Riksha"
    assert categorize_text("Unknown merchant") is None


def test_budget_generation_respects_income_and_fixed_expenses():
    lines = generate_budget(
        BudgetInput(
            monthly_income=Decimal("50000"),
            fixed_expenses=(("Rent/Housing", Decimal("15000")),),
            monthly_goal_need=Decimal("5000"),
            overspending_categories=("Eating Out",),
        )
    )
    assert lines
    assert sum(line.amount for line in lines) <= Decimal("50000")
    assert any(line.category_name == "Rent/Housing" for line in lines)


def test_health_rules():
    assert health_score(Decimal("20"), Decimal("100"), Decimal("100"), Decimal("6")) == 100
    assert health_label(70) == "Good"
    assert recommendations(Decimal("5"), Decimal("60"), Decimal("20"))
