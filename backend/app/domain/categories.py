from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class CategorySeed:
    name: str
    icon: str
    color: str
    kind: str
    group: str
    keywords: tuple[str, ...] = ()


DEFAULT_CATEGORIES: tuple[CategorySeed, ...] = (
    CategorySeed("Rent/Housing", "🏠", "#F97316", "need", "essentials", ("rent", "housing")),
    CategorySeed("Groceries/Kirana", "🛒", "#84CC16", "need", "essentials", ("grocery", "kirana", "dmart", "zepto", "blinkit", "bigbasket")),
    CategorySeed("Utilities", "💡", "#EAB308", "need", "essentials", ("electricity", "water bill", "gas bill", "bescom")),
    CategorySeed("Phone/Internet", "📱", "#3B82F6", "need", "essentials", ("airtel", "jio", "vi ", "bsnl", "recharge", "broadband")),
    CategorySeed("Insurance", "🛡️", "#8B5CF6", "need", "essentials", ("insurance",)),
    CategorySeed("EMI/Loan", "🏦", "#EF4444", "need", "essentials", ("emi", "loan")),
    CategorySeed("Auto/Riksha", "🛺", "#F59E0B", "need", "transport", ("auto rickshaw", "rickshaw", "rapido", "namma yatri")),
    CategorySeed("Fuel/Petrol", "⛽", "#F97316", "need", "transport", ("fuel", "petrol", "diesel", "petrol pump")),
    CategorySeed("Metro/Bus", "🚇", "#06B6D4", "need", "transport", ("metro", "bus pass", "redbus")),
    CategorySeed("Cab/Uber/Ola", "🚗", "#14B8A6", "want", "transport", ("uber", "ola", "cab", "taxi")),
    CategorySeed("Eating Out", "🍽️", "#EC4899", "want", "food", ("restaurant", "cafe", "mcdonalds", "kfc", "dominos", "starbucks")),
    CategorySeed("Chai/Coffee", "☕", "#92400E", "want", "food", ("chai", "coffee", "chaayos")),
    CategorySeed("Swiggy/Zomato", "📦", "#F43F5E", "want", "food", ("swiggy", "zomato")),
    CategorySeed("Shopping", "🛍️", "#A855F7", "want", "lifestyle", ("amazon", "flipkart", "myntra", "ajio", "nykaa")),
    CategorySeed("Entertainment", "🎬", "#D946EF", "want", "lifestyle", ("netflix", "prime video", "hotstar", "spotify", "bookmyshow", "movie")),
    CategorySeed("Health/Medical", "🏥", "#10B981", "need", "lifestyle", ("medical", "pharmacy", "hospital", "doctor", "apollo")),
    CategorySeed("Gym/Fitness", "💪", "#84CC16", "want", "lifestyle", ("gym", "fitness", "cult fit")),
    CategorySeed("Personal Care", "💇", "#FB923C", "want", "lifestyle", ("salon", "personal care", "grooming")),
    CategorySeed("Education", "📚", "#0EA5E9", "need", "lifestyle", ("education", "course", "school", "college", "udemy")),
    CategorySeed("Subscriptions", "📺", "#7C3AED", "want", "subscriptions", ("subscription",)),
    CategorySeed("Gifts/Donations", "🎁", "#F472B6", "want", "other", ("gift", "donation")),
    CategorySeed("Travel/Vacation", "✈️", "#38BDF8", "want", "other", ("flight", "train", "hotel", "travel", "makemytrip", "irctc")),
    CategorySeed("Savings", "💰", "#22D3EE", "saving", "savings", ("savings",)),
    CategorySeed("Emergency Fund", "🚨", "#10B981", "saving", "savings", ("emergency fund",)),
    CategorySeed("Goals", "🎯", "#6366F1", "saving", "savings", ("goal",)),
    CategorySeed("Investments/SIP", "📈", "#14B8A6", "saving", "savings", ("sip", "investment", "mutual fund")),
    CategorySeed("Salary", "💵", "#10B981", "income", "income", ("salary", "payroll")),
    CategorySeed("Freelance", "💻", "#14B8A6", "income", "income", ("freelance",)),
    CategorySeed("Other Income", "₹", "#64748B", "income", "income", ("income",)),
    CategorySeed("Other", "📌", "#6B7280", "want", "other", ()),
)

_BY_NAME = {category.name.lower(): category for category in DEFAULT_CATEGORIES}

# Precompile word-boundary regex patterns for each category.
# Each category gets a single compiled pattern: \b(kw1|kw2|...)\b
_CATEGORY_PATTERNS: list[tuple[CategorySeed, re.Pattern[str]]] = []
for _cat in DEFAULT_CATEGORIES:
    if _cat.keywords:
        _joined = "|".join(re.escape(kw) for kw in _cat.keywords)
        _CATEGORY_PATTERNS.append((_cat, re.compile(rf"\b({_joined})", re.IGNORECASE)))


def category_seed(name: str | None) -> CategorySeed | None:
    if not name:
        return None
    return _BY_NAME.get(name.lower())


def color_for_category(name: str | None) -> str:
    seed = category_seed(name)
    return seed.color if seed else "#6B7280"


def icon_for_category(name: str | None) -> str | None:
    seed = category_seed(name)
    return seed.icon if seed else None


def categorize_text(description: str | None, merchant: str | None = None) -> str | None:
    """Categorize a transaction by matching keywords with word-boundary awareness.

    Uses precompiled regex patterns so 'auto' won't false-match
    'automatic payment', etc.
    """
    text = " ".join(part for part in (description, merchant) if part)
    if not text:
        return None
    for category, pattern in _CATEGORY_PATTERNS:
        if pattern.search(text):
            return category.name
    return None
