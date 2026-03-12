"""
explorer.py — Interactive choropleth + RAG chat workbench

Lives at: wattson_app/pages/explorer.py
Data at:  wattson_app/data/viz_*.parquet
"""

import os
import sys
import json
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from urllib.request import urlopen

st.set_page_config(page_title="ClimateFEAT Explorer", page_icon="🗺️", layout="wide")

# ---------------------------------------------------------------------------
# PATHS & API KEYS
# ---------------------------------------------------------------------------
WATTSON_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_DIR = os.path.dirname(WATTSON_DIR)
RAG_DIR = os.path.join(PROJECT_DIR, "RAG")
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")

if RAG_DIR not in sys.path:
    sys.path.insert(0, RAG_DIR)

for key_name in ("ANTHROPIC_API_KEY", "VOYAGE_API_KEY"):
    if not os.environ.get(key_name):
        try:
            os.environ[key_name] = st.secrets[key_name]
        except (KeyError, FileNotFoundError):
            pass

# ---------------------------------------------------------------------------
# FIPS MAPPING
# ---------------------------------------------------------------------------
COUNTY_FIPS = {
    "Alameda": "06001", "Alpine": "06003", "Amador": "06005", "Butte": "06007",
    "Calaveras": "06009", "Colusa": "06011", "Contra Costa": "06013", "Del Norte": "06015",
    "El Dorado": "06017", "Fresno": "06019", "Glenn": "06021", "Humboldt": "06023",
    "Imperial": "06025", "Inyo": "06027", "Kern": "06029", "Kings": "06031",
    "Lake": "06033", "Lassen": "06035", "Los Angeles": "06037", "Madera": "06039",
    "Marin": "06041", "Mariposa": "06043", "Mendocino": "06045", "Merced": "06047",
    "Modoc": "06049", "Mono": "06051", "Monterey": "06053", "Napa": "06055",
    "Nevada": "06057", "Orange": "06059", "Placer": "06061", "Plumas": "06063",
    "Riverside": "06065", "Sacramento": "06067", "San Benito": "06069",
    "San Bernardino": "06071", "San Diego": "06073", "San Francisco": "06075",
    "San Joaquin": "06077", "San Luis Obispo": "06079", "San Mateo": "06081",
    "Santa Barbara": "06083", "Santa Clara": "06085", "Santa Cruz": "06087",
    "Shasta": "06089", "Sierra": "06091", "Siskiyou": "06093", "Solano": "06095",
    "Sonoma": "06097", "Stanislaus": "06099", "Sutter": "06101", "Tehama": "06103",
    "Trinity": "06105", "Tulare": "06107", "Tuolumne": "06109", "Ventura": "06111",
    "Yolo": "06113", "Yuba": "06115",
}
FIPS_COUNTY = {v: k for k, v in COUNTY_FIPS.items()}

# TAC assignments for coloring the county map by TAC
COUNTY_TAC = {
    'Alameda': 'PGE', 'Alpine': 'PGE', 'Amador': 'PGE', 'Butte': 'PGE',
    'Calaveras': 'PGE', 'Colusa': 'PGE', 'Contra Costa': 'PGE', 'Del Norte': 'PGE',
    'El Dorado': 'PGE', 'Glenn': 'PGE', 'Humboldt': 'PGE', 'Lake': 'PGE',
    'Lassen': 'PGE', 'Marin': 'PGE', 'Mendocino': 'PGE', 'Merced': 'PGE',
    'Modoc': 'PGE', 'Monterey': 'PGE', 'Napa': 'PGE', 'Nevada': 'PGE',
    'Placer': 'PGE', 'Plumas': 'PGE', 'San Benito': 'PGE', 'San Francisco': 'PGE',
    'San Joaquin': 'PGE', 'San Luis Obispo': 'PGE', 'San Mateo': 'PGE',
    'Santa Clara': 'PGE', 'Santa Cruz': 'PGE', 'Shasta': 'PGE', 'Sierra': 'PGE',
    'Siskiyou': 'PGE', 'Solano': 'PGE', 'Sonoma': 'PGE', 'Stanislaus': 'PGE',
    'Sutter': 'PGE', 'Tehama': 'PGE', 'Trinity': 'PGE', 'Yolo': 'PGE', 'Yuba': 'PGE',
    'Orange': 'SCE', 'Riverside': 'SCE', 'San Bernardino': 'SCE', 'Ventura': 'SCE',
    'San Diego': 'SDGE',
    'Kern': 'PGE/SCE', 'Santa Barbara': 'PGE/SCE', 'Tulare': 'PGE/SCE',
    'Kings': 'PGE/SCE', 'Fresno': 'PGE/SCE', 'Madera': 'PGE/SCE', 'Tuolumne': 'PGE/SCE',
    'Los Angeles': 'SCE/LADWP', 'Imperial': 'SCE/IID', 'Mono': 'SCE/LADWP',
    'Inyo': 'SCE/LADWP', 'Sacramento': 'PGE/SMUD', 'Mariposa': 'PGE',
}

# ---------------------------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------------------------
@st.cache_data
def load_viz_data():
    county = pd.read_parquet(os.path.join(DATA_DIR, "viz_county_peaks.parquet"))
    tac = pd.read_parquet(os.path.join(DATA_DIR, "viz_tac_peaks.parquet"))
    state = pd.read_parquet(os.path.join(DATA_DIR, "viz_state_peaks.parquet"))
    # Add FIPS codes
    county["fips"] = county["county"].map(COUNTY_FIPS)
    county["tac_area"] = county["county"].map(COUNTY_TAC).fillna("Other")
    return county, tac, state

@st.cache_data
def load_ca_geojson():
    """Download US counties GeoJSON and filter to California."""
    url = "https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json"
    with urlopen(url) as response:
        counties = json.loads(response.read().decode())
    ca_features = [f for f in counties["features"] if f["id"].startswith("06")]
    for f in ca_features:
        f["properties"]["NAME"] = FIPS_COUNTY.get(f["id"], "Unknown")
    return {"type": "FeatureCollection", "features": ca_features}

county_df, tac_df, state_df = load_viz_data()
ca_geojson = load_ca_geojson()

# ---------------------------------------------------------------------------
# LOAD RAG (optional — graceful fallback if keys missing)
# ---------------------------------------------------------------------------
rag_available = False
try:
    from rag_query import load_collection, retrieve, generate_answer

    missing = [k for k in ("VOYAGE_API_KEY", "ANTHROPIC_API_KEY") if not os.environ.get(k)]
    if not missing:
        @st.cache_resource
        def get_collection():
            return load_collection()
        collection = get_collection()
        rag_available = True
except Exception:
    pass

# ---------------------------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### 🗺️ Explorer Controls")
    st.divider()

    scenario = st.radio("SSP Scenario", ["SSP3-7.0", "SSP2-4.5"], index=0)
    scenario_key = "ssp370" if scenario == "SSP3-7.0" else "ssp245"

    year = st.slider("Year", min_value=2018, max_value=2040, value=2030, step=1)

    color_metric = st.radio(
        "Map color",
        ["Growth vs 2025 (%)", "Peak demand (MWh)", "Ensemble spread (MWh)"],
        index=0,
    )

    peak_type = st.radio("Peak threshold", ["Top 1%", "Top 5%"], index=0)
    pct_key = "1pct" if peak_type == "Top 1%" else "5pct"

    st.divider()
    st.caption("Click a county on the map to ask the RAG about it.")
    st.caption("Data: ClimateFEAT transformer ensemble projections")

# ---------------------------------------------------------------------------
# MAP COLOR SETTINGS
# ---------------------------------------------------------------------------
if color_metric == "Growth vs 2025 (%)":
    color_col = f"peak_{pct_key}_pct_change_vs_2025"
    color_label = "Growth vs 2025 (%)"
    color_scale = "RdYlGn_r"  # green=low growth, red=high growth
    color_range = [-10, 50]
elif color_metric == "Peak demand (MWh)":
    color_col = f"peak_{pct_key}_mean"
    color_label = f"{peak_type} Peak Demand (MWh)"
    color_scale = "YlOrRd"
    color_range = None  # auto
else:
    color_col = f"peak_{pct_key}_spread"
    color_label = "Ensemble Spread (MWh)"
    color_scale = "Purples"
    color_range = None

# ---------------------------------------------------------------------------
# FILTER DATA
# ---------------------------------------------------------------------------
map_data = county_df[(county_df["scenario"] == scenario_key) & (county_df["year"] == year)].copy()

# Add spread column
map_data[f"peak_{pct_key}_spread"] = map_data[f"peak_{pct_key}_p90"] - map_data[f"peak_{pct_key}_p10"]

# Handle NaN in growth for years before 2025
if color_col == f"peak_{pct_key}_pct_change_vs_2025":
    map_data[color_col] = map_data[color_col].fillna(0)

# ---------------------------------------------------------------------------
# HEADER
# ---------------------------------------------------------------------------
st.title("🗺️ ClimateFEAT Explorer")
st.caption(f"{scenario} · {year} · {peak_type} peak days · Color: {color_metric}")
st.divider()

# ---------------------------------------------------------------------------
# METRIC CARDS
# ---------------------------------------------------------------------------
state_row = state_df[(state_df["scenario"] == scenario_key) & (state_df["year"] == year)]
if len(state_row) > 0:
    sr = state_row.iloc[0]
    col1, col2, col3, col4 = st.columns(4)
    col1.metric(
        "Statewide Peak (top 1%)",
        f"{sr['peak_1pct_mean']:,.0f} MWh",
        f"{sr.get('peak_1pct_pct_change_vs_2025', 0):+.1f}% vs 2025" if year >= 2025 else None,
    )
    col2.metric(
        "Ensemble Range",
        f"{sr['peak_1pct_p10']:,.0f}–{sr['peak_1pct_p90']:,.0f}",
    )
    col3.metric(
        "Firm+Storage",
        f"{sr.get('capacity_total', 72041):,.0f} MW",
    )
    margin = sr.get("margin_1pct", None)
    if margin is not None:
        col4.metric(
            "Capacity Margin",
            f"{margin:+,.0f} MW",
            delta=f"{'Surplus' if margin > 0 else 'DEFICIT'}",
            delta_color="normal" if margin > 0 else "inverse",
        )

st.divider()

# ---------------------------------------------------------------------------
# MAP
# ---------------------------------------------------------------------------
fig = px.choropleth_mapbox(
    map_data,
    geojson=ca_geojson,
    locations="fips",
    color=color_col,
    color_continuous_scale=color_scale,
    range_color=color_range,
    mapbox_style="carto-darkmatter",
    zoom=4.8,
    center={"lat": 37.5, "lon": -119.5},
    opacity=0.8,
    hover_name="county",
    hover_data={
        "fips": False,
        color_col: False,
        f"peak_{pct_key}_mean": ":.0f",
        f"peak_{pct_key}_p10": ":.0f",
        f"peak_{pct_key}_p90": ":.0f",
        f"peak_{pct_key}_pct_change_vs_2025": ":.1f",
        "tac_area": True,
        "peak_month_mode": ":.0f",
    },
    labels={
        f"peak_{pct_key}_mean": f"{peak_type} Peak (MWh)",
        f"peak_{pct_key}_p10": "10th Pct",
        f"peak_{pct_key}_p90": "90th Pct",
        f"peak_{pct_key}_pct_change_vs_2025": "Growth vs 2025 (%)",
        "tac_area": "TAC Area",
        "peak_month_mode": "Peak Month",
        color_col: color_label,
    },
)

fig.update_layout(
    margin={"r": 0, "t": 0, "l": 0, "b": 0},
    height=600,
    coloraxis_colorbar=dict(
        title=color_label,
        thickness=15,
        len=0.7,
    ),
    paper_bgcolor="rgba(0,0,0,0)",
)

st.plotly_chart(fig, use_container_width=True, key="county_map")

# ---------------------------------------------------------------------------
# TAC SUMMARY TABLE
# ---------------------------------------------------------------------------
with st.expander("📊 TAC Area Summary"):
    caiso_tacs = ["PGE", "SCE", "SDGE"]
    tac_year = tac_df[
        (tac_df["scenario"] == scenario_key) &
        (tac_df["year"] == year) &
        (tac_df["tac"].isin(caiso_tacs))
    ].copy()

    if len(tac_year) > 0:
        display_cols = {
            "tac": "TAC",
            f"peak_{pct_key}_mean": f"{peak_type} Peak (MW)",
            f"peak_{pct_key}_p10": "10th Pct",
            f"peak_{pct_key}_p90": "90th Pct",
            "capacity_total": "Firm+Storage (MW)",
            f"margin_{pct_key}": "Margin (MW)",
        }
        tac_display = tac_year[[c for c in display_cols.keys() if c in tac_year.columns]].copy()
        tac_display.columns = [display_cols.get(c, c) for c in tac_display.columns]

        for col in tac_display.columns:
            if col != "TAC":
                tac_display[col] = tac_display[col].map(lambda x: f"{x:,.0f}" if pd.notna(x) else "—")

        st.dataframe(tac_display, hide_index=True, use_container_width=True)

# ---------------------------------------------------------------------------
# TOP COUNTIES TABLE
# ---------------------------------------------------------------------------
with st.expander(f"🔥 Top 15 Counties by {peak_type} Peak — {year}"):
    top15 = map_data.nlargest(15, f"peak_{pct_key}_mean")[
        ["county", "tac_area", f"peak_{pct_key}_mean", f"peak_{pct_key}_p10",
         f"peak_{pct_key}_p90", f"peak_{pct_key}_pct_change_vs_2025"]
    ].copy()
    top15.columns = ["County", "TAC", "Peak (MWh)", "10th Pct", "90th Pct", "Growth vs 2025 (%)"]
    for col in ["Peak (MWh)", "10th Pct", "90th Pct"]:
        top15[col] = top15[col].map("{:,.0f}".format)
    top15["Growth vs 2025 (%)"] = top15["Growth vs 2025 (%)"].map("{:+.1f}%".format)
    st.dataframe(top15, hide_index=True, use_container_width=True)

# ---------------------------------------------------------------------------
# RAG CHAT
# ---------------------------------------------------------------------------
st.divider()
st.subheader("💬 Ask about what you see")

if not rag_available:
    st.info("RAG chat unavailable — API keys not configured.")
else:
    # Chat state
    if "explorer_messages" not in st.session_state:
        st.session_state.explorer_messages = []

    # Auto-generate a contextual question suggestion
    if len(map_data) > 0:
        top_county = map_data.nlargest(1, f"peak_{pct_key}_mean").iloc[0]["county"]
        suggestions = [
            f"What drives peak demand in {top_county} county?",
            f"How does the {scenario} projection compare to the CEC forecast at {year}?",
            f"What is the capacity margin for SCE in {year}?",
            f"Why do SSP scenarios converge through 2040?",
        ]
        cols = st.columns(len(suggestions))
        for i, q in enumerate(suggestions):
            if cols[i].button(q, key=f"suggest_{i}", use_container_width=True):
                st.session_state["explorer_input"] = q

    # Chat history
    for msg in st.session_state.explorer_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Input
    prefill = st.session_state.pop("explorer_input", None)
    if prompt := (prefill or st.chat_input("Ask about the map, projections, or capacity...")):
        st.session_state.explorer_messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Searching corpus..."):
                chunks = retrieve(prompt, collection, None)
                answer = generate_answer(prompt, chunks)
            st.markdown(answer)

        st.session_state.explorer_messages.append({"role": "assistant", "content": answer})