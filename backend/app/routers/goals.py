"""Goals router — CRUD + contributions."""
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db_session
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.goal import ContributionCreate, GoalCreate, GoalResponse, GoalUpdate
from app.services.goal_service import GoalService

router = APIRouter()


@router.get("")
async def list_goals(
    status_filter: str | None = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
):
    """Get all goals for the current user."""
    service = GoalService(db)
    goals = await service.get_goals(current_user.id, status=status_filter)
    return [GoalResponse.model_validate(g) for g in goals]


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_goal(
    data: GoalCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
):
    """Create a new financial goal."""
    service = GoalService(db)
    goal = await service.create_goal(current_user.id, data)
    return GoalResponse.model_validate(goal)


@router.get("/{goal_id}")
async def get_goal(
    goal_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
):
    """Get a single goal."""
    service = GoalService(db)
    goal = await service.get_goal(current_user.id, goal_id)
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    return GoalResponse.model_validate(goal)


@router.put("/{goal_id}")
async def update_goal(
    goal_id: UUID,
    data: GoalUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
):
    """Update a goal."""
    service = GoalService(db)
    goal = await service.update_goal(current_user.id, goal_id, data)
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    return GoalResponse.model_validate(goal)


@router.delete("/{goal_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_goal(
    goal_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
):
    """Delete a goal."""
    service = GoalService(db)
    deleted = await service.delete_goal(current_user.id, goal_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Goal not found")


@router.post("/{goal_id}/contribute")
async def contribute_to_goal(
    goal_id: UUID,
    data: ContributionCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
):
    """Add a contribution to a goal."""
    service = GoalService(db)
    try:
        goal = await service.contribute(current_user.id, goal_id, data)
        return GoalResponse.model_validate(goal)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
