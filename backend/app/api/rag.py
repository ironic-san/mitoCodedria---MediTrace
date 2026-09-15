from typing import List
from fastapi import APIRouter, Depends, HTTPException, status

from app.core.dependencies import AuthenticatedUser, require_doctor
from app.schemas.rag import (
    RAGKeywordQueryRequest,
    RAGQueryRequest,
    RAGQueryResponse,
)
from app.services.emergency_service import get_doctor_access_mode
from app.services.rag_service import (
    extract_keywords_and_query_rag,
    query_historical_records,
)
from app.services.supabase_service import get_supabase_service_client

router = APIRouter()


@router.post("", response_model=RAGQueryResponse, summary="Extract keywords and query patient historical records (RAG)")
@router.post("/query", response_model=RAGQueryResponse, summary="Query patient historical medical records using RAG")
def rag_query_endpoint(
    payload: RAGQueryRequest,
    current_user: AuthenticatedUser = Depends(require_doctor),
):
    """
    Doctor-facing patient-scoped RAG query for historical unstructured documents.
    - Requires authenticated DOCTOR.
    - Requires active NORMAL or BREAK_GLASS emergency doctor access.
    - Chunks, indexes, and searches only documents belonging to payload.patient_id.
    - Synthesizes grounded clinical answer with source attribution.
    """
    if not current_user.doctor_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Doctor profile not linked to authenticated user.",
        )

    client = get_supabase_service_client()
    return query_historical_records(
        client=client,
        doctor_id=current_user.doctor_id,
        patient_id=payload.patient_id,
        question=payload.question,
        max_sources=payload.max_sources or 5,
    )


@router.post("/extract-and-query", response_model=RAGQueryResponse, summary="Keyword extraction -> Patient RAG retrieval")
@router.post("/keyword-query", response_model=RAGQueryResponse, summary="Keyword extraction -> Patient RAG retrieval (alias)")
def rag_keyword_query_endpoint(
    payload: RAGKeywordQueryRequest,
    current_user: AuthenticatedUser = Depends(require_doctor),
):
    """
    Explicit medical text keyword extraction and historical RAG retrieval.
    Extracts medical concepts/years from raw text and retrieves patient-isolated evidence.
    """
    if not current_user.doctor_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Doctor profile not linked to authenticated user.",
        )

    client = get_supabase_service_client()
    return extract_keywords_and_query_rag(
        client=client,
        doctor_id=current_user.doctor_id,
        patient_id=payload.patient_id,
        extracted_text=payload.extracted_text,
        max_sources=payload.max_sources or 5,
    )


@router.get("/patient/{patient_id}/documents", summary="List historical documents indexed for RAG")
def list_patient_rag_documents(
    patient_id: str,
    current_user: AuthenticatedUser = Depends(require_doctor),
):
    """Lists indexed medical documents for an authorized patient."""
    if not current_user.doctor_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Doctor profile not linked to authenticated user.",
        )

    client = get_supabase_service_client()
    mode = get_doctor_access_mode(client, current_user.doctor_id, patient_id)
    if not mode:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Doctor does not have valid active access to this patient.",
        )

    res = (
        client.table("medical_documents")
        .select("document_id, patient_id, title, document_date, document_type, ocr_status")
        .eq("patient_id", patient_id)
        .execute()
    )
    return {
        "patient_id": patient_id,
        "access_mode": mode,
        "total_documents": len(res.data or []),
        "documents": res.data or [],
    }
