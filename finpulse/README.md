# FinPulse

FinPulse is a personal finance analytics dashboard built with Streamlit. Upload a monthly bank statement CSV to categorize transactions, visualize spending, track budgets, and explore financial health insights.

## Getting Started

1. Create a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the app:
   ```bash
   streamlit run app.py
   ```

## Features

- Upload bank statement CSVs with fuzzy header matching
- Automatic transaction categorization
- Interactive dashboard with Plotly charts
- Budgets with progress alerts and category limits
- Trend analysis across months
- Export filtered transactions and PDF summary

## Project Structure

- `app.py` — main Streamlit entry point
- `src/` — parsing, categorization, analytics, budgets, charts, and database helpers
- `pages/` — multipage interface
- `assets/style.css` — custom Streamlit styling
- `.streamlit/config.toml` — Streamlit theme
- `data/sample_statement.csv` — demo data

## Notes

Use the sample CSV to explore the app before uploading your own statement.
