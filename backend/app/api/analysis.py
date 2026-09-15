from datetime import datetime, timezone
from typing import Any, Dict
from fastapi import APIRouter, Depends, HTTPException, status

from app.core.dependencies import AuthenticatedUser, require_doctor
from app.schemas.ai import (
    AIPipelineRequest,
    AIPipelineResponse,
    ReviewAnalysisRequest,
    ReviewAnalysisResponse,
)
from app.services.ai_service import extract_nlu_findings
from app.services.audit_service import log_audit_event
from app.services.emergency_service import get_doctor_access_mode
from app.services.patient_service import (
    get_consolidated_medical_summary,
    has_valid_doctor_access,
)
from app.services.rag_service import extract_keywords_and_query_rag
from app.services.supabase_service import get_supabase_service_client

router = APIRouter()


@router.post("/{analysis_id}/review", response_model=ReviewAnalysisResponse, summary="Doctor review of document analysis")
def review_document_analysis(
    analysis_id: str,
    payload: ReviewAnalysisRequest,
    current_user: AuthenticatedUser = Depends(require_doctor),
):
    """
    Doctor reviews AI document analysis result.
    - APPROVE: Accept AI-proposed findings and apply to authoritative medical tables.
    - MODIFY: Apply doctor's modified findings to authoritative medical tables.
    - REJECT: Do NOT modify authoritative tables. Mark analysis as REJECTED.
    Only authenticated doctors with valid ACTIVE NORMAL access can perform this action.
    Break-glass emergency access doctors are strictly prohibited from write/review actions.
    """
    if not current_user.doctor_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Doctor profile not linked to authenticated user.",
        )

    action = payload.review_action.upper()
    if action not in {"APPROVE", "MODIFY", "REJECT"}:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid review_action '{payload.review_action}'. Must be APPROVE, MODIFY, or REJECT.",
        )

    client = get_supabase_service_client()

    # 1. Fetch analysis record
    analysis_res = (
        client.table("document_analysis")
        .select("*")
        .eq("analysis_id", analysis_id)
        .execute()
    )

    if not analysis_res.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Document analysis with ID '{analysis_id}' not found.",
        )

    an_data = analysis_res.data[0]
    patient_id = str(an_data["patient_id"])
    document_id = str(an_data["document_id"])

    # 2. Authorization check: Doctor must have active NORMAL access
    access_mode = get_doctor_access_mode(client, current_user.doctor_id, patient_id)
    if access_mode == "BREAK_GLASS":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Break-glass emergency access does not permit modifying medical records or reviewing findings (Write operation prohibited).",
        )
    elif not access_mode or not has_valid_doctor_access(client, current_user.doctor_id, patient_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Doctor does not have valid active access to this patient.",
        )

    now_utc = datetime.now(timezone.utc)
    updated_records: Dict[str, Any] = {}

    findings_data = (
        payload.modified_findings
        if action == "MODIFY" and payload.modified_findings
        else an_data.get("extracted_data") or {}
    )

    if action in {"APPROVE", "MODIFY"}:
        # Apply findings to authoritative tables
        # A. Allergies
        allergies = findings_data.get("allergies", [])
        if isinstance(allergies, list):
            for alg in allergies:
                alg_name = alg.get("allergen") if isinstance(alg, dict) else str(alg)
                if alg_name:
                    alg_res = client.table("allergies").select("allergy_id").ilike("allergen", f"%{alg_name}%").execute()
                    if alg_res.data:
                        allergy_id = str(alg_res.data[0]["allergy_id"])
                    else:
                        ins_alg = client.table("allergies").insert({"allergen": alg_name, "allergy_type": "DRUG"}).execute()
                        allergy_id = str(ins_alg.data[0]["allergy_id"])

                    existing_pat_alg = (
                        client.table("patient_allergies")
                        .select("*")
                        .eq("patient_id", patient_id)
                        .eq("allergy_id", allergy_id)
                        .execute()
                    )
                    if not existing_pat_alg.data:
                        sev = alg.get("severity", "Severe") if isinstance(alg, dict) else "Severe"
                        react = alg.get("reaction", "Reaction noted") if isinstance(alg, dict) else "Reaction noted"
                        ins_pat_alg = client.table("patient_allergies").insert({
                            "patient_id": patient_id,
                            "allergy_id": allergy_id,
                            "severity": sev,
                            "reaction": react,
                            "status": "ACTIVE",
                        }).execute()
                        updated_records.setdefault("allergies", []).append(ins_pat_alg.data[0])

        # B. Conditions
        conditions = findings_data.get("conditions", [])
        if isinstance(conditions, list):
            for cond in conditions:
                cond_name = cond.get("name") if isinstance(cond, dict) else str(cond)
                if cond_name:
                    cond_res = client.table("medical_conditions").select("condition_id").ilike("name", f"%{cond_name}%").execute()
                    if cond_res.data:
                        condition_id = str(cond_res.data[0]["condition_id"])
                    else:
                        ins_cond = client.table("medical_conditions").insert({"name": cond_name, "description": cond_name}).execute()
                        condition_id = str(ins_cond.data[0]["condition_id"])

                    existing_pat_cond = (
                        client.table("patient_conditions")
                        .select("*")
                        .eq("patient_id", patient_id)
                        .eq("condition_id", condition_id)
                        .execute()
                    )
                    if not existing_pat_cond.data:
                        ins_pat_cond = client.table("patient_conditions").insert({
                            "patient_id": patient_id,
                            "condition_id": condition_id,
                            "status": "ACTIVE",
                            "severity": "Moderate",
                            "diagnosed_date": now_utc.strftime("%Y-%m-%d"),
                        }).execute()
                        updated_records.setdefault("conditions", []).append(ins_pat_cond.data[0])

        # C. Events
        events = findings_data.get("events", [])
        if isinstance(events, list):
            for ev in events:
                if isinstance(ev, dict) and ev.get("title"):
                    ins_ev = client.table("medical_events").insert({
                        "patient_id": patient_id,
                        "doctor_id": current_user.doctor_id,
                        "event_type": ev.get("event_type", "CONSULTATION"),
                        "event_date": ev.get("event_date") or now_utc.strftime("%Y-%m-%d"),
                        "title": ev["title"],
                        "description": ev.get("description", "Approved from document analysis"),
                        "severity": ev.get("severity", "MODERATE"),
                        "is_critical": bool(ev.get("is_critical", False)),
                        "status": "COMPLETED",
                        "source_document_id": document_id,
                    }).execute()
                    if ins_ev.data:
                        updated_records.setdefault("events", []).append(ins_ev.data[0])

    final_db_review_status = "APPROVED" if action in {"APPROVE", "MODIFY"} else "REJECTED"
    external_review_status = "MODIFIED" if action == "MODIFY" else final_db_review_status

    update_payload = {
        "review_status": final_db_review_status,
        "reviewed_by": current_user.doctor_id,
        "reviewed_at": now_utc.isoformat(),
    }
    if action == "MODIFY" and payload.modified_findings:
        update_payload["extracted_data"] = payload.modified_findings

    client.table("document_analysis").update(update_payload).eq("analysis_id", analysis_id).execute()

    action_msg = (
        "Doctor approved AI document analysis and authoritative records were updated."
        if action == "APPROVE"
        else "Doctor applied modified findings to authoritative medical records."
        if action == "MODIFY"
        else "Doctor rejected document analysis. Authoritative records remain unchanged."
    )

    log_audit_event(
        client=client,
        actor_id=current_user.user_id,
        actor_role="DOCTOR",
        patient_id=patient_id,
        action=f"REVIEW_ANALYSIS_{action}",
        access_type="NORMAL",
        entity_type="DOCUMENT_ANALYSIS",
        entity_id=analysis_id,
        reason=action_msg,
        details={"review_action": action, "updated_categories": list(updated_records.keys())},
    )

    return ReviewAnalysisResponse(
        analysis_id=analysis_id,
        document_id=document_id,
        patient_id=patient_id,
        review_status=external_review_status,
        reviewed_by=current_user.doctor_id,
        reviewed_at=now_utc.isoformat(),
        message=action_msg,
        updated_records=updated_records if updated_records else None,
    )


@router.post("/pipeline", response_model=AIPipelineResponse, summary="Execute complete end-to-end AI Pipeline")
def execute_ai_pipeline_endpoint(
    payload: AIPipelineRequest,
    current_user: AuthenticatedUser = Depends(require_doctor),
):
    """
    Full AI Pipeline:
    Document / Extracted Text -> NLU -> DB Comparison + Patient-Scoped RAG -> Clinical Synthesis & Doctor Report.
    Doctor remains the sole decision-maker for applying findings.
    """
    if not current_user.doctor_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Doctor profile not linked to authenticated user.",
        )

    client = get_supabase_service_client()
    patient_id = payload.patient_id

    # 1. Authorization check
    mode = get_doctor_access_mode(client, current_user.doctor_id, patient_id)
    if not mode:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Doctor does not have active access to this patient.",
        )

    # 2. Extract or fetch text
    extracted_text = payload.extracted_text or ""
    if not extracted_text and payload.document_id:
        doc_res = client.table("medical_documents").select("*").eq("document_id", payload.document_id).execute()
        if doc_res.data:
            extracted_text = doc_res.data[0].get("extracted_text") or doc_res.data[0].get("title", "")

    if not extracted_text:
        extracted_text = "Clinical progress evaluation and medical history review."

    # 3. NLU Extraction
    nlu_res = extract_nlu_findings(extracted_text, patient_id=patient_id)

    # 4. DB Context
    db_summary = get_consolidated_medical_summary(client, patient_id)
    db_dict = db_summary.model_dump()

    # 5. RAG Historical Query
    rag_res = extract_keywords_and_query_rag(
        client=client,
        doctor_id=current_user.doctor_id,
        patient_id=patient_id,
        extracted_text=extracted_text,
        max_sources=3,
    )

    # 6. Synthesize Doctor Clinical Report
    report_lines = [
        f"=== MEDITRACE CLINICAL AI PIPELINE REPORT ===",
        f"Patient ID: {patient_id} | Mode: {mode} | Date: {datetime.now(timezone.utc).strftime('%Y-%m-%d')}",
        "",
        f"1. NLU EXTRACTED FINDINGS (Suggestion Only):",
        f"   - Conditions: {len(nlu_res.findings.get('conditions', []))} extracted",
        f"   - Allergies: {len(nlu_res.findings.get('allergies', []))} extracted",
        f"   - Medications: {len(nlu_res.findings.get('medications', []))} extracted",
        f"   - Normalizations applied: {len(nlu_res.normalizations)} clinical abbreviations resolved",
        "",
        f"2. HISTORICAL EVIDENCE (RAG Retrieval):",
        f"   - Grounded Answer: {rag_res.answer}",
        f"   - Sources Cited: {len(rag_res.sources)} patient-scoped document(s)",
        "",
        f"3. CRITICAL FINDINGS & ALERTS:",
    ]

    for alert in nlu_res.critical_findings:
        report_lines.append(f"   [!] {alert}")

    if not nlu_res.critical_findings:
        report_lines.append("   - No immediate acute life-threatening conflicts detected.")

    report_lines.extend([
        "",
        "4. DOCTOR ACTION REQUIRED:",
        "   - Please review proposed findings above.",
        "   - Use POST /document-analysis/{analysis_id}/review to APPROVE, MODIFY, or REJECT before DB modification.",
    ])

    clinical_report = "\n".join(report_lines)

    recommended_actions = [
        "Review extracted allergy reactions against patient passport",
        "Confirm prescription dosages and schedule follow-up",
        "Verify critical surgical events with blockchain integrity ledger",
    ]

    log_audit_event(
        client=client,
        actor_id=current_user.user_id,
        actor_role="DOCTOR",
        patient_id=patient_id,
        action="AI_PIPELINE_EXECUTED",
        access_type=mode,
        entity_type="AI_PIPELINE",
        reason="Full AI clinical pipeline executed for patient",
        details={"sources_cited": len(rag_res.sources), "nlu_findings": len(nlu_res.findings)},
    )

    return AIPipelineResponse(
        patient_id=patient_id,
        document_id=payload.document_id,
        extracted_text=extracted_text,
        nlu_findings=nlu_res.findings,
        rag_historical_evidence={
            "answer": rag_res.answer,
            "sources": [s.model_dump() for s in rag_res.sources],
            "evidence_found": rag_res.evidence_found,
            "extracted_keywords": rag_res.extracted_keywords,
        },
        integrity_verification_results=[],
        comparison_with_db={
            "existing_allergies_count": len(db_dict.get("allergies", [])),
            "existing_conditions_count": len(db_dict.get("conditions", [])),
            "existing_medications_count": len(db_dict.get("medications", [])),
        },
        doctor_clinical_report=clinical_report,
        recommended_actions=recommended_actions,
        review_status="PENDING_DOCTOR_REVIEW",
    )
