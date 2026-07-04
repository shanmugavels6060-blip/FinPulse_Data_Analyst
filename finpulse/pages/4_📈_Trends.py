import streamlit as st
from src.analytics import summarize_financials
from src.charts import trend_line, spend_heatmap
from fpdf import FPDF

st.set_page_config(page_title="Trends | FinPulse", page_icon="📈")

st.markdown("# Trends")

transactions = st.session_state.get("categorized")
if transactions is None:
    st.info("Upload a bank statement in the sidebar to explore trends.")
else:
    summary = summarize_financials(transactions)
    st.markdown("### Monthly Income & Expense")
    st.plotly_chart(trend_line(transactions), use_container_width=True)

    st.markdown("### Daily Spend Heatmap")
    st.plotly_chart(spend_heatmap(transactions), use_container_width=True)

    if st.button("Download PDF Summary"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(0, 10, "FinPulse Monthly Trend Summary", ln=True)
        pdf.cell(0, 8, f"Total income: ${summary['income']:,.0f}", ln=True)
        pdf.cell(0, 8, f"Total spend: ${abs(summary['expenses']):,.0f}", ln=True)
        pdf.cell(0, 8, f"Net savings: ${summary['net_savings']:,.0f}", ln=True)
        st.download_button("Download PDF", data=pdf.output(dest='S').encode('latin-1'), file_name="finpulse_trends.pdf", mime="application/pdf")
