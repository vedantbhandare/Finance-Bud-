"""Chat router — conversational AI finance assistant."""
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db_session
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.chat import ChatRequest, ChatResponse
from app.ai.orchestrator import AIOrchestrator

router = APIRouter()


@router.post("/message", response_model=ChatResponse)
async def send_message(
    data: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
):
    """Send a message to the AI finance assistant."""
    orchestrator = AIOrchestrator(db)
    try:
        response = await orchestrator.chat(
            user_id=current_user.id,
            message=data.message,
            conversation_id=data.conversation_id,
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI service error: {str(e)}")


@router.get("/conversations")
async def list_conversations(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
):
    """Get conversation list for the current user."""
    from app.repositories.conversation_repo import ConversationRepository
    repo = ConversationRepository(db)
    conversations = await repo.get_user_conversations(current_user.id)
    return conversations


@router.get("/conversations/{conversation_id}/messages")
async def get_conversation_messages(
    conversation_id: UUID,
    limit: int = Query(50, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
):
    """Get messages for a specific conversation."""
    from app.repositories.conversation_repo import MessageRepository
    repo = MessageRepository(db)
    messages = await repo.get_conversation_messages(conversation_id, limit=limit)
    return messages
