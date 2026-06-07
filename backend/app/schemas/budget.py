"""Budget schemas."""

from __future__ import annotations

import uuid
from datetime import date
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class BudgetAllocationResponse(BaseModel):
    """Single category allocation in a budget plan."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    category_id: uuid.UUID
    category_name: str | None = None
    allocated_amount: Decimal
    spent_amount: Decimal
    remaining: Decimal
    utilisation_pct: Decimal


class BudgetPlanResponse(BaseModel):
    """Full budget plan with allocations."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    month_start: date
    month_end: date
    total_income: Decimal
    needs_pct: Decimal
    wants_pct: Decimal
    savings_pct: Decimal
    needs_amount: Decimal
    wants_amount: Decimal
    savings_amount: Decimal
    total_allocated: Decimal
    status: str
    is_ai_generated: bool
    ai_reasoning: str | None = None
    allocations: list[BudgetAllocationResponse] = []


class BudgetGenerateRequest(BaseModel):
    """Optional overrides when generating a budget."""

    needs_pct: Decimal | None = None
    wants_pct: Decimal | None = None
    savings_pct: Decimal | None = None


class BudgetGenerateResponse(BaseModel):
    """Response after generating a new budget plan."""

    plan: BudgetPlanResponse
    message: str = "Budget plan generated successfully"
