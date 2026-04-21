"""
tech_behind_this.py -- The Tech Behind SMRT-GridCA

Lives at: wattson_app/pages/tech_behind_this.py

Deep indigo -> electric violet aesthetic. Covers the multi-stream transformer
and the RAG architecture behind Wattson.
"""

import streamlit as st

st.set_page_config(
    page_title="The Tech Behind SMRT-GridCA",
    page_icon="\u26a1",
    layout="wide",
)

# ---------------------------------------------------------------------------
# DESIGN SYSTEM -- indigo/violet, shares type stack with the main app
# ---------------------------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Literata:ital,wght@0,400;0,600;0,700;1,400&family=Manrope:wght@300;400;500;600;700&family=Inconsolata:wght@400;500&display=swap');

:root {
  --accent:        #A78BFA;           /* electric violet */
  --accent-2:      #7C7FE8;           /* indigo glow */
  --accent-dim:    rgba(167,139,250,0.12);
  --accent-border: rgba(167,139,250,0.22);
  --violet-bright: #C4B5FD;
  --violet-muted:  #6B6BA8;
  --text-primary:  #E8E4F5;
  --text-body:     #A8A4C8;
  --text-dim:      #7A78A0;
  --text-faint:    #4A4870;
  --card-bg:       rgba(24,20,48,0.55);
  --card-border:   rgba(167,139,250,0.12);
  --border:        rgba(167,139,250,0.08);
  --sans:  'Manrope', -apple-system, sans-serif;
  --mono:  'Inconsolata', monospace;
  --serif: 'Literata', Georgia, serif;
}

/* Hide default Streamlit sidebar nav + the sidebar entirely */
[data-testid="stSidebar"],
[data-testid="stSidebarNav"],
[data-testid="collapsedControl"] { display: none !important; }
.stApp > header { background: transparent !important; }

/* Page gradient -- deep indigo -> violet night sky */
.stApp {
  background:
    radial-gradient(ellipse at 20% 0%, rgba(124,127,232,0.18) 0%, transparent 55%),
    radial-gradient(ellipse at 85% 15%, rgba(167,139,250,0.12) 0%, transparent 50%),
    linear-gradient(180deg,
      #0B0820 0%,
      #12103A 18%,
      #1A1648 35%,
      #1E1A55 50%,
      #1C1850 65%,
      #16123F 82%,
      #0E0A28 100%
    ) !important;
  font-family: var(--sans) !important;
  color: var(--text-primary) !important;
}

/* Widen main content, kill excessive padding */
.block-container {
  max-width: 1080px !important;
  padding-top: 2rem !important;
  padding-bottom: 4rem !important;
}

/* Headings */
h1, h2, h3 {
  font-family: var(--serif) !important;
  color: var(--text-primary) !important;
  letter-spacing: -0.025em !important;
}
h4, h5, h6, p, span, label, li { font-family: var(--sans) !important; }
.stApp h1 {
  font-size: clamp(36px, 4.5vw, 56px) !important;
  font-weight: 700 !important;
  line-height: 1.05 !important;
  margin-bottom: 12px !important;
}
.stApp h2 {
  font-size: clamp(24px, 2.8vw, 32px) !important;
  font-weight: 700 !important;
  margin-top: 8px !important;
  margin-bottom: 12px !important;
}
.stApp h3 {
  font-size: clamp(18px, 2vw, 22px) !important;
  font-weight: 600 !important;
  color: var(--text-primary) !important;
  margin-top: 4px !important;
  margin-bottom: 8px !important;
}
h4 {
  font-family: var(--serif) !important;
  font-size: 15px !important;
  font-weight: 600 !important;
  color: var(--text-primary) !important;
  letter-spacing: -0.01em !important;
}

/* Body paragraph color/size */
[data-testid="stMarkdownContainer"] p {
  color: var(--text-body) !important;
  font-size: 15px !important;
  line-height: 1.7 !important;
  font-weight: 300 !important;
}

/* Caption -- eyebrow label above titles */
[data-testid="stCaptionContainer"] p {
  font-family: var(--mono) !important;
  font-size: 12px !important;
  color: var(--accent) !important;
  letter-spacing: 0.12em !important;
  text-transform: uppercase !important;
  opacity: 0.85;
}

/* Divider */
hr {
  border: none !important;
  height: 1px !important;
  background: linear-gradient(90deg,
    transparent,
    var(--accent-border),
    transparent) !important;
  margin: 32px 0 !important;
}

/* -------- Card primitives -------- */
.tech-card {
  background: var(--card-bg);
  border: 1px solid var(--card-border);
  border-radius: 14px;
  padding: 24px 26px;
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  height: 100%;
  transition: border-color .3s, transform .3s;
}
.tech-card:hover {
  border-color: var(--accent-border);
  transform: translateY(-2px);
}
.tech-card .card-label {
  font-family: var(--mono);
  font-size: 11px;
  color: var(--accent);
  letter-spacing: 0.12em;
  text-transform: uppercase;
  margin-bottom: 12px;
}
.tech-card h3 {
  font-family: var(--serif) !important;
  font-size: 20px !important;
  font-weight: 600 !important;
  color: var(--text-primary) !important;
  margin: 0 0 10px 0 !important;
  letter-spacing: -0.015em !important;
}
.tech-card p {
  font-family: var(--sans);
  font-size: 14px;
  line-height: 1.65;
  color: var(--text-body);
  font-weight: 300;
  margin: 0 0 10px 0;
}
.tech-card .tech-meta {
  font-family: var(--mono);
  font-size: 12px;
  color: var(--text-faint);
  margin-top: 14px;
  padding-top: 12px;
  border-top: 1px solid var(--border);
  line-height: 1.5;
}

/* Stream list -- the 5 transformer streams */
.stream-row {
  display: flex;
  align-items: baseline;
  gap: 12px;
  padding: 10px 0;
  border-bottom: 1px solid var(--border);
  font-size: 14px;
  line-height: 1.5;
  color: var(--text-body);
}
.stream-row:last-child { border-bottom: none; }
.stream-row .stream-dot {
  width: 7px; height: 7px; border-radius: 50%;
  background: var(--accent); flex-shrink: 0;
  box-shadow: 0 0 8px rgba(167,139,250,0.5);
  transform: translateY(-1px);
}
.stream-row .stream-name {
  font-weight: 600; color: var(--text-primary);
  font-family: var(--mono); font-size: 13px;
  letter-spacing: 0.02em;
  min-width: 150px;
}

/* Metric scorecard table */
.metric-table {
  width: 100%;
  border-collapse: collapse;
  font-family: var(--sans);
  font-size: 13.5px;
}
.metric-table th {
  text-align: left;
  font-family: var(--mono);
  font-size: 11px;
  font-weight: 500;
  color: var(--text-dim);
  letter-spacing: 0.1em;
  text-transform: uppercase;
  padding: 10px 12px 10px 0;
  border-bottom: 1px solid var(--accent-border);
}
.metric-table th.num { text-align: right; }
.metric-table td {
  padding: 12px 12px 12px 0;
  color: var(--text-body);
  border-bottom: 1px solid var(--border);
  font-weight: 300;
}
.metric-table td.metric-name {
  color: var(--text-primary);
  font-weight: 500;
}
.metric-table td.num {
  text-align: right;
  font-family: var(--mono);
  font-size: 14px;
  color: var(--text-primary);
  font-weight: 500;
}
.metric-table td.winner {
  color: var(--accent);
}
.metric-table tr:last-child td { border-bottom: none; }

/* Big stat tiles */
.stat-tile {
  background: var(--card-bg);
  border: 1px solid var(--card-border);
  border-radius: 12px;
  padding: 20px 18px;
  text-align: center;
  backdrop-filter: blur(8px);
}
.stat-tile .stat-num {
  font-family: var(--mono);
  font-size: 28px;
  font-weight: 500;
  color: var(--accent);
  line-height: 1;
  margin-bottom: 8px;
  text-shadow: 0 0 18px rgba(167,139,250,0.25);
}
.stat-tile .stat-label {
  font-size: 11px;
  color: var(--text-dim);
  line-height: 1.4;
  letter-spacing: 0.03em;
}

/* Pipeline arrow flow */
.rag-flow {
  display: flex;
  align-items: stretch;
  gap: 8px;
  flex-wrap: wrap;
  margin: 8px 0 4px 0;
}
.rag-step {
  flex: 1;
  min-width: 140px;
  background: var(--card-bg);
  border: 1px solid var(--card-border);
  border-radius: 10px;
  padding: 14px 14px;
  position: relative;
}
.rag-step .step-num {
  font-family: var(--mono);
  font-size: 10px;
  color: var(--accent);
  letter-spacing: 0.12em;
  margin-bottom: 6px;
}
.rag-step .step-title {
  font-family: var(--serif);
  font-size: 15px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 4px;
}
.rag-step .step-tech {
  font-family: var(--mono);
  font-size: 11px;
  color: var(--text-dim);
  line-height: 1.4;
}
.rag-arrow {
  display: flex; align-items: center;
  color: var(--accent); opacity: 0.5;
  font-family: var(--mono); font-size: 18px;
}

/* Inline code pill */
code, .stMarkdown code {
  font-family: var(--mono) !important;
  font-size: 12.5px !important;
  background: rgba(167,139,250,0.1) !important;
  color: var(--violet-bright) !important;
  padding: 2px 7px !important;
  border-radius: 4px !important;
  border: 1px solid rgba(167,139,250,0.15) !important;
}

/* Eyebrow/footer nav link */
.nav-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  padding-bottom: 16px;
  border-bottom: 1px solid var(--border);
}
.nav-row a {
  font-family: var(--mono);
  font-size: 12px;
  color: var(--accent);
  text-decoration: none;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  transition: opacity .2s;
  opacity: 0.85;
}
.nav-row a:hover { opacity: 1; text-decoration: underline; }

::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--card-border); border-radius: 3px; }
</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# NAV BACK TO EXPLORER
# ---------------------------------------------------------------------------
st.markdown(
    '<div class="nav-row">'
    '<a href="/" target="_self">\u2190 Back to Explorer</a>'
    '<a href="https://github.com/aestew/california_peak_demand_cmip6" target="_blank">github \u2197</a>'
    '</div>',
    unsafe_allow_html=True,
)


# ---------------------------------------------------------------------------
# HERO
# ---------------------------------------------------------------------------
st.caption("Under the hood // SMRT-GridCA")
st.markdown("# The Tech Behind This")
st.markdown(
    '<p style="font-family:var(--serif);font-style:italic;font-size:20px;'
    'color:var(--violet-bright);margin-top:-4px;margin-bottom:22px;'
    'font-weight:400;letter-spacing:-0.01em;">'
    "A multi-stream transformer trained on lived weather, "
    "paired with a RAG system grounded in California's own energy corpus."
    "</p>",
    unsafe_allow_html=True,
)

st.markdown(
    '<p style="color:var(--text-body);font-size:16px;max-width:720px;line-height:1.7;">'
    "Forecasting peak electricity demand through 2040 is harder than it sounds. "
    "California's unique topography means a cool beach evening and a warm inland night "
    "can sit two miles apart \u2014 and existing forecasts blur them together. "
    "SMRT-GridCA takes a different approach: train on what Californians actually lived through, "
    "population-weight it, and let a transformer learn the relationships between weather, "
    "infrastructure, and demand before asking it to reason about the future."
    "</p>",
    unsafe_allow_html=True,
)

st.divider()


# ---------------------------------------------------------------------------
# SECTION 1 -- THE TRANSFORMER
# ---------------------------------------------------------------------------
st.caption("Part 01 // Prediction Model")
st.markdown("## Multi-Stream Transformer")
st.markdown(
    '<p style="color:var(--text-body);font-size:15.5px;max-width:720px;line-height:1.7;">'
    "We started with a feature-tokenizer transformer, but the model struggled to pick up "
    "feature interactions with the data volume we had. So we split the inputs into "
    "five topical streams, let each learn internal structure with its own self-attention "
    "blocks, then used multi-head cross-attention across all five streams to predict "
    "daily county-level peak demand."
    "</p>",
    unsafe_allow_html=True,
)

# Stat tiles
st.markdown('<div style="margin-top:18px;"></div>', unsafe_allow_html=True)
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(
        '<div class="stat-tile">'
        '<div class="stat-num">5</div>'
        '<div class="stat-label">Attention streams</div>'
        '</div>',
        unsafe_allow_html=True,
    )
with c2:
    st.markdown(
        '<div class="stat-tile">'
        '<div class="stat-num">58</div>'
        '<div class="stat-label">CA counties predicted</div>'
        '</div>',
        unsafe_allow_html=True,
    )
with c3:
    st.markdown(
        '<div class="stat-tile">'
        '<div class="stat-num">2.5km</div>'
        '<div class="stat-label">URMA weather grid</div>'
        '</div>',
        unsafe_allow_html=True,
    )
with c4:
    st.markdown(
        '<div class="stat-tile">'
        '<div class="stat-num">2040</div>'
        '<div class="stat-label">Forecast horizon</div>'
        '</div>',
        unsafe_allow_html=True,
    )

st.markdown('<div style="margin-top:28px;"></div>', unsafe_allow_html=True)

# Two-column: stream list + architecture notes
sc1, sc2 = st.columns([1, 1], gap="large")

with sc1:
    st.markdown("### The Five Streams")
    st.markdown(
        '<div class="tech-card" style="padding:20px 24px;">'
        '<div class="stream-row">'
        '<span class="stream-dot"></span>'
        '<span class="stream-name">WEATHER_TIME</span>'
        '<span>Temp, humidity, wind at population-weighted 2.5km URMA grid</span>'
        '</div>'
        '<div class="stream-row">'
        '<span class="stream-dot"></span>'
        '<span class="stream-name">ROLLING_TIME</span>'
        '<span>Rolling weather windows \u2014 thermal inertia of buildings</span>'
        '</div>'
        '<div class="stream-row">'
        '<span class="stream-dot"></span>'
        '<span class="stream-name">GEO_NUMERIC</span>'
        '<span>Population, income, geography static features</span>'
        '</div>'
        '<div class="stream-row">'
        '<span class="stream-dot"></span>'
        '<span class="stream-name">INFRA_TIME</span>'
        '<span>EV fleet size, cumulative data center load buildout</span>'
        '</div>'
        '<div class="stream-row">'
        '<span class="stream-dot"></span>'
        '<span class="stream-name">HEAT_WAVE</span>'
        '<span>CDD/HDD thresholds, consecutive-hot-day flags</span>'
        '</div>'
        '</div>',
        unsafe_allow_html=True,
    )

with sc2:
    st.markdown("### Architecture Notes")
    st.markdown(
        '<div class="tech-card">'
        '<p><strong style="color:var(--text-primary);">Within-stream self-attention.</strong> '
        "Each stream gets two self-attention blocks to learn its own internal relationships "
        "before talking to any other stream.</p>"
        '<p><strong style="color:var(--text-primary);">Cross-stream multi-head attention.</strong> '
        "A shared attention layer learns interactions across all five streams \u2014 this is "
        "where the model figures out, say, that a heat-wave day with a big EV fleet "
        "means something different than a heat-wave day without one.</p>"
        '<p><strong style="color:var(--text-primary);">SiLU over ReLU.</strong> '
        "Swapping the activation from ReLU to SiLU produced a clean jump in performance and "
        "was what pushed the transformer past the tree-based baselines on test data.</p>"
        '<div class="tech-meta">PyTorch \u00b7 5 streams \u00b7 2 self-attn blocks each \u00b7 MHA fusion \u00b7 SiLU</div>'
        '</div>',
        unsafe_allow_html=True,
    )

st.markdown('<div style="margin-top:32px;"></div>', unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# SECTION 1b -- SCORECARD
# ---------------------------------------------------------------------------
st.markdown("### Transformer vs. LightGBM")
st.markdown(
    '<p style="color:var(--text-body);font-size:14.5px;max-width:720px;line-height:1.65;">'
    "The LightGBM baseline is close on validation \u2014 but the transformer generalizes better "
    "out of distribution. The gap between test and val RMSE is the number we actually care about: "
    "it tells us how the model will behave on the 2018\u20132040 inference data it's never seen."
    "</p>",
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="tech-card" style="padding:20px 24px;margin-top:14px;">'
    '<table class="metric-table">'
    '<thead><tr>'
    '<th>Metric</th>'
    '<th class="num">MS Transformer</th>'
    '<th class="num">LightGBM v4</th>'
    '</tr></thead>'
    '<tbody>'
    '<tr>'
    '<td class="metric-name">Val RMSE (MWh)</td>'
    '<td class="num">145</td>'
    '<td class="num winner">141</td>'
    '</tr>'
    '<tr>'
    '<td class="metric-name">Val pop-weighted RMSE</td>'
    '<td class="num">12.4%</td>'
    '<td class="num winner">12.0%</td>'
    '</tr>'
    '<tr>'
    '<td class="metric-name">Test RMSE (MWh)</td>'
    '<td class="num winner">178</td>'
    '<td class="num">199</td>'
    '</tr>'
    '<tr>'
    '<td class="metric-name">Test pop-weighted RMSE</td>'
    '<td class="num winner">15.1%</td>'
    '<td class="num">17.4%</td>'
    '</tr>'
    '<tr>'
    '<td class="metric-name">\u0394 Test vs. Val RMSE</td>'
    '<td class="num winner">+33 (+23%)</td>'
    '<td class="num">+58 (+41%)</td>'
    '</tr>'
    '</tbody>'
    '</table>'
    '</div>',
    unsafe_allow_html=True,
)

st.markdown('<div style="margin-top:32px;"></div>', unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# SECTION 1c -- CLIMATE-INVARIANT FEATURES
# ---------------------------------------------------------------------------
st.markdown("### Keeping Features In-Range Through 2040")
st.markdown(
    '<p style="color:var(--text-body);font-size:14.5px;max-width:720px;line-height:1.65;">'
    "A known failure mode for ML models on climate inference: features that extrapolate "
    "wildly outside the training distribution. We followed the climate-invariant ML literature "
    '(Beucler et al., 2024) and kept most features within ~1.5\u00d7 of training max \u2014 except '
    "BEV fleet size, which grows 10\u00d7 by 2040. A "
    "<code>sqrt(BEV)</code> transform keeps the signal while tamping down the distribution shift."
    "</p>",
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="tech-card" style="padding:20px 24px;margin-top:14px;">'
    '<table class="metric-table">'
    '<thead><tr>'
    '<th>Feature</th>'
    '<th class="num">Train max</th>'
    '<th class="num">Future max</th>'
    '<th class="num">Ratio</th>'
    '</tr></thead>'
    '<tbody>'
    '<tr><td class="metric-name">Max temp (K, pop-wtd)</td><td class="num">322</td><td class="num">327</td><td class="num">1.0\u00d7</td></tr>'
    '<tr><td class="metric-name">CDD75 (pop-wtd)</td><td class="num">16</td><td class="num">19</td><td class="num">1.2\u00d7</td></tr>'
    '<tr><td class="metric-name">HDD65 (pop-wtd)</td><td class="num">30</td><td class="num">43</td><td class="num">1.4\u00d7</td></tr>'
    '<tr><td class="metric-name">Cumulative DC load</td><td class="num">1,449</td><td class="num">2,905</td><td class="num">2.0\u00d7</td></tr>'
    '<tr><td class="metric-name">Total population</td><td class="num">10.1M</td><td class="num">11.2M</td><td class="num">1.1\u00d7</td></tr>'
    '<tr><td class="metric-name" style="color:var(--violet-muted);">BEV (raw)</td><td class="num" style="color:var(--violet-muted);">283K</td><td class="num" style="color:var(--violet-muted);">3.0M</td><td class="num" style="color:var(--violet-muted);">10.6\u00d7</td></tr>'
    '<tr><td class="metric-name" style="color:var(--accent);">sqrt(BEV)</td><td class="num winner">532</td><td class="num winner">1,732</td><td class="num winner">3.3\u00d7</td></tr>'
    '</tbody>'
    '</table>'
    '</div>',
    unsafe_allow_html=True,
)

st.divider()

# ---------------------------------------------------------------------------
# SECTION 2 -- WHY THIS MATTERS
# ---------------------------------------------------------------------------
st.caption("Why the effort // Modeling Choices")
st.markdown("## Why Train on Lived Weather?")
st.markdown(
    '<p style="color:var(--text-body);font-size:15px;max-width:720px;line-height:1.7;">'
    "Most energy-demand forecasts lean on sparse airport weather stations or "
    "ERA5 reanalysis at 31km resolution. Neither captures California well. "
    "A single 31km cell can span ocean and 100\u00b0F inland desert \u2014 "
    "so the model ends up predicting based on an average that nobody actually experiences."
    "</p>",
    unsafe_allow_html=True,
)

wc1, wc2 = st.columns(2, gap="medium")
with wc1:
    st.markdown(
        '<div class="tech-card">'
        '<div class="card-label">What others use</div>'
        '<h3>Coarse averages</h3>'
        '<p>Airport stations, ERA5 at 31km, degree-day proxies from a single GCM. '
        'Signal is blurred across topography that drives very different loads.</p>'
        '<div class="tech-meta">31km \u00b7 ~1 GCM \u00b7 sparse stations</div>'
        '</div>',
        unsafe_allow_html=True,
    )
with wc2:
    st.markdown(
        '<div class="tech-card">'
        '<div class="card-label">What we use</div>'
        '<h3>Lived weather, population-weighted</h3>'
        '<p>NOAA URMA at 2.5km weighted by WorldPop at 1km, then aggregated '
        'to county level. Inference uses 39 CMIP6-LOCA2 ensembles across 7 GCMs '
        'and 2 SSPs so we see uncertainty, not a single trajectory.</p>'
        '<div class="tech-meta">URMA 2.5km \u00b7 WorldPop 1km \u00b7 39 ensembles \u00b7 7 GCMs</div>'
        '</div>',
        unsafe_allow_html=True,
    )

st.markdown('<div style="margin-top:24px;"></div>', unsafe_allow_html=True)
st.markdown(
    '<p style="color:var(--text-body);font-size:14.5px;max-width:720px;line-height:1.7;'
    'font-style:italic;border-left:2px solid var(--accent-border);padding-left:16px;'
    'color:var(--violet-bright);">'
    "This may be the first time actual weather history (URMA) has been used to train "
    "a transformer model that forecasts demand with downscaled climate models. The design "
    "choice was intentional: teach the model the relationship between real weather and real "
    "demand first, then let it reason about futures it's never seen."
    "</p>",
    unsafe_allow_html=True,
)

st.divider()

# ---------------------------------------------------------------------------
# SECTION 3 -- THE RAG LAYER
# ---------------------------------------------------------------------------
st.caption("Part 02 // Retrieval-Augmented Generation")
st.markdown("## The Wattson RAG System")
st.markdown(
    '<p style="color:var(--text-body);font-size:15.5px;max-width:720px;line-height:1.7;">'
    "Good forecasts don't help much if nobody understands where the numbers came from. "
    "Wattson pairs the transformer with a RAG system grounded in the actual California "
    "energy corpus \u2014 CEC IEPR documents, CAISO assessments, "
    "the ClimateFEAT methodology itself \u2014 so every answer ships with its sources."
    "</p>",
    unsafe_allow_html=True,
)

# Pipeline flow
st.markdown(
    '<div class="rag-flow" style="margin-top:18px;">'
    '<div class="rag-step">'
    '<div class="step-num">01</div>'
    '<div class="step-title">Chunk</div>'
    '<div class="step-tech">Heading-aware splits<br>\u00b7 1000 char max<br>\u00b7 150 char overlap</div>'
    '</div>'
    '<div class="rag-arrow">\u2192</div>'
    '<div class="rag-step">'
    '<div class="step-num">02</div>'
    '<div class="step-title">Embed</div>'
    '<div class="step-tech">Voyage voyage-3.5-lite<br>\u00b7 1024-dim vectors<br>\u00b7 128 chunks / batch</div>'
    '</div>'
    '<div class="rag-arrow">\u2192</div>'
    '<div class="rag-step">'
    '<div class="step-num">03</div>'
    '<div class="step-title">Index</div>'
    '<div class="step-tech">ChromaDB persistent<br>\u00b7 Category metadata<br>\u00b7 Section tags</div>'
    '</div>'
    '<div class="rag-arrow">\u2192</div>'
    '<div class="rag-step">'
    '<div class="step-num">04</div>'
    '<div class="step-title">Retrieve</div>'
    '<div class="step-tech">Top-k cosine search<br>\u00b7 Optional category filter<br>\u00b7 k = 3\u201315</div>'
    '</div>'
    '<div class="rag-arrow">\u2192</div>'
    '<div class="rag-step">'
    '<div class="step-num">05</div>'
    '<div class="step-title">Generate</div>'
    '<div class="step-tech">Claude Haiku 4.5<br>\u00b7 Grounded in context<br>\u00b7 Source-cited answers</div>'
    '</div>'
    '</div>',
    unsafe_allow_html=True,
)

st.markdown('<div style="margin-top:24px;"></div>', unsafe_allow_html=True)

# Corpus stats
rc1, rc2, rc3, rc4 = st.columns(4)
with rc1:
    st.markdown('<div class="stat-tile"><div class="stat-num">20</div><div class="stat-label">Corpus documents</div></div>', unsafe_allow_html=True)
with rc2:
    st.markdown('<div class="stat-tile"><div class="stat-num">438</div><div class="stat-label">Indexed chunks</div></div>', unsafe_allow_html=True)
with rc3:
    st.markdown('<div class="stat-tile"><div class="stat-num">1024</div><div class="stat-label">Embedding dims</div></div>', unsafe_allow_html=True)
with rc4:
    st.markdown('<div class="stat-tile"><div class="stat-num">2</div><div class="stat-label">Corpus categories</div></div>', unsafe_allow_html=True)

st.markdown('<div style="margin-top:28px;"></div>', unsafe_allow_html=True)

# Design decisions
rd1, rd2 = st.columns(2, gap="medium")
with rd1:
    st.markdown(
        '<div class="tech-card">'
        '<div class="card-label">Chunking strategy</div>'
        '<h3>Heading-aware hybrid</h3>'
        "<p>Technical docs live and die by their section structure. We split first on markdown "
        "<code>#</code> and <code>##</code> headings, so each chunk inherits the right context. "
        "Oversized sections fall through to a recursive character splitter that "
        "prefers paragraph breaks, then sentence boundaries, then spaces \u2014 never hard-cutting "
        "a number in half. Each chunk carries its source file, category, and section in metadata.</p>"
        '<div class="tech-meta">chunk_corpus.py \u00b7 heading regex \u00b7 recursive fallback \u00b7 char overlap</div>'
        '</div>',
        unsafe_allow_html=True,
    )
with rd2:
    st.markdown(
        '<div class="tech-card">'
        '<div class="card-label">Why Voyage + Chroma + Claude</div>'
        '<h3>Picked for grounding, not hype</h3>'
        "<p><code>voyage-3.5-lite</code> gives strong retrieval quality on technical text without "
        "the latency of frontier embeddings. ChromaDB's persistent client means the index survives "
        "restarts and supports metadata filters (CEC-only, ClimateFEAT-only) for free. "
        "Claude Haiku 4.5 generates the answer with a system prompt that tells it to only "
        "use the retrieved context and cite sources by <code>[Source N]</code> tags.</p>"
        '<div class="tech-meta">voyageai \u00b7 chromadb \u00b7 anthropic \u00b7 grounded prompting</div>'
        '</div>',
        unsafe_allow_html=True,
    )

st.markdown('<div style="margin-top:24px;"></div>', unsafe_allow_html=True)

# System prompt callout
st.markdown(
    '<div class="tech-card" style="background:rgba(167,139,250,0.06);'
    'border:1px solid var(--accent-border);">'
    '<div class="card-label">Guardrails</div>'
    '<h3>Refuse gracefully when context is thin</h3>'
    "<p>The system prompt is explicit: answer only from retrieved context, cite sources, "
    "and if the corpus can't fully answer the question, say what's answerable and what's missing "
    "rather than filling in with outside knowledge. For multi-hop questions "
    "(e.g. <em>\"which county faces the biggest capacity gap?\"</em) it's instructed to "
    "identify sub-questions first, address each from context, then synthesize \u2014 "
    "so gaps show up in the reasoning trace instead of hiding behind confident prose.</p>"
    '</div>',
    unsafe_allow_html=True,
)

st.divider()

# ---------------------------------------------------------------------------
# SECTION 3b -- HOW AI WAS USED
# ---------------------------------------------------------------------------
st.caption("Part 03 // Process")
st.markdown("## How AI Was Used in This Project")
st.markdown(
    '<p style="color:var(--text-body);font-size:15.5px;max-width:720px;line-height:1.7;">'
    "Worth being direct about this since the app itself is built on an LLM. "
    "AI \u2014 mostly Claude \u2014 was a constant collaborator on SMRT-GridCA, but the "
    "technical choices, architecture, and judgment calls belong to the team. "
    "Here's a concrete accounting of where it helped and where it didn't."
    "</p>",
    unsafe_allow_html=True,
)

st.markdown('<div style="margin-top:22px;"></div>', unsafe_allow_html=True)

ac1, ac2 = st.columns(2, gap="medium")

with ac1:
    st.markdown(
        '<div class="tech-card">'
        '<div class="card-label">Where AI helped a lot</div>'
        '<h3>Rubber-ducking &amp; boilerplate</h3>'
        "<p><strong style=\"color:var(--text-primary);\">Thinking out loud.</strong> "
        "Talking through architecture decisions before committing \u2014 does the "
        "cross-stream attention happen before or after the within-stream blocks? "
        "Is sqrt(BEV) enough or do we need log? What should the RAG fallback do when "
        "context is thin? These were conversations, not dictations.</p>"
        "<p><strong style=\"color:var(--text-primary);\">The unsexy code.</strong> "
        "Streamlit scaffolding, Plotly choropleth config, CSS for the Sierra Dusk "
        "aesthetic, the landing page HTML. Writing it from scratch would have been "
        "time taken away from the modeling work.</p>"
        "<p><strong style=\"color:var(--text-primary);\">Debugging.</strong> "
        "Stack traces, shape mismatches, the occasional xarray reprojection that "
        "silently returns the wrong grid. Second pair of eyes at 11pm.</p>"
        "<p><strong style=\"color:var(--text-primary);\">Paper comprehension.</strong> "
        "Working through the climate-invariant ML paper, the LOCA2 downscaling method, "
        "the Perforated AI dendritic intelligence paper (arXiv 2501.18018) \u2014 "
        "fast first-pass explanations that made the actual reading faster.</p>"
        '</div>',
        unsafe_allow_html=True,
    )

with ac2:
    st.markdown(
        '<div class="tech-card">'
        '<div class="card-label">Where AI didn\'t</div>'
        '<h3>The calls that mattered</h3>'
        "<p><strong style=\"color:var(--text-primary);\">Architecture.</strong> "
        "Deciding to split inputs into five topical streams instead of a single "
        "feature-tokenizer transformer was a human call made after watching a "
        "flat model fail to learn interactions. The AI would have happily kept "
        "tuning the thing that wasn't working.</p>"
        "<p><strong style=\"color:var(--text-primary);\">Catching the DOF bug.</strong> "
        "The population data discontinuity inflating 2024+ predictions wasn't in any "
        "error trace \u2014 it showed up as <em>numbers that felt wrong</em>. That's "
        "domain instinct. The AI helped rerun inference across all 12 output folders "
        "once the fix was scoped, but it didn't find the problem.</p>"
        "<p><strong style=\"color:var(--text-primary);\">The novel methodology.</strong> "
        "URMA + WorldPop + LOCA2 as a training \u2192 inference pipeline has no "
        "published precedent. An LLM can't recommend a technique that doesn't "
        "exist in its training data.</p>"
        "<p><strong style=\"color:var(--text-primary);\">Domain judgment.</strong> "
        "Which CEC documents actually matter for the RAG corpus. Which CEC contacts "
        "to follow up with. Whether a 12% pop-weighted RMSE is good enough to ship "
        "to a state agency. Those are calls that require knowing the field.</p>"
        '</div>',
        unsafe_allow_html=True,
    )

st.markdown('<div style="margin-top:22px;"></div>', unsafe_allow_html=True)

# In-product AI (the part the user actually sees)
st.markdown(
    '<div class="tech-card" style="background:rgba(167,139,250,0.06);'
    'border:1px solid var(--accent-border);">'
    '<div class="card-label">In the product itself</div>'
    '<h3>AI you can actually see</h3>'
    "<p>Two places. First, every answer in the Wattson chat is generated by "
    "<code>claude-haiku-4-5</code> with retrieved corpus chunks in context \u2014 the "
    "model is instructed to only use the provided sources and cite them, and to say "
    "what's missing rather than hallucinate when the corpus falls short. "
    "Second, embeddings for the corpus come from Voyage AI's <code>voyage-3.5-lite</code>, "
    "which is an LLM-family model specifically trained for retrieval.</p>"
    "<p>The forecasts themselves do not involve an LLM. Peak demand predictions come "
    "from the multi-stream transformer trained from scratch on URMA weather data. "
    "That's a PyTorch model with learned weights, not a prompt.</p>"
    '</div>',
    unsafe_allow_html=True,
)

st.markdown('<div style="margin-top:22px;"></div>', unsafe_allow_html=True)

# Honest note on the collaboration pattern
st.markdown(
    '<p style="color:var(--violet-bright);font-size:14.5px;max-width:720px;line-height:1.7;'
    'font-style:italic;border-left:2px solid var(--accent-border);padding-left:16px;">'
    "The honest version: AI collaboration worked best when treated like a fast, "
    "confident, slightly-overconfident teammate. Useful for drafts, dangerous without "
    "review, and no substitute for actually understanding the problem. Every line of "
    "generated code got read before it ran. Every suggestion got checked against "
    "the data. That's the part that makes the output trustworthy, not the model."
    "</p>",
    unsafe_allow_html=True,
)

st.divider()

# ---------------------------------------------------------------------------
# SECTION 4 -- SOURCES / FURTHER READING
# ---------------------------------------------------------------------------
st.caption("Further reading // Methodology")
st.markdown("## References")

ref1, ref2 = st.columns(2, gap="medium")
with ref1:
    st.markdown(
        '<div class="tech-card">'
        '<h3 style="font-size:16px !important;">Climate-invariant ML</h3>'
        '<p style="font-size:13px;">Beucler et al. (2024). <em>Climate-invariant machine learning.</em> '
        "Science Advances, 10(6).</p>"
        '<p style="font-size:13px;">Brockway et al. (2022). <em>Grid planning in a changing climate.</em> '
        "Environmental Research Letters 17.</p>"
        '<p style="font-size:13px;">Lehner et al. (2020). <em>Partitioning climate projection uncertainty.</em> '
        "Earth Syst. Dynam. 11.</p>"
        '</div>',
        unsafe_allow_html=True,
    )
with ref2:
    st.markdown(
        '<div class="tech-card">'
        '<h3 style="font-size:16px !important;">Data sources</h3>'
        '<p style="font-size:13px;"><strong style="color:var(--text-primary);">NOAA URMA</strong> \u00b7 '
        "2.5km gridded weather reanalysis (training)</p>"
        '<p style="font-size:13px;"><strong style="color:var(--text-primary);">LOCA2-Hybrid</strong> \u00b7 '
        "3km downscaled CMIP6 (inference through 2040)</p>"
        '<p style="font-size:13px;"><strong style="color:var(--text-primary);">WorldPop</strong> \u00b7 '
        "1km population for spatial weighting</p>"
        '<p style="font-size:13px;"><strong style="color:var(--text-primary);">CEC IEPR + CAISO</strong> \u00b7 '
        "RAG corpus documents</p>"
        '</div>',
        unsafe_allow_html=True,
    )

st.markdown('<div style="margin-top:40px;"></div>', unsafe_allow_html=True)
st.markdown(
    '<div style="text-align:center;padding:24px 0;border-top:1px solid var(--border);">'
    '<p style="font-family:var(--mono);font-size:12px;color:var(--text-faint);'
    'letter-spacing:0.08em;text-transform:uppercase;">'
    "SMRT-GridCA \u00b7 UC Berkeley MIDS Capstone \u00b7 2026"
    "</p>"
    "</div>",
    unsafe_allow_html=True,
)
