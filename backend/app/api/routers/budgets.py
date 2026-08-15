from __future__ import annotations

from fastapi import APIRouter, Depends

from app.api.deps import budget_service, current_user
from app.api.schemas import BudgetEnvelope, BudgetGenerateResponse
from app.application.budgets import BudgetService
from app.infrastructure.orm.models import User

router = APIRouter(prefix="/budgets", tags=["Budgets"])


@router.get("/current", response_model=BudgetEnvelope)
async def current_budget(user: User = Depends(current_user), service: BudgetService = Depends(budget_service)):
    return await service.current(user.id)


@router.post("/generate", response_model=BudgetGenerateResponse)
async def generate_budget(user: User = Depends(current_user), service: BudgetService = Depends(budget_service)):
    return await service.generate(user)

