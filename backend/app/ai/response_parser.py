"""AI response parser — structured output extraction from LLM responses."""
import json
import re


def extract_json_from_response(text: str) -> dict | None:
    """Try to extract JSON from an LLM response that may contain markdown."""
    # Try direct JSON parse first
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # Try extracting from markdown code block
    json_match = re.search(r"```(?:json)?\s*\n(.*?)\n```", text, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group(1))
        except json.JSONDecodeError:
            pass

    return None


def clean_response(text: str) -> str:
    """Clean up LLM response for display."""
    # Remove any system-level artifacts
    text = text.strip()
    # Remove trailing "Assistant:" if present
    if text.startswith("Assistant:"):
        text = text[len("Assistant:"):].strip()
    return text
