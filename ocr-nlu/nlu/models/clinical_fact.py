from enum import Enum
from typing import Any
from pydantic import BaseModel, Field, PrivateAttr
from .context import Context, FactStatus
from .evidence import Evidence

class EntityType(str, Enum):
    CONDITION="CONDITION"; SYMPTOM="SYMPTOM"; FINDING="FINDING"; MEDICATION="MEDICATION"; ALLERGY="ALLERGY"; PROCEDURE="PROCEDURE"; INVESTIGATION="INVESTIGATION"; LAB_RESULT="LAB_RESULT"; IMAGING_FINDING="IMAGING_FINDING"; VITAL_SIGN="VITAL_SIGN"; DEVICE="DEVICE"; ANATOMICAL_SITE="ANATOMICAL_SITE"; PROVIDER="PROVIDER"; ENCOUNTER="ENCOUNTER"; DATE_TIME="DATE_TIME"; MEASUREMENT="MEASUREMENT"; SEVERITY="SEVERITY"; LATERALITY="LATERALITY"; REACTION="REACTION"; RECOMMENDATION="RECOMMENDATION"; CRITICAL_FINDING="CRITICAL_FINDING"; PATIENT_DEMOGRAPHIC="PATIENT_DEMOGRAPHIC"
class ClinicalFact(BaseModel):
    entity_id: str
    entity_type: EntityType
    original_text: str = Field(min_length=1)
    normalized_text: str
    terminology_code: str | None = None
    context: Context = Field(default_factory=Context)
    evidence: Evidence
    extraction_method: str = "rule_based"
    extraction_confidence: float | None = None
    status: FactStatus = FactStatus.EXTRACTED
    attributes: dict[str, Any] = Field(default_factory=dict)
    _context_sentence: str = PrivateAttr(default="")
