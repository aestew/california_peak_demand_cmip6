import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from htbuilder.units import rem
from htbuilder import div, styles

st.set_page_config(page_title="Peak Demand Forecast", page_icon="⚡️", layout="wide")

# ── LOAD DATA ────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    summary_370 = pd.read_parquet("data/summary_370.parquet")
    summary_245 = pd.read_parquet("data/summary_245.parquet")
    monthly_370 = pd.read_parquet("data/monthly_370.parquet")
    monthly_245 = pd.read_parquet("data/monthly_245.parquet")
    hist_annual = pd.read_parquet("data/hist_annual.parquet")
    return summary_370, summary_245, monthly_370, monthly_245, hist_annual

summary_370, summary_245, monthly_370, monthly_245, hist_annual = load_data()

models_370 = sorted(monthly_370["model"].unique())
models_245 = sorted(monthly_245["model"].unique())

# ── SIDEBAR ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### System Status")
    st.success("ECS Cluster: Online")
    st.success("DynamoDB: Connected")
    st.markdown("### Available Features")
    st.caption("Energy Demand Model 1.0")
    st.caption("GoruRAG 1.0")
    st.divider()

    st.markdown("### Chart Controls")
    show_actuals   = st.toggle("Show historical actuals", value=True)
    show_370_range = st.toggle("Show SSP3-7.0 range", value=False)
    show_245_range = st.toggle("Show SSP2-4.5 range", value=False)

    st.divider()
    with st.expander("SSP3-7.0 Model Runs"):
        select_all_370 = st.checkbox("Select all", value=False, key="all_370")
        selected_370 = {}
        for m in models_370:
            selected_370[m] = st.checkbox(m, value=select_all_370, key=f"370_{m}", disabled=select_all_370)

    with st.expander("SSP2-4.5 Model Runs"):
        select_all_245 = st.checkbox("Select all", value=False, key="all_245")
        selected_245 = {}
        for m in models_245:
            selected_245[m] = st.checkbox(m, value=select_all_245, key=f"245_{m}", disabled=select_all_245)

# ── HEADER ───────────────────────────────────────────────────────────────────
st.html(div(style=styles(font_size=rem(4), line_height=1))["⚡️"])
st.title("Peak Demand Forecast")
st.caption("California statewide electricity demand — top 5% peak days per year, 2018–2040")
st.divider()

# ── METRIC CARDS ─────────────────────────────────────────────────────────────
col1, col2, col3 = st.columns(3)
hist_peak      = int(hist_annual["Max_Daily_Electricity_Usage"].max())
mean_2040_370  = int(summary_370[summary_370["year"] == 2040]["mean"].values[0])
mean_2040_245  = int(summary_245[summary_245["year"] == 2040]["mean"].values[0])
col1.metric("CA Peak Demand (Historical Max)",  f"{hist_peak:,} MWh")
col2.metric("SSP3-7.0 Projected Peak (2040)",   f"{mean_2040_370:,} MWh")
col3.metric("SSP2-4.5 Projected Peak (2040)",   f"{mean_2040_245:,} MWh")
st.divider()

# ── PLOT ─────────────────────────────────────────────────────────────────────
fig = go.Figure()

# ── SSP370 mean — always on ──
fig.add_trace(go.Scatter(
    x=summary_370["date"], y=summary_370["mean"],
    mode="lines+markers", name="SSP370 ensemble mean",
    legendgroup="ssp370_mean", legendgrouptitle_text="SSP3-7.0",
    line=dict(color="rgba(50, 100, 160, 0.9)", width=2.5),
    marker=dict(size=6, color="rgba(50, 100, 160, 0.9)"),
    customdata=np.stack([summary_370["low"], summary_370["high"], summary_370["mean"]], axis=1),
    hovertemplate="<b>SSP370 Ensemble mean</b><br>Year: %{x|%Y}<br>Mean MWh: %{customdata[2]:,.0f}<br>10th pct: %{customdata[0]:,.0f}<br>90th pct: %{customdata[1]:,.0f}<extra></extra>"
))

# ── SSP370 range ──
if show_370_range:
    fig.add_trace(go.Scatter(
        x=pd.concat([summary_370["date"], summary_370["date"][::-1]]),
        y=pd.concat([summary_370["high"], summary_370["low"][::-1]]),
        fill="toself", fillcolor="rgba(70, 130, 180, 0.15)",
        line=dict(color="rgba(255,255,255,0)"),
        name="SSP370 range (10th–90th)", legendgroup="ssp370_mean", hoverinfo="skip"
    ))
    fig.add_trace(go.Scatter(
        x=summary_370["date"], y=summary_370["high"],
        mode="markers", name="SSP370 90th pct", legendgroup="ssp370_mean",
        marker=dict(size=7, color="rgba(70, 130, 180, 0.5)"),
        hovertemplate="<b>SSP370 90th pct</b><br>Year: %{x|%Y}<br>MWh: %{y:,.0f}<extra></extra>"
    ))
    fig.add_trace(go.Scatter(
        x=summary_370["date"], y=summary_370["low"],
        mode="markers", name="SSP370 10th pct", legendgroup="ssp370_mean",
        marker=dict(size=7, color="rgba(70, 130, 180, 0.5)"),
        hovertemplate="<b>SSP370 10th pct</b><br>Year: %{x|%Y}<br>MWh: %{y:,.0f}<extra></extra>"
    ))

# ── SSP370 model dots ──
colors_370 = [f"hsl({int(i * 360 / len(models_370))}, 60%, 55%)" for i in range(len(models_370))]
for model, color in zip(models_370, colors_370):
    if select_all_370 or selected_370.get(model):
        subset = monthly_370[monthly_370["model"] == model]
        fig.add_trace(go.Scatter(
            x=subset["date"], y=subset["pred_mwh_top5"],
            mode="markers", name=f"{model} (370)",
            legendgroup="ssp370_dots", legendgrouptitle_text="SSP3-7.0 Model Runs",
            marker=dict(size=5, color=color, opacity=0.4),
            customdata=np.stack([subset["model"], subset["run"], subset["pred_mwh_top5"]], axis=1),
            hovertemplate="<b>%{customdata[0]} (SSP370)</b><br>Run: %{customdata[1]}<br>MWh: %{customdata[2]:,.0f}<br>Date: %{x|%Y-%m}<extra></extra>"
        ))

# ── SSP245 mean — always on ──
fig.add_trace(go.Scatter(
    x=summary_245["date"], y=summary_245["mean"],
    mode="lines+markers", name="SSP245 ensemble mean",
    legendgroup="ssp245_mean", legendgrouptitle_text="SSP2-4.5",
    line=dict(color="rgba(40, 130, 40, 0.9)", width=2.5),
    marker=dict(size=6, color="rgba(40, 130, 40, 0.9)"),
    customdata=np.stack([summary_245["low"], summary_245["high"], summary_245["mean"]], axis=1),
    hovertemplate="<b>SSP245 Ensemble mean</b><br>Year: %{x|%Y}<br>Mean MWh: %{customdata[2]:,.0f}<br>10th pct: %{customdata[0]:,.0f}<br>90th pct: %{customdata[1]:,.0f}<extra></extra>"
))

# ── SSP245 range ──
if show_245_range:
    fig.add_trace(go.Scatter(
        x=pd.concat([summary_245["date"], summary_245["date"][::-1]]),
        y=pd.concat([summary_245["high"], summary_245["low"][::-1]]),
        fill="toself", fillcolor="rgba(100, 180, 100, 0.15)",
        line=dict(color="rgba(255,255,255,0)"),
        name="SSP245 range (10th–90th)", legendgroup="ssp245_mean", hoverinfo="skip"
    ))
    fig.add_trace(go.Scatter(
        x=summary_245["date"], y=summary_245["high"],
        mode="markers", name="SSP245 90th pct", legendgroup="ssp245_mean",
        marker=dict(size=7, color="rgba(60, 150, 60, 0.5)"),
        hovertemplate="<b>SSP245 90th pct</b><br>Year: %{x|%Y}<br>MWh: %{y:,.0f}<extra></extra>"
    ))
    fig.add_trace(go.Scatter(
        x=summary_245["date"], y=summary_245["low"],
        mode="markers", name="SSP245 10th pct", legendgroup="ssp245_mean",
        marker=dict(size=7, color="rgba(60, 150, 60, 0.5)"),
        hovertemplate="<b>SSP245 10th pct</b><br>Year: %{x|%Y}<br>MWh: %{y:,.0f}<extra></extra>"
    ))

# ── SSP245 model dots ──
colors_245 = [f"hsl({int(i * 360 / len(models_245))}, 50%, 70%)" for i in range(len(models_245))]
for model, color in zip(models_245, colors_245):
    if select_all_245 or selected_245.get(model):
        subset = monthly_245[monthly_245["model"] == model]
        fig.add_trace(go.Scatter(
            x=subset["date"], y=subset["pred_mwh_top5"],
            mode="markers", name=f"{model} (245)",
            legendgroup="ssp245_dots", legendgrouptitle_text="SSP2-4.5 Model Runs",
            marker=dict(size=5, color=color, opacity=0.4, symbol="diamond"),
            customdata=np.stack([subset["model"], subset["run"], subset["pred_mwh_top5"]], axis=1),
            hovertemplate="<b>%{customdata[0]} (SSP245)</b><br>Run: %{customdata[1]}<br>MWh: %{customdata[2]:,.0f}<br>Date: %{x|%Y-%m}<extra></extra>"
        ))

# ── Historical actuals ──
if show_actuals:
    fig.add_trace(go.Scatter(
        x=hist_annual["date"], y=hist_annual["Max_Daily_Electricity_Usage"],
        mode="lines+markers", name="Historical actuals",
        legendgroup="actuals", legendgrouptitle_text="Historical",
        line=dict(color="firebrick", width=2.5, dash="dash"),
        marker=dict(size=7, color="firebrick"),
        hovertemplate="<b>Historical actual</b><br>Year: %{x|%Y}<br>MWh: %{y:,.0f}<extra></extra>"
    ))

fig.update_layout(
    title="California Peak Energy Demand — Top 5% Days per Year<br>SSP3-7.0 vs SSP2-4.5 + Historical Actuals",
    xaxis_title="Year",
    yaxis_title="Avg Predicted MWh (top 5% days)",
    xaxis=dict(title_font=dict(size=26), tickfont=dict(size=18)),
    yaxis=dict(title_font=dict(size=26), tickfont=dict(size=18)),
    hovermode="closest",
    hoverlabel=dict(font_size=14, font_family="Arial"),
    height=800,
    legend=dict(
        orientation="v", x=1.01, y=1,
        font=dict(size=14),
        groupclick="togglegroup",
        grouptitlefont=dict(size=16)
    ),
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)"
)

st.plotly_chart(fig, use_container_width=True)

# ── DATA TABLE ───────────────────────────────────────────────────────────────
st.divider()
with st.expander("📊 View Annual Summary Table"):
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**SSP3-7.0**")
        tbl_370 = summary_370[["year", "mean", "low", "high"]].copy()
        tbl_370.columns = ["Year", "Ensemble Mean (MWh)", "10th Pct", "90th Pct"]
        tbl_370["Year"] = tbl_370["Year"].astype(int)
        for col in ["Ensemble Mean (MWh)", "10th Pct", "90th Pct"]:
            tbl_370[col] = tbl_370[col].map("{:,.0f}".format)
        st.dataframe(tbl_370, hide_index=True)
    with col2:
        st.markdown("**SSP2-4.5**")
        tbl_245 = summary_245[["year", "mean", "low", "high"]].copy()
        tbl_245.columns = ["Year", "Ensemble Mean (MWh)", "10th Pct", "90th Pct"]
        tbl_245["Year"] = tbl_245["Year"].astype(int)
        for col in ["Ensemble Mean (MWh)", "10th Pct", "90th Pct"]:
            tbl_245[col] = tbl_245[col].map("{:,.0f}".format)
        st.dataframe(tbl_245, hide_index=True)