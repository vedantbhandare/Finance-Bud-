from __future__ import annotations

from app.api.schemas import FinancialContextResponse


SYSTEM_PROMPT = """You are Finance Buddy, a practical personal finance assistant for Indian users.

Rules:
- Never invent balances, budgets, categories, or goal progress.
- Use only the verified context below for financial facts.
- Use INR and concise mobile-friendly answers.
- Do not recommend specific stocks, funds, or financial products.
- If data is missing, say what is missing and suggest the next useful app action.

Verified financial context:
{context}
"""


def build_prompt(context: FinancialContextResponse, history: list[tuple[str, str]], message: str) -> str:
    history_text = "\n".join(f"{role}: {content}" for role, content in history[-10:])
    context_text = context.model_dump_json(indent=2)
    prompt = SYSTEM_PROMPT.format(context=context_text)
    if history_text:
        prompt += f"\nConversation history:\n{history_text}\n"
    prompt += f"\nUser: {message}\nAssistant:"
    return prompt

