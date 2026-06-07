"""Transaction schemas."""

from __future__ import annotations

import uuid
from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class TransactionCreate(BaseModel):
    """Payload to create a transaction."""

    amount: Decimal = Field(gt=0, max_digits=14, decimal_places=2)
    type: str = Field(pattern="^(expense|income)$")
    description: str | None = Field(default=None, max_length=500)
    merchant: str | None = Field(default=None, max_length=200)
    category_id: uuid.UUID | None = None
    transaction_date: date | None = None
    notes: str | None = None
    is_recurring: bool = False


class TransactionUpdate(BaseModel):
    """Payload to update a transaction (all fields optional)."""

    amount: Decimal | None = Field(default=None, gt=0, max_digits=14, decimal_places=2)
    type: str | None = Field(default=None, pattern="^(expense|income)$")
    description: str | None = Field(default=None, max_length=500)
    merchant: str | None = None
    category_id: uuid.UUID | None = None
    transaction_date: date | None = None
    notes: str | None = None


class CategoryResponse(BaseModel):
    """Category response."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    icon: str | None
    category_type: str


class TransactionResponse(BaseModel):
    """Transaction response serialized for frontend consumption."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    amount: Decimal
    type: str  # 'expense' | 'income'
    description: str | None
    merchant: str | None
    category_id: uuid.UUID | None
    category: CategoryResponse | None = None
    transaction_date: date
    is_recurring: bool = False
    source: str = "manual"
    created_at: datetime

    @classmethod
    def model_validate(cls, obj, *args, **kwargs):
        """Custom validator to map transaction_type enum to string."""
        if hasattr(obj, 'transaction_type'):
            # Convert the SQLAlchemy model to dict-like access
            from app.models.transaction import TransactionType

            data = {
                'id': obj.id,
                'amount': obj.amount,
                'type': 'income' if obj.transaction_type == TransactionType.INCOME else 'expense',
                'description': obj.description,
                'merchant': obj.merchant,
                'category_id': obj.category_id,
                'category': obj.category if hasattr(obj, 'category') and obj.category else None,
                'transaction_date': obj.transaction_date,
                'is_recurring': getattr(obj, 'is_recurring', False),
                'source': getattr(obj, 'source', 'manual'),
                'created_at': obj.created_at,
            }
            return super().model_validate(data, *args, **kwargs)
        return super().model_validate(obj, *args, **kwargs)


class MonthlySummary(BaseModel):
    """Aggregated monthly financial summary."""

    total_income: Decimal
    total_expenses: Decimal
    net: Decimal
    by_category: list[dict] = []
