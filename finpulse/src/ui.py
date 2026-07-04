from __future__ import annotations

from pathlib import Path
from typing import Any

import streamlit as st

from src.categorizer import categorize_dataframe
from src.parser import load_statement


def load_css() -> None:
    if st.session_state.get("css_loaded"):
        return
    css_path = Path("assets/style.css")
    if css_path.exists():
        with css_path.open("r") as style_file:
            st.markdown(f"<style>{style_file.read()}</style>", unsafe_allow_html=True)
    st.session_state["css_loaded"] = True


def sidebar_state() -> Any:
    st.sidebar.markdown("# FinPulse")
    st.sidebar.markdown("A premium personal finance dashboard for monthly statements.")
    uploaded = st.sidebar.file_uploader("Upload bank statement CSV", type=["csv"])
    sample_button = st.sidebar.button("Load sample statement")

    transactions = st.session_state.get("categorized")
    if uploaded is not None:
        data, parse_state = load_statement(uploaded)
        if parse_state["error"]:
            st.sidebar.error(parse_state["message"])
            transactions = None
        else:
            categorized = categorize_dataframe(data)
            st.session_state["transactions"] = data
            st.session_state["categorized"] = categorized
            st.sidebar.success("Statement uploaded successfully")
            transactions = categorized
    elif sample_button:
        sample_path = Path("data/sample_statement.csv")
        if sample_path.exists():
            data, parse_state = load_statement(sample_path)
            if parse_state["error"]:
                st.sidebar.error(parse_state["message"])
                transactions = None
            else:
                categorized = categorize_dataframe(data)
                st.session_state["transactions"] = data
                st.session_state["categorized"] = categorized
                st.sidebar.success("Sample statement loaded")
                transactions = categorized
        else:
            st.sidebar.error("Sample data file not found.")
            transactions = None
    elif transactions is None:
        st.sidebar.info("Upload a CSV or load the sample statement to begin.")

    st.sidebar.markdown("\n---\nPowered by Streamlit + Plotly")
    return transactions
