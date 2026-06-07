"""Conversation and Message repositories."""

from __future__ import annotations

import uuid
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.models.conversation import Conversation, Message
from app.repositories.base import BaseRepository


class ConversationRepository(BaseRepository[Conversation]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(Conversation, session)

    async def get_user_conversations(
        self,
        user_id: uuid.UUID,
        *,
        offset: int = 0,
        limit: int = 20,
    ) -> Sequence[Conversation]:
        result = await self.session.execute(
            select(Conversation)
            .where(Conversation.user_id == user_id)
            .order_by(Conversation.updated_at.desc())
            .offset(offset)
            .limit(limit),
        )
        return result.scalars().all()

    async def get_with_messages(
        self,
        conversation_id: uuid.UUID,
        *,
        message_limit: int = 50,
    ) -> Conversation | None:
        result = await self.session.execute(
            select(Conversation)
            .options(joinedload(Conversation.messages))
            .where(Conversation.id == conversation_id),
        )
        return result.unique().scalar_one_or_none()


class MessageRepository(BaseRepository[Message]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(Message, session)

    async def get_conversation_messages(
        self,
        conversation_id: uuid.UUID,
        *,
        limit: int = 50,
    ) -> Sequence[Message]:
        result = await self.session.execute(
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.created_at.asc())
            .limit(limit),
        )
        return result.scalars().all()

    async def get_recent_messages(
        self,
        conversation_id: uuid.UUID,
        count: int = 10,
    ) -> Sequence[Message]:
        """Return the most recent *count* messages (oldest-first)."""
        result = await self.session.execute(
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.created_at.desc())
            .limit(count),
        )
        return list(reversed(result.scalars().all()))
