"""
utils/categorizer.py
Rule-based expense categorizer using keyword matching.

Categories (in priority order):
  Food & Dining, Transport, Shopping, Entertainment,
  Health & Wellness, Utilities & Bills, Travel, Education, Other
"""

from typing import List, Dict, Any


# Each entry: (category_label, [keywords_lowercase])
CATEGORY_RULES: List[tuple] = [
    ("Food & Dining", [
        "restaurant", "cafe", "coffee", "starbucks", "mcdonald", "kfc", "burger",
        "pizza", "sushi", "food", "lunch", "dinner", "breakfast", "grocery",
        "supermarket", "bakery", "bar", "pub", "swiggy", "zomato", "uber eats",
        "doordash", "grubhub", "subway", "domino",
    ]),
    ("Transport", [
        "uber", "lyft", "taxi", "cab", "metro", "bus", "train", "railway",
        "fuel", "petrol", "gas station", "parking", "toll", "ola", "rapido",
        "transit", "commute", "auto",
    ]),
    ("Shopping", [
        "amazon", "walmart", "target", "ebay", "flipkart", "myntra", "zara",
        "h&m", "clothing", "apparel", "fashion", "shoes", "electronics",
        "gadget", "store", "mall", "shop", "purchase", "order",
    ]),
    ("Entertainment", [
        "netflix", "spotify", "youtube", "prime", "hulu", "cinema", "movie",
        "theatre", "concert", "game", "steam", "playstation", "xbox",
        "subscription", "streaming", "disney",
    ]),
    ("Health & Wellness", [
        "pharmacy", "medicine", "doctor", "hospital", "clinic", "gym",
        "fitness", "health", "dental", "optical", "medic", "drug", "cvs",
        "walgreens", "apollo", "lab test", "wellness",
    ]),
    ("Utilities & Bills", [
        "electricity", "water bill", "internet", "broadband", "phone bill",
        "mobile", "recharge", "utility", "rent", "insurance", "emi",
        "mortgage", "maintenance", "gas bill",
    ]),
    ("Travel", [
        "hotel", "airbnb", "flight", "airline", "booking", "airfare",
        "holiday", "resort", "trip", "travel", "expedia", "makemytrip",
        "goibibo", "hostel", "accommodation",
    ]),
    ("Education", [
        "udemy", "coursera", "book", "course", "tuition", "college",
        "university", "school", "education", "learning", "library",
        "textbook", "certification",
    ]),
]

DEFAULT_CATEGORY = "Other"


def categorize(description: str) -> str:
    """Return category label for a transaction description string."""
    desc_lower = description.lower()
    for category, keywords in CATEGORY_RULES:
        if any(kw in desc_lower for kw in keywords):
            return category
    return DEFAULT_CATEGORY


def categorize_transactions(
    transactions: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """Add a 'category' key to each transaction dict in-place and return list."""
    for tx in transactions:
        tx["category"] = categorize(tx.get("description", ""))
    return transactions


def build_category_summary(
    transactions: List[Dict[str, Any]]
) -> Dict[str, float]:
    """Return total spend per category, sorted descending."""
    summary: Dict[str, float] = {}
    for tx in transactions:
        cat = tx.get("category", DEFAULT_CATEGORY)
        summary[cat] = round(summary.get(cat, 0.0) + float(tx["amount"]), 2)
    return dict(sorted(summary.items(), key=lambda x: x[1], reverse=True))


def build_monthly_summary(
    transactions: List[Dict[str, Any]]
) -> Dict[str, float]:
    """Return total spend per YYYY-MM month string, sorted chronologically."""
    summary: Dict[str, float] = {}
    for tx in transactions:
        month = tx.get("date", "")[:7]  # "YYYY-MM"
        summary[month] = round(summary.get(month, 0.0) + float(tx["amount"]), 2)
    return dict(sorted(summary.items()))
