"""Goal and GoalContribution models."""

from __future__ import annotations

import enum
import uuid
from datetime import date
from decimal import Decimal

from sqlalchemy import Date, Enum, ForeignKey, Numeric, String, Text, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDMixin


class GoalStatus(str, enum.Enum):
    ACTIVE = "active"
    COMPLETED = "completed"
    PAUSED = "paused"
    CANCELLED = "cancelled"


class Goal(Base, UUIDMixin, TimestampMixin):
    """Savings or financial goal set by a user."""

    __tablename__ = "goals"

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    target_amount: Mapped[Decimal] = mapped_column(Numeric(14, 2), nullable=False)
    current_amount: Mapped[Decimal] = mapped_column(
        Numeric(14, 2), default=Decimal("0"), server_default=text("0"),
    )
    target_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    icon: Mapped[str | None] = mapped_column(String(50), nullable=True)
    status: Mapped[GoalStatus] = mapped_column(
        Enum(GoalStatus, name="goal_status_enum"),
        default=GoalStatus.ACTIVE,
        server_default=text("'active'"),
    )

    # Relationships
    user: Mapped["User"] = relationship(back_populates="goals")  # noqa: F821
    contributions: Mapped[list["GoalContribution"]] = relationship(
        back_populates="goal", cascade="all, delete-orphan",
    )

    @property
    def progress_pct(self) -> Decimal:
        if self.target_amount == 0:
            return Decimal("100")
        return ((self.current_amount / self.target_amount) * 100).quantize(Decimal("0.01"))

    @property
    def remaining_amount(self) -> Decimal:
        return max(self.target_amount - self.current_amount, Decimal("0"))


class GoalContribution(Base, UUIDMixin, TimestampMixin):
    """A single contribution towards a goal."""

    __tablename__ = "goal_contributions"

    goal_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("goals.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    amount: Mapped[Decimal] = mapped_column(Numeric(14, 2), nullable=False)
    contribution_date: Mapped[date] = mapped_column(Date, nullable=False)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Relationships
    goal: Mapped[Goal] = relationship(back_populates="contributions")
