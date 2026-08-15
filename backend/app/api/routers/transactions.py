from __future__ import annotations

from datetime import date

from fastapi import APIRouter, Depends, Query, status

from app.api.deps import current_user, transaction_service
from app.api.schemas import MonthlySummary, Page, TransactionCreate, TransactionResponse, TransactionUpdate
from app.application.transactions import TransactionService
from app.infrastructure.orm.models import User

router = APIRouter(prefix="/transactions", tags=["Transactions"])


@router.get("", response_model=Page[TransactionResponse])
async def list_transactions(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    category_id: str | None = None,
    date_from: date | None = None,
    date_to: date | None = None,
    type: str | None = Query(default=None, pattern="^(expense|income)$"),
    user: User = Depends(current_user),
    service: TransactionService = Depends(transaction_service),
):
    return await service.list(user.id, page, limit, category_id, date_from, date_to, type)


@router.post("", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
async def create_transaction(
    data: TransactionCreate,
    user: User = Depends(current_user),
    service: TransactionService = Depends(transaction_service),
):
    return await service.create(user.id, data)


@router.get("/summary/monthly", response_model=MonthlySummary)
async def monthly_summary(
    year: int = Query(..., ge=2000, le=2100),
    month: int = Query(..., ge=1, le=12),
    user: User = Depends(current_user),
    service: TransactionService = Depends(transaction_service),
):
    return await service.monthly_summary(user.id, year, month)


@router.get("/{transaction_id}", response_model=TransactionResponse)
async def get_transaction(
    transaction_id: str,
    user: User = Depends(current_user),
    service: TransactionService = Depends(transaction_service),
):
    return await service.get(user.id, transaction_id)


@router.patch("/{transaction_id}", response_model=TransactionResponse)
async def update_transaction(
    transaction_id: str,
    data: TransactionUpdate,
    user: User = Depends(current_user),
    service: TransactionService = Depends(transaction_service),
):
    return await service.update(user.id, transaction_id, data)


@router.put("/{transaction_id}", response_model=TransactionResponse)
async def replace_transaction(
    transaction_id: str,
    data: TransactionUpdate,
    user: User = Depends(current_user),
    service: TransactionService = Depends(transaction_service),
):
    return await service.update(user.id, transaction_id, data)


@router.delete("/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_transaction(
    transaction_id: str,
    user: User = Depends(current_user),
    service: TransactionService = Depends(transaction_service),
):
    await service.delete(user.id, transaction_id)

