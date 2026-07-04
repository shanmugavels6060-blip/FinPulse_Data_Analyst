from __future__ import annotations

import pandas as pd
import streamlit as st

CATEGORY_THRESHOLD = 0.8


@st.cache_data
def summarize_financials(df: pd.DataFrame) -> dict:
    """Compute overall financial metrics from transactions."""
    expenses = df[df["amount"] < 0]["amount"].sum()
    income = df[df["amount"] >= 0]["amount"].sum()
    net_savings = income + expenses
    spend = abs(expenses)
    savings_rate = 0.0 if income == 0 else max(0.0, min(100.0, net_savings / income * 100))

    categories = (
        df[df["amount"] < 0]
        .groupby("category")["amount"]
        .sum()
        .abs()
        .sort_values(ascending=False)
    )

    top_categories = categories.head(3).reset_index().rename(columns={"amount": "total"})
    biggest_transaction = df.loc[df["amount"].abs().idxmax()] if not df.empty else None

    monthly = (
        df.assign(month=df["date"].dt.to_period("M"))
        .groupby(["month", "type"])["amount"]
        .sum()
        .unstack(fill_value=0)
        .reset_index()
    )

    return {
        "income": income,
        "expenses": expenses,
        "net_savings": net_savings,
        "savings_rate": savings_rate,
        "category_totals": categories,
        "top_categories": top_categories,
        "biggest_transaction": biggest_transaction,
        "monthly_trends": monthly,
    }


def health_score(savings_rate: float, spend_variance: float, adherence_score: float) -> tuple[int, str]:
    score = int(min(100, max(0, savings_rate * 0.4 + adherence_score * 0.3 + (100 - spend_variance) * 0.3)))
    if score >= 80:
        label = "Excellent"
    elif score >= 60:
        label = "Good"
    elif score >= 40:
        label = "Needs Attention"
    else:
        label = "At Risk"
    return score, label


def build_health_score(df: pd.DataFrame, budget_limits: dict | None = None) -> dict:
    summary = summarize_financials(df)
    savings_rate = summary["savings_rate"]
    monthly_spend = (
        df[df["amount"] < 0]
        .assign(month=df["date"].dt.to_period("M"))
        .groupby("month")["amount"]
        .sum()
        .abs()
    )
    variance = 0.0 if len(monthly_spend) <= 1 else float(monthly_spend.pct_change().fillna(0).std() * 100)
    adherence_score = 100.0
    if budget_limits:
        spent_by_category = df[df["amount"] < 0].groupby("category")["amount"].sum().abs()
        ratios = []
        for category, limit in budget_limits.items():
            if limit > 0:
                ratios.append(min(1.0, spent_by_category.get(category, 0.0) / limit))
        adherence_score = 100.0 if not ratios else max(0.0, 100.0 - sum(ratios) / len(ratios) * 100)
    score, label = health_score(savings_rate, variance, adherence_score)
    return {
        "score": score,
        "label": label,
        "savings_rate": savings_rate,
        "variance": variance,
        "adherence_score": adherence_score,
    }


@st.cache_data
def category_percentages(df: pd.DataFrame) -> pd.DataFrame:
    totals = df[df["amount"] < 0].groupby("category")["amount"].sum().abs()
    total_spend = totals.sum()
    if total_spend == 0:
        return pd.DataFrame(columns=["category", "amount", "percent"])
    return (
        totals.reset_index(name="amount")
        .assign(percent=lambda d: d["amount"] / total_spend * 100)
        .sort_values(by="amount", ascending=False)
    )
