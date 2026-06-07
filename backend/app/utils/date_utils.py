"""Date / period helper functions for pay-cycle and budget periods."""

from __future__ import annotations

import calendar
from datetime import date, timedelta


def get_month_range(year: int, month: int) -> tuple[date, date]:
    """Return (first_day, last_day) of the given month."""
    first = date(year, month, 1)
    _, last_day = calendar.monthrange(year, month)
    last = date(year, month, last_day)
    return first, last


def get_current_month_range() -> tuple[date, date]:
    """Return (first_day, last_day) of the current month."""
    today = date.today()
    return get_month_range(today.year, today.month)


def get_pay_cycle_range(pay_cycle_day: int, reference_date: date | None = None) -> tuple[date, date]:
    """Return the pay cycle range containing *reference_date*.

    The pay cycle starts on *pay_cycle_day* of one month and ends
    the day before the next cycle.

    Parameters
    ----------
    pay_cycle_day:
        Day of month when salary is credited (1-28).
    reference_date:
        Date to anchor the cycle. Defaults to today.
    """
    ref = reference_date or date.today()
    pay_cycle_day = min(pay_cycle_day, 28)  # clamp to safe range

    if ref.day >= pay_cycle_day:
        start = ref.replace(day=pay_cycle_day)
    else:
        # Go to previous month
        prev_month = ref.replace(day=1) - timedelta(days=1)
        start = prev_month.replace(day=pay_cycle_day)

    # End is the day before the next cycle start
    if start.month == 12:
        next_start = start.replace(year=start.year + 1, month=1)
    else:
        next_start = start.replace(month=start.month + 1)
    end = next_start - timedelta(days=1)

    return start, end


def days_remaining_in_month(reference_date: date | None = None) -> int:
    """Return the number of days remaining in the month (including today)."""
    ref = reference_date or date.today()
    _, last_day = calendar.monthrange(ref.year, ref.month)
    return last_day - ref.day + 1


def get_previous_months(count: int, reference_date: date | None = None) -> list[tuple[int, int]]:
    """Return a list of (year, month) tuples for the *count* months
    preceding *reference_date* (exclusive of the reference month)."""
    ref = reference_date or date.today()
    result: list[tuple[int, int]] = []
    for i in range(1, count + 1):
        month = ref.month - i
        year = ref.year
        while month <= 0:
            month += 12
            year -= 1
        result.append((year, month))
    return result
