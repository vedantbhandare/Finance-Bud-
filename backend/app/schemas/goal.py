"""Goal schemas."""

from __future__ import annotations

import uuid
from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from app.models.goal import GoalStatus


class GoalCreate(BaseModel):
    """Payload to create a goal."""

    name: str = Field(min_length=1, max_length=200)
    description: str | None = None
    target_amount: Decimal = Field(gt=0, max_digits=14, decimal_places=2)
    target_date: date | None = None
    icon: str | None = None


class GoalUpdate(BaseModel):
    """Payload to update a goal (all optional)."""

    name: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = None
    target_amount: Decimal | None = Field(default=None, gt=0, max_digits=14, decimal_places=2)
    target_date: date | None = None
    icon: str | None = None
    status: GoalStatus | None = None


class GoalResponse(BaseModel):
    """Goal response."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    description: str | None
    target_amount: Decimal
    current_amount: Decimal
    target_date: date | None
    icon: str | None
    status: GoalStatus
    progress_pct: Decimal
    remaining_amount: Decimal
    created_at: datetime


class ContributionCreate(BaseModel):
    """Payload to create a goal contribution."""

    amount: Decimal = Field(gt=0, max_digits=14, decimal_places=2)
    contribution_date: date
    notes: str | None = None


class ContributionResponse(BaseModel):
    """Goal contribution response."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    goal_id: uuid.UUID
    amount: Decimal
    contribution_date: date
    notes: str | None
    created_at: datetime
