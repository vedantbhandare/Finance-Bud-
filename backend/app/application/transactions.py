from __future__ import annotations

from datetime import date
from decimal import Decimal

from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas import (
    CategorySummary,
    DailySpend,
    MonthlySummary,
    Page,
    TransactionCreate,
    TransactionResponse,
    TransactionUpdate,
)
from app.application.serializers import transaction_response
from app.core.errors import NotFoundError, ValidationError
from app.core.time import month_range
from app.domain.categories import categorize_text, color_for_category
from app.infrastructure.orm.models import Transaction
from app.infrastructure.orm.repositories import CategoryRepository, TransactionRepository


class TransactionService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.transactions = TransactionRepository(session)
        self.categories = CategoryRepository(session)

    async def _resolve_category(self, user_id: str, category_id: str | None, category_name: str | None, description: str | None, merchant: str | None):
        # System categories are seeded at app startup (lifespan) — no per-request seeding.
        if category_id:
            category = await self.categories.get_available(category_id, user_id)
            if not category:
                raise ValidationError("Category is not available to this user")
            return category

        resolved_name = category_name or categorize_text(description, merchant)
        if resolved_name:
            return await self.categories.by_name(resolved_name, user_id)
        return None

    async def create(self, user_id: str, data: TransactionCreate) -> TransactionResponse:
        category = await self._resolve_category(
            user_id,
            data.category_id,
            data.category_name,
            data.description,
            data.merchant,
        )
        description = data.description or data.category_name or ("Income" if data.type == "income" else "Expense")
        transaction = Transaction(
            user_id=user_id,
            category_id=category.id if category else None,
            amount=data.amount,
            transaction_type=data.type,
            description=description,
            merchant=data.merchant,
            transaction_date=data.transaction_date or date.today(),
            notes=data.notes,
            is_recurring=data.is_recurring,
            source="manual",
        )
        await self.transactions.add(transaction)
        transaction.category = category
        return transaction_response(transaction)

    async def list(
        self,
        user_id: str,
        page: int,
        limit: int,
        category_id: str | None = None,
        date_from: date | None = None,
        date_to: date | None = None,
        transaction_type: str | None = None,
    ) -> Page[TransactionResponse]:
        offset = (page - 1) * limit
        items = await self.transactions.list_for_user(
            user_id,
            offset,
            limit,
            date_from,
            date_to,
            transaction_type,
            category_id,
        )
        total = await self.transactions.count_for_user(
            user_id,
            date_from,
            date_to,
            transaction_type,
            category_id,
        )
        return Page(
            items=[transaction_response(item) for item in items],
            total=total,
            page=page,
            limit=limit,
            pages=(total + limit - 1) // limit if total else 0,
        )

    async def get(self, user_id: str, transaction_id: str) -> TransactionResponse:
        transaction = await self.transactions.get_for_user(user_id, transaction_id)
        if not transaction:
            raise NotFoundError("Transaction not found")
        return transaction_response(transaction)

    async def update(self, user_id: str, transaction_id: str, data: TransactionUpdate) -> TransactionResponse:
        transaction = await self.transactions.get_for_user(user_id, transaction_id)
        if not transaction:
            raise NotFoundError("Transaction not found")

        update_data = data.model_dump(exclude_unset=True)
        category_name = update_data.pop("category_name", None)
        if "category_id" in update_data or category_name:
            category = await self._resolve_category(
                user_id,
                update_data.get("category_id"),
                category_name,
                update_data.get("description", transaction.description),
                update_data.get("merchant", transaction.merchant),
            )
            transaction.category_id = category.id if category else None
            transaction.category = category

        if "type" in update_data:
            transaction.transaction_type = update_data.pop("type")
        for field_name, value in update_data.items():
            setattr(transaction, field_name, value)
        await self.session.flush()
        return transaction_response(transaction)

    async def delete(self, user_id: str, transaction_id: str) -> None:
        transaction = await self.transactions.get_for_user(user_id, transaction_id)
        if not transaction:
            raise NotFoundError("Transaction not found")
        await self.transactions.delete(transaction)

    async def monthly_summary(self, user_id: str, year: int, month: int) -> MonthlySummary:
        """Compute monthly financial summary using SQL aggregation.

        All heavy lifting (income/expense totals, category breakdown,
        daily trend) is pushed to the database — no Python-side loops
        over raw transaction rows.
        """
        start, end = month_range(year, month)

        # Single SQL query for totals
        totals = await self.transactions.aggregate_monthly(user_id, start, end)
        income = totals["total_income"]
        expenses = totals["total_expenses"]

        # SQL GROUP BY for category breakdown
        category_rows_raw = await self.transactions.spending_by_category(user_id, start, end)
        category_rows = [
            CategorySummary(
                category_id=row["category_id"],
                category_name=row["category_name"],
                total=row["total"],
                percentage=round(float(row["total"] / expenses * 100), 2) if expenses > 0 else 0,
                color=color_for_category(row["category_name"]),
            )
            for row in category_rows_raw
        ]

        # SQL GROUP BY for daily trend
        daily_rows_raw = await self.transactions.daily_spending(user_id, start, end)
        daily_rows = [DailySpend(date=row["date"], amount=row["amount"]) for row in daily_rows_raw]

        return MonthlySummary(
            total_income=income,
            total_expenses=expenses,
            net=income - expenses,
            by_category=category_rows,
            daily_trend=daily_rows,
        )
