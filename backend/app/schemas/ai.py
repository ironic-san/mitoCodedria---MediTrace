from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class MedicalFindingItem(BaseModel):
    """Extracted medical finding item (allergy, condition, medication, event, etc.)."""
    type: str  # allergy, condition, medication, event, procedure, diagnosis
    name: str
    details: Optional[Dict[str, Any]] = None
    document_date: Optional[str] = None
    severity: Optional[str] = None
    is_critical: bool = False


class FindingComparisonItem(BaseModel):
    """Individual comparison item against patient structured records."""
    category: str  # ALLERGY, CONDITION, MEDICATION, EVENT
    extracted_finding: str
    existing_record: Optional[str] = None
    classification: str  # MATCH, NEW, CONFLICT
    details: Optional[str] = None
    is_critical: bool = False


class AIDocumentAnalysisResult(BaseModel):
    """Structured AI & Comparison output."""
    summary: str
    extracted_data: Dict[str, Any] = Field(default_factory=dict)
    critical_findings: List[Dict[str, Any]] = Field(default_factory=list)
    new_findings: List[Dict[str, Any]] = Field(default_factory=list)
    conflicts: List[Dict[str, Any]] = Field(default_factory=list)
    confidence_score: float = 0.95


class DocumentAnalysisResponse(BaseModel):
    """Response payload for document analysis endpoints."""
    analysis_id: str
    document_id: str
    patient_id: str
    analysis_status: str
    extracted_data: Dict[str, Any]
    critical_findings: List[Any]
    new_findings: List[Any]
    conflicts: List[Any]
    ai_summary: str
    confidence_score: float
    review_status: str
    reviewed_by: Optional[str] = None
    reviewed_at: Optional[str] = None
    created_at: str


class ReviewAnalysisRequest(BaseModel):
    """Request payload for doctor review of document analysis."""
    review_action: str  # APPROVE, MODIFY, REJECT
    modified_findings: Optional[Dict[str, Any]] = None
    notes: Optional[str] = None


class ReviewAnalysisResponse(BaseModel):
    """Response confirmation for completed doctor review."""
    analysis_id: str
    document_id: str
    patient_id: str
    review_status: str  # APPROVED, MODIFIED, REJECTED
    reviewed_by: str
    reviewed_at: str
    message: str
    updated_records: Optional[Dict[str, Any]] = None


# --- TASK 6 EXPLICIT NLU SCHEMAS ---

class NLUProcessRequest(BaseModel):
    """Request payload for explicit NLU text analysis."""
    extracted_text: str = Field(..., min_length=3, description="Medical text to extract structured findings from")
    patient_id: Optional[str] = Field(None, description="Optional patient UUID for context-aware extraction")
    document_meta: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Optional document metadata")


class NLUProcessResponse(BaseModel):
    """Response payload for explicit NLU extraction."""
    extracted_text: str
    findings: Dict[str, Any] = Field(default_factory=dict, description="Extracted conditions, allergies, medications, procedures, events")
    normalizations: List[Dict[str, str]] = Field(default_factory=list, description="Medical term normalizations applied (e.g. T2DM -> Type 2 Diabetes)")
    critical_findings: List[str] = Field(default_factory=list, description="Critical findings and emergency risk alerts")
    is_suggestion_only: bool = Field(True, description="Enforces that NLU output is suggestion-only and does NOT write directly to DB")
    summary: str = Field("", description="Clinical summary synthesized from extracted text")


# --- TASK 6 END-TO-END AI PIPELINE SCHEMAS ---

class AIPipelineRequest(BaseModel):
    """Request payload for running the complete AI Pipeline."""
    patient_id: str = Field(..., description="Target patient UUID")
    document_id: Optional[str] = Field(None, description="Existing document UUID if processing an uploaded document")
    extracted_text: Optional[str] = Field(None, description="Raw medical text if running pipeline directly on text")


class AIPipelineResponse(BaseModel):
    """Response payload containing full pipeline execution results."""
    patient_id: str
    document_id: Optional[str] = None
    extracted_text: str
    nlu_findings: Dict[str, Any]
    rag_historical_evidence: Optional[Dict[str, Any]] = None
    integrity_verification_results: Optional[List[Dict[str, Any]]] = None
    comparison_with_db: Dict[str, Any]
    doctor_clinical_report: str
    recommended_actions: List[str] = Field(default_factory=list)
    review_status: str = "PENDING_DOCTOR_REVIEW"
    disclaimer: str = "AI is a clinical assistant. The licensed physician is the sole decision-maker for authoritative records."
