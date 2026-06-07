"""Onboarding step schemas."""

from __future__ import annotations

from datetime import date
from decimal import Decimal

from pydantic import BaseModel, Field


class IncomeSetup(BaseModel):
    """Step 1 — income details."""

    amount: Decimal = Field(gt=0, max_digits=14, decimal_places=2)
    source_name: str | None = Field(default="Primary", max_length=100)
    frequency: str = Field(default="monthly", pattern="^(monthly|biweekly|weekly)$")
    pay_day: int = Field(default=1, ge=1, le=28)


class ExpenseItem(BaseModel):
    """Single recurring expense."""

    description: str = Field(min_length=1, max_length=200)
    amount: Decimal = Field(gt=0, max_digits=14, decimal_places=2)
    frequency: str = Field(default="monthly")
    start_date: date | None = None


class ExpenseSetup(BaseModel):
    """Step 2 — recurring expenses."""

    expenses: list[ExpenseItem] = Field(default_factory=list)


class GoalItem(BaseModel):
    """Single financial goal."""

    name: str = Field(min_length=1, max_length=200)
    target_amount: Decimal = Field(gt=0, max_digits=14, decimal_places=2)
    target_date: date | None = None
    priority: int | None = Field(default=1, ge=1, le=10)


class GoalSetup(BaseModel):
    """Step 3 — financial goals."""

    goals: list[GoalItem] = Field(default_factory=list)


class SpendingStyleSetup(BaseModel):
    """Step 4 — spending personality."""

    overspending_categories: list[str] = Field(default_factory=list)
    ai_personality: str | None = Field(default="balanced")
