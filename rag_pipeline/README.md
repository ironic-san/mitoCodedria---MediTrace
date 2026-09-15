# MediTrace RAG Pipeline — Stage 1

## Overview

Stage 1 of the MediTrace RAG pipeline processes the 15-document synthetic
medical TXT corpus into structured, metadata-rich chunks suitable for
embedding and vector-similarity retrieval.

## Pipeline

```
TXT documents (15 files)
  → Text cleaning (remove separators, footers, structural chrome)
  → Clinical section-aware chunking
  → Metadata attachment (patient_id, document_id, section, etc.)
  → chunks.json
```

## Files

| File | Description |
|---|---|
| `process_documents.py` | Main processing script |
| `requirements.txt` | Dependencies (stdlib only) |
| `chunks.json` | Output — generated chunks with metadata |

## Usage

```bash
cd rag_pipeline
python process_documents.py
```

The script reads from `../documents/` and writes `chunks.json` to the
current directory.

## Chunking Strategy

The chunker does NOT blindly split on character count. Instead it:

1. **Cleans** structural noise (separator lines `===`/`---`, page footers,
   hospital footer text).
2. **Detects clinical sections** by recognizing ALL-CAPS headers that follow
   separator lines (e.g., `PATIENT INFORMATION`, `CHIEF COMPLAINT`,
   `ASSESSMENT & PLAN`, `CURRENT MEDICATIONS`).
3. **Merges tiny sections** (< 80 chars) with their predecessor to avoid
   fragmenting related clinical facts.
4. **Splits oversized sections** (> 2000 chars) only at paragraph boundaries,
   never inside tables.
5. **Preserves tables** — pipe-delimited tables and their headers are kept
   together in the same chunk.
6. **Skips non-clinical sections** (SIGNATURE, DOCUMENT METADATA) that add
   no retrieval value.

## Chunk Schema

```json
{
  "chunk_id": "deterministic-hash-based-id",
  "patient_id": "20000000-0000-0000-0000-000000000001",
  "patient_name": "Aarav Mehta",
  "document_id": "60000000-0000-0000-0000-000000000001",
  "document_type": "CONSULTATION",
  "document_date": "2023-06-14",
  "section": "CLINICAL NOTES",
  "source": "aarav_orthopedic_consultation.txt",
  "chunk_text": "..."
}
```

## Corpus (15 documents)

| Patient | Documents |
|---|---|
| Aarav Mehta | 3 (consultation, imaging, discharge) |
| Ishita Kapoor | 2 (diabetes follow-up, chronic follow-up) |
| Nikhil Varma | 3 (emergency, discharge, follow-up) |
| Diya Srinivasan | 3 (oncology, chemo, surgical discharge) |
| Kabir Malhotra | 2 (allergy assessment, medication history) |
| Tanya Bose | 2 (preoperative, postoperative) |

## What This Does NOT Do

- No pgvector storage (Stage 3)
- No Supabase modifications
- No LLM summarization
- No clinical-meaning normalization

---

## Stage 2: Embedding Generation

### Model

| Property | Value |
|---|---|
| Model | `sentence-transformers/all-MiniLM-L6-v2` |
| Dimension | 384 |
| Normalization | L2 (unit vectors for cosine similarity) |
| Input | `chunk_text` only |

### Usage

```bash
cd rag_pipeline
python generate_embeddings.py
```

Reads `chunks.json` and writes `embeddings.json`.

### Output Schema (embeddings.json)

```json
{
  "chunk_id": "...",
  "patient_id": "...",
  "patient_name": "...",
  "document_id": "...",
  "document_type": "...",
  "document_date": "...",
  "section": "...",
  "source": "...",
  "chunk_text": "...",
  "embedding": [0.0123, -0.0456, ...]
}
```

### Full Pipeline So Far

```
Stage 1: TXT documents -> clean -> chunk -> chunks.json (92 chunks)
Stage 2: chunks.json -> embed -> embeddings.json (92 x 384-dim vectors)
Stage 3: (pending) embeddings.json -> pgvector / Supabase
```
