from __future__ import annotations

import re
import pandas as pd
import streamlit as st
from typing import Any

CATEGORY_RULES = {
    "Food & Dining": ["mcdonald", "starbucks", "swiggy", "zomato", "dominos", "restaurant", "cafe", "kfc", "pizza"],
    "Travel": ["uber", "ola", "lyft", "irctc", "indigo", "airlines", "petrol", "fuel", "metro", "toll"],
    "Shopping": ["amazon", "flipkart", "myntra", "ajio", "mall", "shopping"],
    "Bills & Utilities": ["electricity", "recharge", "airtel", "jio", "broadband", "water bill", "gas bill"],
    "Entertainment": ["netflix", "spotify", "prime video", "hotstar", "movie", "bookmyshow"],
    "Health": ["pharmacy", "hospital", "clinic", "apollo", "medplus"],
    "Rent & Housing": ["rent", "landlord", "maintenance"],
    "Groceries": ["bigbasket", "grofers", "dmart", "grocery", "supermarket"],
    "Income": ["salary", "credited", "refund", "interest"],
    "Transfers": ["upi", "neft", "imps", "transfer"],
    "Other": [],
}


def categorize(description: str) -> str:
    """Return the first matching category for a description."""
    if not isinstance(description, str):
        return "Other"

    normalized = description.lower()
    for category, keywords in CATEGORY_RULES.items():
        for keyword in keywords:
            pattern = rf"\b{re.escape(keyword)}\b"
            if re.search(pattern, normalized):
                return category
    return "Other"


@st.cache_data
def categorize_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Add a category column to the transactions DataFrame."""
    df = df.copy()
    df["category"] = df["description"].apply(categorize)
    return df


def update_category(df: pd.DataFrame, index: int, category: str) -> pd.DataFrame:
    df = df.copy()
    if 0 <= index < len(df):
        df.at[index, "category"] = category
    return df
