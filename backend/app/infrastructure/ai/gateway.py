from __future__ import annotations

import asyncio
import random

from app.core.config import get_settings

FALLBACKS = (
    "I cannot reach the AI service right now. Your dashboard still has the latest verified numbers.",
    "The AI connection is unavailable for a moment. Check your budget and recent transactions, then try again.",
    "I am temporarily offline, but your financial data is safe. Try again shortly.",
)


class AiGateway:
    async def complete(self, prompt: str) -> tuple[str, int, str]:
        settings = get_settings()
        if not settings.gemini_api_key:
            return random.choice(FALLBACKS), 0, "fallback"

        try:
            import google.generativeai as genai

            genai.configure(api_key=settings.gemini_api_key)
            model_name = "gemini-2.0-flash"
            model = genai.GenerativeModel(model_name)
            response = await asyncio.to_thread(
                model.generate_content,
                prompt,
                generation_config=genai.types.GenerationConfig(max_output_tokens=900, temperature=0.6),
            )
            tokens = getattr(getattr(response, "usage_metadata", None), "total_token_count", 0)
            return response.text, int(tokens or 0), model_name
        except Exception:
            return random.choice(FALLBACKS), 0, "fallback"

