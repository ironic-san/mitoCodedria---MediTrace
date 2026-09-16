def detect_certainty(sentence: str) -> str:
    s=sentence.lower()
    if any(x in s for x in ("possible", "may be", "cannot exclude", "?")): return "POSSIBLE"
    if any(x in s for x in ("probable", "likely", "suggestive of")): return "PROBABLE"
    if "uncertain" in s: return "UNCERTAIN"
    return "CERTAIN"
