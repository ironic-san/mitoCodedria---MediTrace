def detect_temporality(sentence: str) -> str:
    s=sentence.lower()
    if any(x in s for x in ("history of", "past medical", "previous", "prior", "formerly")): return "HISTORICAL"
    if any(x in s for x in ("scheduled", "planned", "will ", "follow-up", "to undergo")): return "FUTURE"
    if any(x in s for x in ("recent", "yesterday", "post-operative", "postoperative")): return "RECENT"
    return "CURRENT"
