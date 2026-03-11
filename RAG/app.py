"""
app.py — Step 4 of the ClimateFEAT RAG pipeline

Streamlit chat interface for querying the ClimateFEAT RAG system.

Prerequisites:
    pip install streamlit voyageai chromadb anthropic

    Set your API keys:
    export VOYAGE_API_KEY="pa-your-key-here"
    export ANTHROPIC_API_KEY="sk-ant-your-key-here"

Run from the RAG/ directory:
    streamlit run app.py
"""

import os
import streamlit as st

# Import our RAG functions from query_rag.py
from query_rag import load_collection, retrieve, generate_answer

# ---------------------------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="ClimateFEAT RAG",
    page_icon="⚡",
    layout="wide"
)

# ---------------------------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------------------------
with st.sidebar:
    st.title("⚡ ClimateFEAT RAG")
    st.markdown(
        "Ask questions about the ClimateFEAT project and "
        "CEC demand forecasting context."
    )

    st.divider()

    # Category filter
    st.markdown("**Filter by source**")
    category = st.radio(
        "Search scope:",
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

    st.divider()

    # Number of chunks to retrieve
    top_k = st.slider("Chunks to retrieve", min_value=3, max_value=15, value=8)

    # Show sources toggle
    show_sources = st.checkbox("Show retrieved sources", value=True)

    st.divider()

    st.markdown("**Corpus**")
    st.markdown(
        "- 3 CEC documents\n"
        "- 7 ClimateFEAT documents\n"
        "- 302 chunks indexed"
    )

    st.divider()

    st.markdown("**Sample questions**")
    st.markdown(
        "- How does ClimateFEAT handle humidity?\n"
        "- What is the CAISO peak forecast for 2040?\n"
        "- What features are in the heat wave stream?\n"
        "- How do SSP370 and SSP245 compare?\n"
        "- What is the CEC's data center methodology?\n"
        "- What is dpd_k and how is it derived?"
    )

# ---------------------------------------------------------------------------
# LOAD COLLECTION (cached so it only loads once)
# ---------------------------------------------------------------------------
@st.cache_resource
def get_collection():
    """Load ChromaDB collection once, reuse across reruns."""
    return load_collection()

# Check for API keys before loading anything
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

collection = get_collection()

# ---------------------------------------------------------------------------
# CHAT STATE
# ---------------------------------------------------------------------------
# Streamlit reruns the whole script on every interaction.
# st.session_state persists between reruns.
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------------------------------------------------------------------
# DISPLAY CHAT HISTORY
# ---------------------------------------------------------------------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

        # Show sources if they were saved with this message
        if message["role"] == "assistant" and "sources" in message and show_sources:
            with st.expander("📄 Sources"):
                for src in message["sources"]:
                    st.markdown(
                        f"**{src['source']}** → {src['section']}  \n"
                        f"Distance: {src['distance']:.3f}"
                    )
                    st.code(src["text"][:300] + "...", language=None)

# ---------------------------------------------------------------------------
# HANDLE NEW INPUT
# ---------------------------------------------------------------------------
if prompt := st.chat_input("Ask a question about ClimateFEAT or CEC forecasting..."):
    # Display user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Retrieve + Generate
    with st.chat_message("assistant"):
        # Show a spinner while retrieving and generating
        with st.spinner("Searching corpus and generating answer..."):
            # Step 1: Retrieve relevant chunks
            chunks = retrieve(prompt, collection, category_filter)

            # Override top_k if user changed the slider
            # (retrieve uses the module-level TOP_K, so we re-query if needed)
            if top_k != 8:
                import query_rag
                original_top_k = query_rag.TOP_K
                query_rag.TOP_K = top_k
                chunks = retrieve(prompt, collection, category_filter)
                query_rag.TOP_K = original_top_k

            # Step 2: Generate answer via Claude
            answer = generate_answer(prompt, chunks)

        # Display the answer
        st.markdown(answer)

        # Display sources
        if show_sources:
            with st.expander("📄 Sources"):
                for i, chunk in enumerate(chunks):
                    st.markdown(
                        f"**{chunk['source']}** → {chunk['section']}  \n"
                        f"Distance: {chunk['distance']:.3f}"
                    )
                    st.code(chunk["text"][:300] + "...", language=None)

    # Save to chat history
    st.session_state.messages.append({
        "role": "assistant",
        "content": answer,
        "sources": chunks
    })