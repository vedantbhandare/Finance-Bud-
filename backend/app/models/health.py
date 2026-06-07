"""HealthSnapshot and UserPreference models."""

from __future__ import annotations

import uuid
from datetime import date
from decimal import Decimal

from sqlalchemy import Date, ForeignKey, Index, Numeric, String, Text, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDMixin


class HealthSnapshot(Base, UUIDMixin, TimestampMixin):
    """Point-in-time financial health score for a user."""

    __tablename__ = "health_snapshots"

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    snapshot_date: Mapped[date] = mapped_column(Date, nullable=False)
    overall_score: Mapped[int] = mapped_column(nullable=False)  # 0-100
    savings_score: Mapped[int] = mapped_column(nullable=False)
    budget_adherence_score: Mapped[int] = mapped_column(nullable=False)
    goal_progress_score: Mapped[int] = mapped_column(nullable=False)
    spending_consistency_score: Mapped[int] = mapped_column(nullable=False)
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Relationships
    user: Mapped["User"] = relationship(back_populates="health_snapshots")  # noqa: F821

    __table_args__ = (
        Index("ix_health_snapshots_user_date", "user_id", "snapshot_date", unique=True),
    )


class UserPreference(Base, UUIDMixin, TimestampMixin):
    """User-specific preferences and onboarding selections."""

    __tablename__ = "user_preferences"

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )
    spending_style: Mapped[str | None] = mapped_column(
        String(50), nullable=True,
    )  # "frugal", "moderate", "generous"
    top_expense_categories: Mapped[str | None] = mapped_column(
        Text, nullable=True,
    )  # JSON-encoded list
    financial_goals_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    monthly_savings_target_pct: Mapped[Decimal] = mapped_column(
        Numeric(5, 2), default=Decimal("20"), server_default=text("20"),
    )
    preferred_budget_strategy: Mapped[str] = mapped_column(
        String(50), default="50/30/20", server_default=text("'50/30/20'"),
    )

    # Relationships
    user: Mapped["User"] = relationship(back_populates="preferences")  # noqa: F821
