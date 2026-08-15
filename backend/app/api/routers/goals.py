from __future__ import annotations

from fastapi import APIRouter, Depends, Query, status

from app.api.deps import current_user, goal_service
from app.api.schemas import ContributionCreate, GoalCreate, GoalResponse, GoalUpdate
from app.application.goals import GoalService
from app.infrastructure.orm.models import User

router = APIRouter(prefix="/goals", tags=["Goals"])


@router.get("", response_model=list[GoalResponse])
async def list_goals(
    status_filter: str | None = Query(default=None, pattern="^(active|paused|completed|abandoned)$"),
    user: User = Depends(current_user),
    service: GoalService = Depends(goal_service),
):
    return await service.list(user.id, status_filter)


@router.post("", response_model=GoalResponse, status_code=status.HTTP_201_CREATED)
async def create_goal(data: GoalCreate, user: User = Depends(current_user), service: GoalService = Depends(goal_service)):
    return await service.create(user.id, data)


@router.get("/{goal_id}", response_model=GoalResponse)
async def get_goal(goal_id: str, user: User = Depends(current_user), service: GoalService = Depends(goal_service)):
    return await service.get(user.id, goal_id)


@router.patch("/{goal_id}", response_model=GoalResponse)
async def update_goal(goal_id: str, data: GoalUpdate, user: User = Depends(current_user), service: GoalService = Depends(goal_service)):
    return await service.update(user.id, goal_id, data)


@router.put("/{goal_id}", response_model=GoalResponse)
async def replace_goal(goal_id: str, data: GoalUpdate, user: User = Depends(current_user), service: GoalService = Depends(goal_service)):
    return await service.update(user.id, goal_id, data)


@router.delete("/{goal_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_goal(goal_id: str, user: User = Depends(current_user), service: GoalService = Depends(goal_service)):
    await service.delete(user.id, goal_id)


@router.post("/{goal_id}/contribute", response_model=GoalResponse)
async def contribute(goal_id: str, data: ContributionCreate, user: User = Depends(current_user), service: GoalService = Depends(goal_service)):
    return await service.contribute(user.id, goal_id, data)

