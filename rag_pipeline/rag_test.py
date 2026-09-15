import json
import re
import numpy as np
from sentence_transformers import SentenceTransformer


# ============================================================
# CONFIGURATION
# ============================================================

EMBEDDINGS_FILE = "embeddings.json"
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

TOP_K = 5


# ============================================================
# PATIENT ALIASES
# ============================================================

PATIENT_ALIASES = {
    "aarav": "Aarav Mehta",
    "aarav mehta": "Aarav Mehta",

    "ishita": "Ishita Kapoor",
    "ishita kapoor": "Ishita Kapoor",

    "nikhil": "Nikhil Varma",
    "nikhil varma": "Nikhil Varma",

    "diya": "Diya Srinivasan",
    "diya srinivasan": "Diya Srinivasan",

    "kabir": "Kabir Malhotra",
    "kabir malhotra": "Kabir Malhotra",

    "tanya": "Tanya Bose",
    "tanya bose": "Tanya Bose",
}


# ============================================================
# SECTIONS THAT ARE NOT USEFUL FOR RAG
# ============================================================

EXCLUDED_SECTIONS = {
    "HEADER",
    "DOCUMENT HEADER",
    "ADMINISTRATIVE",
    "SIGNATURE",
}


# ============================================================
# CLINICAL INTENT / SECTION KEYWORDS
# ============================================================

INTENT_SECTIONS = {
    "procedure": [
        "procedure",
        "surgery",
        "operation",
        "pci",
        "angioplasty",
        "stent",
        "craniotomy",
        "biopsy",
        "chemotherapy",
        "treatment",
    ],

    "medication": [
        "medication",
        "medicine",
        "drug",
        "tablet",
        "dose",
        "prescribed",
        "current medications",
        "medications",
    ],

    "allergy": [
        "allergy",
        "allergic",
        "anaphylaxis",
        "reaction",
        "penicillin",
        "amoxicillin",
    ],

    "diagnosis": [
        "diagnosis",
        "diagnosed",
        "condition",
        "disease",
        "infarction",
        "stemI",
        "tumor",
        "astrocytoma",
        "diabetes",
        "cancer",
    ],

    "symptoms": [
        "symptom",
        "symptoms",
        "pain",
        "chest pain",
        "headache",
        "seizure",
        "swelling",
        "fever",
    ],

    "investigation": [
        "investigation",
        "test",
        "lab",
        "laboratory",
        "mri",
        "ct",
        "x-ray",
        "ecg",
        "troponin",
        "blood work",
        "imaging",
    ],

    "followup": [
        "follow-up",
        "followup",
        "review",
        "monitoring",
        "next appointment",
        "repeat mri",
        "follow up",
    ],
}


# ============================================================
# COMMON NON-INFORMATION WORDS
# ============================================================

STOPWORDS = {
    "what",
    "when",
    "where",
    "which",
    "who",
    "why",
    "how",
    "does",
    "did",
    "do",
    "is",
    "are",
    "was",
    "were",
    "has",
    "have",
    "had",
    "can",
    "could",
    "would",
    "should",
    "the",
    "a",
    "an",
    "of",
    "to",
    "for",
    "in",
    "on",
    "with",
    "and",
    "or",
    "about",
    "from",
    "patient",
    "patients",
}


# ============================================================
# LOAD EMBEDDINGS
# ============================================================

print("\nLoading embeddings...")

with open(EMBEDDINGS_FILE, "r", encoding="utf-8") as f:
    records = json.load(f)

print(f"Loaded {len(records)} chunks.")

print("Loading embedding model...")
model = SentenceTransformer(MODEL_NAME)
print("Model loaded.")


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def get_text(record):
    """
    Safely retrieve chunk text.
    """
    return str(record.get("chunk_text", "")).strip()


def get_section(record):
    """
    Safely retrieve section.
    """
    return str(record.get("section", "")).strip()


def get_patient(record):
    """
    Safely retrieve patient name.
    """
    return str(record.get("patient_name", record.get("patient", ""))).strip()


def is_clinical_chunk(record):
    """
    Remove administrative/header-only chunks.
    """

    section = get_section(record).upper()
    text = get_text(record)

    if not text:
        return False

    if section in EXCLUDED_SECTIONS:
        return False

    if text.upper().startswith("HEADER:"):
        return False

    # Remove chunks that are mostly document metadata
    header_markers = [
        "DOCUMENT TITLE:",
        "DOCUMENT ID:",
        "DATE OF DOCUMENT:",
    ]

    marker_count = sum(
        marker in text.upper()
        for marker in header_markers
    )

    if marker_count >= 2:
        return False

    # Ignore signature-only chunks
    if "SIGNATURE:" in text.upper():
        clinical_words = [
            "diagnosis",
            "procedure",
            "treatment",
            "medication",
            "finding",
            "history",
            "assessment",
            "plan",
            "symptom",
            "investigation",
            "imaging",
        ]

        if not any(word in text.lower() for word in clinical_words):
            return False

    return True


def detect_patient(question):
    """
    Detect patient from the question.
    """

    q = question.lower()

    # Try longest names first
    aliases = sorted(
        PATIENT_ALIASES.items(),
        key=lambda x: len(x[0]),
        reverse=True
    )

    for alias, patient_name in aliases:
        if re.search(r"\b" + re.escape(alias) + r"\b", q):
            return patient_name

    return None


def tokenize(text):
    """
    Extract meaningful words from text.
    """

    words = re.findall(r"\b[a-zA-Z0-9]+\b", text.lower())

    return {
        word
        for word in words
        if word not in STOPWORDS and len(word) >= 3
    }


def keyword_score(question, chunk_text):
    """
    Calculate keyword overlap between question and chunk.

    Returns value between 0 and 1.
    """

    query_words = tokenize(question)
    chunk_words = tokenize(chunk_text)

    if not query_words:
        return 0.0

    overlap = query_words.intersection(chunk_words)

    return len(overlap) / len(query_words)


def section_score(question, section, chunk_text):
    """
    Determine whether the chunk's clinical section matches
    the intent of the question.

    Returns value between 0 and 1.
    """

    q = question.lower()
    section_lower = section.lower()
    text_lower = chunk_text.lower()

    scores = []

    for intent, keywords in INTENT_SECTIONS.items():

        query_matches = [
            keyword
            for keyword in keywords
            if keyword in q
        ]

        if not query_matches:
            continue

        section_matches = [
            keyword
            for keyword in keywords
            if keyword in section_lower
        ]

        text_matches = [
            keyword
            for keyword in keywords
            if keyword in text_lower
        ]

        if section_matches:
            scores.append(1.0)

        elif text_matches:
            scores.append(0.6)

    if not scores:
        return 0.0

    return max(scores)


def cosine_similarity(query_embedding, document_embedding):
    """
    Calculate cosine similarity.
    """

    query_norm = np.linalg.norm(query_embedding)
    doc_norm = np.linalg.norm(document_embedding)

    if query_norm == 0 or doc_norm == 0:
        return 0.0

    return float(
        np.dot(query_embedding, document_embedding)
        / (query_norm * doc_norm)
    )


# ============================================================
# RETRIEVAL
# ============================================================

def retrieve(question):

    # --------------------------------------------------------
    # Detect patient
    # --------------------------------------------------------

    detected_patient = detect_patient(question)

    # --------------------------------------------------------
    # Filter clinical chunks
    # --------------------------------------------------------

    clinical_records = [
        record
        for record in records
        if is_clinical_chunk(record)
    ]

    # --------------------------------------------------------
    # Patient filtering
    # --------------------------------------------------------

    if detected_patient:

        patient_records = [
            record
            for record in clinical_records
            if get_patient(record).lower() == detected_patient.lower()
        ]

        # Only use patient filtering if records were found
        if patient_records:
            clinical_records = patient_records

    # --------------------------------------------------------
    # Query embedding
    # --------------------------------------------------------

    query_embedding = model.encode(
        question,
        normalize_embeddings=True
    )

    # --------------------------------------------------------
    # Score every chunk
    # --------------------------------------------------------

    scored_results = []

    for record in clinical_records:

        embedding = record.get("embedding")

        if embedding is None:
            continue

        document_embedding = np.array(
            embedding,
            dtype=np.float32
        )

        semantic = cosine_similarity(
            query_embedding,
            document_embedding
        )

        keywords = keyword_score(
            question,
            get_text(record)
        )

        section = section_score(
            question,
            get_section(record),
            get_text(record)
        )

        # ----------------------------------------------------
        # Hybrid score
        #
        # 70% semantic
        # 15% keyword
        # 15% section relevance
        # ----------------------------------------------------

        hybrid = (
            0.70 * semantic
            + 0.15 * keywords
            + 0.15 * section
        )

        result = dict(record)

        result["semantic_score"] = semantic
        result["keyword_score"] = keywords
        result["section_score"] = section
        result["hybrid_score"] = hybrid

        scored_results.append(result)

    # --------------------------------------------------------
    # Sort by hybrid score
    # --------------------------------------------------------

    scored_results.sort(
        key=lambda x: x["hybrid_score"],
        reverse=True
    )

    return detected_patient, scored_results


# ============================================================
# NO-MATCH DECISION
# ============================================================

def is_relevant_question(question, results):

    if not results:
        return False

    best = results[0]

    semantic = best["semantic_score"]
    keyword = best["keyword_score"]
    section = best["section_score"]
    hybrid = best["hybrid_score"]

    # --------------------------------------------------------
    # Very weak semantic similarity with no supporting
    # keyword or section evidence = probably unrelated
    # --------------------------------------------------------

    if (
        semantic < 0.20
        and keyword == 0
        and section == 0
    ):
        return False

    # --------------------------------------------------------
    # If semantic similarity is weak but the question has
    # strong keyword/section evidence, allow it.
    #
    # This is important for questions such as:
    #
    # "Does Kabir have a confirmed Amoxicillin allergy?"
    # --------------------------------------------------------

    if keyword >= 0.25:
        return True

    if section >= 0.6:
        return True

    if hybrid >= 0.15:
        return True

    return False


# ============================================================
# DISPLAY RESULTS
# ============================================================

def display_results(
    question,
    detected_patient,
    results
):

    print("\n" + "=" * 70)
    print("QUESTION")
    print("=" * 70)

    print(question)

    print(
        f"\nDetected patient: "
        f"{detected_patient if detected_patient else 'None'}"
    )

    # --------------------------------------------------------
    # Check relevance
    # --------------------------------------------------------

    if not is_relevant_question(question, results):

        print("\n" + "-" * 70)
        print("NO RELEVANT MATCH FOUND")
        print("-" * 70)

        print(
            "\nThe question does not have sufficiently relevant "
            "evidence in the medical document corpus."
        )

        print(
            "\nTry asking something related to the patient's "
            "medical history."
        )

        return

    # --------------------------------------------------------
    # Display top results
    # --------------------------------------------------------

    print("\n" + "=" * 70)
    print("TOP 5 CLINICAL CHUNKS")
    print("=" * 70)

    for index, result in enumerate(
        results[:TOP_K],
        start=1
    ):

        print(
            f"\n--- Result {index} ---"
        )

        print(
            f"Hybrid score    : "
            f"{result['hybrid_score']:.4f}"
        )

        print(
            f"Semantic score  : "
            f"{result['semantic_score']:.4f}"
        )

        print(
            f"Keyword score   : "
            f"{result['keyword_score']:.4f}"
        )

        print(
            f"Section score   : "
            f"{result['section_score']:.4f}"
        )

        print(
            f"Patient         : "
            f"{get_patient(result)}"
        )

        print(
            f"Document type   : "
            f"{result.get('document_type', 'N/A')}"
        )

        print(
            f"Document date   : "
            f"{result.get('document_date', 'N/A')}"
        )

        print(
            f"Section         : "
            f"{get_section(result)}"
        )

        print(
            f"Source          : "
            f"{result.get('source', result.get('filename', 'N/A'))}"
        )

        print("\nChunk text:")

        print(get_text(result))


# ============================================================
# MAIN INTERACTIVE LOOP
# ============================================================

def main():

    print("\n" + "=" * 70)
    print("MEDITRACE - LOCAL RAG RETRIEVAL TEST")
    print("=" * 70)

    print(
        "\nType a medical question."
        "\nType 'exit' to stop."
    )

    while True:

        try:

            question = input(
                "\nQuestion > "
            ).strip()

        except KeyboardInterrupt:

            print("\n\nExiting...")
            break

        # ----------------------------------------------------
        # Exit
        # ----------------------------------------------------

        if question.lower() in {
            "exit",
            "quit",
            "q"
        }:

            print("\nExiting...")
            break

        # ----------------------------------------------------
        # Empty question
        # ----------------------------------------------------

        if not question:

            print(
                "\nPlease enter a question."
            )

            continue

        # ----------------------------------------------------
        # Very short input
        # ----------------------------------------------------

        if len(question) < 4:

            print(
                "\nNo sufficiently relevant medical "
                "information found."
            )

            print(
                "Please enter a meaningful medical question."
            )

            continue

        # ----------------------------------------------------
        # Retrieve
        # ----------------------------------------------------

        detected_patient, results = retrieve(
            question
        )

        # ----------------------------------------------------
        # Display
        # ----------------------------------------------------

        display_results(
            question,
            detected_patient,
            results
        )


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    main()