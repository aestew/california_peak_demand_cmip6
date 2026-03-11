"""
embed_and_index.py — Step 2 of the ClimateFEAT RAG pipeline

Takes chunks from chunk_corpus.py, embeds them via Voyage AI,
and stores everything in a ChromaDB database on disk.

Prerequisites:
    pip install voyageai chromadb

    Set your Voyage API key:
    export VOYAGE_API_KEY="pa-your-key-here"

Run from the RAG/ directory:
    python embed_and_index.py

Output: creates RAG/chroma_db/ directory containing the vector database.
"""

import os
import sys
import time

# ---------------------------------------------------------------------------
# CONFIG
# ---------------------------------------------------------------------------
CHROMA_DIR = os.path.join(os.path.dirname(__file__), "chroma_db")
COLLECTION_NAME = "climatefeat_corpus"
VOYAGE_MODEL = "voyage-3.5-lite"  # good balance of quality + cost; upgrade to voyage-3.5 if you want
VOYAGE_BATCH_SIZE = 128           # Voyage API max per request
EMBEDDING_DIM = 1024              # voyage-3.5-lite output dimension


# ---------------------------------------------------------------------------
# STEP 1: Import chunks from chunk_corpus.py
# ---------------------------------------------------------------------------
def load_chunks():
    """
    Imports and runs get_chunks() from chunk_corpus.py.
    Returns the list of chunk dicts.
    """
    from chunk_corpus import get_chunks
    chunks = get_chunks()
    print(f"\nLoaded {len(chunks)} chunks from chunk_corpus.py")
    return chunks


# ---------------------------------------------------------------------------
# STEP 2: Embed chunks via Voyage AI
# ---------------------------------------------------------------------------
def embed_chunks(chunks: list[dict]) -> list[list[float]]:
    """
    Sends chunk text to Voyage AI in batches, returns a list of
    embedding vectors (one per chunk, same order).

    Each embedding is a list of 1024 floats representing the
    semantic meaning of that chunk in vector space.
    """
    import voyageai

    # Check for API key
    api_key = os.environ.get("VOYAGE_API_KEY")
    if not api_key:
        print("ERROR: VOYAGE_API_KEY environment variable not set.")
        print("Run: export VOYAGE_API_KEY=\"pa-your-key-here\"")
        sys.exit(1)

    vo = voyageai.Client(api_key=api_key)

    # Extract just the text from each chunk
    texts = [chunk["text"] for chunk in chunks]

    all_embeddings = []
    total_batches = (len(texts) + VOYAGE_BATCH_SIZE - 1) // VOYAGE_BATCH_SIZE

    print(f"\nEmbedding {len(texts)} chunks via Voyage AI ({VOYAGE_MODEL})")
    print(f"  Batch size: {VOYAGE_BATCH_SIZE}")
    print(f"  Total batches: {total_batches}")
    print()

    for i in range(0, len(texts), VOYAGE_BATCH_SIZE):
        batch = texts[i : i + VOYAGE_BATCH_SIZE]
        batch_num = (i // VOYAGE_BATCH_SIZE) + 1

        print(f"  Batch {batch_num}/{total_batches} ({len(batch)} chunks)...", end=" ")

        # Call Voyage AI
        # input_type="document" tells Voyage these are documents being indexed
        # (vs "query" which is used at search time — Voyage optimizes differently)
        result = vo.embed(
            texts=batch,
            model=VOYAGE_MODEL,
            input_type="document"
        )

        batch_embeddings = result.embeddings
        all_embeddings.extend(batch_embeddings)

        print(f"done. ({result.total_tokens} tokens)")

        # Small delay between batches to be nice to the API
        if batch_num < total_batches:
            time.sleep(0.5)

    print(f"\nEmbedding complete. Got {len(all_embeddings)} vectors.")
    print(f"  Vector dimension: {len(all_embeddings[0])}")

    return all_embeddings


# ---------------------------------------------------------------------------
# STEP 3: Store in ChromaDB
# ---------------------------------------------------------------------------
def store_in_chroma(chunks: list[dict], embeddings: list[list[float]]):
    """
    Creates a ChromaDB collection and adds all chunks with their
    embeddings and metadata.

    The database is persisted to disk at RAG/chroma_db/ so it
    survives between runs. You don't need to re-embed every time.
    """
    import chromadb

    # Create a persistent ChromaDB client
    # This stores the database as files in CHROMA_DIR
    client = chromadb.PersistentClient(path=CHROMA_DIR)

    # Delete existing collection if it exists (fresh index each time)
    try:
        client.delete_collection(name=COLLECTION_NAME)
        print(f"\nDeleted existing collection '{COLLECTION_NAME}'")
    except Exception:
        pass  # Collection doesn't exist yet, that's fine

    # Create a new collection
    collection = client.create_collection(
        name=COLLECTION_NAME,
        metadata={"description": "ClimateFEAT RAG corpus — 10 markdown docs"}
    )

    print(f"Created collection '{COLLECTION_NAME}'")

    # Prepare the data for ChromaDB's add() method
    # ChromaDB wants parallel lists: ids, embeddings, documents, metadatas
    ids = []
    documents = []
    metadatas = []

    for chunk in chunks:
        ids.append(chunk["chunk_id"])
        documents.append(chunk["text"])
        metadatas.append({
            "source": chunk["source"],
            "category": chunk["category"],
            "section": chunk["section"]
        })

    # Add everything in one call
    # ChromaDB handles batching internally
    collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=documents,
        metadatas=metadatas
    )

    print(f"Added {len(ids)} chunks to ChromaDB")
    print(f"Database saved to: {os.path.abspath(CHROMA_DIR)}")

    # Quick sanity check: count what's in the collection
    count = collection.count()
    print(f"Verification: collection contains {count} items")

    return collection


# ---------------------------------------------------------------------------
# STEP 4: Print a quick test query to verify it works
# ---------------------------------------------------------------------------
def test_query(collection):
    """
    Runs a sample query against the collection to make sure
    everything is wired up correctly.
    """
    import voyageai

    vo = voyageai.Client(api_key=os.environ.get("VOYAGE_API_KEY"))

    test_question = "How does ClimateFEAT handle humidity differently from the CEC forecast?"

    print(f"\n{'=' * 70}")
    print(f"TEST QUERY: {test_question}")
    print(f"{'=' * 70}")

    # Embed the question
    # input_type="query" tells Voyage this is a search query (not a document)
    result = vo.embed(
        texts=[test_question],
        model=VOYAGE_MODEL,
        input_type="query"
    )
    query_embedding = result.embeddings[0]

    # Search ChromaDB — find the 5 most similar chunks
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=5,
        include=["documents", "metadatas", "distances"]
    )

    # Print results
    for i in range(len(results["ids"][0])):
        chunk_id = results["ids"][0][i]
        distance = results["distances"][0][i]
        source = results["metadatas"][0][i]["source"]
        section = results["metadatas"][0][i]["section"]
        text_preview = results["documents"][0][i][:200]

        print(f"\n  [{i+1}] distance: {distance:.4f}")
        print(f"      source:  {source}")
        print(f"      section: {section}")
        print(f"      text:    {text_preview}...")

    print()


# ---------------------------------------------------------------------------
# Run it
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # Step 1: Load chunks
    chunks = load_chunks()

    # Step 2: Embed via Voyage AI
    embeddings = embed_chunks(chunks)

    # Step 3: Store in ChromaDB
    collection = store_in_chroma(chunks, embeddings)

    # Step 4: Quick test
    test_query(collection)

    print("=" * 70)
    print("DONE. Your vector database is ready at:")
    print(f"  {os.path.abspath(CHROMA_DIR)}")
    print()
    print("Next step: python query_rag.py")
    print("=" * 70)