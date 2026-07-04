import streamlit as st
import pandas as pd
from src.categorizer import categorize, categorize_dataframe, update_category

st.set_page_config(page_title="Transactions | FinPulse", page_icon="🗂️")

st.markdown("# Transactions")

transactions = st.session_state.get("categorized")
if transactions is None:
    st.info("Upload a bank statement in the sidebar to view transactions.")
else:
    df = transactions.copy()
    st.markdown("## Search & recategorize")
    search_value = st.text_input("Search transactions", value="")
    filtered = df[df["description"].str.contains(search_value, case=False, na=False)] if search_value else df

    csv = filtered.to_csv(index=False)
    st.download_button("Export filtered CSV", data=csv, file_name="finpulse_transactions.csv", mime="text/csv")

    st.markdown("### Manual category overrides")
    categories = list(sorted(set(df["category"])))
    overrides = []
    for idx, row in filtered.reset_index().iterrows():
        category = st.selectbox(
            f"Category for {row['description']}",
            options=categories,
            index=categories.index(row["category"]),
            key=f"category_{idx}",
        )
        if category != row["category"]:
            overrides.append((row["index"], category))
    if overrides:
        for original_idx, new_category in overrides:
            df.at[original_idx, "category"] = new_category
        st.session_state["categorized"] = df
        st.success("Categories updated.")

    st.dataframe(filtered, use_container_width=True)
