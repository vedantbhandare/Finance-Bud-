from __future__ import annotations

from datetime import date
from decimal import Decimal

from sqlalchemy import Boolean, Date, ForeignKey, Index, Integer, Numeric, String, Text, UniqueConstraint, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.orm.base import Base, IdMixin, TimestampMixin


class User(Base, IdMixin, TimestampMixin):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(320), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(Text)
    full_name: Mapped[str] = mapped_column(String(200), default="User")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, server_default=text("1"))
    is_onboarded: Mapped[bool] = mapped_column(Boolean, default=False, server_default=text("0"))
    monthly_salary: Mapped[Decimal | None] = mapped_column(Numeric(14, 2), nullable=True)
    pay_cycle_day: Mapped[int] = mapped_column(Integer, default=1, server_default=text("1"))

    categories: Mapped[list[Category]] = relationship(back_populates="user", cascade="all, delete-orphan")
    transactions: Mapped[list[Transaction]] = relationship(back_populates="user", cascade="all, delete-orphan")
    recurring_rules: Mapped[list[RecurringRule]] = relationship(back_populates="user", cascade="all, delete-orphan")
    budget_plans: Mapped[list[BudgetPlan]] = relationship(back_populates="user", cascade="all, delete-orphan")
    goals: Mapped[list[Goal]] = relationship(back_populates="user", cascade="all, delete-orphan")
    conversations: Mapped[list[Conversation]] = relationship(back_populates="user", cascade="all, delete-orphan")
    preferences: Mapped[UserPreference | None] = relationship(back_populates="user", uselist=False, cascade="all, delete-orphan")


class Category(Base, IdMixin, TimestampMixin):
    __tablename__ = "categories"
    __table_args__ = (UniqueConstraint("user_id", "name", name="uq_category_user_name"),)

    user_id: Mapped[str | None] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=True, index=True)
    name: Mapped[str] = mapped_column(String(100))
    icon: Mapped[str | None] = mapped_column(String(50), nullable=True)
    category_type: Mapped[str] = mapped_column(String(20))
    is_system: Mapped[bool] = mapped_column(Boolean, default=False, server_default=text("0"))

    user: Mapped[User | None] = relationship(back_populates="categories")
    transactions: Mapped[list[Transaction]] = relationship(back_populates="category")


class RecurringRule(Base, IdMixin, TimestampMixin):
    __tablename__ = "recurring_rules"

    user_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    category_id: Mapped[str | None] = mapped_column(ForeignKey("categories.id", ondelete="SET NULL"), nullable=True)
    amount: Mapped[Decimal] = mapped_column(Numeric(14, 2))
    description: Mapped[str] = mapped_column(String(500))
    frequency: Mapped[str] = mapped_column(String(20))
    start_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    end_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    next_due_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, server_default=text("1"))
    transaction_type: Mapped[str] = mapped_column(String(20))

    user: Mapped[User] = relationship(back_populates="recurring_rules")
    category: Mapped[Category | None] = relationship()
    transactions: Mapped[list[Transaction]] = relationship(back_populates="recurring_rule")


class Transaction(Base, IdMixin, TimestampMixin):
    __tablename__ = "transactions"
    __table_args__ = (
        Index("ix_transactions_user_date", "user_id", "transaction_date"),
        Index("ix_transactions_transaction_date", "transaction_date"),
    )

    user_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    category_id: Mapped[str | None] = mapped_column(ForeignKey("categories.id", ondelete="SET NULL"), nullable=True)
    recurring_rule_id: Mapped[str | None] = mapped_column(ForeignKey("recurring_rules.id", ondelete="SET NULL"), nullable=True)
    amount: Mapped[Decimal] = mapped_column(Numeric(14, 2))
    transaction_type: Mapped[str] = mapped_column(String(20))
    description: Mapped[str | None] = mapped_column(String(500), nullable=True)
    merchant: Mapped[str | None] = mapped_column(String(200), nullable=True)
    transaction_date: Mapped[date] = mapped_column(Date)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_recurring: Mapped[bool] = mapped_column(Boolean, default=False, server_default=text("0"))
    source: Mapped[str] = mapped_column(String(50), default="manual", server_default=text("'manual'"))

    user: Mapped[User] = relationship(back_populates="transactions")
    category: Mapped[Category | None] = relationship(back_populates="transactions")
    recurring_rule: Mapped[RecurringRule | None] = relationship(back_populates="transactions")


class BudgetPlan(Base, IdMixin, TimestampMixin):
    __tablename__ = "budget_plans"
    __table_args__ = (
        UniqueConstraint("user_id", "month_start", name="uq_budget_plans_user_month_start"),
        Index("ix_budget_plans_user_month", "user_id", "month_start", unique=True),
    )

    user_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    month_start: Mapped[date] = mapped_column(Date)
    month_end: Mapped[date] = mapped_column(Date)
    total_income: Mapped[Decimal] = mapped_column(Numeric(14, 2))
    needs_pct: Mapped[Decimal] = mapped_column(Numeric(5, 2), default=Decimal("50.00"), server_default=text("50"))
    wants_pct: Mapped[Decimal] = mapped_column(Numeric(5, 2), default=Decimal("30.00"), server_default=text("30"))
    savings_pct: Mapped[Decimal] = mapped_column(Numeric(5, 2), default=Decimal("20.00"), server_default=text("20"))
    status: Mapped[str] = mapped_column(String(20), default="active", server_default=text("'active'"))
    is_ai_generated: Mapped[bool] = mapped_column(Boolean, default=False, server_default=text("0"))
    ai_reasoning: Mapped[str | None] = mapped_column(Text, nullable=True)

    user: Mapped[User] = relationship(back_populates="budget_plans")
    allocations: Mapped[list[BudgetAllocation]] = relationship(back_populates="budget_plan", cascade="all, delete-orphan")


class BudgetAllocation(Base, IdMixin, TimestampMixin):
    __tablename__ = "budget_allocations"

    budget_plan_id: Mapped[str] = mapped_column(ForeignKey("budget_plans.id", ondelete="CASCADE"), index=True)
    category_id: Mapped[str | None] = mapped_column(ForeignKey("categories.id", ondelete="CASCADE"), nullable=True)
    allocated_amount: Mapped[Decimal] = mapped_column(Numeric(14, 2))
    spent_amount: Mapped[Decimal] = mapped_column(Numeric(14, 2), default=Decimal("0.00"), server_default=text("0"))

    budget_plan: Mapped[BudgetPlan] = relationship(back_populates="allocations")
    category: Mapped[Category | None] = relationship()


class Goal(Base, IdMixin, TimestampMixin):
    __tablename__ = "goals"

    user_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    name: Mapped[str] = mapped_column(String(200))
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    target_amount: Mapped[Decimal] = mapped_column(Numeric(14, 2))
    current_amount: Mapped[Decimal] = mapped_column(Numeric(14, 2), default=Decimal("0.00"), server_default=text("0"))
    target_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    icon: Mapped[str | None] = mapped_column(String(50), nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="active", server_default=text("'active'"))

    user: Mapped[User] = relationship(back_populates="goals")
    contributions: Mapped[list[GoalContribution]] = relationship(back_populates="goal", cascade="all, delete-orphan")


class GoalContribution(Base, IdMixin, TimestampMixin):
    __tablename__ = "goal_contributions"

    goal_id: Mapped[str] = mapped_column(ForeignKey("goals.id", ondelete="CASCADE"), index=True)
    amount: Mapped[Decimal] = mapped_column(Numeric(14, 2))
    contribution_date: Mapped[date] = mapped_column(Date)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    goal: Mapped[Goal] = relationship(back_populates="contributions")


class Conversation(Base, IdMixin, TimestampMixin):
    __tablename__ = "conversations"

    user_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    title: Mapped[str] = mapped_column(String(300))

    user: Mapped[User] = relationship(back_populates="conversations")
    messages: Mapped[list[Message]] = relationship(back_populates="conversation", cascade="all, delete-orphan")


class Message(Base, IdMixin, TimestampMixin):
    __tablename__ = "messages"

    conversation_id: Mapped[str] = mapped_column(ForeignKey("conversations.id", ondelete="CASCADE"), index=True)
    role: Mapped[str] = mapped_column(String(20))
    content: Mapped[str] = mapped_column(Text)
    token_count: Mapped[int | None] = mapped_column(Integer, nullable=True)

    conversation: Mapped[Conversation] = relationship(back_populates="messages")


class HealthSnapshot(Base, IdMixin, TimestampMixin):
    __tablename__ = "health_snapshots"
    __table_args__ = (UniqueConstraint("user_id", "snapshot_date", name="uq_health_snapshots_user_date"),)

    user_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    snapshot_date: Mapped[date] = mapped_column(Date)
    overall_score: Mapped[int] = mapped_column(Integer)
    savings_score: Mapped[int] = mapped_column(Integer)
    budget_adherence_score: Mapped[int] = mapped_column(Integer)
    goal_progress_score: Mapped[int] = mapped_column(Integer)
    spending_consistency_score: Mapped[int] = mapped_column(Integer)
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)


class UserPreference(Base, IdMixin, TimestampMixin):
    __tablename__ = "user_preferences"

    user_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), unique=True)
    spending_style: Mapped[str | None] = mapped_column(String(50), nullable=True)
    top_expense_categories: Mapped[str | None] = mapped_column(Text, nullable=True)
    financial_goals_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    monthly_savings_target_pct: Mapped[Decimal] = mapped_column(Numeric(5, 2), default=Decimal("20.00"), server_default=text("20"))
    preferred_budget_strategy: Mapped[str] = mapped_column(String(50), default="50/30/20", server_default=text("'50/30/20'"))

    user: Mapped[User] = relationship(back_populates="preferences")

