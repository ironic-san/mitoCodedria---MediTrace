def detect_experiencer(sentence: str) -> str:
    s=sentence.lower()
    return "FAMILY" if any(x in s for x in ("family history", "mother", "father", "sibling")) else ("OTHER" if any(x in s for x in ("caregiver", "relative")) else "PATIENT")
