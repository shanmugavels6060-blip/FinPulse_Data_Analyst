import streamlit as st
from src.analytics import summarize_financials, build_health_score, category_percentages
from src.charts import category_donut, savings_gauge, trend_line

st.set_page_config(page_title="Dashboard | FinPulse", page_icon="📊")

st.markdown("# Dashboard")

transactions = st.session_state.get("categorized")
if transactions is None:
    st.info("Upload a bank statement in the sidebar to see the dashboard metrics.")
else:
    with st.spinner("Analyzing your spending..."):
        summary = summarize_financials(transactions)
        health = build_health_score(transactions)
        category_data = category_percentages(transactions)

    metrics = st.columns(4)
    metrics[0].metric("Total Income", f"${summary['income']:,.0f}")
    metrics[1].metric("Total Spend", f"${abs(summary['expenses']):,.0f}")
    metrics[2].metric("Savings Rate", f"{summary['savings_rate']:.1f}%")
    metrics[3].metric("Health Score", f"{health['score']} / 100")

    st.markdown("---")
    top_row = st.columns((2, 1))
    with top_row[0]:
        st.markdown("### Category Breakdown")
        st.plotly_chart(category_donut(transactions), use_container_width=True)
    with top_row[1]:
        st.markdown("### Financial Health")
        st.plotly_chart(savings_gauge(health["score"]), use_container_width=True)

    st.markdown("---")
    trend_col, callout_col = st.columns((2, 1))
    with trend_col:
        st.markdown("### Monthly Trend")
        st.plotly_chart(trend_line(transactions), use_container_width=True)
    with callout_col:
        st.markdown("### Top Categories")
        for _, row in summary["top_categories"].iterrows():
            st.markdown(f"**{row['category']}** — ${row['total']:,.0f}")
        biggest = summary["biggest_transaction"]
        st.markdown("### Biggest Transaction")
        st.markdown(f"**{biggest['description']}** on {biggest['date'].date()} — ${biggest['amount']:,.2f}")

    st.markdown("---")
    st.markdown("#### Spending health snapshot")
    st.write(f"Category share details and month-over-month consistency support your financial plan.")
