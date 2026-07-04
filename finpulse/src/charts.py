from __future__ import annotations

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

PALETTE = ["#6C5CE7", "#4B7CF2", "#56CCF2", "#FF6B6B", "#FFC75F", "#A29BFE", "#00B894", "#F3A683"]


def load_palette() -> list[str]:
    return PALETTE


def category_donut(df: pd.DataFrame) -> go.Figure:
    totals = df[df["amount"] < 0].groupby("category")["amount"].sum().abs()
    labels = totals.index.tolist()
    values = totals.values.tolist()
    total_spend = sum(values)

    fig = go.Figure(go.Pie(
        labels=labels,
        values=values,
        hole=0.55,
        marker=dict(colors=PALETTE),
        hoverinfo="label+percent+value",
        textinfo="percent",
    ))
    fig.update_layout(
        showlegend=True,
        margin=dict(t=10, b=10, l=10, r=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        annotations=[dict(text=f"<b>${total_spend:,.0f}</b><br><span style='font-size:12px'>spent</span>", x=0.5, y=0.5, font_size=14, showarrow=False)],
    )
    return fig


def trend_line(df: pd.DataFrame) -> go.Figure:
    monthly = (
        df.assign(month=df["date"].dt.to_period("M").dt.to_timestamp())
        .groupby(["month", "type"])["amount"]
        .sum()
        .unstack(fill_value=0)
        .reset_index()
    )
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=monthly["month"],
        y=monthly.get("credit", [0]) if "credit" in monthly else [0],
        mode="lines+markers",
        name="Income",
        line=dict(color=PALETTE[0], width=3),
    ))
    fig.add_trace(go.Scatter(
        x=monthly["month"],
        y=monthly.get("debit", [0]).abs(),
        mode="lines+markers",
        name="Expenses",
        fill="tozeroy",
        line=dict(color=PALETTE[3], width=3),
    ))
    fig.update_layout(
        margin=dict(t=10, b=30, l=10, r=10),
        xaxis_title="Month",
        yaxis_title="Amount",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
    return fig


def budget_bar_chart(spend_by_category: pd.Series, budget_limits: dict) -> go.Figure:
    categories = list(budget_limits.keys())
    spent = [abs(spend_by_category.get(category, 0.0)) for category in categories]
    limits = [budget_limits.get(category, 0.0) for category in categories]
    fig = go.Figure()
    fig.add_trace(go.Bar(x=categories, y=spent, name="Spent", marker_color=PALETTE[3]))
    fig.add_trace(go.Bar(x=categories, y=limits, name="Budget", marker_color=PALETTE[1]))
    fig.update_layout(
        barmode="group",
        margin=dict(t=20, b=40, l=10, r=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
    return fig


def savings_gauge(score: int) -> go.Figure:
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        domain={"x": [0, 1], "y": [0, 1]},
        gauge={
            "axis": {"range": [0, 100], "tickwidth": 1, "tickcolor": "#1e1e2e"},
            "bar": {"color": PALETTE[0]},
            "bgcolor": "rgba(246, 246, 255, 0.9)",
            "steps": [
                {"range": [0, 40], "color": "#ff7d7d"},
                {"range": [40, 60], "color": "#f7c04a"},
                {"range": [60, 80], "color": "#6c5ce7"},
                {"range": [80, 100], "color": "#22c55e"},
            ],
        },
        number={"suffix": "%"},
        title={"text": "Health Score"},
    ))
    fig.update_layout(margin=dict(t=10, b=10, l=10, r=10), paper_bgcolor="rgba(0,0,0,0)")
    return fig


def spend_heatmap(df: pd.DataFrame) -> go.Figure:
    daily = (
        df[df["amount"] < 0]
        .assign(date_only=df["date"].dt.date)
        .groupby("date_only")["amount"]
        .sum()
        .abs()
        .reset_index()
    )
    if daily.empty:
        return go.Figure()
    daily["weekday"] = daily["date_only"].apply(lambda d: d.weekday())
    daily["week"] = daily["date_only"].apply(lambda d: d.isocalendar()[1])
    pivot = daily.pivot(index="weekday", columns="week", values="amount").reindex(range(7), fill_value=0)
    fig = go.Figure(data=go.Heatmap(
        z=pivot.values,
        x=pivot.columns.astype(str),
        y=["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        colorscale="Blues",
    ))
    fig.update_layout(
        margin=dict(t=30, b=20, l=40, r=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis_title="Week",
        yaxis_title="Day",
    )
    return fig
