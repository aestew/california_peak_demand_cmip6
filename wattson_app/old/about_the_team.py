"""
about_the_team.py -- About the Team

Lives at: wattson_app/pages/about_the_team.py
"""

import streamlit as st

st.set_page_config(page_title="About the Team — ClimateFEAT", page_icon="👥", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Literata:ital,wght@0,400;0,600;0,700;1,400&family=Manrope:wght@300;400;500;600;700&family=Inconsolata:wght@400;500&display=swap');
:root {
  --accent: #5AAAE8; --accent-dim: rgba(90,170,232,0.12); --accent-border: rgba(90,170,232,0.22);
  --green-muted: #4E8878; --text-primary: #DEE8E2; --text-body: #8AA8A0;
  --text-dim: #5A8A78; --text-faint: #3A6858; --card-bg: rgba(14,28,26,0.55);
  --card-border: rgba(90,170,232,0.10); --border: rgba(90,170,232,0.08);
  --sans: 'Manrope', -apple-system, sans-serif; --mono: 'Inconsolata', monospace;
  --serif: 'Literata', Georgia, serif;
}
[data-testid="stSidebarNav"] { display: none !important; }
.stApp {
  background: linear-gradient(180deg, #080E18 0%, #0A1520 8%, #0C1822 20%,
    #0D1A22 32%, #0E1C22 42%, #0F1E1C 55%, #0F1E1A 68%, #0E1D18 80%, #0C1A14 100%) !important;
  font-family: var(--sans) !important; color: var(--text-primary) !important;
}
h1,h2,h3 { font-family: var(--serif) !important; color: var(--text-primary) !important; letter-spacing: -0.025em !important; }
h4 { font-family: var(--serif) !important; font-size: 15px !important; font-weight: 600 !important; color: var(--text-primary) !important; }
.stApp h1 { font-size: clamp(28px,3vw,40px) !important; font-weight: 700 !important; }
[data-testid="stCaptionContainer"] p {
  font-family: var(--mono) !important; font-size: 16px !important;
  color: var(--green-muted) !important; letter-spacing: 0.07em !important; text-transform: uppercase !important;
}
[data-testid="stMarkdownContainer"] strong {
  color: var(--accent) !important; font-family: var(--mono) !important;
  font-size: 16px !important; letter-spacing: 0.08em !important; text-transform: uppercase !important;
}
[data-testid="stImage"] img { border-radius: 12px !important; }
hr { border: none !important; height: 1px !important;
  background: linear-gradient(90deg, transparent, var(--accent-border), transparent) !important; }
::-webkit-scrollbar { width: 6px; } ::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--card-border); border-radius: 3px; }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("**Pages**")
    st.page_link("wattson_draft.py", label="ClimateFEAT Explorer", icon="🗺️")
    st.page_link("pages/data_explorer.py", label="Data Explorer", icon="🔍")
    st.page_link("pages/about_the_team.py", label="About the Team", icon="👥")

st.title("Meet the Team")
st.caption("UC Berkeley MIDS // Capstone 2026")

st.markdown("""
We are a group of MIDS students passionate about leveraging technology to solve complex problems
in energy demand forecasting and resource planning. Our team combines expertise in data analysis,
machine learning, software development, and project management to create innovative solutions
that can help shape the future of energy in California.
""")

st.divider()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.image(
        "https://raw.githubusercontent.com/aestew/california_peak_demand_cmip6/refs/heads/main/wattson_app/images/amy.png",
        use_container_width=True,
    )
    st.markdown("#### Amy Steward")
    st.write("**Role:** Lead Researcher, ML Engineer")

with col2:
    st.image(
        "https://raw.githubusercontent.com/aestew/california_peak_demand_cmip6/refs/heads/main/wattson_app/images/chad.png",
        use_container_width=True,
    )
    st.markdown("#### Chad Adelman")
    st.write("**Role:** RAG Evaluator & Data Support")

with col3:
    st.image(
        "https://raw.githubusercontent.com/aestew/california_peak_demand_cmip6/refs/heads/main/wattson_app/images/kristen.png",
        use_container_width=True,
    )
    st.markdown("#### Kristen Lin")
    st.write("**Role:** Data Infra")

with col4:
    st.image(
        "https://raw.githubusercontent.com/aestew/california_peak_demand_cmip6/refs/heads/main/wattson_app/images/vishnu.png",
        use_container_width=True,
    )
    st.markdown("#### Vishnu Gorur")
    st.write("**Role:** GenAI Engineer")

st.divider()
st.markdown("#### Contact Us")
st.write("Have questions? Email us at asteward@berkeley.edu.")