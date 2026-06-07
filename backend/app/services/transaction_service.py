"""Transaction service — business logic for income/expense tracking."""
from datetime import date
from decimal import Decimal
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.transaction import Transaction, TransactionType
from app.repositories.transaction_repo import TransactionRepository
from app.schemas.transaction import TransactionCreate, TransactionUpdate
from app.utils.date_utils import get_month_range


class TransactionService:
    """Business logic for transaction management."""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = TransactionRepository(db)

    async def create_transaction(self, user_id: UUID, data: TransactionCreate) -> Transaction:
        """Create a new transaction."""
        # Map string type to enum
        txn_type = TransactionType.INCOME if data.type == "income" else TransactionType.EXPENSE
        txn = Transaction(
            user_id=user_id,
            category_id=data.category_id,
            amount=data.amount,
            transaction_type=txn_type,
            description=data.description,
            merchant=data.merchant,
            transaction_date=data.transaction_date or date.today(),
            source="manual",
        )
        return await self.repo.create(txn)

    async def get_transactions(
        self,
        user_id: UUID,
        page: int = 1,
        limit: int = 20,
        category_id: UUID | None = None,
        date_from: date | None = None,
        date_to: date | None = None,
        txn_type: str | None = None,
    ) -> tuple[list[Transaction], int]:
        """Get paginated transactions with filters."""
        offset = (page - 1) * limit
        mapped_type = None
        if txn_type == "income":
            mapped_type = TransactionType.INCOME
        elif txn_type == "expense":
            mapped_type = TransactionType.EXPENSE

        transactions = await self.repo.get_user_transactions(
            user_id=user_id,
            offset=offset,
            limit=limit,
            start_date=date_from,
            end_date=date_to,
            transaction_type=mapped_type,
            category_id=category_id,
        )
        total = await self.repo.count_user_transactions(
            user_id=user_id,
            start_date=date_from,
            end_date=date_to,
        )
        return list(transactions), total

    async def get_transaction(self, user_id: UUID, txn_id: UUID) -> Transaction | None:
        """Get a single transaction by ID."""
        txn = await self.repo.get_by_id(txn_id)
        if txn and txn.user_id == user_id:
            return txn
        return None

    async def update_transaction(
        self, user_id: UUID, txn_id: UUID, data: TransactionUpdate
    ) -> Transaction | None:
        """Update a transaction."""
        txn = await self.get_transaction(user_id, txn_id)
        if not txn:
            return None

        update_data = data.model_dump(exclude_unset=True)
        mapped: dict = {}
        for key, value in update_data.items():
            if key == "type":
                # Map schema "type" to ORM "transaction_type" and convert to enum
                mapped["transaction_type"] = (
                    TransactionType.INCOME if value == "income" else TransactionType.EXPENSE
                )
            else:
                mapped[key] = value

        return await self.repo.update_by_id(txn_id, mapped)

    async def delete_transaction(self, user_id: UUID, txn_id: UUID) -> bool:
        """Delete a transaction."""
        txn = await self.get_transaction(user_id, txn_id)
        if not txn:
            return False
        await self.repo.delete_by_id(txn_id)
        return True

    async def get_monthly_summary(self, user_id: UUID, year: int, month: int) -> dict:
        """Get spending summary for a given month."""
        totals = await self.repo.get_monthly_totals(user_id, year, month)

        start, end = get_month_range(year, month)
        category_breakdown = await self.repo.get_category_breakdown(user_id, start, end)

        total_expenses = float(totals.get("total_expenses", 0))
        by_category = []
        for cat_name, cat_total in category_breakdown.items():
            cat_float = float(cat_total)
            pct = (cat_float / total_expenses * 100) if total_expenses > 0 else 0
            by_category.append({
                "category_name": cat_name,
                "total": cat_float,
                "percentage": round(pct, 1),
                "color": "#10B981",
            })

        return {
            "total_income": float(totals.get("total_income", 0)),
            "total_expenses": total_expenses,
            "net": float(totals.get("net_savings", 0)),
            "by_category": sorted(by_category, key=lambda x: x["total"], reverse=True),
        }

    async def get_total_spent_this_month(self, user_id: UUID) -> Decimal:
        """Get total expenses for the current month."""
        today = date.today()
        summary = await self.get_monthly_summary(user_id, today.year, today.month)
        return Decimal(str(summary.get("total_expenses", 0)))

    async def get_recent_transactions(self, user_id: UUID, limit: int = 10) -> list[Transaction]:
        """Get most recent transactions."""
        txns = await self.repo.get_user_transactions(user_id=user_id, offset=0, limit=limit)
        return list(txns)
