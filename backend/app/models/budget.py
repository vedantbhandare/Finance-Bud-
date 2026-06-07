"""BudgetPlan and BudgetAllocation models."""

from __future__ import annotations

import enum
import uuid
from datetime import date
from decimal import Decimal

from sqlalchemy import Date, Enum, ForeignKey, Index, Numeric, String, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDMixin


class BudgetStatus(str, enum.Enum):
    ACTIVE = "active"
    EXPIRED = "expired"
    DRAFT = "draft"


class BudgetPlan(Base, UUIDMixin, TimestampMixin):
    """Monthly budget plan tied to a user."""

    __tablename__ = "budget_plans"

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    month_start: Mapped[date] = mapped_column(Date, nullable=False)
    month_end: Mapped[date] = mapped_column(Date, nullable=False)
    total_income: Mapped[Decimal] = mapped_column(Numeric(14, 2), nullable=False)
    needs_pct: Mapped[Decimal] = mapped_column(
        Numeric(5, 2), default=Decimal("50"), server_default=text("50"),
    )
    wants_pct: Mapped[Decimal] = mapped_column(
        Numeric(5, 2), default=Decimal("30"), server_default=text("30"),
    )
    savings_pct: Mapped[Decimal] = mapped_column(
        Numeric(5, 2), default=Decimal("20"), server_default=text("20"),
    )
    status: Mapped[BudgetStatus] = mapped_column(
        Enum(BudgetStatus, name="budget_status_enum"),
        default=BudgetStatus.ACTIVE,
        server_default=text("'active'"),
    )
    is_ai_generated: Mapped[bool] = mapped_column(default=True, server_default=text("1"))
    ai_reasoning: Mapped[str | None] = mapped_column(String, nullable=True)

    # Relationships
    user: Mapped["User"] = relationship(back_populates="budget_plans")  # noqa: F821
    allocations: Mapped[list["BudgetAllocation"]] = relationship(
        back_populates="budget_plan", cascade="all, delete-orphan",
    )

    __table_args__ = (
        Index("ix_budget_plans_user_month", "user_id", "month_start", unique=True),
    )

    @property
    def needs_amount(self) -> Decimal:
        return (self.total_income * self.needs_pct / Decimal("100")).quantize(Decimal("0.01"))

    @property
    def wants_amount(self) -> Decimal:
        return (self.total_income * self.wants_pct / Decimal("100")).quantize(Decimal("0.01"))

    @property
    def savings_amount(self) -> Decimal:
        return (self.total_income * self.savings_pct / Decimal("100")).quantize(Decimal("0.01"))

    @property
    def total_allocated(self) -> Decimal:
        return self.needs_amount + self.wants_amount + self.savings_amount


class BudgetAllocation(Base, UUIDMixin, TimestampMixin):
    """Per-category allocation within a budget plan."""

    __tablename__ = "budget_allocations"

    budget_plan_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("budget_plans.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    category_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("categories.id", ondelete="CASCADE"),
        nullable=True,
    )
    allocated_amount: Mapped[Decimal] = mapped_column(Numeric(14, 2), nullable=False)
    spent_amount: Mapped[Decimal] = mapped_column(
        Numeric(14, 2), default=Decimal("0"), server_default=text("0"),
    )

    # Relationships
    budget_plan: Mapped[BudgetPlan] = relationship(back_populates="allocations")
    category: Mapped["Category"] = relationship()  # noqa: F821

    @property
    def remaining(self) -> Decimal:
        return self.allocated_amount - self.spent_amount

    @property
    def utilisation_pct(self) -> Decimal:
        if self.allocated_amount == 0:
            return Decimal("0")
        return ((self.spent_amount / self.allocated_amount) * 100).quantize(Decimal("0.01"))
