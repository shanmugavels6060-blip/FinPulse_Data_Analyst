import streamlit as st
from src.budgets import initialize_budgets, evaluate_budgets
from src.charts import budget_bar_chart

st.set_page_config(page_title="Budgets | FinPulse", page_icon="🎯")

st.markdown("# Budgets")

transactions = st.session_state.get("categorized")
if transactions is None:
    st.info("Upload a bank statement in the sidebar to manage budgets.")
else:
    categories = sorted(transactions["category"].unique())
    if "budgets" not in st.session_state:
        st.session_state["budgets"] = initialize_budgets(categories)

    with st.form("budget_form"):
        st.markdown("### Set monthly limits")
        for category in categories:
            current = st.session_state["budgets"].get(category, 500.0)
            st.session_state["budgets"][category] = st.number_input(
                category,
                min_value=0.0,
                value=float(current),
                step=50.0,
                key=f"budget_{category}",
            )
        submitted = st.form_submit_button("Save budgets")

    if submitted:
        st.success("Budget targets saved for this session.")

    alerts = evaluate_budgets(transactions, st.session_state["budgets"])
    for alert in alerts:
        card_class = f"alert-card {alert['status']}"
        st.markdown(f"<div class='{card_class}'>\n  <p class='card-title'>{alert['category']}</p>\n  <p class='card-copy'>Spent ${alert['spent']:,.0f} of ${alert['limit']:,.0f} ({alert['ratio']*100:.0f}%)</p>\n</div>", unsafe_allow_html=True)

    st.markdown("---")
    st.plotly_chart(budget_bar_chart(transactions[transactions["amount"] < 0].groupby("category")["amount"].sum().abs(), st.session_state["budgets"]), use_container_width=True)
