from __future__ import annotations

from fastapi import APIRouter, Depends

from app.api.deps import current_user, onboarding_service
from app.api.schemas import ExpenseSetup, GoalSetup, IncomeSetup, SpendingStyleSetup, StatusResponse
from app.application.onboarding import OnboardingService
from app.infrastructure.orm.models import User

router = APIRouter(prefix="/onboarding", tags=["Onboarding"])


@router.post("/income", response_model=StatusResponse)
async def income(data: IncomeSetup, user: User = Depends(current_user), service: OnboardingService = Depends(onboarding_service)):
    return await service.income(user, data)


@router.post("/expenses", response_model=StatusResponse)
async def expenses(data: ExpenseSetup, user: User = Depends(current_user), service: OnboardingService = Depends(onboarding_service)):
    return await service.expenses(user, data)


@router.post("/goals", response_model=StatusResponse)
async def goals(data: GoalSetup, user: User = Depends(current_user), service: OnboardingService = Depends(onboarding_service)):
    return await service.goals(user, data)


@router.post("/spending-style", response_model=StatusResponse)
async def spending_style(data: SpendingStyleSetup, user: User = Depends(current_user), service: OnboardingService = Depends(onboarding_service)):
    return await service.spending_style(user, data)


@router.post("/complete", response_model=StatusResponse)
async def complete(user: User = Depends(current_user), service: OnboardingService = Depends(onboarding_service)):
    return await service.complete(user)

