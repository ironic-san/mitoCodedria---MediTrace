"""Quick inspection of chunks.json quality."""
import json

with open("chunks.json", encoding="utf-8") as f:
    chunks = json.load(f)

sizes = [len(c["chunk_text"]) for c in chunks]
print(f"Chunk size range: {min(sizes)} - {max(sizes)} chars")
print(f"Average chunk size: {sum(sizes) // len(sizes)} chars")
print(f"Median chunk size: {sorted(sizes)[len(sizes) // 2]} chars")
print()

# 5 smallest
print("=== 5 SMALLEST CHUNKS ===")
by_size = sorted(chunks, key=lambda c: len(c["chunk_text"]))
for c in by_size[:5]:
    sec = c["section"]
    src = c["source"]
    sz = len(c["chunk_text"])
    print(f"  [{sz:>4d} chars] {src:<40s} | {sec}")
    preview = c["chunk_text"][:120].replace("\n", " ")
    print(f"    {preview}")
    print()

# Nikhil angioplasty sections
print("=== NIKHIL ANGIOPLASTY DISCHARGE SECTIONS ===")
for c in chunks:
    if c["source"] == "nikhil_angioplasty_discharge.txt":
        sz = len(c["chunk_text"])
        print(f"  [{sz:>4d} chars] {c['section']}")
print()

# Kabir medication history sections
print("=== KABIR MEDICATION HISTORY SECTIONS ===")
for c in chunks:
    if c["source"] == "kabir_medication_history.txt":
        sz = len(c["chunk_text"])
        print(f"  [{sz:>4d} chars] {c['section']}")
print()

# Ishita diabetes followup sections
print("=== ISHITA DIABETES FOLLOWUP SECTIONS ===")
for c in chunks:
    if c["source"] == "ishita_diabetes_followup.txt":
        sz = len(c["chunk_text"])
        print(f"  [{sz:>4d} chars] {c['section']}")
print()

# Check Kabir allergy table is intact
print("=== KABIR CONFIRMED ALLERGY TABLE CHUNK ===")
for c in chunks:
    if "CONFIRMED ALLERGY TABLE" in c["section"]:
        print(c["chunk_text"])
        print()

# Check Ishita medication table is intact
print("=== ISHITA CURRENT MEDICATIONS CHUNK ===")
for c in chunks:
    if c["source"] == "ishita_diabetes_followup.txt" and "MEDICATION" in c["section"].upper():
        print(c["chunk_text"])
        print()

# All unique sections across all documents
print("=== ALL UNIQUE SECTION NAMES ===")
section_names = sorted(set(c["section"] for c in chunks))
for s in section_names:
    count = sum(1 for c in chunks if c["section"] == s)
    print(f"  {count:>2d}x  {s}")
