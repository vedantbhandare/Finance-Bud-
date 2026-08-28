from __future__ import annotations

from collections.abc import Sequence
from datetime import date
from typing import Any, Generic, TypeVar

from sqlalchemy import Select, case, func, or_, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from app.domain.categories import DEFAULT_CATEGORIES
from app.infrastructure.orm.base import Base
from app.infrastructure.orm.models import (
    BudgetAllocation,
    BudgetPlan,
    Category,
    Conversation,
    Goal,
    GoalContribution,
    Message,
    RecurringRule,
    Transaction,
    User,
    UserPreference,
)

ModelT = TypeVar("ModelT", bound=Base)


class Repository(Generic[ModelT]):
    def __init__(self, session: AsyncSession, model: type[ModelT]) -> None:
        self.session = session
        self.model = model

    async def get(self, entity_id: str) -> ModelT | None:
        return await self.session.get(self.model, entity_id)

    async def add(self, entity: ModelT) -> ModelT:
        self.session.add(entity)
        await self.session.flush()
        return entity

    async def delete(self, entity: ModelT) -> None:
        await self.session.delete(entity)
        await self.session.flush()


class UserRepository(Repository[User]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, User)

    async def by_email(self, email: str) -> User | None:
        return await self.session.scalar(select(User).where(User.email == email.lower()))


class CategoryRepository(Repository[Category]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Category)

    async def ensure_system_categories(self) -> None:
        existing_names = set(
            await self.session.scalars(select(Category.name).where(Category.is_system.is_(True)))
        )
        for seed in DEFAULT_CATEGORIES:
            if seed.name in existing_names:
                continue
            self.session.add(
                Category(
                    name=seed.name,
                    icon=seed.icon,
                    category_type=seed.kind,
                    is_system=True,
                )
            )
        await self.session.flush()

    async def available_to_user(self, user_id: str) -> Sequence[Category]:
        stmt = (
            select(Category)
            .where(or_(Category.is_system.is_(True), Category.user_id == user_id))
            .order_by(Category.category_type, Category.name)
        )
        return (await self.session.scalars(stmt)).all()

    async def by_name(self, name: str, user_id: str | None = None) -> Category | None:
        stmt = select(Category).where(Category.name == name)
        if user_id:
            stmt = stmt.where(or_(Category.is_system.is_(True), Category.user_id == user_id))
        else:
            stmt = stmt.where(Category.is_system.is_(True))
        return await self.session.scalar(stmt.limit(1))

    async def get_available(self, category_id: str, user_id: str) -> Category | None:
        stmt = select(Category).where(
            Category.id == category_id,
            or_(Category.is_system.is_(True), Category.user_id == user_id),
        )
        return await self.session.scalar(stmt)


class TransactionRepository(Repository[Transaction]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Transaction)

    def _filtered(
        self,
        user_id: str,
        start_date: date | None = None,
        end_date: date | None = None,
        transaction_type: str | None = None,
        category_id: str | None = None,
    ) -> Select[tuple[Transaction]]:
        stmt = select(Transaction).where(Transaction.user_id == user_id)
        if start_date:
            stmt = stmt.where(Transaction.transaction_date >= start_date)
        if end_date:
            stmt = stmt.where(Transaction.transaction_date <= end_date)
        if transaction_type:
            stmt = stmt.where(Transaction.transaction_type == transaction_type)
        if category_id:
            stmt = stmt.where(Transaction.category_id == category_id)
        return stmt

    async def list_for_user(
        self,
        user_id: str,
        offset: int,
        limit: int,
        start_date: date | None = None,
        end_date: date | None = None,
        transaction_type: str | None = None,
        category_id: str | None = None,
    ) -> Sequence[Transaction]:
        stmt = (
            self._filtered(user_id, start_date, end_date, transaction_type, category_id)
            .options(joinedload(Transaction.category))
            .order_by(Transaction.transaction_date.desc(), Transaction.created_at.desc())
            .offset(offset)
            .limit(limit)
        )
        return (await self.session.scalars(stmt)).all()

    async def get_for_user(self, user_id: str, transaction_id: str) -> Transaction | None:
        stmt = (
            select(Transaction)
            .options(joinedload(Transaction.category))
            .where(Transaction.id == transaction_id, Transaction.user_id == user_id)
        )
        return await self.session.scalar(stmt)

    async def count_for_user(
        self,
        user_id: str,
        start_date: date | None = None,
        end_date: date | None = None,
        transaction_type: str | None = None,
        category_id: str | None = None,
    ) -> int:
        subquery = self._filtered(user_id, start_date, end_date, transaction_type, category_id).subquery()
        return await self.session.scalar(select(func.count()).select_from(subquery)) or 0

    # ---- SQL aggregation methods (no Python-side loops) ----

    async def aggregate_monthly(
        self, user_id: str, start: date, end: date,
    ) -> dict[str, "Decimal"]:
        """Single SQL query for income, expenses, and net."""
        from decimal import Decimal as D

        stmt = select(
            func.coalesce(
                func.sum(case((Transaction.transaction_type == "income", Transaction.amount), else_=0)), 0
            ).label("total_income"),
            func.coalesce(
                func.sum(case((Transaction.transaction_type == "expense", Transaction.amount), else_=0)), 0
            ).label("total_expenses"),
        ).where(
            Transaction.user_id == user_id,
            Transaction.transaction_date >= start,
            Transaction.transaction_date <= end,
        )
        row = (await self.session.execute(stmt)).one()
        income = D(str(row.total_income))
        expenses = D(str(row.total_expenses))
        return {"total_income": income, "total_expenses": expenses, "net": income - expenses}

    async def spending_by_category(
        self, user_id: str, start: date, end: date,
    ) -> list[dict]:
        """SQL GROUP BY for expense breakdown per category."""
        stmt = (
            select(
                Transaction.category_id,
                Category.name.label("category_name"),
                func.sum(Transaction.amount).label("total"),
            )
            .join(Category, Transaction.category_id == Category.id, isouter=True)
            .where(
                Transaction.user_id == user_id,
                Transaction.transaction_type == "expense",
                Transaction.transaction_date >= start,
                Transaction.transaction_date <= end,
            )
            .group_by(Transaction.category_id, Category.name)
            .order_by(func.sum(Transaction.amount).desc())
        )
        from decimal import Decimal as D

        rows = (await self.session.execute(stmt)).all()
        return [
            {
                "category_id": row.category_id,
                "category_name": row.category_name or "Uncategorized",
                "total": D(str(row.total)),
            }
            for row in rows
        ]

    async def daily_spending(
        self, user_id: str, start: date, end: date,
    ) -> list[dict]:
        """SQL GROUP BY for daily expense totals."""
        from decimal import Decimal as D

        stmt = (
            select(
                Transaction.transaction_date,
                func.sum(Transaction.amount).label("amount"),
            )
            .where(
                Transaction.user_id == user_id,
                Transaction.transaction_type == "expense",
                Transaction.transaction_date >= start,
                Transaction.transaction_date <= end,
            )
            .group_by(Transaction.transaction_date)
            .order_by(Transaction.transaction_date)
        )
        rows = (await self.session.execute(stmt)).all()
        return [{"date": row.transaction_date, "amount": D(str(row.amount))} for row in rows]


class RecurringRuleRepository(Repository[RecurringRule]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, RecurringRule)

    async def active_for_user(self, user_id: str) -> Sequence[RecurringRule]:
        stmt = select(RecurringRule).options(joinedload(RecurringRule.category)).where(
            RecurringRule.user_id == user_id,
            RecurringRule.is_active.is_(True),
        )
        return (await self.session.scalars(stmt)).all()


class BudgetRepository(Repository[BudgetPlan]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, BudgetPlan)

    async def current(self, user_id: str) -> BudgetPlan | None:
        stmt = (
            select(BudgetPlan)
            .options(selectinload(BudgetPlan.allocations).joinedload(BudgetAllocation.category))
            .where(BudgetPlan.user_id == user_id, BudgetPlan.status == "active")
            .order_by(BudgetPlan.month_start.desc())
            .limit(1)
        )
        return await self.session.scalar(stmt)

    async def expire_active(self, user_id: str) -> None:
        await self.session.execute(
            update(BudgetPlan)
            .where(BudgetPlan.user_id == user_id, BudgetPlan.status == "active")
            .values(status="expired")
        )
        await self.session.flush()


class GoalRepository(Repository[Goal]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Goal)

    async def list_for_user(self, user_id: str, status: str | None = None) -> Sequence[Goal]:
        stmt = select(Goal).where(Goal.user_id == user_id)
        if status:
            stmt = stmt.where(Goal.status == status)
        stmt = stmt.order_by(Goal.created_at.desc())
        return (await self.session.scalars(stmt)).all()

    async def active_for_user(self, user_id: str) -> Sequence[Goal]:
        return await self.list_for_user(user_id, "active")


class GoalContributionRepository(Repository[GoalContribution]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, GoalContribution)


class PreferenceRepository(Repository[UserPreference]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, UserPreference)

    async def for_user(self, user_id: str) -> UserPreference | None:
        return await self.session.scalar(select(UserPreference).where(UserPreference.user_id == user_id))


class ConversationRepository(Repository[Conversation]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Conversation)

    async def for_user(self, user_id: str, offset: int = 0, limit: int = 20) -> Sequence[Conversation]:
        stmt = (
            select(Conversation)
            .where(Conversation.user_id == user_id)
            .order_by(Conversation.updated_at.desc())
            .offset(offset)
            .limit(limit)
        )
        return (await self.session.scalars(stmt)).all()


class MessageRepository(Repository[Message]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Message)

    async def recent(self, conversation_id: str, limit: int = 20) -> Sequence[Message]:
        stmt = (
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.created_at.desc())
            .limit(limit)
        )
        messages = (await self.session.scalars(stmt)).all()
        return list(reversed(messages))

    async def list_for_conversation(self, conversation_id: str, limit: int = 50) -> Sequence[Message]:
        stmt = (
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.created_at.asc())
            .limit(limit)
        )
        return (await self.session.scalars(stmt)).all()
