from __future__ import annotations

from fastapi import APIRouter, Depends

from app.api.deps import current_user, health_service
from app.api.schemas import HealthScoreResponse
from app.application.health import HealthService
from app.infrastructure.orm.models import User

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("/score", response_model=HealthScoreResponse)
async def score(user: User = Depends(current_user), service: HealthService = Depends(health_service)):
    return await service.current(user.id)


@router.get("/history")
async def history(user: User = Depends(current_user)):
    return {"snapshots": []}

