"""AI fallbacks — graceful degradation when Gemini is unavailable.

Uses random selection instead of the original global mutable index,
making the module stateless and process-safe.
"""

from __future__ import annotations

import random

FALLBACK_RESPONSES = [
    (
        "I'm having a bit of trouble connecting right now, but don't worry! "
        "Check your dashboard for your latest spending summary and budget status. "
        "I'll be back to full speed shortly! 💪"
    ),
    (
        "Looks like I need a moment to gather my thoughts. "
        "In the meantime, your financial data is always available on your dashboard. "
        "Try again in a few seconds! 🙏"
    ),
    (
        "I'm temporarily offline — but your numbers are safe! "
        "Head to the dashboard for your spending summary while I reconnect. 🔄"
    ),
]


def generate_fallback_response() -> str:
    """Return a helpful fallback response (stateless, random selection)."""
    return random.choice(FALLBACK_RESPONSES)
