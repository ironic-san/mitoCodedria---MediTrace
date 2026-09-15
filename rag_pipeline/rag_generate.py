import os
import json
import re
import time
from pathlib import Path

import numpy as np
import requests
from sentence_transformers import SentenceTransformer


# ============================================================
# MEDiTRACE RAG + GEMINI GENERATION
# ============================================================
#
# Pipeline:
#
# Medical TXT files
#       ↓
# Chunking
#       ↓
# Embeddings
#       ↓
# Patient filtering
#       ↓
# Hybrid retrieval
#       ↓
# Top 3 evidence
#       ↓
# Gemini 3.5 Flash-Lite
#       ↓
# Grounded answer
#
# NO SUPABASE WRITES
# ============================================================


# ============================================================
# CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

EMBEDDINGS_FILE = BASE_DIR / "embeddings.json"

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# FINAL GEMINI MODEL
LLM_MODEL = "gemini-3.5-flash-lite"

TOP_K = 3

# Gemini request settings
MAX_OUTPUT_TOKENS = 500
TEMPERATURE = 0.1

# Retry settings for temporary Gemini errors
MAX_RETRIES = 3
RETRY_DELAYS = [2, 5, 10]


# ============================================================
# PATIENT ALIASES
# ============================================================

PATIENT_ALIASES = {
    "aarav": "Aarav Mehta",
    "ishita": "Ishita Kapoor",
    "nikhil": "Nikhil Varma",
    "diya": "Diya Srinivasan",
    "kabir": "Kabir Malhotra",
    "tanya": "Tanya Bose",
}


# ============================================================
# EXCLUDED SECTIONS
# ============================================================

EXCLUDED_SECTIONS = {
    "HEADER",
    "DOCUMENT HEADER",
    "ADMINISTRATIVE",
    "ADMINISTRATIVE INFORMATION",
    "SIGNATURE",
}


# ============================================================
# CLINICAL INTENT → RELEVANT SECTIONS
# ============================================================

INTENT_SECTIONS = {

    "procedure": [
        "PROCEDURE",
        "PROCEDURE DETAILS",
        "SURGERY",
        "OPERATIVE",
        "INTERVENTION",
        "TREATMENT",
    ],

    "medication": [
        "MEDICATION",
        "MEDICATIONS",
        "MEDICATION HISTORY",
        "CURRENT MEDICATIONS",
        "DISCHARGE MEDICATIONS",
        "MEDICATION-RELATED ALERTS",
    ],

    "allergy": [
        "ALLERGY",
        "ALLERGIES",
        "CONFIRMED ALLERGY TABLE",
        "ALLERGY DETERMINATION TABLE",
        "POSSIBLE/UNCONFIRMED ALLERGY-RELATED FINDING",
        "MEDICATION-RELATED ALERTS",
    ],

    "diagnosis": [
        "DIAGNOSIS",
        "ASSESSMENT",
        "CLINICAL IMPRESSION",
        "IMPRESSION",
        "FINAL DIAGNOSIS",
    ],

    "symptoms": [
        "SYMPTOMS",
        "PRESENTING COMPLAINT",
        "CHIEF COMPLAINT",
        "HISTORY OF PRESENT ILLNESS",
    ],

    "investigation": [
        "LABORATORY",
        "LAB RESULTS",
        "IMAGING",
        "INVESTIGATION",
        "FINDINGS",
        "RADIOLOGY",
    ],

    "followup": [
        "FOLLOW-UP",
        "FOLLOWUP",
        "PLAN",
        "CLINICAL NOTES",
        "RECOMMENDATIONS",
    ],
}


# ============================================================
# STOPWORDS
# ============================================================

STOPWORDS = {
    "what",
    "what's",
    "which",
    "who",
    "when",
    "where",
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
    "in",
    "on",
    "for",
    "to",
    "from",
    "with",
    "and",
    "or",
    "patient",
    "medical",
    "record",
    "records",
    "history",
    "information",
    "document",
    "documents",
}


# ============================================================
# LOAD EMBEDDINGS
# ============================================================

print("\n" + "=" * 70)
print("MEDiTRACE - RAG + GEMINI GENERATION")
print("=" * 70)

print("\nLoading embeddings...")

if not EMBEDDINGS_FILE.exists():

    raise FileNotFoundError(
        f"\nembeddings.json was not found at:\n"
        f"{EMBEDDINGS_FILE}\n\n"
        f"Make sure you run Stage 2 first."
    )


with open(
    EMBEDDINGS_FILE,
    "r",
    encoding="utf-8"
) as f:

    records = json.load(f)


print(
    f"Loaded {len(records)} chunks."
)


# ============================================================
# LOAD EMBEDDING MODEL
# ============================================================

print("\nLoading embedding model...")

embedding_model = SentenceTransformer(
    EMBEDDING_MODEL
)

print(
    "Embedding model loaded."
)


# ============================================================
# GEMINI API KEY
# ============================================================

api_key = os.getenv(
    "GEMINI_API_KEY"
)

if not api_key:

    raise RuntimeError(
        "\nGEMINI_API_KEY is not set.\n\n"
        "Run this in PowerShell:\n\n"
        '$env:GEMINI_API_KEY="YOUR_ACTUAL_GEMINI_API_KEY"\n'
    )


print(
    "\nGemini API key loaded."
)

print(
    f"Gemini model: {LLM_MODEL}"
)


# ============================================================
# TEXT NORMALIZATION
# ============================================================

def normalize_text(text):

    if not text:

        return ""

    text = str(text).lower()

    text = re.sub(
        r"[^a-z0-9\s\-/]",
        " ",
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# ============================================================
# KEYWORDS
# ============================================================

def get_keywords(text):

    words = normalize_text(
        text
    ).split()

    return {
        word
        for word in words
        if word not in STOPWORDS
        and len(word) >= 2
    }


# ============================================================
# PATIENT DETECTION
# ============================================================

def detect_patient(query):

    query_lower = query.lower()

    for alias, full_name in PATIENT_ALIASES.items():

        if re.search(
            r"\b" + re.escape(alias) + r"\b",
            query_lower
        ):

            return full_name

    return None


# ============================================================
# INTENT DETECTION
# ============================================================

def detect_intent(query):

    q = query.lower()

    # Procedure
    if any(
        x in q
        for x in [
            "procedure",
            "surgery",
            "operation",
            "underwent",
            "performed",
            "stent",
            "angioplasty",
            "craniotomy",
        ]
    ):

        return "procedure"


    # Medication
    if any(
        x in q
        for x in [
            "medication",
            "medications",
            "medicine",
            "medicines",
            "drug",
            "drugs",
            "taking",
            "prescribed",
            "current meds",
        ]
    ):

        return "medication"


    # Allergy
    if any(
        x in q
        for x in [
            "allergy",
            "allergic",
            "allergies",
            "reaction",
            "anaphylaxis",
            "penicillin",
            "amoxicillin",
        ]
    ):

        return "allergy"


    # Diagnosis
    if any(
        x in q
        for x in [
            "diagnosis",
            "diagnosed",
            "condition",
            "disease",
        ]
    ):

        return "diagnosis"


    # Symptoms
    if any(
        x in q
        for x in [
            "symptom",
            "symptoms",
            "complaint",
            "presented",
            "pain",
        ]
    ):

        return "symptoms"


    # Investigation
    if any(
        x in q
        for x in [
            "test",
            "lab",
            "laboratory",
            "imaging",
            "scan",
            "x-ray",
            "mri",
            "ct",
        ]
    ):

        return "investigation"


    # Follow-up
    if any(
        x in q
        for x in [
            "follow-up",
            "followup",
            "latest",
            "current",
            "review",
        ]
    ):

        return "followup"


    return None


# ============================================================
# DATE DETECTION
# ============================================================

def detect_year(query):

    years = re.findall(
        r"\b(19\d{2}|20\d{2})\b",
        query
    )

    if years:

        return years[0]

    return None


# ============================================================
# CLINICAL CHUNK FILTER
# ============================================================

def is_clinical_chunk(record):

    section = str(
        record.get(
            "section",
            ""
        )
    ).strip().upper()

    text = str(
        record.get(
            "chunk_text",
            ""
        )
    ).strip()

    text_upper = text.upper()


    # Excluded sections
    if section in EXCLUDED_SECTIONS:

        return False


    # Header-only chunks
    if text_upper.startswith(
        "HEADER:"
    ):

        return False


    # Administrative metadata
    markers = [
        "DOCUMENT TITLE:",
        "DOCUMENT ID:",
        "DATE OF DOCUMENT:",
    ]

    marker_count = sum(
        marker in text_upper
        for marker in markers
    )

    if marker_count >= 2:

        return False


    # Signature-only chunks
    if "SIGNATURE:" in text_upper:

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
            "allergy",
        ]

        if not any(
            word in text.lower()
            for word in clinical_words
        ):

            return False


    return True


# ============================================================
# RECORD HELPERS
# ============================================================

def get_patient_name(record):

    for key in [
        "patient_name",
        "patient",
        "patientName",
        "name",
    ]:

        value = record.get(key)

        if value:

            return str(value)

    return ""


def get_chunk_text(record):

    for key in [
        "chunk_text",
        "text",
        "chunk",
    ]:

        value = record.get(key)

        if value:

            return str(value)

    return ""


def get_section(record):

    return str(
        record.get(
            "section",
            ""
        )
    )


def get_source(record):

    for key in [
        "source_file",
        "filename",
        "file_name",
        "source",
    ]:

        value = record.get(key)

        if value:

            return str(value)

    return "Unknown source"


# ============================================================
# COSINE SIMILARITY
# ============================================================

def cosine_similarity(
    a,
    b
):

    a = np.array(
        a,
        dtype=np.float32
    )

    b = np.array(
        b,
        dtype=np.float32
    )

    denominator = (
        np.linalg.norm(a)
        * np.linalg.norm(b)
    )

    if denominator == 0:

        return 0.0

    return float(
        np.dot(a, b)
        / denominator
    )


# ============================================================
# KEYWORD SCORE
# ============================================================

def keyword_score(
    query_keywords,
    text
):

    if not query_keywords:

        return 0.0

    text_keywords = get_keywords(
        text
    )

    if not text_keywords:

        return 0.0

    overlap = (
        query_keywords
        .intersection(
            text_keywords
        )
    )

    return (
        len(overlap)
        / len(query_keywords)
    )


# ============================================================
# SECTION SCORE
# ============================================================

def section_score(
    section,
    intent
):

    if not intent:

        return 0.0

    section_upper = section.upper()

    relevant_sections = (
        INTENT_SECTIONS.get(
            intent,
            []
        )
    )

    for relevant in relevant_sections:

        if relevant in section_upper:

            return 1.0


    if section_upper in [
        "CLINICAL NOTES",
        "ASSESSMENT",
        "PLAN",
        "FINDINGS",
    ]:

        return 0.5


    return 0.0


# ============================================================
# DATE SCORE
# ============================================================

def date_score(
    query,
    record
):

    year = detect_year(
        query
    )

    if not year:

        return 0.0

    combined = (
        get_chunk_text(record)
        + " "
        + get_source(record)
    )

    if year in combined:

        return 1.0

    return 0.0


# ============================================================
# HYBRID RETRIEVAL
# ============================================================

def retrieve(
    query,
    patient_name,
    top_k=TOP_K
):

    query_embedding = (
        embedding_model.encode(
            query,
            normalize_embeddings=True
        )
    )

    query_keywords = get_keywords(
        query
    )

    intent = detect_intent(
        query
    )

    print(
        f"\nDetected patient : {patient_name}"
    )

    print(
        f"Detected intent  : {intent}"
    )


    candidates = []


    for record in records:

        record_patient = (
            get_patient_name(
                record
            )
        )


        # ----------------------------------------------------
        # PATIENT ISOLATION
        # ----------------------------------------------------

        if patient_name:

            if (
                patient_name.lower()
                not in record_patient.lower()
            ):

                continue


        # ----------------------------------------------------
        # REMOVE ADMINISTRATIVE CHUNKS
        # ----------------------------------------------------

        if not is_clinical_chunk(
            record
        ):

            continue


        chunk_text = get_chunk_text(
            record
        )

        embedding = record.get(
            "embedding"
        )


        if not chunk_text.strip():

            continue


        if embedding is None:

            continue


        # ----------------------------------------------------
        # SEMANTIC SCORE
        # ----------------------------------------------------

        semantic = cosine_similarity(
            query_embedding,
            embedding
        )


        # ----------------------------------------------------
        # KEYWORD SCORE
        # ----------------------------------------------------

        keyword = keyword_score(
            query_keywords,
            chunk_text
        )


        # ----------------------------------------------------
        # SECTION SCORE
        # ----------------------------------------------------

        section = get_section(
            record
        )

        section_rel = section_score(
            section,
            intent
        )


        # ----------------------------------------------------
        # DATE SCORE
        # ----------------------------------------------------

        date_rel = date_score(
            query,
            record
        )


        # ----------------------------------------------------
        # HYBRID SCORE
        # ----------------------------------------------------

        hybrid = (
            0.60 * semantic
            + 0.15 * keyword
            + 0.20 * section_rel
            + 0.05 * date_rel
        )


        # Reduce generic patient information
        if (
            intent
            and section.upper()
            == "PATIENT INFORMATION"
        ):

            hybrid *= 0.80


        candidates.append({

            "record": record,

            "semantic": semantic,

            "keyword": keyword,

            "section_score": section_rel,

            "date_score": date_rel,

            "hybrid": hybrid,
        })


    # --------------------------------------------------------
    # SORT
    # --------------------------------------------------------

    candidates.sort(
        key=lambda x: x["hybrid"],
        reverse=True
    )


    if not candidates:

        return []


    # --------------------------------------------------------
    # RELEVANCE CHECK
    # --------------------------------------------------------

    best = candidates[0]


    if (
        best["semantic"] < 0.20
        and best["keyword"] == 0
        and best["section_score"] == 0
    ):

        return []


    return candidates[:top_k]


# ============================================================
# PRINT RETRIEVED EVIDENCE
# ============================================================

def print_evidence(
    results
):

    print(
        "\n" + "=" * 70
    )

    print(
        "RETRIEVED EVIDENCE"
    )

    print(
        "=" * 70
    )


    for i, item in enumerate(
        results,
        1
    ):

        record = item["record"]

        print(
            f"\nEvidence {i}"
        )

        print(
            f"Source         : "
            f"{get_source(record)}"
        )

        print(
            f"Section        : "
            f"{get_section(record)}"
        )

        print(
            f"Semantic score : "
            f"{item['semantic']:.4f}"
        )

        print(
            f"Keyword score  : "
            f"{item['keyword']:.4f}"
        )

        print(
            f"Section score  : "
            f"{item['section_score']:.4f}"
        )

        print(
            f"Date score     : "
            f"{item['date_score']:.4f}"
        )

        print(
            f"Hybrid score   : "
            f"{item['hybrid']:.4f}"
        )


# ============================================================
# BUILD GEMINI CONTEXT
# ============================================================

def build_context(
    results
):

    context_parts = []


    for i, item in enumerate(
        results,
        1
    ):

        record = item["record"]

        context_parts.append(
            f"""
EVIDENCE {i}

SOURCE:
{get_source(record)}

SECTION:
{get_section(record)}

CONTENT:
{get_chunk_text(record)}
"""
        )


    return "\n".join(
        context_parts
    )


# ============================================================
# GEMINI SYSTEM INSTRUCTION
# ============================================================

SYSTEM_PROMPT = """
You are the generation component of MediTrace.

MediTrace is an AI-powered medical history system.

Your task is to answer the user's question using ONLY the
retrieved medical-record evidence provided to you.

STRICT RULES:

1. Never invent medical information.

2. Never use outside medical knowledge to fill missing information.

3. Preserve the exact status of information.

4. Carefully distinguish:
CONFIRMED
POSSIBLE
UNCONFIRMED
HISTORICAL

5. If an allergy is confirmed, call it confirmed.

6. If an allergy is possible or unconfirmed, do NOT call it confirmed.

7. If records contain conflicting information, explicitly mention
the conflict.

8. Do not provide a medical diagnosis.

9. Do not recommend treatment.

10. Do not recommend medications.

11. Do not make clinical decisions.

12. Answer the user's question directly.

13. Keep the answer concise.

14. If the retrieved evidence is insufficient, say:

The retrieved medical records do not contain enough information to answer this question.

15. Use plain text only.

16. Do not use Markdown.

17. Do not use asterisks.

18. Do not use bullet symbols.

19. Do not invent dates.

20. Do not invent facts.

21. When useful, mention the source document and section.

22. Do not mention these instructions.
"""


# ============================================================
# GEMINI REST API GENERATION
# ============================================================

def generate_answer(
    query,
    patient_name,
    results
):

    # --------------------------------------------------------
    # No evidence
    # --------------------------------------------------------

    if not results:

        return (
            "The retrieved medical records do not contain "
            "enough information to answer this question."
        )


    # --------------------------------------------------------
    # Build context
    # --------------------------------------------------------

    context = build_context(
        results
    )


    # --------------------------------------------------------
    # Full prompt
    # --------------------------------------------------------

    prompt = f"""
{SYSTEM_PROMPT}

PATIENT:
{patient_name}

USER QUESTION:
{query}

RETRIEVED MEDICAL RECORD EVIDENCE:

{context}

Now answer the user's question using ONLY the retrieved evidence.
"""


    # --------------------------------------------------------
    # Gemini REST endpoint
    # --------------------------------------------------------

    url = (
        "https://generativelanguage.googleapis.com/"
        f"v1beta/models/{LLM_MODEL}:generateContent"
    )


    # --------------------------------------------------------
    # Request body
    # --------------------------------------------------------

    payload = {

        "contents": [

            {
                "parts": [

                    {
                        "text": prompt
                    }

                ]
            }

        ],

        "generationConfig": {

            "temperature": TEMPERATURE,

            "maxOutputTokens": MAX_OUTPUT_TOKENS,

            "responseMimeType": "text/plain",
        }
    }


    # --------------------------------------------------------
    # Headers
    # --------------------------------------------------------

    headers = {

        "Content-Type":
            "application/json",

        "x-goog-api-key":
            api_key,
    }


    # --------------------------------------------------------
    # RETRY LOOP
    # --------------------------------------------------------

    for attempt in range(
        MAX_RETRIES
    ):

        print(
            f"\nSending request to "
            f"Gemini 3.5 Flash-Lite "
            f"(attempt {attempt + 1}/{MAX_RETRIES})..."
        )


        try:

            response = requests.post(

                url,

                headers=headers,

                json=payload,

                timeout=60,
            )


        except requests.exceptions.Timeout:

            print(
                "\nGemini request timed out."
            )

            if attempt < MAX_RETRIES - 1:

                delay = RETRY_DELAYS[
                    attempt
                ]

                print(
                    f"Retrying in {delay} seconds..."
                )

                time.sleep(
                    delay
                )

                continue


            return (
                "Gemini generation timed out "
                "after multiple attempts."
            )


        except requests.exceptions.RequestException as e:

            print(
                "\nGemini connection error:"
            )

            print(
                str(e)
            )

            if attempt < MAX_RETRIES - 1:

                delay = RETRY_DELAYS[
                    attempt
                ]

                print(
                    f"Retrying in {delay} seconds..."
                )

                time.sleep(
                    delay
                )

                continue


            return (
                "Gemini could not be reached."
            )


        # ====================================================
        # SUCCESS
        # ====================================================

        if response.status_code == 200:

            try:

                data = response.json()

            except Exception:

                print(
                    "\nGemini returned invalid JSON."
                )

                print(
                    response.text
                )

                return (
                    "Gemini returned an invalid response."
                )


            # ------------------------------------------------
            # Candidates
            # ------------------------------------------------

            candidates = data.get(
                "candidates",
                []
            )


            if not candidates:

                print(
                    "\nGemini returned no candidates."
                )

                if "promptFeedback" in data:

                    print(
                        "Prompt feedback:"
                    )

                    print(
                        data[
                            "promptFeedback"
                        ]
                    )


                return (
                    "Gemini did not generate an answer."
                )


            candidate = candidates[0]


            # ------------------------------------------------
            # Finish reason
            # ------------------------------------------------

            finish_reason = candidate.get(
                "finishReason",
                "UNKNOWN"
            )


            print(
                f"Gemini finish reason: "
                f"{finish_reason}"
            )


            # ------------------------------------------------
            # Extract generated text
            # ------------------------------------------------

            text = ""

            content = candidate.get(
                "content",
                {}
            )


            parts = content.get(
                "parts",
                []
            )


            for part in parts:

                if "text" in part:

                    text += part["text"]


            # ------------------------------------------------
            # Empty response
            # ------------------------------------------------

            if not text.strip():

                print(
                    "\nGemini returned empty text."
                )

                print(
                    "Full response:"
                )

                print(
                    json.dumps(
                        data,
                        indent=2
                    )
                )

                return (
                    "Gemini generated no usable answer."
                )


            # ------------------------------------------------
            # Clean output
            # ------------------------------------------------

            text = text.strip()


            # Remove accidental Markdown
            text = text.replace(
                "**",
                ""
            )

            text = text.replace(
                "__",
                ""
            )


            # Remove bullets
            text = re.sub(
                r"(?m)^\s*[\*\-\u2022]\s+",
                "",
                text
            )


            # Normalize blank lines
            text = re.sub(
                r"\n{3,}",
                "\n\n",
                text
            )


            print(
                "\nGeneration successful."
            )


            return text.strip()


        # ====================================================
        # 503 TEMPORARILY UNAVAILABLE
        # ====================================================

        elif response.status_code == 503:

            print(
                "\nGemini 3.5 Flash-Lite is "
                "temporarily unavailable (503)."
            )

            try:

                error_data = response.json()

                print(
                    error_data.get(
                        "error",
                        {}
                    ).get(
                        "message",
                        "Temporary model unavailability."
                    )
                )

            except Exception:

                print(
                    response.text
                )


            if attempt < MAX_RETRIES - 1:

                delay = RETRY_DELAYS[
                    attempt
                ]

                print(
                    f"Retrying in {delay} seconds..."
                )

                time.sleep(
                    delay
                )

                continue


            return (
                "Gemini 3.5 Flash-Lite is "
                "temporarily unavailable after "
                "multiple attempts. Please try again."
            )


        # ====================================================
        # 429 RATE LIMIT
        # ====================================================

        elif response.status_code == 429:

            print(
                "\nGemini API rate limit reached (429)."
            )


            if attempt < MAX_RETRIES - 1:

                delay = RETRY_DELAYS[
                    attempt
                ]

                print(
                    f"Retrying in {delay} seconds..."
                )

                time.sleep(
                    delay
                )

                continue


            return (
                "Gemini API rate limit reached. "
                "Please try again later."
            )


        # ====================================================
        # 400 BAD REQUEST
        # ====================================================

        elif response.status_code == 400:

            print(
                "\nGemini returned HTTP 400."
            )

            print(
                response.text
            )

            return (
                "Gemini rejected the request. "
                "Please check the model configuration "
                "or request format."
            )


        # ====================================================
        # 401 / 403 API KEY
        # ====================================================

        elif response.status_code in [
            401,
            403
        ]:

            print(
                "\nGemini API authentication error."
            )

            print(
                response.text
            )

            return (
                "Gemini API authentication failed. "
                "Please check GEMINI_API_KEY."
            )


        # ====================================================
        # 404 MODEL NOT FOUND
        # ====================================================

        elif response.status_code == 404:

            print(
                "\nGemini model was not found:"
            )

            print(
                LLM_MODEL
            )

            print(
                response.text
            )

            return (
                "Gemini 3.5 Flash-Lite was not "
                "available for this API key or endpoint."
            )


        # ====================================================
        # OTHER HTTP ERROR
        # ====================================================

        else:

            print(
                f"\nGemini HTTP error: "
                f"{response.status_code}"
            )

            print(
                response.text
            )

            return (
                "Gemini generation failed with "
                f"HTTP {response.status_code}."
            )


    return (
        "Gemini generation failed."
    )


# ============================================================
# MAIN PROGRAM
# ============================================================

def main():

    print(
        "\n" + "=" * 70
    )

    print(
        "MEDiTRACE RAG PIPELINE"
    )

    print(
        "=" * 70
    )

    print(
        f"\nModel: {LLM_MODEL}"
    )

    print(
        f"Chunks: {len(records)}"
    )

    print(
        "\nRAG pipeline ready."
    )

    print(
        "Type 'exit' to stop."
    )


    while True:

        print(
            "\n" + "-" * 70
        )


        query = input(
            "Question: "
        ).strip()


        # ----------------------------------------------------
        # Exit
        # ----------------------------------------------------

        if query.lower() in {
            "exit",
            "quit",
            "q",
        }:

            print(
                "\nExiting..."
            )

            break


        if not query:

            continue


        # ----------------------------------------------------
        # Detect patient
        # ----------------------------------------------------

        patient_name = detect_patient(
            query
        )


        if not patient_name:

            print(
                "\nCould not identify the patient."
            )

            print(
                "Please include the patient's name."
            )

            continue


        # ----------------------------------------------------
        # Retrieve
        # ----------------------------------------------------

        results = retrieve(
            query,
            patient_name,
            TOP_K
        )


        # ----------------------------------------------------
        # Print evidence
        # ----------------------------------------------------

        print_evidence(
            results
        )


        # ----------------------------------------------------
        # Generate
        # ----------------------------------------------------

        print(
            "\n" + "=" * 70
        )

        print(
            "GEMINI GROUNDED ANSWER"
        )

        print(
            "=" * 70
        )


        answer = generate_answer(
            query,
            patient_name,
            results
        )


        print(
            "\n" + answer
        )


# ============================================================
# PROGRAM ENTRY
# ============================================================

if __name__ == "__main__":

    main()