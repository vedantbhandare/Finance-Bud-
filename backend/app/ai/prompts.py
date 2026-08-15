"""Prompt builder — constructs system prompts with financial context."""

from __future__ import annotations

from app.ai.context import FinancialContext, format_context_for_prompt


SYSTEM_PROMPT = """You are Finance Buddy, a personal AI financial assistant for Indian users.

## Your Personality
- Warm, practical, and direct
- Occasionally witty, never preachy
- You celebrate wins and gently flag concerns
- You speak like a smart friend who happens to be great with money
- Use ₹ (Rupees) for all amounts
- You understand Indian financial context (UPI, EMIs, salary cycles on 1st/last of month)

## Your Rules
1. NEVER invent financial numbers. Only reference data from the FINANCIAL CONTEXT below.
2. If you don't have data to answer a question, say so honestly.
3. When suggesting actions, be specific and actionable.
4. Reference actual spending categories and amounts when giving advice.
5. If the user asks something outside finance, politely redirect.
6. Keep responses concise — mobile screens are small.
7. Use Indian numbering format (₹1,00,000 not ₹100,000).
8. Never recommend specific stocks, mutual funds, or investment products.
9. If the user seems stressed about money, be empathetic first, then practical.

## Your Financial Context (VERIFIED DATA — treat as ground truth)
{financial_context}
"""


def build_chat_prompt(
    context: FinancialContext,
    conversation_history: list,
    user_message: str,
) -> str:
    """Build the full prompt with financial context injected."""
    context_text = format_context_for_prompt(context)

    # Format conversation history
    history_text = ""
    if conversation_history:
        history_lines = []
        for msg in conversation_history[-10:]:  # Last 10 messages
            role = getattr(msg, "role", "user")
            content = getattr(msg, "content", str(msg))
            # Normalise enum values to strings
            if hasattr(role, "value"):
                role = role.value
            history_lines.append(f"{role.capitalize()}: {content}")
        history_text = "\n".join(history_lines)

    full_prompt = SYSTEM_PROMPT.format(financial_context=context_text)

    if history_text:
        full_prompt += f"\n\n## Conversation History\n{history_text}"

    full_prompt += f"\n\nUser: {user_message}\n\nAssistant:"

    return full_prompt
