"""Transaction and Category repositories."""

from __future__ import annotations

import uuid
from datetime import date
from decimal import Decimal
from typing import Sequence

from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.models.transaction import Category, CategoryType, RecurringRule, Transaction, TransactionType
from app.repositories.base import BaseRepository


class CategoryRepository(BaseRepository[Category]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(Category, session)

    async def get_user_categories(self, user_id: uuid.UUID) -> Sequence[Category]:
        """Get system categories + user-specific categories."""
        result = await self.session.execute(
            select(Category).where(
                (Category.is_system == True) | (Category.user_id == user_id),  # noqa: E712
            ).order_by(Category.name),
        )
        return result.scalars().all()

    async def get_by_name(self, name: str, user_id: uuid.UUID | None = None) -> Category | None:
        result = await self.session.execute(
            select(Category).where(
                Category.name == name,
                (Category.user_id == user_id) | (Category.is_system == True),  # noqa: E712
            ),
        )
        return result.scalar_one_or_none()

    async def seed_defaults(self, user_id: uuid.UUID | None = None) -> list[Category]:
        """Seed default India-specific categories."""
        defaults = [
            # Needs
            ("Rent/EMI", "🏠", CategoryType.NEED),
            ("Groceries/Kirana", "🛒", CategoryType.NEED),
            ("Utilities", "💡", CategoryType.NEED),
            ("Transport/Metro", "🚇", CategoryType.NEED),
            ("Auto/Riksha", "🛺", CategoryType.NEED),
            ("Medical/Health", "🏥", CategoryType.NEED),
            ("Insurance", "🛡️", CategoryType.NEED),
            ("Phone/Internet", "📱", CategoryType.NEED),
            ("Education", "📚", CategoryType.NEED),
            # Wants
            ("Dining Out", "🍽️", CategoryType.WANT),
            ("Chai/Coffee", "☕", CategoryType.WANT),
            ("Shopping", "🛍️", CategoryType.WANT),
            ("Entertainment", "🎬", CategoryType.WANT),
            ("Subscriptions", "📺", CategoryType.WANT),
            ("Travel/Holiday", "✈️", CategoryType.WANT),
            ("Personal Care", "💈", CategoryType.WANT),
            ("Gifts/Donations", "🎁", CategoryType.WANT),
            # Savings
            ("Savings", "💰", CategoryType.SAVING),
            ("Investments/SIP", "📈", CategoryType.SAVING),
            ("Emergency Fund", "🆘", CategoryType.SAVING),
            # Income
            ("Salary", "💵", CategoryType.INCOME),
            ("Freelance", "💻", CategoryType.INCOME),
            ("Other Income", "📥", CategoryType.INCOME),
        ]
        categories = [
            Category(
                user_id=user_id,
                name=name,
                icon=icon,
                category_type=cat_type,
                is_system=user_id is None,
            )
            for name, icon, cat_type in defaults
        ]
        return await self.bulk_create(categories)


class TransactionRepository(BaseRepository[Transaction]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(Transaction, session)

    async def get_user_transactions(
        self,
        user_id: uuid.UUID,
        *,
        offset: int = 0,
        limit: int = 50,
        start_date: date | None = None,
        end_date: date | None = None,
        transaction_type: TransactionType | None = None,
        category_id: uuid.UUID | None = None,
    ) -> Sequence[Transaction]:
        stmt = (
            select(Transaction)
            .options(joinedload(Transaction.category))
            .where(Transaction.user_id == user_id)
        )
        if start_date:
            stmt = stmt.where(Transaction.transaction_date >= start_date)
        if end_date:
            stmt = stmt.where(Transaction.transaction_date <= end_date)
        if transaction_type:
            stmt = stmt.where(Transaction.transaction_type == transaction_type)
        if category_id:
            stmt = stmt.where(Transaction.category_id == category_id)

        stmt = stmt.order_by(Transaction.transaction_date.desc()).offset(offset).limit(limit)
        result = await self.session.execute(stmt)
        return result.unique().scalars().all()

    async def count_user_transactions(
        self,
        user_id: uuid.UUID,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> int:
        stmt = select(func.count()).select_from(Transaction).where(Transaction.user_id == user_id)
        if start_date:
            stmt = stmt.where(Transaction.transaction_date >= start_date)
        if end_date:
            stmt = stmt.where(Transaction.transaction_date <= end_date)
        result = await self.session.execute(stmt)
        return result.scalar_one()

    async def get_monthly_totals(
        self,
        user_id: uuid.UUID,
        year: int,
        month: int,
    ) -> dict[str, Decimal]:
        """Get income / expense totals for a given month."""
        from app.utils.date_utils import get_month_range

        start, end = get_month_range(year, month)

        income_result = await self.session.execute(
            select(func.coalesce(func.sum(Transaction.amount), 0)).where(
                Transaction.user_id == user_id,
                Transaction.transaction_type == TransactionType.INCOME,
                Transaction.transaction_date >= start,
                Transaction.transaction_date <= end,
            ),
        )
        expense_result = await self.session.execute(
            select(func.coalesce(func.sum(Transaction.amount), 0)).where(
                Transaction.user_id == user_id,
                Transaction.transaction_type == TransactionType.EXPENSE,
                Transaction.transaction_date >= start,
                Transaction.transaction_date <= end,
            ),
        )
        total_income = Decimal(str(income_result.scalar_one()))
        total_expenses = Decimal(str(expense_result.scalar_one()))
        return {
            "total_income": total_income,
            "total_expenses": total_expenses,
            "net_savings": total_income - total_expenses,
        }

    async def get_category_breakdown(
        self,
        user_id: uuid.UUID,
        start_date: date,
        end_date: date,
    ) -> dict[str, Decimal]:
        """Get spending grouped by category name for a date range."""
        stmt = (
            select(Category.name, func.sum(Transaction.amount))
            .join(Category, Transaction.category_id == Category.id)
            .where(
                Transaction.user_id == user_id,
                Transaction.transaction_type == TransactionType.EXPENSE,
                Transaction.transaction_date >= start_date,
                Transaction.transaction_date <= end_date,
            )
            .group_by(Category.name)
        )
        result = await self.session.execute(stmt)
        return {name: Decimal(str(total)) for name, total in result.all()}

    async def get_spending_by_category_type(
        self,
        user_id: uuid.UUID,
        start_date: date,
        end_date: date,
    ) -> dict[str, Decimal]:
        """Get spending grouped by category type (need/want/saving)."""
        stmt = (
            select(Category.category_type, func.sum(Transaction.amount))
            .join(Category, Transaction.category_id == Category.id)
            .where(
                Transaction.user_id == user_id,
                Transaction.transaction_type == TransactionType.EXPENSE,
                Transaction.transaction_date >= start_date,
                Transaction.transaction_date <= end_date,
            )
            .group_by(Category.category_type)
        )
        result = await self.session.execute(stmt)
        return {cat_type.value: Decimal(str(total)) for cat_type, total in result.all()}


class RecurringRuleRepository(BaseRepository[RecurringRule]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(RecurringRule, session)

    async def get_active_rules(self, user_id: uuid.UUID) -> Sequence[RecurringRule]:
        result = await self.session.execute(
            select(RecurringRule).where(
                RecurringRule.user_id == user_id,
                RecurringRule.is_active == True,  # noqa: E712
            ),
        )
        return result.scalars().all()

    async def get_due_rules(self, as_of: date) -> Sequence[RecurringRule]:
        result = await self.session.execute(
            select(RecurringRule).where(
                RecurringRule.is_active == True,  # noqa: E712
                RecurringRule.next_due_date <= as_of,
            ),
        )
        return result.scalars().all()
