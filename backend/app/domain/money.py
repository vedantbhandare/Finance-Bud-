from __future__ import annotations

from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from typing import Any

PAISE = Decimal("0.01")


def money(value: Any) -> Decimal:
    try:
        amount = Decimal(str(value))
    except (InvalidOperation, TypeError, ValueError) as exc:
        raise ValueError(f"Invalid money amount: {value!r}") from exc
    return amount.quantize(PAISE, rounding=ROUND_HALF_UP)


def positive_money(value: Any) -> Decimal:
    amount = money(value)
    if amount <= 0:
        raise ValueError("Amount must be greater than zero")
    return amount


def percent(value: Any) -> Decimal:
    amount = money(value)
    if amount < 0 or amount > 100:
        raise ValueError("Percentage must be between 0 and 100")
    return amount

