"""
MediTrace RAG Pipeline — Stage 1: Document Processing & Clinical Chunking

Reads the 15-document TXT corpus, performs text cleaning, clinical
section-aware chunking, metadata extraction, and outputs chunks.json.

No embeddings. No LLM calls. No data modification.
"""

import json
import os
import re
import uuid
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Optional


# ──────────────────────────────────────────────────────────────────────
# 1. CORPUS DEFINITION — only the 15 RAG-designated documents
# ──────────────────────────────────────────────────────────────────────

RAG_CORPUS_FILES = [
    # Aarav Mehta
    "aarav_orthopedic_consultation.txt",
    "aarav_femur_xray.txt",
    "aarav_discharge_summary.txt",
    # Ishita Kapoor
    "ishita_diabetes_followup.txt",
    "ishita_chronic_followup.txt",
    # Nikhil Varma
    "nikhil_cardiac_emergency.txt",
    "nikhil_angioplasty_discharge.txt",
    "nikhil_cardiology_followup.txt",
    # Diya Srinivasan
    "diya_oncology_report.txt",
    "diya_chemotherapy_record.txt",
    "diya_surgical_discharge.txt",
    # Kabir Malhotra
    "kabir_allergy_assessment.txt",
    "kabir_medication_history.txt",
    # Tanya Bose
    "tanya_preoperative_assessment.txt",
    "tanya_postoperative_followup.txt",
]

# ──────────────────────────────────────────────────────────────────────
# 2. METADATA LOOKUP — authoritative mapping from Supabase
# ──────────────────────────────────────────────────────────────────────

DOCUMENT_METADATA = {
    "aarav_orthopedic_consultation.txt": {
        "document_id": "60000000-0000-0000-0000-000000000001",
        "patient_id": "20000000-0000-0000-0000-000000000001",
        "patient_name": "Aarav Mehta",
        "document_type": "CONSULTATION",
        "document_date": "2023-06-14",
    },
    "aarav_femur_xray.txt": {
        "document_id": "60000000-0000-0000-0000-000000000002",
        "patient_id": "20000000-0000-0000-0000-000000000001",
        "patient_name": "Aarav Mehta",
        "document_type": "IMAGING",
        "document_date": "2023-06-20",
    },
    "aarav_discharge_summary.txt": {
        "document_id": "60000000-0000-0000-0000-000000000003",
        "patient_id": "20000000-0000-0000-0000-000000000001",
        "patient_name": "Aarav Mehta",
        "document_type": "DISCHARGE_SUMMARY",
        "document_date": "2023-06-22",
    },
    "ishita_diabetes_followup.txt": {
        "document_id": "60000000-0000-0000-0000-000000000004",
        "patient_id": "20000000-0000-0000-0000-000000000002",
        "patient_name": "Ishita Kapoor",
        "document_type": "FOLLOWUP",
        "document_date": "2023-08-01",
    },
    "ishita_chronic_followup.txt": {
        "document_id": "60000000-0000-0000-0000-000000000006",
        "patient_id": "20000000-0000-0000-0000-000000000002",
        "patient_name": "Ishita Kapoor",
        "document_type": "FOLLOWUP",
        "document_date": "2026-09-12",
    },
    "nikhil_cardiac_emergency.txt": {
        "document_id": "60000000-0000-0000-0000-000000000007",
        "patient_id": "20000000-0000-0000-0000-000000000003",
        "patient_name": "Nikhil Varma",
        "document_type": "EMERGENCY_REPORT",
        "document_date": "2023-08-21",
    },
    "nikhil_angioplasty_discharge.txt": {
        "document_id": "60000000-0000-0000-0000-000000000008",
        "patient_id": "20000000-0000-0000-0000-000000000003",
        "patient_name": "Nikhil Varma",
        "document_type": "DISCHARGE_SUMMARY",
        "document_date": "2023-08-24",
    },
    "nikhil_cardiology_followup.txt": {
        "document_id": "60000000-0000-0000-0000-000000000009",
        "patient_id": "20000000-0000-0000-0000-000000000003",
        "patient_name": "Nikhil Varma",
        "document_type": "FOLLOWUP",
        "document_date": "2026-09-10",
    },
    "diya_oncology_report.txt": {
        "document_id": "60000000-0000-0000-0000-000000000010",
        "patient_id": "20000000-0000-0000-0000-000000000004",
        "patient_name": "Diya Srinivasan",
        "document_type": "ONCOLOGY_REPORT",
        "document_date": "2022-05-11",
    },
    "diya_chemotherapy_record.txt": {
        "document_id": "60000000-0000-0000-0000-000000000011",
        "patient_id": "20000000-0000-0000-0000-000000000004",
        "patient_name": "Diya Srinivasan",
        "document_type": "CHEMOTHERAPY_RECORD",
        "document_date": "2022-06-01",
    },
    "diya_surgical_discharge.txt": {
        "document_id": "60000000-0000-0000-0000-000000000012",
        "patient_id": "20000000-0000-0000-0000-000000000004",
        "patient_name": "Diya Srinivasan",
        "document_type": "SURGICAL_DISCHARGE",
        "document_date": "2023-03-18",
    },
    "kabir_allergy_assessment.txt": {
        "document_id": "60000000-0000-0000-0000-000000000013",
        "patient_id": "20000000-0000-0000-0000-000000000005",
        "patient_name": "Kabir Malhotra",
        "document_type": "ALLERGY_ASSESSMENT",
        "document_date": "2019-06-20",
    },
    "kabir_medication_history.txt": {
        "document_id": "60000000-0000-0000-0000-000000000015",
        "patient_id": "20000000-0000-0000-0000-000000000005",
        "patient_name": "Kabir Malhotra",
        "document_type": "MEDICATION_HISTORY",
        "document_date": "2024-01-18",
    },
    "tanya_preoperative_assessment.txt": {
        "document_id": "60000000-0000-0000-0000-000000000018",
        "patient_id": "20000000-0000-0000-0000-000000000006",
        "patient_name": "Tanya Bose",
        "document_type": "PREOPERATIVE_ASSESSMENT",
        "document_date": "2025-09-05",
    },
    "tanya_postoperative_followup.txt": {
        "document_id": "60000000-0000-0000-0000-000000000017",
        "patient_id": "20000000-0000-0000-0000-000000000006",
        "patient_name": "Tanya Bose",
        "document_type": "POSTOPERATIVE_FOLLOWUP",
        "document_date": "2025-10-12",
    },
}


# ──────────────────────────────────────────────────────────────────────
# 3. TEXT CLEANING
# ──────────────────────────────────────────────────────────────────────

# Patterns that are structural chrome, not clinical content
SEPARATOR_RE = re.compile(r"^[=\-]{6,}\s*$")
PAGE_FOOTER_RE = re.compile(
    r"^Page\s+\d+\s+of\s+\d+\s*$", re.IGNORECASE
)
HOSPITAL_FOOTER_RE = re.compile(
    r"^(Meridian Care|Nova Health|Apex Clinical|Lakeside Medical)\b.*$",
    re.IGNORECASE,
)
HOSPITAL_MOTTO_RE = re.compile(
    r'^".*"$|^.*["""].*["""].*$'  # quoted motto lines
)


def is_noise_line(line: str) -> bool:
    """Return True if the line is structural noise (separators, footers)."""
    stripped = line.strip()
    if not stripped:
        return False  # blank lines are kept as paragraph separators
    if SEPARATOR_RE.match(stripped):
        return True
    if PAGE_FOOTER_RE.match(stripped):
        return True
    if HOSPITAL_FOOTER_RE.match(stripped):
        return True
    return False


def clean_text(raw: str) -> str:
    """Strip structural chrome while preserving all clinical content."""
    lines = raw.splitlines()
    cleaned = []
    for line in lines:
        if is_noise_line(line):
            continue
        cleaned.append(line.rstrip())
    # collapse 3+ consecutive blank lines into 2
    text = "\n".join(cleaned)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


# ──────────────────────────────────────────────────────────────────────
# 4. SECTION-AWARE CHUNKING
# ──────────────────────────────────────────────────────────────────────

# Recognised section headers (ALL CAPS, possibly with trailing colon)
SECTION_HEADER_RE = re.compile(
    r"^([A-Z][A-Z &/\-]{2,}[A-Z):])(?:\s*$|:\s*$)"
)

# Sub-section headers inside a parent section (mixed case with trailing colon)
SUBSECTION_HEADER_RE = re.compile(
    r"^([A-Z][A-Za-z\s/\-()]+):\s*$"
)

# Recognised clinical section names for chunking boundaries
MAJOR_SECTION_KEYWORDS = {
    "PATIENT INFORMATION", "CLINICAL NOTES", "CLINICAL DOCUMENTATION",
    "CLINICAL DETAILS", "CLINICAL COURSE",
    "CHIEF COMPLAINT", "HISTORY OF PRESENT ILLNESS",
    "PAST MEDICAL HISTORY", "FAMILY HISTORY", "PERSONAL HISTORY",
    "ALLERGIES", "MEDICATION HISTORY",
    "PRESENTATION", "DIAGNOSTIC FINDINGS",
    "EXAMINATION", "OBJECTIVE / EXAMINATION",
    "ASSESSMENT", "ASSESSMENT & MANAGEMENT", "ASSESSMENT & PLAN",
    "PLAN", "DISCHARGE PLAN", "LONG-TERM PLAN",
    "HOSPITAL COURSE", "ADMISSION DETAILS",
    "PROCEDURE DETAILS", "OPERATIVE DETAILS",
    "FINDINGS", "IMPRESSION",
    "CURRENT MEDICATIONS", "DISCHARGE MEDICATIONS",
    "FOLLOW-UP", "RECOMMENDATIONS",
    "SIGNATURE", "DOCUMENT METADATA",
    "PREOPERATIVE ASSESSMENT", "POSTOPERATIVE FOLLOW-UP CLINIC NOTE",
    "CHEMOTHERAPY ADMINISTRATION TABLE",
    "SUPPORTIVE MEDICATIONS", "ADVERSE EFFECTS MONITORING PLAN",
    "NEXT CYCLE",
    "ALLERGY ASSESSMENT REPORT", "ALLERGY DETERMINATION TABLE",
    "CONFIRMED ALLERGY TABLE", "POSSIBLE/UNCONFIRMED ALLERGY-RELATED FINDING",
    "MEDICATION-RELATED ALERTS",
    "TREATMENT PROTOCOL", "PRE-TREATMENT ASSESSMENT",
    "NEOADJUVANT RESPONSE",
    "NEUROLOGICAL EXAMINATION", "NEUROLOGICAL HISTORY",
}

# These sections should be EXCLUDED from chunks (non-clinical metadata)
SKIP_SECTIONS = {
    "SIGNATURE",
    "DOCUMENT METADATA",
}

# Maximum chunk size in characters (soft limit — only split further if
# a single section exceeds this)
MAX_CHUNK_CHARS = 2000

# Minimum chunk size — merge tiny sections with the previous chunk
MIN_CHUNK_CHARS = 80


def detect_sections(text: str) -> list[dict]:
    """
    Parse cleaned text into a list of {header, content} dicts.

    Uses a two-pass approach:
    1. Find major section boundaries (ALL CAPS header lines, or lines
       matching known clinical header patterns).
    2. Within each major section, keep inline sub-sections together.
    """
    lines = text.splitlines()
    sections: list[dict] = []
    current_header = "HEADER"
    current_lines: list[str] = []

    for line in lines:
        stripped = line.strip()
        if not stripped:
            current_lines.append("")
            continue

        # Check if this line is a major section header
        is_major = False

        # Pattern 1: ALL CAPS header (the common pattern in these docs)
        if SECTION_HEADER_RE.match(stripped):
            candidate = stripped.rstrip(":").strip()
            if candidate in MAJOR_SECTION_KEYWORDS or len(candidate) > 3:
                is_major = True

        # Pattern 2: Known header text that might not match the regex perfectly
        for kw in MAJOR_SECTION_KEYWORDS:
            if stripped.upper().startswith(kw) and len(stripped) <= len(kw) + 5:
                is_major = True
                break

        if is_major:
            # Save the previous section
            if current_lines:
                sections.append({
                    "header": current_header,
                    "content": "\n".join(current_lines).strip(),
                })
            current_header = stripped.rstrip(":").strip()
            current_lines = []
        else:
            current_lines.append(line)

    # Save the last section
    if current_lines:
        sections.append({
            "header": current_header,
            "content": "\n".join(current_lines).strip(),
        })

    return sections


def merge_related_sections(sections: list[dict]) -> list[dict]:
    """
    Merge small sections into their neighbours to keep clinical context
    together, and combine tightly related pairs (e.g., Assessment + Plan).

    Special rules:
    - HEADER chunks (hospital name/location) are always merged forward.
    - PATIENT INFORMATION is merged forward into the first clinical section.
    - Signature / Document Metadata sections are dropped entirely.
    - Sections below MIN_CHUNK_CHARS are merged with their predecessor.
    """
    if not sections:
        return sections

    # Phase 1: filter out sections to skip and empty sections
    filtered: list[dict] = []
    for sec in sections:
        content = sec["content"].strip()
        header = sec["header"]
        if not content:
            continue
        if header in SKIP_SECTIONS:
            continue
        filtered.append({"header": header, "content": content})

    if not filtered:
        return filtered

    # Phase 2: merge HEADER and PATIENT INFORMATION into the next
    # substantive clinical section (they provide context but should
    # not be standalone retrieval chunks)
    ABSORB_FORWARD = {"HEADER"}
    merged: list[dict] = []
    pending_prefix: list[tuple[str, str]] = []  # (header, content) pairs

    for sec in filtered:
        header = sec["header"]
        content = sec["content"]

        if header in ABSORB_FORWARD:
            pending_prefix.append((header, content))
            continue

        # If we have accumulated prefix sections, prepend them
        if pending_prefix:
            prefix_text = "\n\n".join(
                f"{h}:\n{c}" for h, c in pending_prefix
            )
            content = f"{prefix_text}\n\n{content}"
            pending_prefix = []

        merged.append({"header": header, "content": content})

    # Flush any remaining pending prefix
    if pending_prefix and merged:
        prefix_text = "\n\n".join(
            f"{h}:\n{c}" for h, c in pending_prefix
        )
        merged[-1]["content"] += f"\n\n{prefix_text}"
    elif pending_prefix:
        for h, c in pending_prefix:
            merged.append({"header": h, "content": c})

    # Phase 3: merge tiny sections (< MIN_CHUNK_CHARS) with predecessor
    final: list[dict] = []
    for sec in merged:
        content = sec["content"]
        header = sec["header"]

        if final and len(content) < MIN_CHUNK_CHARS:
            prev = final[-1]
            prev["content"] += f"\n\n{header}:\n{content}"
            prev["header"] += f" + {header}"
            continue

        final.append({"header": header, "content": content})

    return final


def split_oversized_section(header: str, content: str) -> list[dict]:
    """
    If a single section exceeds MAX_CHUNK_CHARS, split at paragraph
    boundaries. Tables are never split.
    """
    if len(content) <= MAX_CHUNK_CHARS:
        return [{"header": header, "content": content}]

    # Split on double newlines (paragraph boundaries)
    paragraphs = re.split(r"\n\n+", content)
    chunks = []
    current_parts: list[str] = []
    current_len = 0

    for para in paragraphs:
        para_len = len(para)

        # If adding this paragraph would exceed the limit, flush
        if current_parts and current_len + para_len > MAX_CHUNK_CHARS:
            chunks.append({
                "header": header,
                "content": "\n\n".join(current_parts),
            })
            current_parts = []
            current_len = 0

        current_parts.append(para)
        current_len += para_len

    # Flush remaining
    if current_parts:
        chunks.append({
            "header": header,
            "content": "\n\n".join(current_parts),
        })

    # Label split chunks with part numbers
    if len(chunks) > 1:
        for i, chunk in enumerate(chunks):
            chunk["header"] = f"{header} (Part {i + 1}/{len(chunks)})"

    return chunks


def generate_chunk_id(doc_id: str, section: str, content: str) -> str:
    """Deterministic chunk ID from document ID + section + content hash."""
    content_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()[:12]
    section_slug = re.sub(r"[^a-z0-9]+", "-", section.lower()).strip("-")[:40]
    return f"{doc_id}__{section_slug}__{content_hash}"


# ──────────────────────────────────────────────────────────────────────
# 5. MAIN PROCESSING PIPELINE
# ──────────────────────────────────────────────────────────────────────

def process_document(filepath: Path, filename: str) -> list[dict]:
    """
    Process a single TXT document:
      1. Read raw text
      2. Clean structural noise
      3. Detect clinical sections
      4. Merge small sections
      5. Split oversized sections
      6. Attach metadata to each chunk
    """
    raw = filepath.read_text(encoding="utf-8")
    cleaned = clean_text(raw)
    sections = detect_sections(cleaned)
    sections = merge_related_sections(sections)

    meta = DOCUMENT_METADATA[filename]
    chunks = []

    for sec in sections:
        sub_chunks = split_oversized_section(sec["header"], sec["content"])
        for sc in sub_chunks:
            chunk_id = generate_chunk_id(
                meta["document_id"], sc["header"], sc["content"]
            )
            chunks.append({
                "chunk_id": chunk_id,
                "patient_id": meta["patient_id"],
                "patient_name": meta["patient_name"],
                "document_id": meta["document_id"],
                "document_type": meta["document_type"],
                "document_date": meta["document_date"],
                "section": sc["header"],
                "source": filename,
                "chunk_text": sc["content"],
            })

    return chunks


def main():
    # Resolve paths
    script_dir = Path(__file__).resolve().parent
    docs_dir = script_dir.parent / "documents"
    output_path = script_dir / "chunks.json"

    if not docs_dir.exists():
        print(f"ERROR: Documents directory not found: {docs_dir}")
        return

    all_chunks: list[dict] = []
    doc_count = 0
    patient_chunks: dict[str, int] = {}
    doc_chunks: dict[str, int] = {}

    print("=" * 70)
    print("MediTrace RAG Pipeline -- Stage 1: Clinical Chunking")
    print("=" * 70)
    print()

    for filename in RAG_CORPUS_FILES:
        filepath = docs_dir / filename
        if not filepath.exists():
            print(f"WARNING: File not found, skipping: {filename}")
            continue

        chunks = process_document(filepath, filename)
        all_chunks.extend(chunks)
        doc_count += 1

        # Track counts
        patient_name = DOCUMENT_METADATA[filename]["patient_name"]
        patient_chunks[patient_name] = patient_chunks.get(patient_name, 0) + len(chunks)
        doc_chunks[filename] = len(chunks)

        print(f"  [OK] {filename:<45s} -> {len(chunks):>2d} chunks")

    print()

    # Write output
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, indent=2, ensure_ascii=False)

    print(f"Output written to: {output_path}")
    print()

    # ── Summary ──
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Total documents processed: {doc_count}")
    print(f"Total chunks generated:    {len(all_chunks)}")
    print()

    print("Chunks by patient:")
    for name in [
        "Aarav Mehta", "Ishita Kapoor", "Nikhil Varma",
        "Diya Srinivasan", "Kabir Malhotra", "Tanya Bose"
    ]:
        count = patient_chunks.get(name, 0)
        print(f"  {name:<20s} {count:>3d}")
    print()

    print("Chunks by document:")
    for filename in RAG_CORPUS_FILES:
        count = doc_chunks.get(filename, 0)
        print(f"  {filename:<45s} {count:>3d}")
    print()

    # ── Representative chunks ──
    print("=" * 70)
    print("REPRESENTATIVE CHUNKS")
    print("=" * 70)

    # Find one representative chunk per requested patient
    representatives = {
        "Aarav Mehta": None,
        "Nikhil Varma": None,
        "Kabir Malhotra": None,
    }
    # Preferred sections to show
    preferred = {
        "Aarav Mehta": "HOSPITAL COURSE",
        "Nikhil Varma": "PROCEDURE DETAILS",
        "Kabir Malhotra": "CONFIRMED ALLERGY TABLE",
    }
    for chunk in all_chunks:
        name = chunk["patient_name"]
        if name in representatives and representatives[name] is None:
            pref = preferred.get(name, "")
            if pref.lower() in chunk["section"].lower():
                representatives[name] = chunk
    # Fallback: pick any chunk with clinical content
    for chunk in all_chunks:
        name = chunk["patient_name"]
        if name in representatives and representatives[name] is None:
            if chunk["section"] not in ("HEADER", "PATIENT INFORMATION"):
                representatives[name] = chunk

    for i, (name, chunk) in enumerate(representatives.items(), 1):
        if chunk is None:
            continue
        print(f"\n{'-' * 70}")
        print(f"Representative Chunk {i} -- {name}")
        print(f"{'-' * 70}")
        print(f"  chunk_id:      {chunk['chunk_id'][:60]}...")
        print(f"  document_id:   {chunk['document_id']}")
        print(f"  document_type: {chunk['document_type']}")
        print(f"  document_date: {chunk['document_date']}")
        print(f"  section:       {chunk['section']}")
        print(f"  source:        {chunk['source']}")
        print(f"  chunk_text:")
        # Show first 400 chars
        preview = chunk["chunk_text"][:400]
        for line in preview.splitlines():
            print(f"    {line}")
        if len(chunk["chunk_text"]) > 400:
            print(f"    ... [{len(chunk['chunk_text'])} chars total]")
        print()


if __name__ == "__main__":
    main()
