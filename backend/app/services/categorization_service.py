"""Categorization service — rule-based + AI fallback for expense categorization."""
from app.rules.categorization_rules import categorize_by_keyword


class CategorizationService:
    """Categorizes transactions using rules first, AI as fallback."""

    def categorize(self, description: str, merchant: str | None = None) -> str | None:
        """Attempt to categorize a transaction.

        Returns category name or None if no match found.
        """
        # Try rule-based first (fast, deterministic)
        text = f"{description} {merchant or ''}".strip()
        category = categorize_by_keyword(text)
        if category:
            return category

        # TODO: AI fallback — call Gemini for ambiguous transactions
        return None
