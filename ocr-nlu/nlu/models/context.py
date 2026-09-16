from enum import Enum
from pydantic import BaseModel

class Negation(str, Enum): AFFIRMED = "AFFIRMED"; NEGATED = "NEGATED"
class Certainty(str, Enum): CERTAIN = "CERTAIN"; POSSIBLE = "POSSIBLE"; PROBABLE = "PROBABLE"; UNCERTAIN = "UNCERTAIN"
class Temporality(str, Enum): CURRENT = "CURRENT"; HISTORICAL = "HISTORICAL"; RECENT = "RECENT"; FUTURE = "FUTURE"; UNKNOWN = "UNKNOWN"
class Experiencer(str, Enum): PATIENT = "PATIENT"; FAMILY = "FAMILY"; OTHER = "OTHER"
class FactStatus(str, Enum): EXTRACTED = "EXTRACTED"; NORMALIZED = "NORMALIZED"; VALIDATED = "VALIDATED"; NEEDS_REVIEW = "NEEDS_REVIEW"; CONFLICTING = "CONFLICTING"; REJECTED = "REJECTED"
class Context(BaseModel):
    negation: Negation = Negation.AFFIRMED
    certainty: Certainty = Certainty.CERTAIN
    temporality: Temporality = Temporality.UNKNOWN
    experiencer: Experiencer = Experiencer.PATIENT
    status: str = "UNKNOWN"
