import re
def detect_negation(sentence: str, entity: str) -> str:
    s=sentence.lower(); e=entity.lower()
    return "NEGATED" if re.search(r"\b(no evidence of|no sign of|without|denies?|denied|negative for|no known)\b[^.]{0,80}\b"+re.escape(e)+r"\b", s) else "AFFIRMED"
