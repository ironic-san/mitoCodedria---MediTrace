from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class RAGQueryRequest(BaseModel):
    """Doctor request payload for historical medical RAG query."""
    patient_id: str = Field(..., description="Target patient UUID")
    question: str = Field(..., min_length=2, description="Clinical question about patient history")
    max_sources: Optional[int] = Field(5, ge=1, le=15, description="Maximum evidence sources to return")


class RAGRetrievalRequest(BaseModel):
    patient_id: str
    query: str = Field(..., min_length=2)
    max_sources: Optional[int] = Field(5, ge=1, le=15)


class RAGKeywordQueryRequest(BaseModel):
    """Request payload for keyword-derived historical RAG retrieval."""
    patient_id: str = Field(..., description="Target patient UUID")
    extracted_text: str = Field(..., min_length=2, description="Extracted medical text to derive keywords and query history")
    max_sources: Optional[int] = Field(5, ge=1, le=15, description="Maximum evidence sources to return")


class RAGSourceItem(BaseModel):
    """Retrieved evidence document chunk and source attribution."""
    document_id: str
    title: str
    document_date: Optional[str] = None
    chunk_text: str
    similarity_score: float
    score: Optional[float] = None
    patient_id: str
    section: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class RAGRetrievalResponse(BaseModel):
    patient_id: str
    query: str
    retrievals: List[RAGSourceItem] = Field(default_factory=list)


class RAGQueryResponse(BaseModel):
    """Synthesized RAG clinical answer with source citations."""
    patient_id: str
    question: str
    answer: str
    sources: List[RAGSourceItem] = Field(default_factory=list)
    confidence_score: float = Field(0.95, ge=0.0, le=1.0)
    evidence_found: bool = True
    extracted_keywords: Optional[List[str]] = None
