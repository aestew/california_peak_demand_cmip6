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

from rag_query import load_collection, retrieve, generate_answer


# ---------------------------------------------------------------------------
# CHECK API KEYS
# ---------------------------------------------------------------------------
missing_keys = []
if not os.environ.get("VOYAGE_API_KEY"):
    missing_keys.append("VOYAGE_API_KEY")
if not os.environ.get("ANTHROPIC_API_KEY"):
    missing_keys.append("ANTHROPIC_API_KEY")

if missing_keys:
    st.error(
        f"Missing environment variable(s): {', '.join(missing_keys)}\n\n"
        "Set them before running:\n"
        "```\n"
        'export VOYAGE_API_KEY="pa-..."\n'
        'export ANTHROPIC_API_KEY="sk-ant-..."\n'
        "```"
    )
    st.stop()

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
        label_visibility="collapsed"
    )
    category_map = {
        "All documents": None,
        "ClimateFEAT only": "climatefeat",
        "CEC only": "cec"
    }
    category_filter = category_map[category]

    show_sources = st.checkbox("Show retrieved sources", value=True)

    st.divider()

    st.markdown("**Sample questions**")
    sample_questions = [
        "How does ClimateFEAT handle humidity?",
        "What is the CAISO peak forecast for 2040?",
        "What features are in the heat wave stream?",
        "How do SSP370 and SSP245 compare?",
        "What is the CEC's data center methodology?",
        "What is dpd_k and how is it derived?",
        "What are the known loads in the 2025 IEPR?",
        "How does ClimateFEAT's spatial resolution compare to the CEC?",
    ]
    for q in sample_questions:
        if st.button(q, key=f"sample_{q}", use_container_width=True):
            st.session_state["rag_input"] = q

    st.divider()
    st.caption(f"Corpus: 302 chunks from 10 documents")

# ---------------------------------------------------------------------------
# HEADER
# ---------------------------------------------------------------------------
st.title("🔍 Ask ClimateFEAT")
st.caption(
    "Chat with the ClimateFEAT documentation corpus — "
    "project methodology, CEC forecasting context, and IEPR comparisons."
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
# HANDLE INPUT
# ---------------------------------------------------------------------------
# Check if a sample question was clicked
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
        "sources": chunks
    })