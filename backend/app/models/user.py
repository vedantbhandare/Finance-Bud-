"""User and IncomeProfile models."""

from __future__ import annotations

import uuid
from decimal import Decimal

from sqlalchemy import ForeignKey, Numeric, String, Text, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDMixin


class User(Base, UUIDMixin, TimestampMixin):
    """Application user account."""

    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(320), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(Text, nullable=False)
    full_name: Mapped[str] = mapped_column(String(200), nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True, server_default=text("true"))
    is_onboarded: Mapped[bool] = mapped_column(default=False, server_default=text("false"))

    # Onboarding fields stored directly on user (simpler than separate table for MVP)
    monthly_salary: Mapped[Decimal | None] = mapped_column(
        Numeric(14, 2), default=None, nullable=True,
    )
    pay_cycle_day: Mapped[int] = mapped_column(default=1, server_default=text("1"))

    # Relationships
    categories: Mapped[list["Category"]] = relationship(  # noqa: F821
        back_populates="user", cascade="all, delete-orphan",
    )
    transactions: Mapped[list["Transaction"]] = relationship(  # noqa: F821
        back_populates="user", cascade="all, delete-orphan",
    )
    recurring_rules: Mapped[list["RecurringRule"]] = relationship(  # noqa: F821
        back_populates="user", cascade="all, delete-orphan",
    )
    goals: Mapped[list["Goal"]] = relationship(  # noqa: F821
        back_populates="user", cascade="all, delete-orphan",
    )
    budget_plans: Mapped[list["BudgetPlan"]] = relationship(  # noqa: F821
        back_populates="user", cascade="all, delete-orphan",
    )
    conversations: Mapped[list["Conversation"]] = relationship(  # noqa: F821
        back_populates="user", cascade="all, delete-orphan",
    )
    health_snapshots: Mapped[list["HealthSnapshot"]] = relationship(  # noqa: F821
        back_populates="user", cascade="all, delete-orphan",
    )
    preferences: Mapped["UserPreference | None"] = relationship(  # noqa: F821
        back_populates="user", uselist=False, cascade="all, delete-orphan",
    )
