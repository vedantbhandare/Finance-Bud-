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

Budget pacing (spent vs. allocated per category):
{budget_pacing}

Spending trend vs. last month: {spending_trend}
"""


def _format_budget_pacing(context: FinancialContextResponse) -> str:
    if not context.budget_allocations:
        return "No active budget allocations."
    lines: list[str] = []
    for a in context.budget_allocations:
        pct = f"{a.utilization_pct:.0f}%" if a.utilization_pct else "0%"
        lines.append(
            f"  {a.category_name}: ₹{a.spent_amount:,.0f} / ₹{a.allocated_amount:,.0f} ({pct} used)"
        )
    return "\n".join(lines)


def build_prompt(context: FinancialContextResponse, history: list[tuple[str, str]], message: str) -> str:
    history_text = "\n".join(f"{role}: {content}" for role, content in history[-10:])
    context_text = context.model_dump_json(indent=2)
    budget_pacing = _format_budget_pacing(context)
    prompt = SYSTEM_PROMPT.format(
        context=context_text,
        budget_pacing=budget_pacing,
        spending_trend=context.spending_trend,
    )
    if history_text:
        prompt += f"\nConversation history:\n{history_text}\n"
    prompt += f"\nUser: {message}\nAssistant:"
    return prompt
