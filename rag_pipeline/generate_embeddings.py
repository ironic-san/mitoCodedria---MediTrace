"""
MediTrace RAG Pipeline -- Stage 2: Embedding Generation

Reads the approved chunks.json from Stage 1, generates embedding vectors
using sentence-transformers/all-MiniLM-L6-v2, and outputs embeddings.json
with all original metadata preserved.

No LLM calls. No Supabase writes. No data modification.
"""

import json
import sys
import time
from pathlib import Path

try:
    from sentence_transformers import SentenceTransformer
except ImportError:
    print("ERROR: sentence-transformers is not installed.")
    print("Run:  pip install sentence-transformers")
    sys.exit(1)


# ──────────────────────────────────────────────────────────────────────
# Configuration
# ──────────────────────────────────────────────────────────────────────

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
INPUT_FILE = "chunks.json"
OUTPUT_FILE = "embeddings.json"
BATCH_SIZE = 32  # encode in batches for efficiency


def main():
    script_dir = Path(__file__).resolve().parent
    input_path = script_dir / INPUT_FILE
    output_path = script_dir / OUTPUT_FILE

    print("=" * 70)
    print("MediTrace RAG Pipeline -- Stage 2: Embedding Generation")
    print("=" * 70)
    print()

    # ── 1. Load chunks ──
    if not input_path.exists():
        print(f"ERROR: Input file not found: {input_path}")
        sys.exit(1)

    with open(input_path, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    total_chunks = len(chunks)
    print(f"Loaded {total_chunks} chunks from {INPUT_FILE}")
    print()

    # ── 2. Load model ──
    print(f"Loading model: {MODEL_NAME}")
    print("  (first run will download the model; subsequent runs use cache)")
    t0 = time.time()
    model = SentenceTransformer(MODEL_NAME)
    load_time = time.time() - t0
    print(f"  Model loaded in {load_time:.1f}s")
    print(f"  Embedding dimension: {model.get_sentence_embedding_dimension()}")
    print()

    # ── 3. Extract chunk texts ──
    texts = [chunk["chunk_text"] for chunk in chunks]

    # Validate all texts are non-empty strings
    empty_indices = [i for i, t in enumerate(texts) if not t or not t.strip()]
    if empty_indices:
        print(f"WARNING: {len(empty_indices)} chunks have empty text at indices: {empty_indices}")
    else:
        print(f"All {total_chunks} chunks have non-empty text")

    # ── 4. Generate embeddings ──
    print()
    print(f"Generating embeddings (batch_size={BATCH_SIZE})...")
    t0 = time.time()
    embeddings = model.encode(
        texts,
        batch_size=BATCH_SIZE,
        show_progress_bar=True,
        normalize_embeddings=True,  # L2-normalize for cosine similarity
    )
    embed_time = time.time() - t0
    print(f"  Embeddings generated in {embed_time:.1f}s")
    print(f"  Shape: {embeddings.shape}")
    print()

    # ── 5. Validate dimensions ──
    expected_dim = model.get_sentence_embedding_dimension()
    actual_dim = embeddings.shape[1]
    if actual_dim != expected_dim:
        print(f"ERROR: Dimension mismatch! Expected {expected_dim}, got {actual_dim}")
        sys.exit(1)

    actual_count = embeddings.shape[0]
    if actual_count != total_chunks:
        print(f"ERROR: Count mismatch! Expected {total_chunks} embeddings, got {actual_count}")
        sys.exit(1)

    # ── 6. Build output records ──
    output_records = []
    failures = 0

    for i, chunk in enumerate(chunks):
        try:
            record = {
                "chunk_id": chunk["chunk_id"],
                "patient_id": chunk["patient_id"],
                "patient_name": chunk["patient_name"],
                "document_id": chunk["document_id"],
                "document_type": chunk["document_type"],
                "document_date": chunk["document_date"],
                "section": chunk["section"],
                "source": chunk["source"],
                "chunk_text": chunk["chunk_text"],
                "embedding": embeddings[i].tolist(),
            }
            output_records.append(record)
        except Exception as e:
            failures += 1
            print(f"  FAILURE at chunk {i} ({chunk.get('chunk_id', '?')}): {e}")

    # ── 7. Write output ──
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output_records, f, ensure_ascii=False)

    output_size_mb = output_path.stat().st_size / (1024 * 1024)

    # ── 8. Summary ──
    print("=" * 70)
    print("STAGE 2 SUMMARY")
    print("=" * 70)
    print(f"Model:                  {MODEL_NAME}")
    print(f"Embedding dimension:    {expected_dim}")
    print(f"Normalization:          L2 (unit vectors for cosine similarity)")
    print(f"Chunks processed:       {total_chunks}")
    print(f"Embeddings generated:   {len(output_records)}")
    print(f"Failures:               {failures}")
    print(f"Output file:            {output_path}")
    print(f"Output file size:       {output_size_mb:.2f} MB")
    print(f"Model load time:        {load_time:.1f}s")
    print(f"Embedding time:         {embed_time:.1f}s")
    print()

    # Verify 1:1 mapping
    if len(output_records) == total_chunks and failures == 0:
        print("VALIDATION: Every chunk received exactly one embedding. [OK]")
    else:
        print(f"VALIDATION: FAILED -- {total_chunks - len(output_records)} chunks missing embeddings")

    # Show per-patient breakdown
    print()
    print("Embeddings by patient:")
    patient_counts: dict[str, int] = {}
    for rec in output_records:
        name = rec["patient_name"]
        patient_counts[name] = patient_counts.get(name, 0) + 1
    for name in [
        "Aarav Mehta", "Ishita Kapoor", "Nikhil Varma",
        "Diya Srinivasan", "Kabir Malhotra", "Tanya Bose"
    ]:
        count = patient_counts.get(name, 0)
        print(f"  {name:<20s} {count:>3d}")

    # Spot-check: show first 5 values of first and last embedding
    print()
    print("Spot-check (first 5 values):")
    first = output_records[0]
    last = output_records[-1]
    print(f"  First chunk ({first['source']}, {first['section'][:30]}):")
    print(f"    {first['embedding'][:5]}")
    print(f"  Last  chunk ({last['source']}, {last['section'][:30]}):")
    print(f"    {last['embedding'][:5]}")
    print()
    print("Stage 2 complete. Embeddings saved locally. No Supabase modifications.")


if __name__ == "__main__":
    main()
