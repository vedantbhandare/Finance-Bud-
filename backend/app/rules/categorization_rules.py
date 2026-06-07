"""Categorization rules — keyword-based expense categorization.

Pure functions. Fast, deterministic, no AI required.
"""

# Keyword → category mapping (India-specific)
KEYWORD_MAP: dict[str, list[str]] = {
    "Rent/Housing": ["rent", "housing", "flat", "apartment", "pg", "hostel", "society maintenance"],
    "Groceries/Kirana": ["grocery", "kirana", "bigbasket", "blinkit", "zepto", "dmart", "reliance fresh", "vegetable", "fruits"],
    "Utilities": ["electricity", "water bill", "gas", "lpg", "cylinder", "piped gas", "bescom", "msedcl"],
    "Phone/Internet": ["jio", "airtel", "vi", "bsnl", "wifi", "broadband", "recharge", "mobile bill"],
    "Insurance": ["insurance", "lic", "term plan", "health insurance", "star health", "hdfc ergo"],
    "EMI/Loan": ["emi", "loan", "home loan", "car loan", "personal loan", "credit card bill", "bajaj finserv"],
    "Auto/Riksha": ["auto", "riksha", "rickshaw", "auto fare"],
    "Fuel/Petrol": ["petrol", "diesel", "fuel", "hp", "iocl", "bpcl", "indian oil"],
    "Metro/Bus": ["metro", "bus", "dtc", "bmtc", "best bus", "metro card", "transit"],
    "Cab/Uber/Ola": ["uber", "ola", "rapido", "cab", "taxi", "indriver"],
    "Eating Out": ["restaurant", "hotel", "dhaba", "cafe", "dining", "lunch", "dinner", "brunch"],
    "Chai/Coffee": ["chai", "tea", "coffee", "starbucks", "ccd", "chaayos", "tapri"],
    "Swiggy/Zomato": ["swiggy", "zomato", "food delivery", "dunzo"],
    "Shopping": ["amazon", "flipkart", "myntra", "ajio", "meesho", "shopping", "clothes", "shoes"],
    "Entertainment": ["movie", "pvr", "inox", "netflix", "hotstar", "prime", "spotify", "concert", "game"],
    "Health/Medical": ["doctor", "hospital", "pharmacy", "medicine", "medical", "apollo", "1mg", "pharmeasy", "lab test"],
    "Gym/Fitness": ["gym", "fitness", "yoga", "cult.fit", "crossfit", "workout"],
    "Personal Care": ["salon", "haircut", "parlour", "beauty", "grooming", "spa"],
    "Education": ["course", "udemy", "coursera", "tuition", "school", "college", "books", "stationary"],
    "Subscriptions": ["subscription", "premium", "annual plan", "monthly plan"],
    "Gifts/Donations": ["gift", "donation", "charity", "birthday", "wedding"],
    "Travel/Vacation": ["flight", "train", "irctc", "makemytrip", "goibibo", "hotel booking", "vacation", "trip"],
}


def categorize_by_keyword(text: str) -> str | None:
    """Match transaction description to a category using keywords.

    Returns category name or None if no match found.
    Case-insensitive matching.
    """
    text_lower = text.lower().strip()
    if not text_lower:
        return None

    for category, keywords in KEYWORD_MAP.items():
        for keyword in keywords:
            if keyword in text_lower:
                return category

    return None
