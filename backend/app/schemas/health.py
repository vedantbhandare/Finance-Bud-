"""Health score schemas."""

from __future__ import annotations

import uuid
from datetime import date, datetime

from pydantic import BaseModel, ConfigDict


class HealthScoreResponse(BaseModel):
    """Current financial health score breakdown."""

    model_config = ConfigDict(from_attributes=True)

    overall_score: int
    savings_score: int
    budget_adherence_score: int
    goal_progress_score: int
    spending_consistency_score: int
    summary: str | None = None
    snapshot_date: date
    tips: list[str] = []


class HealthHistoryItem(BaseModel):
    """Historical health score entry."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    snapshot_date: date
    overall_score: int
    created_at: datetime
