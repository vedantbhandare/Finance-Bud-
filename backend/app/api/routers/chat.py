from __future__ import annotations

from fastapi import APIRouter, Depends, Query

from app.api.deps import chat_service, current_user
from app.api.schemas import ChatRequest, ChatResponse, ConversationResponse, MessageResponse
from app.application.chat import ChatService
from app.infrastructure.orm.models import User

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("/message", response_model=ChatResponse)
async def send(data: ChatRequest, user: User = Depends(current_user), service: ChatService = Depends(chat_service)):
    return await service.send(user, data.message, data.conversation_id)


@router.get("/conversations", response_model=list[ConversationResponse])
async def conversations(user: User = Depends(current_user), service: ChatService = Depends(chat_service)):
    return await service.list_conversations(user.id)


@router.get("/conversations/{conversation_id}/messages", response_model=list[MessageResponse])
async def messages(
    conversation_id: str,
    limit: int = Query(50, ge=1, le=100),
    user: User = Depends(current_user),
    service: ChatService = Depends(chat_service),
):
    return await service.messages_for(user.id, conversation_id, limit)

