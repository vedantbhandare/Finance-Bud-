"""Chat schemas."""

from __future__ import annotations

import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ChatRequest(BaseModel):
    """User message to the AI assistant."""

    message: str = Field(min_length=1, max_length=2000)
    conversation_id: uuid.UUID | None = None


class ChatMetadata(BaseModel):
    """Response metadata for debugging."""
    tokens_used: int = 0
    model: str = "gemini-2.0-flash"
    latency_ms: int = 0


class ChatResponse(BaseModel):
    """AI response to user."""

    conversation_id: uuid.UUID
    reply: str
    suggestions: list[str] = []
    metadata: ChatMetadata = ChatMetadata()


class ConversationResponse(BaseModel):
    """Conversation summary."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    title: str
    created_at: datetime
    updated_at: datetime


class MessageResponse(BaseModel):
    """Single message in a conversation."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    role: str
    content: str
    created_at: datetime
