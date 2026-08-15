from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import current_user
from app.api.schemas import CategoryResponse, category_to_response
from app.core.database import db_session
from app.infrastructure.orm.models import User
from app.infrastructure.orm.repositories import CategoryRepository

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get("", response_model=list[CategoryResponse])
async def list_categories(user: User = Depends(current_user), session: AsyncSession = Depends(db_session)):
    repo = CategoryRepository(session)
    await repo.ensure_system_categories()
    return [category_to_response(category) for category in await repo.available_to_user(user.id)]

