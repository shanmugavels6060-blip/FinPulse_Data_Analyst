from __future__ import annotations

import pandas as pd
from typing import Any

STATUS_THRESHOLDS = {
    "on_track": 0.8,
    "warning": 1.0,
}


def initialize_budgets(categories: list[str], default_limit: float = 500.0) -> dict:
    return {category: default_limit for category in categories}


def evaluate_budgets(df: pd.DataFrame, budgets: dict) -> list[dict[str, Any]]:
    spent = df[df["amount"] < 0].groupby("category")["amount"].sum().abs()
    alerts = []
    for category, limit in budgets.items():
        spent_amount = float(spent.get(category, 0.0))
        ratio = 0.0 if limit <= 0 else spent_amount / limit
        status = "on_track" if ratio < STATUS_THRESHOLDS["on_track"] else "warning" if ratio <= STATUS_THRESHOLDS["warning"] else "exceeded"
        alerts.append({
            "category": category,
            "spent": spent_amount,
            "limit": limit,
            "ratio": ratio,
            "status": status,
        })
    return alerts
