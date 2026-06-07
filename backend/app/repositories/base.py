"""Generic base repository with reusable CRUD operations."""

from __future__ import annotations

import uuid
from typing import Any, Generic, Sequence, TypeVar

from sqlalchemy import Select, delete, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.base import Base

ModelT = TypeVar("ModelT", bound=Base)


class BaseRepository(Generic[ModelT]):
    """Thin async repository wrapping common SQLAlchemy queries."""

    def __init__(self, model: type[ModelT], session: AsyncSession) -> None:
        self.model = model
        self.session = session

    async def get_by_id(self, entity_id: uuid.UUID) -> ModelT | None:
        result = await self.session.execute(
            select(self.model).where(self.model.id == entity_id),  # type: ignore[attr-defined]
        )
        return result.scalar_one_or_none()

    async def get_all(
        self,
        *,
        offset: int = 0,
        limit: int = 50,
        order_by: Any | None = None,
    ) -> Sequence[ModelT]:
        stmt: Select = select(self.model)
        if order_by is not None:
            stmt = stmt.order_by(order_by)
        stmt = stmt.offset(offset).limit(limit)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def count(self) -> int:
        result = await self.session.execute(
            select(func.count()).select_from(self.model),
        )
        return result.scalar_one()

    async def create(self, entity: ModelT) -> ModelT:
        self.session.add(entity)
        await self.session.flush()
        await self.session.refresh(entity)
        return entity

    async def update_by_id(
        self,
        entity_id: uuid.UUID,
        values: dict[str, Any],
    ) -> ModelT | None:
        await self.session.execute(
            update(self.model)
            .where(self.model.id == entity_id)  # type: ignore[attr-defined]
            .values(**values),
        )
        await self.session.flush()
        return await self.get_by_id(entity_id)

    async def delete_by_id(self, entity_id: uuid.UUID) -> bool:
        result = await self.session.execute(
            delete(self.model).where(self.model.id == entity_id),  # type: ignore[attr-defined]
        )
        await self.session.flush()
        return result.rowcount > 0  # type: ignore[union-attr]

    async def bulk_create(self, entities: list[ModelT]) -> list[ModelT]:
        self.session.add_all(entities)
        await self.session.flush()
        for entity in entities:
            await self.session.refresh(entity)
        return entities
