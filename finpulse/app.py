import streamlit as st
from src.ui import load_css, sidebar_state

st.set_page_config(page_title="FinPulse", page_icon="💼", layout="wide")
load_css()

transactions = sidebar_state()

if transactions is None:
    st.markdown("# Welcome to FinPulse")
    st.markdown("Upload a CSV statement to unlock your spending story in elegant charts and budget insights.")
    st.markdown("#### Use the sidebar to load a sample statement and explore the pages.")
else:
    st.success("Statement loaded. Use the page menu to explore dashboard, transactions, budgets, and trends.")
