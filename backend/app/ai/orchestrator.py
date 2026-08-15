"""AI Orchestrator — coordinates context assembly, prompt building, and LLM calls.

Uses Google Gemini API (free tier).
NEVER computes financial truth — only interprets pre-computed context.
"""

from __future__ import annotations

import asyncio
import time
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.context import assemble_context
from app.ai.fallbacks import generate_fallback_response
from app.ai.prompts import build_chat_prompt
from app.config import get_settings
from app.models.conversation import Conversation, Message
from app.repositories.conversation import ConversationRepository, MessageRepository
from app.schemas.chat import ChatMetadata, ChatResponse


class AIOrchestrator:
    """Main AI coordination — assembles context, calls Gemini, parses response."""

    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        self.settings = get_settings()
        self.conv_repo = ConversationRepository(db)
        self.msg_repo = MessageRepository(db)

    async def chat(
        self,
        user_id: UUID,
        message: str,
        conversation_id: UUID | None = None,
    ) -> ChatResponse:
        """Process a user message and return AI response."""
        start_time = time.time()

        # Get or create conversation
        conversation: Conversation | None = None
        if conversation_id:
            conversation = await self.conv_repo.get_by_id(conversation_id)
            if conversation and conversation.user_id != user_id:
                conversation = None

        if conversation is None:
            conversation = Conversation(user_id=user_id, title=message[:100])
            self.db.add(conversation)
            await self.db.flush()

        # Save user message
        user_msg = Message(
            conversation_id=conversation.id,
            role="user",
            content=message,
        )
        self.db.add(user_msg)

        # Assemble financial context (deterministic — all from DB)
        context = await assemble_context(user_id, self.db)

        # Get conversation history (last 20 messages)
        history = await self.msg_repo.get_recent_messages(conversation.id, count=20)

        # Build prompt
        prompt_text = build_chat_prompt(context, history, message)

        # Call Gemini
        reply_text, tokens_used, model_used = await self._call_gemini(prompt_text)

        latency_ms = int((time.time() - start_time) * 1000)

        # Save assistant response
        assistant_msg = Message(
            conversation_id=conversation.id,
            role="assistant",
            content=reply_text,
            token_count=tokens_used,
        )
        self.db.add(assistant_msg)
        await self.db.flush()

        return ChatResponse(
            reply=reply_text,
            conversation_id=conversation.id,
            metadata=ChatMetadata(
                tokens_used=tokens_used,
                model=model_used,
                latency_ms=latency_ms,
            ),
        )

    async def _call_gemini(self, prompt: str) -> tuple[str, int, str]:
        """Call Google Gemini API. Returns (response_text, tokens_used, model_name)."""
        model_name = "gemini-2.0-flash"

        if not self.settings.gemini_api_key:
            return generate_fallback_response(), 0, "fallback"

        try:
            import google.generativeai as genai

            genai.configure(api_key=self.settings.gemini_api_key)
            model = genai.GenerativeModel(model_name)

            response = await asyncio.to_thread(
                model.generate_content,
                prompt,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=1024,
                    temperature=0.7,
                ),
            )

            tokens_used = 0
            if hasattr(response, "usage_metadata"):
                tokens_used = getattr(
                    response.usage_metadata, "total_token_count", 0
                )

            return response.text, tokens_used, model_name

        except Exception:
            # Graceful degradation — never leave the user hanging
            return generate_fallback_response(), 0, "fallback"
