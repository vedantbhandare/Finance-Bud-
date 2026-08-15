from __future__ import annotations

import calendar
from datetime import date, datetime, timedelta, timezone


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def month_range(year: int, month: int) -> tuple[date, date]:
    last_day = calendar.monthrange(year, month)[1]
    return date(year, month, 1), date(year, month, last_day)


def current_month_range(reference: date | None = None) -> tuple[date, date]:
    today = reference or date.today()
    return month_range(today.year, today.month)


def pay_cycle_range(pay_day: int, reference: date | None = None) -> tuple[date, date]:
    today = reference or date.today()
    pay_day = min(max(pay_day, 1), 28)

    if today.day >= pay_day:
        start = date(today.year, today.month, pay_day)
        next_year = today.year + 1 if today.month == 12 else today.year
        next_month = 1 if today.month == 12 else today.month + 1
        end = date(next_year, next_month, pay_day) - timedelta(days=1)
    else:
        prev_year = today.year - 1 if today.month == 1 else today.year
        prev_month = 12 if today.month == 1 else today.month - 1
        start = date(prev_year, prev_month, pay_day)
        end = date(today.year, today.month, pay_day) - timedelta(days=1)
    return start, end

