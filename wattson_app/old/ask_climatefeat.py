"""
ask_climatefeat.py — RAG chat page for the Wattson Streamlit app

Lives at: wattson_app/pages/ask_climatefeat.py
Imports from: RAG/rag_query.py (sibling directory)
"""

import os
import sys
import streamlit as st

# ---------------------------------------------------------------------------
# Add RAG directory to Python path so we can import rag_query
# ---------------------------------------------------------------------------
WATTSON_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_DIR = os.path.dirname(WATTSON_DIR)  # california_peak_demand_cmip6/
RAG_DIR = os.path.join(PROJECT_DIR, "RAG")

if RAG_DIR not in sys.path:
    sys.path.insert(0, RAG_DIR)

# ---------------------------------------------------------------------------
# LOAD API KEYS — st.secrets (Streamlit Cloud) → env vars (local)
# Must happen BEFORE importing rag_query so Voyage/Anthropic clients pick
# up the keys from os.environ.
# ---------------------------------------------------------------------------
for key_name in ("ANTHROPIC_API_KEY", "VOYAGE_API_KEY"):
    if not os.environ.get(key_name):
        try:
            os.environ[key_name] = st.secrets[key_name]
        except (KeyError, FileNotFoundError):
            pass

missing_keys = [k for k in ("VOYAGE_API_KEY", "ANTHROPIC_API_KEY") if not os.environ.get(k)]
if missing_keys:
    st.error(
        f"Missing API key(s): {', '.join(missing_keys)}\n\n"
        "Set them in Streamlit Cloud Secrets (TOML format) or as environment variables."
    )
    st.stop()

from rag_query import load_collection, retrieve, generate_answer

# ---------------------------------------------------------------------------
# LOAD CHROMADB (cached)
# ---------------------------------------------------------------------------
@st.cache_resource
def get_collection():
    return load_collection()

collection = get_collection()

# ---------------------------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### 🔍 Ask ClimateFEAT")

    st.divider()

    st.markdown("**Search scope**")
    category = st.radio(
        "Filter:",
        options=["All documents", "ClimateFEAT only", "CEC only"],
        index=0,
        label_visibility="collapsed",
    )
    category_map = {
        "All documents": None,
        "ClimateFEAT only": "climatefeat",
        "CEC only": "cec",
    }
    category_filter = category_map[category]

    show_sources = st.checkbox("Show retrieved sources", value=True)

    st.divider()

    st.markdown("**Sample questions**")
    sample_questions = [
        "How does ClimateFEAT compare to the CEC forecast?",
        "What is the CAISO peak forecast for 2040?",
        "How much battery storage does California have?",
        "How do SSP370 and SSP245 compare?",
        "What is the capacity margin at 2040?",
        "What features are in the heat wave stream?",
        "What are the known loads in the 2025 IEPR?",
        "Which county has the highest projected peak demand?",
    ]
    for q in sample_questions:
        if st.button(q, key=f"sample_{q}", use_container_width=True):
            st.session_state["rag_input"] = q

    st.divider()
    st.caption("Corpus: 438 chunks from 20 documents")

# ---------------------------------------------------------------------------
# HEADER
# ---------------------------------------------------------------------------
st.title("🔍 Ask ClimateFEAT")
st.caption(
    "Chat with the ClimateFEAT documentation corpus — "
    "project methodology, CEC forecasting context, projections, "
    "and capacity adequacy."
)
st.divider()

# ---------------------------------------------------------------------------
# CHAT STATE
# ---------------------------------------------------------------------------
if "rag_messages" not in st.session_state:
    st.session_state.rag_messages = []

# ---------------------------------------------------------------------------
# DISPLAY CHAT HISTORY
# ---------------------------------------------------------------------------
for message in st.session_state.rag_messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message["role"] == "assistant" and "sources" in message and show_sources:
            with st.expander("📄 Sources"):
                for src in message["sources"]:
                    cat_badge = "🟦 CEC" if src["category"] == "cec" else "🟩 ClimateFEAT"
                    st.markdown(
                        f"{cat_badge} **{src['source']}** → {src['section']}  \n"
                        f"Distance: {src['distance']:.3f}"
                    )
                    st.code(src["text"][:300] + "...", language=None)

# ---------------------------------------------------------------------------
# HANDLE INPUT — always call st.chat_input() before checking prefill
# ---------------------------------------------------------------------------
prefill = st.session_state.pop("rag_input", None)

if prompt := (prefill or st.chat_input("Ask a question about ClimateFEAT or CEC forecasting...")):
    # Display user message
    st.session_state.rag_messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Retrieve + Generate
    with st.chat_message("assistant"):
        with st.spinner("Searching corpus and generating answer..."):
            chunks = retrieve(prompt, collection, category_filter)
            answer = generate_answer(prompt, chunks)

        st.markdown(answer)

        if show_sources:
            with st.expander("📄 Sources"):
                for src in chunks:
                    cat_badge = "🟦 CEC" if src["category"] == "cec" else "🟩 ClimateFEAT"
                    st.markdown(
                        f"{cat_badge} **{src['source']}** → {src['section']}  \n"
                        f"Distance: {src['distance']:.3f}"
                    )
                    st.code(src["text"][:300] + "...", language=None)

    # Save to history
    st.session_state.rag_messages.append({
        "role": "assistant",
        "content": answer,
        "sources": chunks,
    })