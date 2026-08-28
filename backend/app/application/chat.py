from __future__ import annotations

import time
from datetime import date
from decimal import Decimal

from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas import (
    ChatMetadata,
    ChatResponse,
    ConversationResponse,
    FinancialContextResponse,
    MessageResponse,
)
from app.application.budgets import BudgetService
from app.application.goals import GoalService
from app.application.health import HealthService
from app.application.serializers import budget_allocation_response
from app.application.transactions import TransactionService
from app.core.errors import NotFoundError
from app.core.time import pay_cycle_range
from app.infrastructure.ai.gateway import AiGateway
from app.infrastructure.ai.prompts import build_prompt
from app.infrastructure.orm.models import Conversation, Message, User
from app.infrastructure.orm.repositories import ConversationRepository, MessageRepository


class ChatService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.conversations = ConversationRepository(session)
        self.messages = MessageRepository(session)
        self.ai = AiGateway()

    async def context(self, user: User) -> FinancialContextResponse:
        today = date.today()
        txns = TransactionService(self.session)
        goals = GoalService(self.session)
        health = HealthService(self.session)
        budgets = BudgetService(self.session)

        summary = await txns.monthly_summary(user.id, today.year, today.month)
        recent = await txns.list(user.id, 1, 5)
        active_goals = await goals.list(user.id, "active")
        score = await health.current(user.id)
        _, cycle_end = pay_cycle_range(user.pay_cycle_day, today)
        income = user.monthly_salary or Decimal("0.00")

        # Include budget pacing data so the AI can answer
        # "Can I afford Swiggy tonight?" accurately.
        budget_envelope = await budgets.current(user.id)
        allocation_responses = []
        if budget_envelope.budget:
            allocation_responses = budget_envelope.budget.allocations

        return FinancialContextResponse(
            monthly_income=income,
            total_spent_this_month=summary.total_expenses,
            remaining_budget=max(Decimal("0.00"), income - summary.total_expenses),
            savings_rate=score.savings_rate,
            health_score=score.overall_score,
            days_until_payday=max((cycle_end - today).days, 0),
            spending_trend=score.spending_trend,
            top_spending_categories=summary.by_category[:5],
            recent_transactions=recent.items,
            active_goals=active_goals,
            budget_allocations=allocation_responses,
        )

    async def send(self, user: User, message_text: str, conversation_id: str | None = None) -> ChatResponse:
        start = time.time()
        conversation = None
        if conversation_id:
            conversation = await self.conversations.get(conversation_id)
            if not conversation or conversation.user_id != user.id:
                raise NotFoundError("Conversation not found")

        if not conversation:
            conversation = Conversation(user_id=user.id, title=message_text[:100])
            await self.conversations.add(conversation)

        self.session.add(Message(conversation_id=conversation.id, role="user", content=message_text))
        await self.session.flush()

        recent_messages = await self.messages.recent(conversation.id, 20)
        history = [(msg.role, msg.content) for msg in recent_messages]
        prompt = build_prompt(await self.context(user), history, message_text)
        reply, tokens, model = await self.ai.complete(prompt)

        self.session.add(Message(conversation_id=conversation.id, role="assistant", content=reply, token_count=tokens))
        await self.session.flush()

        return ChatResponse(
            conversation_id=conversation.id,
            reply=reply,
            suggestions=[],
            metadata=ChatMetadata(
                tokens_used=tokens,
                model=model,
                latency_ms=int((time.time() - start) * 1000),
            ),
        )

    async def list_conversations(self, user_id: str) -> list[ConversationResponse]:
        return [
            ConversationResponse.model_validate(conv, from_attributes=True)
            for conv in await self.conversations.for_user(user_id)
        ]

    async def messages_for(self, user_id: str, conversation_id: str, limit: int) -> list[MessageResponse]:
        conversation = await self.conversations.get(conversation_id)
        if not conversation or conversation.user_id != user_id:
            raise NotFoundError("Conversation not found")
        return [
            MessageResponse.model_validate(msg, from_attributes=True)
            for msg in await self.messages.list_for_conversation(conversation_id, limit)
        ]
