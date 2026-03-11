"""
rag_query.py — Step 3 of the ClimateFEAT RAG pipeline

Takes a question, retrieves relevant chunks from ChromaDB,
and generates a grounded answer via Claude.

Works in three environments:
    1. Local terminal (reads from .env or environment variables)
    2. Streamlit local (reads from .env or environment variables)
    3. Streamlit Cloud (reads from st.secrets)

Run from the RAG/ directory:
    python rag_query.py "How does ClimateFEAT handle humidity?"
    python rag_query.py  (interactive mode)
"""

import os
import sys

# ---------------------------------------------------------------------------
# SECRET HANDLING — try all sources in order
# ---------------------------------------------------------------------------

# Source 1: .env file (local development)
try:
    from dotenv import load_dotenv
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env")
    load_dotenv(env_path)
except ImportError:
    pass  # python-dotenv not installed, that's fine

# Source 2: Streamlit Cloud secrets
try:
    import streamlit as st
    if hasattr(st, "secrets"):
        for key in ["ANTHROPIC_API_KEY", "VOYAGE_API_KEY"]:
            try:
                val = st.secrets[key]
                if val:
                    os.environ[key] = val
            except (KeyError, FileNotFoundError):
                pass
except Exception:
    pass


# ---------------------------------------------------------------------------
# CONFIG
# ---------------------------------------------------------------------------
CHROMA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chroma_db")
COLLECTION_NAME = "climatefeat_corpus"
VOYAGE_MODEL = "voyage-3.5-lite"
CLAUDE_MODEL = "claude-haiku-4-5-20251001"
TOP_K = 8
MAX_TOKENS = 1500


# ---------------------------------------------------------------------------
# STEP 1: Load ChromaDB collection
# ---------------------------------------------------------------------------
def load_collection():
    import chromadb
    client = chromadb.PersistentClient(path=CHROMA_DIR)
    collection = client.get_collection(name=COLLECTION_NAME)
    print(f"Loaded ChromaDB collection: {collection.count()} chunks")
    return collection


# ---------------------------------------------------------------------------
# STEP 2: Retrieve relevant chunks for a question
# ---------------------------------------------------------------------------
def retrieve(question: str, collection, category_filter: str = None) -> list[dict]:
    import voyageai

    api_key = os.environ.get("VOYAGE_API_KEY")
    if not api_key:
        raise ValueError("VOYAGE_API_KEY not found in environment or Streamlit secrets")

    vo = voyageai.Client(api_key=api_key)

    result = vo.embed(
        texts=[question],
        model=VOYAGE_MODEL,
        input_type="query"
    )
    query_embedding = result.embeddings[0]

    query_params = {
        "query_embeddings": [query_embedding],
        "n_results": TOP_K,
        "include": ["documents", "metadatas", "distances"]
    }

    if category_filter:
        query_params["where"] = {"category": category_filter}

    results = collection.query(**query_params)

    retrieved = []
    for i in range(len(results["ids"][0])):
        retrieved.append({
            "text": results["documents"][0][i],
            "source": results["metadatas"][0][i]["source"],
            "section": results["metadatas"][0][i]["section"],
            "category": results["metadatas"][0][i]["category"],
            "distance": results["distances"][0][i],
        })

    return retrieved


# ---------------------------------------------------------------------------
# STEP 3: Build the prompt and call Claude
# ---------------------------------------------------------------------------
def generate_answer(question: str, retrieved_chunks: list[dict]) -> str:
    import anthropic

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY not found in environment or Streamlit secrets")

    client = anthropic.Anthropic(api_key=api_key)

    context_parts = []
    for i, chunk in enumerate(retrieved_chunks):
        context_parts.append(
            f"[Source {i+1}: {chunk['source']} — {chunk['section']}]\n"
            f"{chunk['text']}"
        )
    context_block = "\n\n---\n\n".join(context_parts)

    system_prompt = """You are a technical assistant for the ClimateFEAT project, 
a climate-informed electricity demand forecasting model for California. 

You answer questions using ONLY the provided context from the ClimateFEAT 
documentation corpus. This corpus includes both ClimateFEAT project documents 
and CEC (California Energy Commission) reference documents.

Rules:
1. Answer based on the provided context only. Do not use outside knowledge.
2. Cite your sources by referencing the [Source N] tags.
3. If the context doesn't contain enough information to answer, say so clearly.
4. Be specific — use numbers, feature names, model names when they appear in context.
5. Keep answers concise but complete. Use technical language appropriate for 
   energy forecasting professionals."""

    user_message = f"""Question: {question}

Context from the ClimateFEAT documentation corpus:

{context_block}"""

    response = client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=MAX_TOKENS,
        system=system_prompt,
        messages=[
            {"role": "user", "content": user_message}
        ]
    )

    return response.content[0].text


# ---------------------------------------------------------------------------
# STEP 4: Pretty-print the full result
# ---------------------------------------------------------------------------
def ask(question: str, collection, category_filter: str = None, show_sources: bool = True):
    chunks = retrieve(question, collection, category_filter)

    if show_sources:
        print(f"\n{'─' * 60}")
        print(f"Retrieved {len(chunks)} chunks:")
        for i, chunk in enumerate(chunks):
            print(f"  [{i+1}] {chunk['source']} → {chunk['section']} (dist: {chunk['distance']:.3f})")
        print(f"{'─' * 60}")

    print(f"\nGenerating answer...\n")
    answer = generate_answer(question, chunks)
    print(answer)
    print()

    return answer


# ---------------------------------------------------------------------------
# Run it (command line mode)
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    if not os.environ.get("VOYAGE_API_KEY"):
        print("ERROR: VOYAGE_API_KEY not set.")
        sys.exit(1)
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("ERROR: ANTHROPIC_API_KEY not set.")
        sys.exit(1)

    collection = load_collection()

    if len(sys.argv) > 1:
        question = " ".join(sys.argv[1:])
        ask(question, collection)
        sys.exit(0)

    print("\nClimateFEAT RAG — ask questions about the project and CEC context.")
    print("Type 'quit' to exit. Prefix with 'cec:' or 'cf:' to filter by category.\n")

    while True:
        try:
            question = input("Question: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye!")
            break

        if not question:
            continue
        if question.lower() in ("quit", "exit", "q"):
            print("Bye!")
            break

        category_filter = None
        if question.lower().startswith("cec:"):
            category_filter = "cec"
            question = question[4:].strip()
        elif question.lower().startswith("cf:"):
            category_filter = "climatefeat"
            question = question[3:].strip()

        ask(question, collection, category_filter)