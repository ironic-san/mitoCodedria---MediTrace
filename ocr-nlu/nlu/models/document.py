from enum import Enum
from pydantic import BaseModel, Field
class DocumentType(str, Enum):
    DISCHARGE_SUMMARY="DISCHARGE_SUMMARY"; LABORATORY_REPORT="LABORATORY_REPORT"; IMAGING_REPORT="IMAGING_REPORT"; MRI_REPORT="MRI_REPORT"; CT_REPORT="CT_REPORT"; RADIOLOGY_REPORT="RADIOLOGY_REPORT"; OPERATIVE_REPORT="OPERATIVE_REPORT"; SURGICAL_REPORT="SURGICAL_REPORT"; CONSULTATION="CONSULTATION"; FOLLOW_UP="FOLLOW_UP"; MEDICATION_HISTORY="MEDICATION_HISTORY"; ALLERGY_ASSESSMENT="ALLERGY_ASSESSMENT"; ONCOLOGY_REPORT="ONCOLOGY_REPORT"; CHEMOTHERAPY_RECORD="CHEMOTHERAPY_RECORD"; PREOPERATIVE_ASSESSMENT="PREOPERATIVE_ASSESSMENT"; POSTOPERATIVE_FOLLOWUP="POSTOPERATIVE_FOLLOWUP"; CARDIOLOGY_REPORT="CARDIOLOGY_REPORT"; ORTHOPEDIC_REPORT="ORTHOPEDIC_REPORT"; NEUROLOGY_REPORT="NEUROLOGY_REPORT"; UNKNOWN="UNKNOWN"
class Section(BaseModel):
    name: str
    heading: str
    text: str
    start: int
    end: int
class DocumentStructure(BaseModel):
    document_id: str
    file_path: str
    document_type: DocumentType = DocumentType.UNKNOWN
    classification_confidence: float = 0.0
    classification_reasoning: list[str] = Field(default_factory=list)
    sections: list[Section] = Field(default_factory=list)
    metadata: dict = Field(default_factory=dict)
