"""Financial value validators."""

from __future__ import annotations

from decimal import Decimal, InvalidOperation


def validate_amount(value: Decimal | str | float) -> Decimal:
    """Validate and normalise a monetary amount.

    Raises
    ------
    ValueError
        If the value is not a valid positive amount.
    """
    try:
        amount = Decimal(str(value))
    except (InvalidOperation, TypeError) as exc:
        raise ValueError(f"Invalid amount: {value}") from exc

    if amount < 0:
        raise ValueError("Amount must not be negative")

    # Round to 2 decimal places
    return amount.quantize(Decimal("0.01"))


def validate_percentage(value: Decimal | str | float) -> Decimal:
    """Validate a percentage is between 0 and 100."""
    try:
        pct = Decimal(str(value))
    except (InvalidOperation, TypeError) as exc:
        raise ValueError(f"Invalid percentage: {value}") from exc

    if not (Decimal("0") <= pct <= Decimal("100")):
        raise ValueError("Percentage must be between 0 and 100")

    return pct.quantize(Decimal("0.01"))


SUPPORTED_CURRENCIES = {"INR"}


def validate_currency(currency: str) -> str:
    """Validate currency code (only INR for MVP)."""
    code = currency.upper().strip()
    if code not in SUPPORTED_CURRENCIES:
        raise ValueError(f"Unsupported currency: {code}. Supported: {SUPPORTED_CURRENCIES}")
    return code
