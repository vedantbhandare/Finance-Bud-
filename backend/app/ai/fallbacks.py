"""AI fallbacks — graceful degradation when Gemini is unavailable."""

FALLBACK_RESPONSES = [
    "I'm having a bit of trouble connecting right now, but don't worry! "
    "Check your dashboard for your latest spending summary and budget status. "
    "I'll be back to full speed shortly! 💪",

    "Looks like I need a moment to gather my thoughts. "
    "In the meantime, your financial data is always available on your dashboard. "
    "Try again in a few seconds! 🙏",
]

_fallback_index = 0


def generate_fallback_response() -> str:
    """Generate a helpful response without AI.
    Rotates through fallback messages.
    """
    global _fallback_index
    response = FALLBACK_RESPONSES[_fallback_index % len(FALLBACK_RESPONSES)]
    _fallback_index += 1
    return response
