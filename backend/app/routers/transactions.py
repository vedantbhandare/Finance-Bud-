"""Transactions router — CRUD + monthly summary."""
from datetime import date
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db_session
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.transaction import TransactionCreate, TransactionResponse, TransactionUpdate
from app.services.transaction_service import TransactionService

router = APIRouter()


@router.get("")
async def list_transactions(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    category_id: UUID | None = None,
    date_from: date | None = None,
    date_to: date | None = None,
    type: str | None = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
):
    """Get paginated transactions with optional filters."""
    service = TransactionService(db)
    items, total = await service.get_transactions(
        user_id=current_user.id,
        page=page,
        limit=limit,
        category_id=category_id,
        date_from=date_from,
        date_to=date_to,
        txn_type=type,
    )
    return {
        "items": [TransactionResponse.model_validate(t) for t in items],
        "total": total,
        "page": page,
        "limit": limit,
        "pages": (total + limit - 1) // limit,
    }


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_transaction(
    data: TransactionCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
):
    """Create a new transaction."""
    service = TransactionService(db)
    txn = await service.create_transaction(current_user.id, data)
    return TransactionResponse.model_validate(txn)


@router.get("/summary/monthly")
async def monthly_summary(
    year: int = Query(...),
    month: int = Query(..., ge=1, le=12),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
):
    """Get spending summary for a given month."""
    service = TransactionService(db)
    return await service.get_monthly_summary(current_user.id, year, month)


@router.get("/{txn_id}")
async def get_transaction(
    txn_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
):
    """Get a single transaction by ID."""
    service = TransactionService(db)
    txn = await service.get_transaction(current_user.id, txn_id)
    if not txn:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return TransactionResponse.model_validate(txn)


@router.put("/{txn_id}")
async def update_transaction(
    txn_id: UUID,
    data: TransactionUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
):
    """Update a transaction."""
    service = TransactionService(db)
    txn = await service.update_transaction(current_user.id, txn_id, data)
    if not txn:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return TransactionResponse.model_validate(txn)


@router.delete("/{txn_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_transaction(
    txn_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
):
    """Delete a transaction."""
    service = TransactionService(db)
    deleted = await service.delete_transaction(current_user.id, txn_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Transaction not found")
