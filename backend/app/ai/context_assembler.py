"""Context assembler — builds financial snapshot for AI prompts.

This is the CRITICAL BRIDGE between deterministic services and AI.
The AI only sees what this module provides. It cannot access the DB directly.
"""
from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession


@dataclass
class FinancialContext:
    """Pre-computed financial snapshot injected into AI prompts."""
    monthly_income: Decimal = Decimal("0")
    total_spent_this_month: Decimal = Decimal("0")
    remaining_budget: Decimal = Decimal("0")
    top_spending_categories: list[dict] = field(default_factory=list)
    recent_transactions: list[dict] = field(default_factory=list)
    active_goals: list[dict] = field(default_factory=list)
    health_score: int = 0
    days_until_payday: int = 0
    overspending_alerts: list[str] = field(default_factory=list)
    savings_rate: Decimal = Decimal("0")
    currency: str = "INR"


async def assemble_context(user_id: UUID, db: AsyncSession) -> FinancialContext:
    """Gather all relevant financial data into a structured context.

    This is the ONLY data the AI sees. It cannot access the DB directly.
    All values are pre-computed by deterministic services.
    """
    context = FinancialContext()

    try:
        from app.services.transaction_service import TransactionService

        txn_service = TransactionService(db)
        today = date.today()

        # Get recent transactions
        recent = await txn_service.get_recent_transactions(user_id, limit=5)
        context.recent_transactions = [
            {
                "amount": str(t.amount),
                "type": t.transaction_type.value,
                "description": t.description or "N/A",
                "date": str(t.transaction_date),
            }
            for t in recent
        ]

        # Get monthly spending
        context.total_spent_this_month = await txn_service.get_total_spent_this_month(user_id)

    except Exception:
        pass  # Context assembly should never crash — partial context is fine

    return context


def format_context_for_prompt(context: FinancialContext) -> str:
    """Format financial context as human-readable text for prompt injection."""
    lines = [
        f"Currency: ₹ (INR)",
        f"Monthly Income: ₹{context.monthly_income:,.2f}",
        f"Spent This Month: ₹{context.total_spent_this_month:,.2f}",
        f"Remaining Budget: ₹{context.remaining_budget:,.2f}",
        f"Health Score: {context.health_score}/100",
    ]

    if context.recent_transactions:
        lines.append("\nRecent Transactions:")
        for t in context.recent_transactions[:5]:
            lines.append(f"  • ₹{t['amount']} ({t['type']}) — {t['description']} on {t['date']}")

    if context.active_goals:
        lines.append("\nActive Goals:")
        for g in context.active_goals:
            lines.append(f"  • {g['name']}: ₹{g['current']}/{g['target']} ({g['progress_pct']}%)")

    if context.overspending_alerts:
        lines.append("\n⚠️ Alerts:")
        for alert in context.overspending_alerts:
            lines.append(f"  • {alert}")

    return "\n".join(lines)
