"""
wattson_draft.py -- ClimateFEAT Explorer (main app)

Lives at: wattson_app/wattson_draft.py
Data at:  wattson_app/data/
"""

import os
import sys
import json
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from urllib.request import urlopen

st.set_page_config(page_title="ClimateFEAT Explorer", page_icon="\U0001f321\ufe0f", layout="wide")

# ---------------------------------------------------------------------------
# DESIGN SYSTEM
# ---------------------------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Literata:ital,wght@0,400;0,600;0,700;1,400&family=Manrope:wght@300;400;500;600;700&family=Inconsolata:wght@400;500&display=swap');

:root {
  --accent:        #5AAAE8;
  --accent-dim:    rgba(90,170,232,0.12);
  --accent-border: rgba(90,170,232,0.22);
  --green-muted:   #4E8878;
  --text-primary:  #DEE8E2;
  --text-body:     #8AA8A0;
  --text-dim:      #5A8A78;
  --text-faint:    #3A6858;
  --card-bg:       rgba(14,28,26,0.55);
  --card-border:   rgba(90,170,232,0.10);
  --border:        rgba(90,170,232,0.08);
  --sans:          'Manrope', -apple-system, sans-serif;
  --mono:          'Inconsolata', monospace;
  --serif:         'Literata', Georgia, serif;
}

.stApp {
  background: linear-gradient(180deg,
    #080E18 0%, #0A1520 8%, #0C1822 20%,
    #0D1A22 32%, #0E1C22 42%, #0F1E1C 55%,
    #0F1E1A 68%, #0E1D18 80%, #0C1A14 100%
  ) !important;
  font-family: var(--sans) !important;
  color: var(--text-primary) !important;
}

h1, h2, h3 {
  font-family: var(--serif) !important;
  color: var(--text-primary) !important;
  letter-spacing: -0.025em !important;
}
h4, h5, h6, p, span, label { font-family: var(--sans) !important; }
h4 {
  font-family: var(--serif) !important;
  font-size: 15px !important;
  font-weight: 600 !important;
  color: var(--text-primary) !important;
  letter-spacing: -0.01em !important;
  line-height: 1.4 !important;
}
.stApp h1 {
  font-size: clamp(28px, 3vw, 40px) !important;
  font-weight: 700 !important;
  margin-bottom: 0 !important;
}
[data-testid="stCaptionContainer"] { margin-top: 2px !important; margin-bottom: 8px !important; }
[data-testid="stCaptionContainer"] p {
  font-family: var(--mono) !important;
  font-size: 13px !important;
  color: var(--green-muted) !important;
  letter-spacing: 0.07em !important;
  text-transform: uppercase !important;
}

/* Selectbox */
[data-testid="stSelectbox"] > div > div {
  background: var(--card-bg) !important;
  border: 1px solid var(--card-border) !important;
  border-radius: 8px !important;
  color: var(--text-primary) !important;
  font-family: var(--sans) !important;
  font-size: 13px !important;
}
[data-testid="stSelectbox"] label {
  color: var(--accent) !important;
  font-family: var(--mono) !important;
  font-size: 13px !important;
  letter-spacing: 0.08em !important;
  text-transform: uppercase !important;
}

/* Checkboxes */
[data-testid="stCheckbox"] label,
[data-testid="stCheckbox"] label span,
[data-testid="stCheckbox"] label p {
  color: var(--text-body) !important;
  font-family: var(--mono) !important;
  font-size: 13px !important;
  font-weight: 400 !important;
  letter-spacing: 0.05em !important;
  line-height: 1.4 !important;
}

/* Chat submit button icon fix */
[data-testid="stChatInputContainer"] button span[data-testid="stIconMaterial"] { display: none !important; }
[data-testid="stChatInputContainer"] button { font-size: 0 !important; }
[data-testid="stChatInputContainer"] button svg { display: block !important; font-size: initial !important; }

/* Chat messages */
[data-testid="stChatMessage"] {
  background: var(--card-bg) !important;
  border: 1px solid var(--card-border) !important;
  border-radius: 10px !important;
  margin-bottom: 8px !important;
  font-family: var(--sans) !important;
}
[data-testid="stChatMessage"] p,
[data-testid="stChatMessage"] span,
[data-testid="stChatMessage"] div,
[data-testid="stChatMessage"] li,
[data-testid="stChatMessage"] a,
[data-testid="stChatMessage"] strong,
[data-testid="stChatMessage"] em,
[data-testid="stChatMessage"] code {
  color: var(--text-body) !important;
  font-family: var(--sans) !important;
  font-size: 13px !important;
  line-height: 1.65 !important;
}
[data-testid="stChatInputContainer"] textarea {
  background: var(--card-bg) !important;
  border: 1px solid var(--card-border) !important;
  border-radius: 8px !important;
  color: var(--text-primary) !important;
  font-family: var(--sans) !important;
  font-size: 13px !important;
}
[data-testid="stChatInputContainer"] textarea::placeholder {
  color: var(--text-faint) !important;
  font-family: var(--mono) !important;
  font-size: 13px !important;
  letter-spacing: 0.04em !important;
}

/* Slider */
[data-testid="stSlider"] label { display: none !important; }
[data-testid="stSlider"] [data-testid="stSliderThumbValue"] {
  font-family: var(--mono) !important;
  font-size: 13px !important;
  font-weight: 700 !important;
  color: #E53935 !important;
}
[data-testid="stSlider"] [role="slider"],
[data-testid="stSlider"] [role="slider"]:focus {
  background-color: #E53935 !important;
  border-color: #E53935 !important;
  box-shadow: 0 0 0 2px rgba(229,57,53,0.25) !important;
}
[data-testid="stSlider"] [data-baseweb="slider"] [role="progressbar"] {
  background-color: #E53935 !important;
}
[data-testid="stTickBarMin"],
[data-testid="stTickBarMax"] {
  font-family: var(--mono) !important;
  font-size: 13px !important;
  color: var(--text-dim) !important;
}
/* CSS fallback for slider alignment; JS overrides after render */
[data-testid="stSlider"] {
  padding-left: 60px !important;
  padding-right: 10px !important;
  margin-top: -4px !important;
  margin-bottom: 2px !important;
}

/* Buttons */
.stButton > button {
  background: var(--card-bg) !important;
  border: 1px solid var(--card-border) !important;
  border-radius: 8px !important;
  color: var(--text-body) !important;
  font-family: var(--sans) !important;
  font-size: 13px !important;
  font-weight: 400 !important;
  transition: border-color 0.2s, color 0.2s, background 0.2s !important;
}
.stButton > button:hover {
  border-color: var(--accent-border) !important;
  color: var(--accent) !important;
  background: var(--accent-dim) !important;
}

/* Info box */
[data-testid="stInfo"] {
  background: var(--accent-dim) !important;
  border: 1px solid var(--accent-border) !important;
  border-radius: 8px !important;
  color: var(--text-body) !important;
}

/* Tabs */
[data-testid="stTabs"] [data-baseweb="tab-list"] {
  background: transparent !important;
  border-bottom: 1px solid var(--border) !important;
  gap: 4px !important;
}
[data-testid="stTabs"] [data-baseweb="tab"] {
  background: transparent !important;
  color: var(--text-dim) !important;
  font-family: var(--mono) !important;
  font-size: 13px !important;
  letter-spacing: 0.06em !important;
  text-transform: uppercase !important;
  border: none !important;
}
[data-testid="stTabs"] [aria-selected="true"] {
  color: var(--accent) !important;
  border-bottom: 2px solid var(--accent) !important;
}

/* Dataframe */
[data-testid="stDataFrame"] {
  border: 1px solid var(--card-border) !important;
  border-radius: 10px !important;
  overflow: hidden !important;
}
[data-testid="stDataFrame"] th {
  background: rgba(14,28,26,0.8) !important;
  color: var(--accent) !important;
  font-family: var(--mono) !important;
  font-size: 13px !important;
  letter-spacing: 0.05em !important;
  text-transform: uppercase !important;
  border-bottom: 1px solid var(--border) !important;
}
[data-testid="stDataFrame"] td {
  background: var(--card-bg) !important;
  color: var(--text-body) !important;
  font-family: var(--mono) !important;
  font-size: 13px !important;
  border-bottom: 1px solid var(--border) !important;
}

hr {
  border: none !important;
  height: 1px !important;
  background: linear-gradient(90deg, transparent, var(--accent-border), transparent) !important;
  margin: 8px auto !important;
}

[data-testid="stMarkdownContainer"] strong {
  color: var(--accent) !important;
  font-family: var(--mono) !important;
  font-size: 13px !important;
  letter-spacing: 0.08em !important;
  text-transform: uppercase !important;
}

::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--card-border); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--accent-border); }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# PATHS & API KEYS
# ---------------------------------------------------------------------------
APP_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(APP_DIR)
RAG_DIR = os.path.join(PROJECT_DIR, "RAG")
DATA_DIR = os.path.join(APP_DIR, "data")

if RAG_DIR not in sys.path:
    sys.path.insert(0, RAG_DIR)

for key_name in ("ANTHROPIC_API_KEY", "VOYAGE_API_KEY"):
    if not os.environ.get(key_name):
        try:
            os.environ[key_name] = st.secrets[key_name]
        except (KeyError, FileNotFoundError):
            pass

# ---------------------------------------------------------------------------
# FIPS + TAC MAPPINGS
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
def load_forecast_data():
    summary_370 = pd.read_parquet(os.path.join(DATA_DIR, "summary_370.parquet"))
    summary_245 = pd.read_parquet(os.path.join(DATA_DIR, "summary_245.parquet"))
    hist_annual = pd.read_parquet(os.path.join(DATA_DIR, "hist_annual.parquet"))
    return summary_370, summary_245, hist_annual

@st.cache_data
def load_viz_data():
    county = pd.read_parquet(os.path.join(DATA_DIR, "viz_county_peaks.parquet"))
    tac = pd.read_parquet(os.path.join(DATA_DIR, "viz_tac_peaks.parquet"))
    state = pd.read_parquet(os.path.join(DATA_DIR, "viz_state_peaks.parquet"))
    capacity = pd.read_parquet(os.path.join(DATA_DIR, "viz_capacity_trajectory.parquet"))
    county["fips"] = county["county"].map(COUNTY_FIPS)
    county["tac_area"] = county["county"].map(COUNTY_TAC).fillna("Other")
    return county, tac, state, capacity

@st.cache_data
def load_ca_geojson():
    url = "https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json"
    with urlopen(url) as response:
        counties = json.loads(response.read().decode())
    ca_features = [f for f in counties["features"] if f["id"].startswith("06")]
    for f in ca_features:
        f["properties"]["NAME"] = FIPS_COUNTY.get(f["id"], "Unknown")
    return {"type": "FeatureCollection", "features": ca_features}

@st.cache_data
def load_tac_geojson():
    with open(os.path.join(DATA_DIR, "tac_geojson.json")) as f:
        return json.load(f)

@st.cache_data
def load_transmission_lines():
    df = pd.read_parquet(os.path.join(DATA_DIR, "transmission_lines.parquet"))
    return df.to_dict("records")


summary_370, summary_245, hist_annual = load_forecast_data()
county_df, tac_df, state_df, capacity_df = load_viz_data()
ca_geojson = load_ca_geojson()
tac_geojson = load_tac_geojson()
transmission_lines = load_transmission_lines()

# ---------------------------------------------------------------------------
# LOAD RAG
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
# HEADER
# ---------------------------------------------------------------------------
st.title("ClimateFEAT Explorer")
st.caption(
    "Climate-informed peak electricity demand projections for California "
    "// 58 counties // 2018-2040 // CMIP6 ensemble uncertainty"
)

# =====================================================================
# TOP CONTROLS -- single row of dropdowns
# =====================================================================
c1, c2, c3, c4 = st.columns(4, gap="medium")

with c1:
    scenario = st.selectbox(
        "Emissions scenario",
        ["High Emissions (SSP3-7.0)", "Moderate Emissions (SSP2-4.5)"],
        index=0,
        key="scenario_select",
    )

with c2:
    color_metric = st.selectbox(
        "Map shading",
        ["Growth vs 2025", "Peak demand"],
        index=0,
        key="map_color",
    )

with c3:
    color_view = st.selectbox(
        "Units",
        ["% change", "Absolute (MWh)"],
        index=0,
        key="map_color_view",
    )

with c4:
    grid_mode = st.selectbox(
        "Boundaries",
        ["County", "TAC areas"],
        index=0,
        key="grid_mode",
    )

scenario_key = "ssp370" if "SSP3-7.0" in scenario else "ssp245"
pct_key = "1pct"
peak_type = "Top 1%"

# =====================================================================
# MAIN SECTION:  MAP (left)  |  CHAT (right)  --  50 / 50
# =====================================================================
map_col, chat_col = st.columns([1, 1], gap="medium")

# -- MAP --
with map_col:
    year = st.session_state.get("explorer_year", 2030)
    use_tac = grid_mode == "TAC areas"
    use_pct = color_view == "% change"

    if color_metric == "Growth vs 2025":
        if use_pct:
            color_col = f"peak_{pct_key}_pct_change_vs_2025"
            color_label = "Growth vs 2025 (%)"
        else:
            color_col = f"peak_{pct_key}_delta_vs_2025"
            color_label = "Growth vs 2025 (MWh)"
        color_scale = "RdYlGn_r"
        color_range = None
    else:
        if use_pct:
            color_col = "_peak_pct_of_2025"
            color_label = "Peak as % of 2025 baseline"
        else:
            color_col = f"peak_{pct_key}_mean"
            color_label = "Peak demand (MWh)"
        color_scale = "YlOrRd"
        color_range = None

    def dynamic_range(series):
        lo = min(0.0, float(series.min()))
        hi = max(0.0, float(series.max())) * 1.05
        return [lo, max(hi, 1.0)]

    if use_tac:
        tac_data = tac_df[
            (tac_df["scenario"] == scenario_key)
            & (tac_df["year"] == year)
            & (tac_df["tac"].isin(["PGE", "SCE", "SDGE"]))
        ].copy()
        tac_data[f"peak_{pct_key}_spread"] = (
            tac_data[f"peak_{pct_key}_p90"] - tac_data[f"peak_{pct_key}_p10"]
        )
        tac_data["_peak_pct_of_2025"] = (
            tac_data[f"peak_{pct_key}_mean"]
            / tac_data[f"peak_{pct_key}_baseline_2025"]
            * 100
        )
        if color_metric == "Growth vs 2025":
            tac_data[color_col] = tac_data[color_col].fillna(0)
        color_range = dynamic_range(tac_data[color_col].dropna())

        fig_map = px.choropleth_mapbox(
            tac_data,
            geojson=tac_geojson,
            locations="tac",
            color=color_col,
            color_continuous_scale=color_scale,
            range_color=color_range,
            mapbox_style="carto-darkmatter",
            zoom=4.8,
            center={"lat": 37.5, "lon": -119.5},
            opacity=0.8,
            hover_name="tac",
            hover_data={
                "tac": False,
                color_col: False,
                f"peak_{pct_key}_mean": ":.0f",
                f"peak_{pct_key}_p10": ":.0f",
                f"peak_{pct_key}_p90": ":.0f",
            },
            labels={
                f"peak_{pct_key}_mean": f"{peak_type} Peak (MWh)",
                f"peak_{pct_key}_p10": "10th Pct",
                f"peak_{pct_key}_p90": "90th Pct",
                color_col: color_label,
            },
        )
        fig_map.update_traces(marker_line_color="black", marker_line_width=1.2)
        map_data = county_df[
            (county_df["scenario"] == scenario_key) & (county_df["year"] == year)
        ].copy()
        map_data[f"peak_{pct_key}_spread"] = (
            map_data[f"peak_{pct_key}_p90"] - map_data[f"peak_{pct_key}_p10"]
        )
    else:
        map_data = county_df[
            (county_df["scenario"] == scenario_key) & (county_df["year"] == year)
        ].copy()
        map_data[f"peak_{pct_key}_spread"] = (
            map_data[f"peak_{pct_key}_p90"] - map_data[f"peak_{pct_key}_p10"]
        )
        map_data["_peak_pct_of_2025"] = (
            map_data[f"peak_{pct_key}_mean"]
            / map_data[f"peak_{pct_key}_baseline_2025"]
            * 100
        )
        if color_metric == "Growth vs 2025":
            map_data[color_col] = map_data[color_col].fillna(0)
        color_range = dynamic_range(map_data[color_col].dropna())

        fig_map = px.choropleth_mapbox(
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

    fig_map.update_layout(
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        height=520,
        coloraxis_colorbar=dict(
            title=color_label, title_side="right",
            thickness=10, len=0.7, x=1.01, tickfont=dict(size=13),
        ),
        paper_bgcolor="rgba(0,0,0,0)",
    )
    if not use_tac:
        fig_map.update_traces(marker_line_color="black", marker_line_width=0.5)

    st.plotly_chart(fig_map, use_container_width=True, key="county_map")

# -- CHAT --
with chat_col:
    st.markdown("#### Ask about the model")

    if not rag_available:
        st.info("RAG unavailable -- set API keys in Streamlit Secrets.")
    else:
        temp_year = st.session_state.get("explorer_year", 2030)
        temp_map = county_df[
            (county_df["scenario"] == scenario_key)
            & (county_df["year"] == temp_year)
        ]
        top_county = (
            temp_map.nlargest(1, f"peak_{pct_key}_mean").iloc[0]["county"]
            if len(temp_map) > 0
            else "Los Angeles"
        )

        suggestions = [
            f"What drives demand in {top_county}?",
            "ClimateFEAT vs CEC comparison?",
            "SCE capacity margin?",
            "Why do SSPs converge?",
        ]
        s1, s2 = st.columns(2)
        with s1:
            if st.button(suggestions[0], key="sug_0", use_container_width=True):
                st.session_state["explorer_input"] = suggestions[0]
            if st.button(suggestions[2], key="sug_2", use_container_width=True):
                st.session_state["explorer_input"] = suggestions[2]
        with s2:
            if st.button(suggestions[1], key="sug_1", use_container_width=True):
                st.session_state["explorer_input"] = suggestions[1]
            if st.button(suggestions[3], key="sug_3", use_container_width=True):
                st.session_state["explorer_input"] = suggestions[3]

        if "explorer_messages" not in st.session_state:
            st.session_state.explorer_messages = []

        if st.session_state.explorer_messages:
            chat_container = st.container(height=420)
            with chat_container:
                for msg in st.session_state.explorer_messages:
                    with st.chat_message(msg["role"]):
                        st.markdown(msg["content"])
        else:
            chat_container = st.container()

        user_input = st.chat_input(
            "Ask about projections, capacity, methodology...",
            key="explorer_chat",
        )
        prefill = st.session_state.pop("explorer_input", None)
        prompt = prefill or user_input

        if prompt:
            with st.chat_message("user"):
                st.markdown(prompt)
            with st.chat_message("assistant"):
                with st.spinner("Searching corpus..."):
                    chunks = retrieve(prompt, collection, None)
                    answer = generate_answer(prompt, chunks)
                st.markdown(answer)
            st.session_state.explorer_messages.append(
                {"role": "assistant", "content": answer}
            )


# =====================================================================
# FORECAST CHART
# =====================================================================
st.divider()

chart_col, layer_col = st.columns([5, 1], gap="medium")

summary = summary_370 if scenario_key == "ssp370" else summary_245
summary_other = summary_245 if scenario_key == "ssp370" else summary_370
other_label = "SSP2-4.5" if scenario_key == "ssp370" else "SSP3-7.0"

show_historical = st.session_state.get("layer_hist", True)
show_ensemble = st.session_state.get("layer_ens", False)
show_capacity = st.session_state.get("layer_cap", True)
show_storage_fill = st.session_state.get("layer_fill", True)
year = st.session_state.get("explorer_year", 2030)

X_MIN_YEAR = 2018
X_MAX_YEAR = 2040

fig_ts = go.Figure()

if show_capacity and show_storage_fill:
    fig_ts.add_trace(go.Scatter(
        x=pd.concat([capacity_df["date"], capacity_df["date"][::-1]]),
        y=pd.concat([capacity_df["total_mw"], capacity_df["firm_gen_mw"][::-1]]),
        fill="toself",
        fillcolor="rgba(255, 180, 50, 0.15)",
        line=dict(color="rgba(255,255,255,0)"),
        name="4h battery band", hoverinfo="skip", legendgroup="capacity",
    ))

if show_capacity:
    fig_ts.add_trace(go.Scatter(
        x=capacity_df["date"], y=capacity_df["firm_gen_mw"],
        mode="lines", name="Firm gen (gas+hydro+nuke+geo+bio)",
        line=dict(color="rgba(255, 90, 50, 0.7)", width=2, dash="dash"),
        legendgroup="capacity",
        hovertemplate="<b>Firm Gen</b><br>Year: %{x|%Y}<br>%{y:,.0f} MW<extra></extra>",
    ))

if show_capacity:
    fig_ts.add_trace(go.Scatter(
        x=capacity_df["date"], y=capacity_df["total_mw"],
        mode="lines", name="Firm + 4h battery",
        line=dict(color="rgba(255, 180, 50, 0.9)", width=2.5),
        legendgroup="capacity",
        customdata=np.stack([
            capacity_df["firm_gen_mw"], capacity_df["storage_mw"], capacity_df["total_mw"]
        ], axis=1),
        hovertemplate=(
            "<b>Firm + 4h Battery</b><br>Year: %{x|%Y}<br>"
            "Firm: %{customdata[0]:,.0f} MW<br>"
            "Battery: %{customdata[1]:,.0f} MW<br>"
            "<b>Total: %{customdata[2]:,.0f} MW</b><extra></extra>"
        ),
    ))

fig_ts.add_trace(go.Scatter(
    x=summary["date"], y=summary["mean"],
    mode="lines+markers", name=f"{scenario} ensemble mean",
    line=dict(color="rgba(50, 130, 200, 0.9)", width=3),
    marker=dict(size=5, color="rgba(50, 130, 200, 0.9)"),
    customdata=np.stack([summary["low"], summary["high"], summary["mean"]], axis=1),
    hovertemplate=(
        f"<b>{scenario} Ensemble Mean</b><br>Year: %{{x|%Y}}<br>"
        "Mean: %{customdata[2]:,.0f} MWh<br>"
        "10th: %{customdata[0]:,.0f}<br>"
        "90th: %{customdata[1]:,.0f}<extra></extra>"
    ),
))

if show_ensemble:
    fig_ts.add_trace(go.Scatter(
        x=pd.concat([summary["date"], summary["date"][::-1]]),
        y=pd.concat([summary["high"], summary["low"][::-1]]),
        fill="toself", fillcolor="rgba(50, 130, 200, 0.12)",
        line=dict(color="rgba(255,255,255,0)"),
        name=f"{scenario} range (p10-p90)", hoverinfo="skip",
    ))

fig_ts.add_trace(go.Scatter(
    x=summary_other["date"], y=summary_other["mean"],
    mode="lines", name=f"{other_label} mean",
    line=dict(color="rgba(130, 130, 130, 0.4)", width=1.5, dash="dot"),
    hovertemplate=f"<b>{other_label}</b><br>Year: %{{x|%Y}}<br>Mean: %{{y:,.0f}} MWh<extra></extra>",
))

if show_historical:
    fig_ts.add_trace(go.Scatter(
        x=hist_annual["date"], y=hist_annual["Max_Daily_Electricity_Usage"],
        mode="lines+markers", name="Historical actuals",
        line=dict(color="firebrick", width=2.5, dash="dash"),
        marker=dict(size=6, color="firebrick"),
        hovertemplate="<b>Historical</b><br>Year: %{x|%Y}<br>MWh: %{y:,.0f}<extra></extra>",
    ))

fig_ts.add_vline(
    x=pd.Timestamp(f"{year}-01-01"),
    line_dash="solid", line_color="rgba(255, 255, 255, 0.35)", line_width=1.5,
)

fig_ts.update_layout(
    xaxis_title="Year",
    yaxis_title="Peak Demand / Capacity (MWh / MW)",
    xaxis=dict(
        tickfont=dict(size=14),
        range=["2018-01-01", "2040-01-01"],
    ),
    yaxis=dict(tickfont=dict(size=14)),
    hovermode="x unified",
    height=370,
    margin={"r": 10, "t": 10, "l": 60, "b": 40},
    legend=dict(orientation="h", y=-0.2, font=dict(size=13)),
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
)

with chart_col:
    year = st.slider(
        "Year", min_value=X_MIN_YEAR, max_value=X_MAX_YEAR,
        value=year, step=1, key="explorer_year",
    )
    st.plotly_chart(fig_ts, use_container_width=True, key="forecast_chart")

    # JS: measure plotly plot-area rect, set slider padding to match exactly.
    st.markdown("""
    <script>
    (function alignSlider() {
        function tryAlign() {
            var pa = document.querySelector('.nsewdrag');
            var sl = document.querySelector('[data-testid="stSlider"]');
            if (!pa || !sl) return false;
            var pr = pa.getBoundingClientRect();
            var sr = sl.getBoundingClientRect();
            var pl = Math.max(0, pr.left - sr.left);
            var prr = Math.max(0, sr.right - pr.right);
            sl.style.setProperty('padding-left',  pl  + 'px', 'important');
            sl.style.setProperty('padding-right', prr + 'px', 'important');
            return true;
        }
        var n = 0;
        var iv = setInterval(function() { n++; if (tryAlign() || n > 50) clearInterval(iv); }, 100);
    })();
    </script>
    """, unsafe_allow_html=True)

with layer_col:
    st.markdown("**Chart layers**")
    show_historical = st.checkbox("Historical actuals", value=True, key="layer_hist")
    show_ensemble = st.checkbox("Ensemble range", value=False, key="layer_ens")
    show_capacity = st.checkbox("Capacity lines", value=True, key="layer_cap")
    show_storage_fill = st.checkbox("Storage band", value=True, key="layer_fill")

# =====================================================================
# TABLES
# =====================================================================
tab1, tab2 = st.tabs(["TAC Summary", "Top 15 Counties"])

with tab1:
    caiso_tacs = ["PGE", "SCE", "SDGE"]
    tac_year = tac_df[
        (tac_df["scenario"] == scenario_key)
        & (tac_df["year"] == year)
        & (tac_df["tac"].isin(caiso_tacs))
    ].copy()
    if len(tac_year) > 0:
        display = tac_year[[
            "tac", f"peak_{pct_key}_mean", f"peak_{pct_key}_p10",
            f"peak_{pct_key}_p90", "capacity_total", f"margin_{pct_key}",
        ]].copy()
        display.columns = [
            "TAC", f"{peak_type} Peak (MW)", "10th Pct", "90th Pct",
            "Firm+Storage (MW)", "Margin (MW)",
        ]
        for col in display.columns:
            if col != "TAC":
                display[col] = display[col].map(
                    lambda x: f"{x:,.0f}" if pd.notna(x) else "-"
                )
        st.dataframe(display, hide_index=True, use_container_width=True)

with tab2:
    if len(map_data) > 0:
        top15 = map_data.nlargest(15, f"peak_{pct_key}_mean")[
            [
                "county", "tac_area",
                f"peak_{pct_key}_mean", f"peak_{pct_key}_p10",
                f"peak_{pct_key}_p90", f"peak_{pct_key}_pct_change_vs_2025",
            ]
        ].copy()
        top15.columns = [
            "County", "TAC", "Peak (MWh)", "10th Pct", "90th Pct", "Growth (%)",
        ]
        for col in ["Peak (MWh)", "10th Pct", "90th Pct"]:
            top15[col] = top15[col].map("{:,.0f}".format)
        top15["Growth (%)"] = top15["Growth (%)"].map("{:+.1f}%".format)
        st.dataframe(top15, hide_index=True, use_container_width=True)