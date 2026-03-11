"""
chunk_corpus.py — Step 1 of the ClimateFEAT RAG pipeline

Reads markdown files from RAG/corpus/, splits them into chunks
using heading-aware + fixed-size hybrid chunking, and tags each
chunk with metadata (source, category, section).

Run from the RAG/ directory:
    python chunk_corpus.py

Output: prints a summary of all chunks for inspection.
The get_chunks() function returns a list of dicts that Step 2
(embedding) will consume.
"""

import os
import re
import json
from pathlib import Path

# ---------------------------------------------------------------------------
# CONFIG — tweak these if you want different chunk sizes
# ---------------------------------------------------------------------------
CORPUS_DIR = os.path.join(os.path.dirname(__file__), "corpus")
MAX_CHUNK_SIZE = 1000      # characters — target max size per chunk
CHUNK_OVERLAP = 150        # characters — overlap between consecutive chunks


# ---------------------------------------------------------------------------
# STEP 1: Read all markdown files from corpus/
# ---------------------------------------------------------------------------
def load_documents(corpus_dir: str) -> list[dict]:
    """
    Reads every .md file in corpus_dir.
    Returns a list of dicts: [{"filename": "...", "text": "..."}]
    """
    docs = []
    corpus_path = Path(corpus_dir)

    if not corpus_path.exists():
        raise FileNotFoundError(
            f"Corpus directory not found: {corpus_dir}\n"
            f"Make sure you're running this from the RAG/ directory."
        )

    for filepath in sorted(corpus_path.glob("*.md")):
        text = filepath.read_text(encoding="utf-8")
        docs.append({
            "filename": filepath.name,
            "text": text
        })

    print(f"Loaded {len(docs)} documents from {corpus_dir}")
    for doc in docs:
        print(f"  {doc['filename']} ({len(doc['text']):,} chars)")
    print()

    return docs


# ---------------------------------------------------------------------------
# STEP 2: Split a single document into sections based on markdown headings
# ---------------------------------------------------------------------------
def split_by_headings(text: str) -> list[dict]:
    """
    Splits markdown text on lines that start with # or ##.
    Returns a list of dicts: [{"section": "heading text", "text": "..."}]

    The heading line itself is included at the top of each section's text,
    so the LLM sees the context when reading a chunk.
    """
    # This regex matches lines starting with 1-3 # characters
    # re.MULTILINE makes ^ match start of each line, not just start of string
    heading_pattern = re.compile(r"^(#{1,3})\s+(.+)", re.MULTILINE)

    sections = []
    matches = list(heading_pattern.finditer(text))

    if not matches:
        # No headings found — treat the whole document as one section
        return [{"section": "full_document", "text": text.strip()}]

    # If there's text before the first heading (e.g., YAML frontmatter,
    # title line, or intro paragraph), capture it as a "preamble" section
    if matches[0].start() > 0:
        preamble = text[:matches[0].start()].strip()
        if preamble:
            sections.append({
                "section": "preamble",
                "text": preamble
            })

    # For each heading, grab everything from that heading to the next heading
    for i, match in enumerate(matches):
        heading_text = match.group(2).strip()

        # Start of this section = start of this heading line
        start = match.start()

        # End of this section = start of next heading, or end of document
        if i + 1 < len(matches):
            end = matches[i + 1].start()
        else:
            end = len(text)

        section_text = text[start:end].strip()

        sections.append({
            "section": heading_text,
            "text": section_text
        })

    return sections


# ---------------------------------------------------------------------------
# STEP 3: Split a long section into smaller chunks (fixed-size fallback)
# ---------------------------------------------------------------------------
def split_text_recursive(text: str, max_size: int, overlap: int) -> list[str]:
    """
    Splits text into chunks of roughly max_size characters, with overlap.

    Tries to split on these separators in order (best → worst):
      1. Double newline (paragraph break)
      2. Single newline
      3. Sentence-ending punctuation followed by a space
      4. Any space (last resort)

    This is the same logic as LangChain's RecursiveCharacterTextSplitter
    but written out explicitly so you can see exactly what's happening.
    """
    if len(text) <= max_size:
        return [text]

    # Try each separator in order of preference
    separators = ["\n\n", "\n", ". ", " "]

    for sep in separators:
        parts = text.split(sep)
        if len(parts) == 1:
            continue  # This separator doesn't appear in the text

        # Build chunks by accumulating parts until we'd exceed max_size
        chunks = []
        current = ""

        for part in parts:
            # Would adding this part exceed our limit?
            candidate = current + sep + part if current else part

            if len(candidate) <= max_size:
                current = candidate
            else:
                if current:
                    chunks.append(current.strip())
                current = part

        if current:
            chunks.append(current.strip())

        # If we got a reasonable split, add overlap and return
        if len(chunks) > 1:
            return _add_overlap(chunks, overlap)

    # If nothing worked (e.g., one giant word), just hard-cut
    chunks = []
    for i in range(0, len(text), max_size - overlap):
        chunks.append(text[i:i + max_size])
    return chunks


def _add_overlap(chunks: list[str], overlap: int) -> list[str]:
    """
    Adds character overlap between consecutive chunks so context
    isn't lost at boundaries.

    For each chunk after the first, we prepend the last `overlap`
    characters from the previous chunk.
    """
    if overlap == 0 or len(chunks) <= 1:
        return chunks

    overlapped = [chunks[0]]
    for i in range(1, len(chunks)):
        # Grab the tail of the previous chunk
        prev_tail = chunks[i - 1][-overlap:]

        # Try to start the overlap at a word boundary
        space_idx = prev_tail.find(" ")
        if space_idx != -1:
            prev_tail = prev_tail[space_idx + 1:]

        overlapped.append(prev_tail + " " + chunks[i])

    return overlapped


# ---------------------------------------------------------------------------
# STEP 4: Determine category from filename prefix
# ---------------------------------------------------------------------------
def get_category(filename: str) -> str:
    """
    Returns 'cec' or 'climatefeat' based on the filename prefix.
    This is used for metadata filtering in ChromaDB — e.g., you can
    search only CEC docs or only ClimateFEAT docs.
    """
    if filename.startswith("cec_"):
        return "cec"
    elif filename.startswith("climatefeat_"):
        return "climatefeat"
    else:
        return "other"


# ---------------------------------------------------------------------------
# STEP 5: Put it all together — the main chunking function
# ---------------------------------------------------------------------------
def get_chunks() -> list[dict]:
    """
    Main entry point. Returns a list of chunk dicts:

    [
        {
            "chunk_id": "cec_iepr_2025_preliminary.md::Data Centers::0",
            "text": "## 5. Data Centers\n\nThe pipeline includes...",
            "source": "cec_iepr_2025_preliminary.md",
            "category": "cec",
            "section": "Data Centers"
        },
        ...
    ]
    """
    docs = load_documents(CORPUS_DIR)
    all_chunks = []
    global_idx = 0

    for doc in docs:
        filename = doc["filename"]
        category = get_category(filename)

        # Split into heading-based sections first
        sections = split_by_headings(doc["text"])

        for section in sections:
            section_name = section["section"]
            section_text = section["text"]

            # If the section is small enough, keep it as one chunk
            if len(section_text) <= MAX_CHUNK_SIZE:
                text_pieces = [section_text]
            else:
                # Otherwise, split it further with the recursive splitter
                text_pieces = split_text_recursive(
                    section_text, MAX_CHUNK_SIZE, CHUNK_OVERLAP
                )

            # Create a chunk dict for each piece
            for i, piece in enumerate(text_pieces):
                chunk = {
                    "chunk_id": f"{filename}::{section_name}::{global_idx}",
                    "text": piece,
                    "source": filename,
                    "category": category,
                    "section": section_name,
                }
                all_chunks.append(chunk)
                global_idx += 1

    return all_chunks


# ---------------------------------------------------------------------------
# STEP 6: Print a human-readable summary for inspection
# ---------------------------------------------------------------------------
def print_summary(chunks: list[dict]):
    """Prints chunk counts per doc + per section, and a sample chunk."""

    print("=" * 70)
    print(f"TOTAL CHUNKS: {len(chunks)}")
    print("=" * 70)

    # Group by source file
    by_source = {}
    for chunk in chunks:
        src = chunk["source"]
        if src not in by_source:
            by_source[src] = []
        by_source[src].append(chunk)

    for source, source_chunks in by_source.items():
        category = source_chunks[0]["category"]
        print(f"\n{source}  [{category}]  →  {len(source_chunks)} chunks")

        # Show sections found in this doc
        sections_seen = []
        for c in source_chunks:
            if c["section"] not in sections_seen:
                sections_seen.append(c["section"])

        for section in sections_seen:
            section_chunks = [c for c in source_chunks if c["section"] == section]
            total_chars = sum(len(c["text"]) for c in section_chunks)
            print(f"    {section} → {len(section_chunks)} chunk(s), {total_chars:,} chars")

    # Show one sample chunk so you can eyeball it
    print("\n" + "=" * 70)
    print("SAMPLE CHUNK (first chunk from the corpus):")
    print("=" * 70)
    sample = chunks[0]
    print(f"  chunk_id: {sample['chunk_id']}")
    print(f"  source:   {sample['source']}")
    print(f"  category: {sample['category']}")
    print(f"  section:  {sample['section']}")
    print(f"  length:   {len(sample['text'])} chars")
    print(f"  text preview:")
    print(f"    {sample['text'][:300]}...")
    print()


# ---------------------------------------------------------------------------
# Run it
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    chunks = get_chunks()
    print_summary(chunks)

    # Optionally save to JSON for inspection or debugging
    output_path = os.path.join(os.path.dirname(__file__), "chunks_debug.json")
    with open(output_path, "w") as f:
        json.dump(chunks, f, indent=2)
    print(f"Full chunk data saved to {output_path} for inspection.")