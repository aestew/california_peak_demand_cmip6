"""
query_rag.py — Step 3 of the ClimateFEAT RAG pipeline

Takes a question, retrieves relevant chunks from ChromaDB,
and generates a grounded answer via Claude.

Prerequisites:
    pip install voyageai chromadb anthropic

    Set your API keys:
    export VOYAGE_API_KEY="pa-your-key-here"
    export ANTHROPIC_API_KEY="sk-ant-your-key-here"

Run from the RAG/ directory:
    python query_rag.py "How does ClimateFEAT handle humidity?"
    python query_rag.py  (interactive mode — keeps asking for questions)
"""

import os
import sys

# ---------------------------------------------------------------------------
# CONFIG
# ---------------------------------------------------------------------------
CHROMA_DIR = os.path.join(os.path.dirname(__file__), "chroma_db")
COLLECTION_NAME = "climatefeat_corpus"
VOYAGE_MODEL = "voyage-3.5-lite"
CLAUDE_MODEL = "claude-haiku-4-5-20251001"
TOP_K = 8                 # number of chunks to retrieve
MAX_TOKENS = 1500         # max length of Claude's answer


# ---------------------------------------------------------------------------
# STEP 1: Load ChromaDB collection
# ---------------------------------------------------------------------------
def load_collection():
    """
    Opens the existing ChromaDB database from disk.
    Returns the collection object.
    """
    import chromadb

    client = chromadb.PersistentClient(path=CHROMA_DIR)
    collection = client.get_collection(name=COLLECTION_NAME)
    print(f"Loaded ChromaDB collection: {collection.count()} chunks")
    return collection


# ---------------------------------------------------------------------------
# STEP 2: Retrieve relevant chunks for a question
# ---------------------------------------------------------------------------
def retrieve(question: str, collection, category_filter: str = None) -> list[dict]:
    """
    Embeds the question via Voyage AI, searches ChromaDB,
    and returns the top-k most relevant chunks.

    Args:
        question: the user's question
        collection: ChromaDB collection object
        category_filter: optional — "cec" or "climatefeat" to restrict search

    Returns:
        list of dicts with keys: text, source, section, category, distance
    """
    import voyageai

    vo = voyageai.Client(api_key=os.environ.get("VOYAGE_API_KEY"))

    # Embed the question
    # input_type="query" tells Voyage to optimize for search queries
    result = vo.embed(
        texts=[question],
        model=VOYAGE_MODEL,
        input_type="query"
    )
    query_embedding = result.embeddings[0]

    # Build the ChromaDB query
    query_params = {
        "query_embeddings": [query_embedding],
        "n_results": TOP_K,
        "include": ["documents", "metadatas", "distances"]
    }

    # Optional: filter by category (only search CEC docs or only ClimateFEAT docs)
    if category_filter:
        query_params["where"] = {"category": category_filter}

    results = collection.query(**query_params)

    # Package results into a clean list of dicts
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
    """
    Builds a prompt with the retrieved chunks as context,
    sends it to Claude, and returns the answer.
    """
    import anthropic

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("ERROR: ANTHROPIC_API_KEY environment variable not set.")
        print("Run: export ANTHROPIC_API_KEY=\"sk-ant-your-key-here\"")
        sys.exit(1)

    client = anthropic.Anthropic(api_key=api_key)

    # Build the context block from retrieved chunks
    context_parts = []
    for i, chunk in enumerate(retrieved_chunks):
        context_parts.append(
            f"[Source {i+1}: {chunk['source']} — {chunk['section']}]\n"
            f"{chunk['text']}"
        )
    context_block = "\n\n---\n\n".join(context_parts)

    # System prompt: tells Claude how to behave
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

    # User message: question + context
    user_message = f"""Question: {question}

Context from the ClimateFEAT documentation corpus:

{context_block}"""

    # Call Claude
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
    """
    Full RAG pipeline: retrieve → generate → print.
    """
    # Retrieve
    chunks = retrieve(question, collection, category_filter)

    if show_sources:
        print(f"\n{'─' * 60}")
        print(f"Retrieved {len(chunks)} chunks:")
        for i, chunk in enumerate(chunks):
            print(f"  [{i+1}] {chunk['source']} → {chunk['section']} (dist: {chunk['distance']:.3f})")
        print(f"{'─' * 60}")

    # Generate
    print(f"\nGenerating answer...\n")
    answer = generate_answer(question, chunks)

    print(answer)
    print()

    return answer


# ---------------------------------------------------------------------------
# Run it
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # Check API keys
    if not os.environ.get("VOYAGE_API_KEY"):
        print("ERROR: VOYAGE_API_KEY not set. Run: export VOYAGE_API_KEY=\"pa-...\"")
        sys.exit(1)
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("ERROR: ANTHROPIC_API_KEY not set. Run: export ANTHROPIC_API_KEY=\"sk-ant-...\"")
        sys.exit(1)

    # Load the collection
    collection = load_collection()

    # If a question was passed on the command line, answer it and exit
    if len(sys.argv) > 1:
        question = " ".join(sys.argv[1:])
        ask(question, collection)
        sys.exit(0)

    # Otherwise, interactive mode
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

        # Check for category prefix
        category_filter = None
        if question.lower().startswith("cec:"):
            category_filter = "cec"
            question = question[4:].strip()
        elif question.lower().startswith("cf:"):
            category_filter = "climatefeat"
            question = question[3:].strip()

        ask(question, collection, category_filter)