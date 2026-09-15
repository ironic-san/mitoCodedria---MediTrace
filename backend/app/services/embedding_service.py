import math
import re
from typing import Dict, List, Set


# Medical synonym dictionary for semantic grounding and term expansion
MEDICAL_SYNONYMS: Dict[str, Set[str]] = {
    "mi": {"myocardial", "infarction", "heart", "attack", "cardiac", "coronary", "acute"},
    "myocardial": {"mi", "infarction", "heart", "attack", "cardiac", "coronary"},
    "infarction": {"mi", "myocardial", "heart", "attack", "cardiac"},
    "cardiac": {"mi", "heart", "coronary", "myocardial", "angioplasty", "stent"},
    "angioplasty": {"stent", "coronary", "pci", "cardiac", "catheterization"},
    "stent": {"angioplasty", "coronary", "pci", "cardiac", "placement"},
    "fracture": {"broken", "bone", "femur", "femoral", "shaft", "intramedullary", "fixation"},
    "femur": {"fracture", "thigh", "bone", "femoral", "intramedullary", "fixation"},
    "intramedullary": {"fixation", "femur", "fracture", "orthopedic", "nail", "surgery"},
    "diabetes": {"t2dm", "mellitus", "glucose", "glycemic", "hba1c", "metformin", "sugar"},
    "t2dm": {"diabetes", "mellitus", "glucose", "glycemic", "hba1c", "metformin"},
    "hypertension": {"htn", "blood", "pressure", "elevated", "telmisartan", "amlodipine"},
    "osteosarcoma": {"tumor", "bone", "cancer", "malignancy", "chemotherapy", "limb", "sparing"},
    "chemotherapy": {"chemo", "infusion", "osteosarcoma", "oncology", "cancer", "cisplatin", "doxorubicin"},
    "penicillin": {"allergy", "anaphylaxis", "amoxicillin", "rash", "antibiotic", "reaction"},
    "anaphylaxis": {"severe", "allergy", "penicillin", "shock", "swelling", "emergency"},
    "craniotomy": {"brain", "surgery", "neurosurgery", "intracranial", "lesion", "resection"},
    "brain": {"craniotomy", "surgery", "neurosurgery", "intracranial", "lesion", "tumor", "neurological"},
    "neurosurgery": {"brain", "surgery", "craniotomy", "intracranial", "lesion", "resection"},
    "pneumonia": {"lung", "infection", "respiratory", "fever", "cough", "hospitalization"},
}

STOPWORDS = {
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", "as", "at",
    "be", "because", "been", "before", "being", "below", "between", "both", "but", "by", "could", "did", "do",
    "does", "doing", "down", "during", "each", "few", "for", "from", "further", "had", "has", "have", "having",
    "he", "her", "here", "hers", "herself", "him", "himself", "his", "how", "i", "if", "in", "into", "is", "it",
    "its", "itself", "just", "me", "more", "most", "my", "myself", "no", "nor", "not", "now", "of", "off", "on",
    "once", "only", "or", "other", "ought", "our", "ours", "ourselves", "out", "over", "own", "same", "she",
    "should", "so", "some", "such", "than", "that", "the", "their", "theirs", "them", "themselves", "then",
    "there", "these", "they", "this", "those", "through", "to", "too", "under", "until", "up", "very", "was",
    "we", "were", "what", "when", "where", "which", "while", "who", "whom", "why", "with", "would", "you", "your",
    "yours", "yourself", "yourselves", "undergo", "underwent", "did", "patient"
}


def tokenize(text: str) -> List[str]:
    """Tokenizes and normalizes text into cleaned lower-case tokens."""
    if not text:
        return []
    cleaned = re.sub(r"[^a-zA-Z0-9\s]", " ", text.lower())
    tokens = [t.strip() for t in cleaned.split() if t.strip() and t.strip() not in STOPWORDS]
    return tokens


def expand_tokens(tokens: List[str]) -> Dict[str, float]:
    """Expands tokens with medical synonyms and assigns weighted term frequencies."""
    tf: Dict[str, float] = {}
    for t in tokens:
        tf[t] = tf.get(t, 0.0) + 1.0
        # Expand synonyms
        if t in MEDICAL_SYNONYMS:
            for syn in MEDICAL_SYNONYMS[t]:
                tf[syn] = tf.get(syn, 0.0) + 0.65

    # Check for multi-word phrases (e.g. type 2, heart attack, femur fracture)
    joined = " ".join(tokens)
    if "type 2" in joined or "t2dm" in joined:
        tf["diabetes"] = tf.get("diabetes", 0.0) + 1.5
    if "heart attack" in joined or "myocardial infarction" in joined:
        tf["mi"] = tf.get("mi", 0.0) + 1.5
        tf["cardiac"] = tf.get("cardiac", 0.0) + 1.5
    if "brain surgery" in joined or "intracranial" in joined:
        tf["neurosurgery"] = tf.get("neurosurgery", 0.0) + 1.5
    if "femur fracture" in joined or "intramedullary" in joined:
        tf["orthopedic"] = tf.get("orthopedic", 0.0) + 1.5

    return tf


def compute_cosine_similarity(vec1: Dict[str, float], vec2: Dict[str, float]) -> float:
    """Computes cosine similarity between two sparse term-frequency vectors."""
    if not vec1 or not vec2:
        return 0.0

    dot = 0.0
    for term, val in vec1.items():
        if term in vec2:
            dot += val * vec2[term]

    norm1 = math.sqrt(sum(v * v for v in vec1.values()))
    norm2 = math.sqrt(sum(v * v for v in vec2.values()))

    if norm1 == 0.0 or norm2 == 0.0:
        return 0.0

    return dot / (norm1 * norm2)
