from __future__ import annotations

import pandas as pd
import streamlit as st
from io import StringIO
from typing import Dict, Tuple

REQUIRED_COLUMNS = ["date", "description", "amount"]
COLUMN_SYNONYMS = {
    "date": ["date", "transaction date", "posted date", "value date"],
    "description": ["description", "narration", "details", "memo", "transaction details"],
    "amount": ["amount", "debit", "credit", "debit amount", "credit amount", "transaction amount"],
}


def _find_normalized_name(header: str) -> str | None:
    normalized = header.strip().lower()
    for canonical, synonyms in COLUMN_SYNONYMS.items():
        if normalized in [item.lower() for item in synonyms]:
            return canonical
    return None


def _detect_columns(columns: pd.Index) -> Dict[str, str]:
    mapping: Dict[str, str] = {}
    lower_columns = [col.strip().lower() for col in columns]
    for original, normalized in zip(columns, lower_columns):
        found = _find_normalized_name(normalized)
        if found and found not in mapping:
            mapping[found] = original
    if "amount" not in mapping:
        debit_col = next((orig for orig, normalized in zip(columns, lower_columns) if normalized == "debit"), None)
        credit_col = next((orig for orig, normalized in zip(columns, lower_columns) if normalized == "credit"), None)
        if debit_col and credit_col:
            mapping["debit"] = debit_col
            mapping["credit"] = credit_col
    return mapping


def _build_amount(df: pd.DataFrame, mapping: Dict[str, str]) -> pd.Series:
    if "amount" in df.columns:
        amounts = pd.to_numeric(df["amount"], errors="coerce")
        return amounts
    if "debit" in df.columns and "credit" in df.columns:
        debit = pd.to_numeric(df["debit"], errors="coerce").fillna(0.0)
        credit = pd.to_numeric(df["credit"], errors="coerce").fillna(0.0)
        return credit - debit
    if "amount" in mapping:
        return pd.to_numeric(df[mapping["amount"]], errors="coerce")
    raise ValueError("Could not resolve amount columns")


def _build_type(amount_series: pd.Series) -> pd.Series:
    return amount_series.apply(lambda value: "credit" if value >= 0 else "debit")


def load_statement(uploaded_file) -> Tuple[pd.DataFrame | None, Dict[str, object]]:
    try:
        df = pd.read_csv(uploaded_file)
    except Exception as exc:
        return None, {"error": True, "message": "We could not read this CSV file. Please upload a valid bank statement."}

    if df.empty:
        return None, {"error": True, "message": "The uploaded CSV is empty. Please choose a valid bank statement export."}

    mapping = _detect_columns(df.columns)
    if not mapping or "description" not in mapping or ("amount" not in mapping and not ("debit" in mapping and "credit" in mapping)) or "date" not in mapping:
        return None, {"error": True, "message": "The file is missing one or more required columns: Date, Description, and Amount/Debit/Credit."}

    df = df.rename(columns={mapping[key]: key for key in mapping if key in mapping})
    df["date"] = pd.to_datetime(df["date"], dayfirst=False, errors="coerce")
    invalid_date_count = df["date"].isna().sum()
    df = df.dropna(subset=["date", "description"])

    amount_series = _build_amount(df, mapping)
    df["amount"] = amount_series
    df = df.dropna(subset=["amount"])
    df["type"] = _build_type(df["amount"])
    df = df[["date", "description", "amount", "type"]]
    df = df.sort_values(by="date", ascending=False).reset_index(drop=True)

    if invalid_date_count > 0:
        st.warning(f"{invalid_date_count} rows were dropped because the date could not be parsed.")

    return df, {"error": False, "message": "Statement loaded successfully."}
