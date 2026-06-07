"""Transaction, RecurringRule, and Category models."""

from __future__ import annotations

import enum
import uuid
from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import (
    Date,
    Enum,
    ForeignKey,
    Index,
    Numeric,
    String,
    Text,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDMixin


class TransactionType(str, enum.Enum):
    EXPENSE = "expense"
    INCOME = "income"
    TRANSFER = "transfer"


class CategoryType(str, enum.Enum):
    NEED = "need"
    WANT = "want"
    SAVING = "saving"
    INCOME = "income"


class RecurrenceFrequency(str, enum.Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    BIWEEKLY = "biweekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    YEARLY = "yearly"


class Category(Base, UUIDMixin, TimestampMixin):
    """Transaction categories — seeded + user-customisable."""

    __tablename__ = "categories"

    user_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    icon: Mapped[str | None] = mapped_column(String(50), nullable=True)
    category_type: Mapped[CategoryType] = mapped_column(
        Enum(CategoryType, name="category_type_enum"),
        nullable=False,
    )
    is_system: Mapped[bool] = mapped_column(default=False, server_default=text("false"))

    # Relationships
    user: Mapped["User | None"] = relationship(back_populates="categories")  # noqa: F821
    transactions: Mapped[list["Transaction"]] = relationship(back_populates="category")

    __table_args__ = (
        Index("ix_categories_user_name", "user_id", "name", unique=True),
    )


class Transaction(Base, UUIDMixin, TimestampMixin):
    """Individual financial transaction."""

    __tablename__ = "transactions"

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    category_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("categories.id", ondelete="SET NULL"),
        nullable=True,
    )
    amount: Mapped[Decimal] = mapped_column(Numeric(14, 2), nullable=False)
    transaction_type: Mapped[TransactionType] = mapped_column(
        Enum(TransactionType, name="transaction_type_enum"),
        nullable=False,
    )
    description: Mapped[str | None] = mapped_column(String(500), nullable=True)
    merchant: Mapped[str | None] = mapped_column(String(200), nullable=True)
    transaction_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_recurring: Mapped[bool] = mapped_column(default=False, server_default=text("false"))
    source: Mapped[str] = mapped_column(String(50), default="manual", server_default=text("'manual'"))
    recurring_rule_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("recurring_rules.id", ondelete="SET NULL"),
        nullable=True,
    )

    # Relationships
    user: Mapped["User"] = relationship(back_populates="transactions")  # noqa: F821
    category: Mapped[Category | None] = relationship(back_populates="transactions")
    recurring_rule: Mapped["RecurringRule | None"] = relationship(back_populates="transactions")

    __table_args__ = (
        Index("ix_transactions_user_date", "user_id", "transaction_date"),
    )


class RecurringRule(Base, UUIDMixin, TimestampMixin):
    """Rule for auto-generating recurring transactions."""

    __tablename__ = "recurring_rules"

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    category_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("categories.id", ondelete="SET NULL"),
        nullable=True,
    )
    amount: Mapped[Decimal] = mapped_column(Numeric(14, 2), nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=False)
    frequency: Mapped[RecurrenceFrequency] = mapped_column(
        Enum(RecurrenceFrequency, name="recurrence_frequency_enum"),
        nullable=False,
    )
    start_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    end_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    next_due_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    is_active: Mapped[bool] = mapped_column(default=True, server_default=text("true"))
    transaction_type: Mapped[TransactionType] = mapped_column(
        Enum(TransactionType, name="transaction_type_enum", create_type=False),
        nullable=False,
        default=TransactionType.EXPENSE,
    )

    # Relationships
    user: Mapped["User"] = relationship(back_populates="recurring_rules")  # noqa: F821
    category: Mapped[Category | None] = relationship()
    transactions: Mapped[list[Transaction]] = relationship(back_populates="recurring_rule")
