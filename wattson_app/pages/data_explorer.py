"""
data_explorer.py -- FastAPI-connected data explorer chat

Lives at: wattson_app/pages/data_explorer.py
Connects to Vishnu's FastAPI RAG backend for data queries.
"""

import os
import streamlit as st
import requests

st.set_page_config(page_title="Data Explorer — ClimateFEAT", page_icon="🔍", layout="wide")

# ---------------------------------------------------------------------------
# DESIGN SYSTEM (same as main app)
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

[data-testid="stIconMaterial"] {
  font-size: 0 !important; visibility: hidden !important;
  width: 0 !important; height: 0 !important; overflow: hidden !important;
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

h1, h2, h3 { font-family: var(--serif) !important; color: var(--text-primary) !important; letter-spacing: -0.025em !important; }
h4 { font-family: var(--serif) !important; font-size: 15px !important; font-weight: 600 !important; color: var(--text-primary) !important; }

.stApp h1 { font-size: clamp(28px, 3vw, 40px) !important; font-weight: 700 !important; margin-bottom: 0 !important; }

[data-testid="stCaptionContainer"] { margin-top: 2px !important; margin-bottom: 8px !important; }
[data-testid="stCaptionContainer"] p {
  font-family: var(--mono) !important; font-size: 16px !important;
  color: var(--green-muted) !important; letter-spacing: 0.07em !important; text-transform: uppercase !important;
}

[data-testid="stChatInputContainer"] button span[data-testid="stIconMaterial"] { display: none !important; }
[data-testid="stChatInputContainer"] button { font-size: 0 !important; }
[data-testid="stChatInputContainer"] button svg { display: block !important; font-size: initial !important; }

[data-testid="stChatMessage"] {
  background: var(--card-bg) !important; border: 1px solid var(--card-border) !important;
  border-radius: 10px !important; margin-bottom: 8px !important; font-family: var(--sans) !important;
}
[data-testid="stChatMessage"] p, [data-testid="stChatMessage"] span,
[data-testid="stChatMessage"] div, [data-testid="stChatMessage"] li,
[data-testid="stChatMessage"] strong, [data-testid="stChatMessage"] code {
  color: var(--text-body) !important; font-family: var(--sans) !important;
  font-size: 16px !important; line-height: 1.65 !important;
}
[data-testid="stChatInputContainer"] textarea {
  background: var(--card-bg) !important; border: 1px solid var(--card-border) !important;
  border-radius: 8px !important; color: var(--text-primary) !important;
  font-family: var(--sans) !important; font-size: 16px !important;
}
[data-testid="stChatInputContainer"] textarea::placeholder {
  color: var(--text-faint) !important; font-family: var(--mono) !important;
  font-size: 16px !important; letter-spacing: 0.04em !important;
}

.stButton > button {
  background: var(--card-bg) !important; border: 1px solid var(--card-border) !important;
  border-radius: 8px !important; color: var(--text-body) !important;
  font-family: var(--sans) !important; font-size: 16px !important;
  transition: border-color 0.2s, color 0.2s, background 0.2s !important;
}
.stButton > button:hover {
  border-color: var(--accent-border) !important; color: var(--accent) !important;
  background: var(--accent-dim) !important;
}

[data-testid="stInfo"] {
  background: var(--accent-dim) !important; border: 1px solid var(--accent-border) !important;
  border-radius: 8px !important; color: var(--text-body) !important;
}

[data-testid="stTextInput"] > div > div {
  background: var(--card-bg) !important; border: 1px solid var(--card-border) !important;
  border-radius: 8px !important; color: var(--text-primary) !important;
  font-family: var(--mono) !important; font-size: 14px !important;
}
[data-testid="stTextInput"] label {
  color: var(--accent) !important; font-family: var(--mono) !important;
  font-size: 11px !important; letter-spacing: 0.08em !important; text-transform: uppercase !important;
}

[data-testid="stMarkdownContainer"] strong {
  color: var(--accent) !important; font-family: var(--mono) !important;
  font-size: 16px !important; letter-spacing: 0.08em !important; text-transform: uppercase !important;
}

hr {
  border: none !important; height: 1px !important;
  background: linear-gradient(90deg, transparent, var(--accent-border), transparent) !important;
  margin: 8px auto !important;
}

::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--card-border); border-radius: 3px; }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# SIDEBAR — endpoint config
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown("#### Data Explorer")
    st.caption("Query the ClimateFEAT dataset through Vishnu's RAG backend")

    st.divider()

    api_url = st.text_input(
        "FastAPI endpoint",
        value=st.session_state.get("api_url", "http://localhost:8000/query"),
        key="api_url_input",
        help="URL of the FastAPI /query endpoint",
    )
    st.session_state["api_url"] = api_url

    # Connection test
    if st.button("Test connection", use_container_width=True):
        with st.spinner("Connecting..."):
            try:
                # Try /health first
                health_url = api_url.replace("/query", "/health")
                r = requests.get(health_url, timeout=5)
                if r.ok:
                    st.session_state["api_connected"] = True
                    st.success(f"Connected")
                else:
                    raise Exception()
            except Exception:
                # Try POST to /query directly
                try:
                    r = requests.post(
                        api_url,
                        json={"question": "test", "query": "test"},
                        timeout=5,
                    )
                    if r.ok:
                        st.session_state["api_connected"] = True
                        st.success(f"Connected")
                    else:
                        st.session_state["api_connected"] = False
                        st.error(f"API returned {r.status_code}")
                except requests.exceptions.ConnectionError:
                    st.session_state["api_connected"] = False
                    st.error("Cannot reach endpoint")
                except Exception as e:
                    st.session_state["api_connected"] = False
                    st.error(f"Error: {e}")

    connected = st.session_state.get("api_connected", False)

    if connected:
        st.markdown("🟢 **Connected**")
    else:
        st.markdown("🔴 **Not connected** — using mock mode")
        st.caption("Mock mode returns sample answers for testing the UI without a running API.")

    st.divider()
    st.markdown("**Pages**")
    st.page_link("wattson_draft.py", label="ClimateFEAT Explorer", icon="🗺️")
    st.page_link("pages/data_explorer.py", label="Data Explorer", icon="🔍")

# ---------------------------------------------------------------------------
# MOCK RESPONSES (for testing without FastAPI)
# ---------------------------------------------------------------------------
MOCK_RESPONSES = {
    "default": {
        "answer": "I can answer questions about California electricity demand data, county-level statistics, BEV adoption, income data, and weather patterns. Try asking about a specific county or metric.",
        "citations": [],
    },
    "bev": {
        "answer": "**BEV registrations in Alameda County (2020):** approximately 36,200 vehicles, growing to ~52,100 by 2021 — a 44% year-over-year increase.\n\nAlameda consistently ranks among the top 5 California counties for BEV adoption, behind only Los Angeles and Santa Clara.",
        "citations": ["structured_data: bev by county"],
    },
    "income": {
        "answer": "**Highest average income:** Marin County at $173,436 per capita\n\n**Lowest average income:** Imperial County at $37,965 per capita\n\nThe statewide average across all 58 counties (2018–2023) is $72,204.",
        "citations": ["structured_data: per_capita_personal_income_adjusted"],
    },
    "peak": {
        "answer": "**Los Angeles County** had the highest peak electricity demand in 2021 at **269,731 MWh**, approximately 13x higher than San Francisco's peak of 20,541 MWh.\n\nThis reflects LA's much larger population, geographic extent, and cooling load during summer months.",
        "citations": ["structured_data: max_daily_electricity_usage"],
    },
    "weather": {
        "answer": "Extreme humidity events in San Francisco cluster in **late summer (Aug–Sep)** for highs and **winter (Jan–Feb)** plus **fall (Oct–Nov)** for lows. The peak humidity recorded was 0.0129 kg/kg on September 16, 2020.",
        "citations": ["structured_data: spfh_peak_kgkg_pop"],
    },
}


def get_mock_response(question: str) -> dict:
    q = question.lower()
    if any(w in q for w in ["bev", "ev", "electric vehicle", "zev"]):
        return MOCK_RESPONSES["bev"]
    if any(w in q for w in ["income", "rich", "poor", "salary", "wealth"]):
        return MOCK_RESPONSES["income"]
    if any(w in q for w in ["peak", "demand", "electricity", "usage", "mwh"]):
        return MOCK_RESPONSES["peak"]
    if any(w in q for w in ["weather", "humidity", "temperature", "heat", "cold"]):
        return MOCK_RESPONSES["weather"]
    return MOCK_RESPONSES["default"]


# ---------------------------------------------------------------------------
# QUERY FUNCTION
# ---------------------------------------------------------------------------
def query_api(question: str) -> dict:
    """Send question to FastAPI or fall back to mock."""
    connected = st.session_state.get("api_connected", False)
    api_url = st.session_state.get("api_url", "http://localhost:8000/query")

    if not connected:
        return get_mock_response(question)

    try:
        r = requests.post(
            api_url,
            json={"question": question, "query": question},
            timeout=30,
        )
        r.raise_for_status()
        data = r.json()

        # Normalize response — adjust field names to match Vishnu's API schema
        answer = (
            data.get("answer")
            or data.get("model_answer")
            or data.get("response")
            or data.get("result")
            or str(data)
        )
        citations = (
            data.get("citations")
            or data.get("sources")
            or data.get("retrieved_contexts")
            or []
        )

        return {"answer": answer, "citations": citations}

    except requests.exceptions.ConnectionError:
        st.session_state["api_connected"] = False
        return {
            "answer": "⚠️ Lost connection to API — falling back to mock mode.",
            "citations": [],
        }
    except Exception as e:
        return {"answer": f"⚠️ API error: {e}", "citations": []}


# ---------------------------------------------------------------------------
# HEADER
# ---------------------------------------------------------------------------
st.title("Data Explorer")
st.caption("Query the ClimateFEAT dataset // powered by FastAPI RAG backend")
st.divider()

# ---------------------------------------------------------------------------
# CHAT INTERFACE
# ---------------------------------------------------------------------------
left_col, right_col = st.columns([2, 1], gap="large")

with left_col:
    st.markdown("#### Ask about the data")

    # Suggestion buttons
    suggestions = [
        "Which county has the highest and lowest average income?",
        "How many BEVs were in San Mateo in 2021?",
        "Was peak demand higher in SF or LA in 2021?",
        "What was cloud cover in Monterey in 2018?",
    ]
    s1, s2 = st.columns(2)
    with s1:
        if st.button(suggestions[0], key="de_sug_0", use_container_width=True):
            st.session_state["de_input"] = suggestions[0]
        if st.button(suggestions[2], key="de_sug_2", use_container_width=True):
            st.session_state["de_input"] = suggestions[2]
    with s2:
        if st.button(suggestions[1], key="de_sug_1", use_container_width=True):
            st.session_state["de_input"] = suggestions[1]
        if st.button(suggestions[3], key="de_sug_3", use_container_width=True):
            st.session_state["de_input"] = suggestions[3]

    # Chat history
    if "de_messages" not in st.session_state:
        st.session_state.de_messages = []

    chat_container = st.container(height=500)
    with chat_container:
        for msg in st.session_state.de_messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
                if msg.get("citations"):
                    cites = msg["citations"]
                    if isinstance(cites, list) and len(cites) > 0:
                        # Show first 5 citations max
                        cite_strs = [str(c)[:80] for c in cites[:5]]
                        st.caption("Sources: " + " · ".join(cite_strs))

    # Input
    user_input = st.chat_input(
        "Ask about counties, BEVs, income, weather, demand...",
        key="de_chat",
    )
    prefill = st.session_state.pop("de_input", None)
    prompt = prefill or user_input

    if prompt:
        st.session_state.de_messages.append({"role": "user", "content": prompt})

        with st.spinner("Querying..."):
            result = query_api(prompt)

        st.session_state.de_messages.append({
            "role": "assistant",
            "content": result["answer"],
            "citations": result.get("citations", []),
        })
        st.rerun()

with right_col:
    st.markdown("#### How it works")
    st.markdown("""
    This page connects to a **FastAPI backend** that queries the ClimateFEAT dataset using a RAG pipeline.

    **Data queries** — county-level lookups, rankings, comparisons, and time-series questions are decomposed into SQL and answered from the structured dataset.

    **Domain questions** — methodology, climate science, and policy context are answered from a curated document corpus.
    """)

    st.divider()

    st.markdown("#### Sample questions")
    st.markdown("""
    - What was the ratio of hot to cold days in Santa Cruz?
    - How many BEVs were in Alameda in 2019?
    - Compare peak demand: SF vs LA in 2021
    - What's the min/max cloud cover for Monterey 2018?
    - How have EVs affected load forecasting?
    - How have data centers affected load forecasting?
    """)

    st.divider()

    if st.button("Clear chat", use_container_width=True):
        st.session_state.de_messages = []
        st.rerun()