from pydantic import BaseModel, Field
from .clinical_fact import ClinicalFact
from .document import DocumentStructure
from .relationships import Relationship
class ValidationIssue(BaseModel):
    code: str
    message: str
    severity: str = "WARNING"
    entity_ids: list[str] = Field(default_factory=list)
class NLUResult(BaseModel):
    document: DocumentStructure
    candidate_facts: list[ClinicalFact] = Field(default_factory=list)
    verified_facts: list[ClinicalFact] = Field(default_factory=list)
    relationships: list[Relationship] = Field(default_factory=list)
    validation_issues: list[ValidationIssue] = Field(default_factory=list)

    def model_dump_json_safe(self) -> str:
        return self.model_dump_json()
