import io
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.main import app
from app.services.supabase_service import get_supabase_service_client

client = TestClient(app)

# Seed test IDs
DOCTOR_ADITYA_EMAIL = "aditya.krishnan@meditrace.demo"
DOCTOR_ADITYA_PASS = "Doctor@123!"
DOCTOR_ADITYA_ID = "10000000-0000-0000-0000-000000000001"

KABIR_EMAIL = "kabir.malhotra@meditrace.demo"
KABIR_PASS = "Patient@123!"
KABIR_ID = "20000000-0000-0000-0000-000000000005"

TANYA_EMAIL = "tanya.bose@meditrace.demo"
TANYA_PASS = "Patient@123!"
TANYA_ID = "20000000-0000-0000-0000-000000000006"

NIKHIL_ID = "20000000-0000-0000-0000-000000000003"
AARAV_ID = "20000000-0000-0000-0000-000000000001"

SAMPLE_PDF_BYTES = (
    b"%PDF-1.4\n1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n"
    b"2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n"
    b"3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R >>\nendobj\n"
    b"4 0 obj\n<< /Length 120 >>\nstream\nBT\n/F1 12 Tf\n100 700 Td\n"
    b"(Patient with T2DM and prior MI. Prescribed Metformin 500mg BID and Atorvastatin 20mg OD.) Tj\n"
    b"ET\nendstream\nendobj\ntrailer\n<< /Root 1 0 R >>\n%%EOF"
)


def get_tokens():
    doc_res = client.post("/auth/login", json={"email": DOCTOR_ADITYA_EMAIL, "password": DOCTOR_ADITYA_PASS})
    assert doc_res.status_code == 200, f"Doctor login failed: {doc_res.text}"
    doc_token = doc_res.json()["access_token"]

    kabir_res = client.post("/auth/login", json={"email": KABIR_EMAIL, "password": KABIR_PASS})
    assert kabir_res.status_code == 200, f"Kabir login failed: {kabir_res.text}"
    kabir_token = kabir_res.json()["access_token"]

    tanya_res = client.post("/auth/login", json={"email": TANYA_EMAIL, "password": TANYA_PASS})
    assert tanya_res.status_code == 200, f"Tanya login failed: {tanya_res.text}"
    tanya_token = tanya_res.json()["access_token"]

    return {
        "doc_token": doc_token,
        "doc_headers": {"Authorization": f"Bearer {doc_token}"},
        "kabir_token": kabir_token,
        "kabir_headers": {"Authorization": f"Bearer {kabir_token}"},
        "tanya_token": tanya_token,
        "tanya_headers": {"Authorization": f"Bearer {tanya_token}"},
    }


def setup_clean_db():
    db = get_supabase_service_client()
    # Clean up break-glass or active access for Tanya to ensure fresh test state
    db.table("doctor_patient").delete().eq("doctor_id", DOCTOR_ADITYA_ID).eq("patient_id", TANYA_ID).execute()
    # Ensure active normal access for Kabir & Nikhil & Aarav
    db.table("doctor_patient").delete().eq("doctor_id", DOCTOR_ADITYA_ID).in_("patient_id", [KABIR_ID, NIKHIL_ID, AARAV_ID]).execute()
    db.table("doctor_patient").insert([
        {"doctor_id": DOCTOR_ADITYA_ID, "patient_id": KABIR_ID, "status": "ACTIVE", "relationship_type": "PRIMARY_CARE"},
        {"doctor_id": DOCTOR_ADITYA_ID, "patient_id": NIKHIL_ID, "status": "ACTIVE", "relationship_type": "PRIMARY_CARE"},
        {"doctor_id": DOCTOR_ADITYA_ID, "patient_id": AARAV_ID, "status": "ACTIVE", "relationship_type": "PRIMARY_CARE"},
    ]).execute()
    return db


# --------------------------------------------------------------------------
# TEST 1: Break-Glass Initiation by Doctor (200 OK)
# --------------------------------------------------------------------------
def test_01_break_glass_initiation_by_doctor():
    tokens = get_tokens()
    setup_clean_db()

    res = client.post(
        "/emergency/break-glass",
        headers=tokens["doc_headers"],
        json={
            "patient_id": TANYA_ID,
            "reason": "Acute intracranial hemorrhage requiring emergency craniotomy",
            "duration_hours": 4,
        },
    )
    assert res.status_code == 200, f"Break glass initiation failed: {res.text}"
    data = res.json()
    assert data["status"] == "ACTIVE"
    assert data["patient_id"] == TANYA_ID
    assert data["doctor_id"] == DOCTOR_ADITYA_ID
    assert any("CRITICAL" in s for s in data["allowed_scopes"])
    assert "RAG_HISTORICAL_QUERY" in data["allowed_scopes"]
    assert "INTEGRITY_VERIFICATION" in data["allowed_scopes"]
    assert data["expires_at"] is not None
    print("   [PASS] Test 1: Doctor initiated Break-Glass access 200 OK.")


# --------------------------------------------------------------------------
# TEST 2: Non-Doctor Break-Glass Initiation Rejection (403 Forbidden)
# --------------------------------------------------------------------------
def test_02_non_doctor_break_glass_forbidden():
    tokens = get_tokens()

    res = client.post(
        "/emergency/break-glass",
        headers=tokens["kabir_headers"],
        json={
            "patient_id": TANYA_ID,
            "reason": "Unauthorized patient attempting emergency break-glass",
        },
    )
    assert res.status_code == 403, f"Expected 403 for non-doctor, got {res.status_code}"
    print("   [PASS] Test 2: Non-doctor break-glass rejected 403 Forbidden.")


# --------------------------------------------------------------------------
# TEST 3: Break-Glass Doctor Reading Critical Emergency Data (200 OK)
# --------------------------------------------------------------------------
def test_03_break_glass_reading_critical_emergency_data():
    tokens = get_tokens()
    # Ensure active break-glass
    client.post(
        "/emergency/break-glass",
        headers=tokens["doc_headers"],
        json={
            "patient_id": TANYA_ID,
            "reason": "Emergency critical summary read test",
            "duration_hours": 2,
        },
    )

    res = client.get(
        f"/emergency/patient/{TANYA_ID}",
        headers=tokens["doc_headers"],
    )
    assert res.status_code == 200, f"Failed to get emergency summary: {res.text}"
    data = res.json()
    assert data["access_type"] == "BREAK_GLASS"
    assert data["profile"]["patient_id"] == TANYA_ID
    assert "EMERGENCY BREAK-GLASS" in data["disclaimer"]
    print("   [PASS] Test 3: Break-glass doctor retrieved emergency summary 200 OK.")


# --------------------------------------------------------------------------
# TEST 4: Break-Glass Write Rejection: Document Upload (403 Forbidden)
# --------------------------------------------------------------------------
def test_04_break_glass_write_rejection_document_upload():
    tokens = get_tokens()

    res = client.post(
        "/documents/upload",
        headers=tokens["doc_headers"],
        files={"file": ("test_doc.pdf", io.BytesIO(SAMPLE_PDF_BYTES), "application/pdf")},
        data={"patient_id": TANYA_ID, "document_type": "LAB_REPORT"},
    )
    assert res.status_code == 403, f"Expected 403 for break-glass upload, got {res.status_code}"
    assert "prohibited" in res.json()["detail"].lower() or "break-glass" in res.json()["detail"].lower()
    print("   [PASS] Test 4: Break-glass write rejection on document upload 403 Forbidden.")


# --------------------------------------------------------------------------
# TEST 5: Break-Glass Review Rejection: AI Findings Review (403 Forbidden)
# --------------------------------------------------------------------------
def test_05_break_glass_review_rejection():
    tokens = get_tokens()
    db = get_supabase_service_client()

    # Create dummy document analysis for Tanya
    fake_analysis_id = "80000000-0000-0000-0000-000000000099"
    db.table("document_analysis").delete().eq("analysis_id", fake_analysis_id).execute()
    db.table("document_analysis").insert({
        "analysis_id": fake_analysis_id,
        "document_id": "60000000-0000-0000-0000-000000000006",
        "patient_id": TANYA_ID,
        "extracted_data": {"allergies": [{"allergen": "Sulfa", "severity": "HIGH"}]},
        "analysis_status": "COMPLETED",
        "review_status": "PENDING",
    }).execute()

    res = client.post(
        f"/document-analysis/{fake_analysis_id}/review",
        headers=tokens["doc_headers"],
        json={"review_action": "APPROVE"},
    )
    assert res.status_code == 403, f"Expected 403 for break-glass review, got {res.status_code}"
    print("   [PASS] Test 5: Break-glass review/approval rejected 403 Forbidden.")


# --------------------------------------------------------------------------
# TEST 6: Expired Break-Glass Access Rejection (403 Forbidden)
# --------------------------------------------------------------------------
def test_06_expired_break_glass_access_rejected():
    tokens = get_tokens()
    db = get_supabase_service_client()

    # Expire Tanya's break-glass relationship in DB
    now = datetime.now(timezone.utc)
    started_past = (now - timedelta(hours=4)).isoformat()
    ended_past = (now - timedelta(hours=2)).isoformat()
    db.table("doctor_patient").update({
        "started_at": started_past,
        "ended_at": ended_past,
    }).eq("doctor_id", DOCTOR_ADITYA_ID).eq("patient_id", TANYA_ID).execute()

    res = client.get(
        f"/emergency/patient/{TANYA_ID}",
        headers=tokens["doc_headers"],
    )
    assert res.status_code == 403, f"Expected 403 for expired break-glass access, got {res.status_code}"
    print("   [PASS] Test 6: Expired break-glass access rejected 403 Forbidden.")


# --------------------------------------------------------------------------
# TEST 7: Break-Glass Explicit Termination
# --------------------------------------------------------------------------
def test_07_break_glass_explicit_termination():
    tokens = get_tokens()
    # Re-initiate break-glass
    client.post(
        "/emergency/break-glass",
        headers=tokens["doc_headers"],
        json={
            "patient_id": TANYA_ID,
            "reason": "Emergency stabilization procedure",
            "duration_hours": 2,
        },
    )

    # End break-glass session
    res = client.post(
        "/emergency/break-glass/end",
        headers=tokens["doc_headers"],
        json={
            "patient_id": TANYA_ID,
            "reason": "Patient stabilized and transferred to ICU",
        },
    )
    assert res.status_code == 200, f"End break glass failed: {res.text}"
    assert res.json()["status"] in {"ENDED", "CONCLUDED", "REVOKED"}

    # Verify subsequent access fails with 403
    post_res = client.get(
        f"/emergency/patient/{TANYA_ID}",
        headers=tokens["doc_headers"],
    )
    assert post_res.status_code == 403
    print("   [PASS] Test 7: Break-glass session explicitly concluded 200 OK, revoked access verified.")


# --------------------------------------------------------------------------
# TEST 8: Explicit OCR Endpoint (200 OK)
# --------------------------------------------------------------------------
def test_08_explicit_ocr_endpoint():
    tokens = get_tokens()

    res = client.post(
        "/ocr",
        headers=tokens["kabir_headers"],
        files={"file": ("prescription_note.pdf", io.BytesIO(SAMPLE_PDF_BYTES), "application/pdf")},
        data={"patient_id": KABIR_ID},
    )
    assert res.status_code == 200, f"OCR endpoint failed: {res.text}"
    data = res.json()
    assert data["ocr_status"] == "COMPLETED"
    assert data["char_count"] > 0
    assert data["word_count"] > 0
    assert "T2DM" in data["extracted_text"] or "Metformin" in data["extracted_text"]
    print("   [PASS] Test 8: Explicit OCR endpoint extracted text 200 OK.")


# --------------------------------------------------------------------------
# TEST 9: Explicit NLU Endpoint with Medical Normalization (200 OK)
# --------------------------------------------------------------------------
def test_09_explicit_nlu_endpoint_normalization():
    tokens = get_tokens()

    sample_text = (
        "Patient with confirmed T2DM and prior MI. "
        "Prescribed Metformin 500mg BID and Atorvastatin 20mg OD. "
        "Known severe Penicillin allergy causing anaphylaxis."
    )

    res = client.post(
        "/nlu",
        headers=tokens["kabir_headers"],
        json={
            "extracted_text": sample_text,
            "patient_id": KABIR_ID,
        },
    )
    assert res.status_code == 200, f"NLU endpoint failed: {res.text}"
    data = res.json()
    assert data["is_suggestion_only"] is True
    norms = data["normalizations"]
    norm_abbrs = {n.get("abbreviation") for n in norms if isinstance(n, dict)}
    assert bool(norm_abbrs.intersection({"T2DM", "BID", "MI", "OD"}))
    print(f"   [PASS] Test 9: Explicit NLU extracted findings with clinical normalizations: {norm_abbrs}")


# --------------------------------------------------------------------------
# TEST 10: NLU Suggestion-Only Guarantee (No Direct DB Mutation)
# --------------------------------------------------------------------------
def test_10_nlu_suggestion_only_no_db_mutations():
    tokens = get_tokens()
    db = get_supabase_service_client()

    allergies_before = db.table("patient_allergies").select("*").eq("patient_id", KABIR_ID).execute().data
    conditions_before = db.table("patient_conditions").select("*").eq("patient_id", KABIR_ID).execute().data

    # Execute NLU with novel medical assertions
    client.post(
        "/nlu",
        headers=tokens["kabir_headers"],
        json={
            "extracted_text": "Severe novel allergy to Peanut causing bronchospasm. Stage 4 Chronic Kidney Disease.",
            "patient_id": KABIR_ID,
        },
    )

    allergies_after = db.table("patient_allergies").select("*").eq("patient_id", KABIR_ID).execute().data
    conditions_after = db.table("patient_conditions").select("*").eq("patient_id", KABIR_ID).execute().data

    assert len(allergies_before) == len(allergies_after)
    assert len(conditions_before) == len(conditions_after)
    print("   [PASS] Test 10: NLU suggestion-only guarantee confirmed: 0 database mutations.")


# --------------------------------------------------------------------------
# TEST 11: Explicit RAG Keyword-Derived Extraction Query (200 OK)
# --------------------------------------------------------------------------
def test_11_explicit_rag_keyword_extraction_query():
    tokens = get_tokens()

    res = client.post(
        "/rag/extract-and-query",
        headers=tokens["doc_headers"],
        json={
            "patient_id": NIKHIL_ID,
            "extracted_text": "History of cardiac intervention, angioplasty, and stent in 2023.",
            "max_sources": 3,
        },
    )
    assert res.status_code == 200, f"RAG extract and query failed: {res.text}"
    data = res.json()
    assert data["evidence_found"] is True
    assert len(data["sources"]) > 0
    assert any("cardiac" in s["title"].lower() or "angioplasty" in s["title"].lower() for s in data["sources"])
    print(f"   [PASS] Test 11: Explicit RAG keyword-derived query retrieved {len(data['sources'])} grounded sources.")


# --------------------------------------------------------------------------
# TEST 12: RAG Strict Patient Isolation Verification
# --------------------------------------------------------------------------
def test_12_rag_patient_isolation():
    tokens = get_tokens()

    res = client.post(
        "/rag/query",
        headers=tokens["doc_headers"],
        json={
            "patient_id": AARAV_ID,
            "question": "What bone fracture surgery did Aarav undergo in 2023?",
            "max_sources": 5,
        },
    )
    assert res.status_code == 200, f"RAG query failed: {res.text}"
    data = res.json()
    for src in data["sources"]:
        assert src["patient_id"] == AARAV_ID, f"Patient isolation violated! Source belonged to {src['patient_id']} instead of {AARAV_ID}"
    print("   [PASS] Test 12: RAG patient isolation verified (100% Aarav sources, 0 cross-patient leaks).")


# --------------------------------------------------------------------------
# TEST 13: Full AI Pipeline Integration (200 OK)
# --------------------------------------------------------------------------
def test_13_full_ai_pipeline_integration():
    tokens = get_tokens()

    sample_report_text = (
        "Patient Nikhil Joshi follow-up evaluation. "
        "Reports occasional mild angina on exertion. "
        "Diagnosed with T2DM. Prescribed Metformin 500mg BID. "
        "History of coronary angioplasty with drug-eluting stent in 2023."
    )

    res = client.post(
        "/document-analysis/pipeline",
        headers=tokens["doc_headers"],
        json={
            "patient_id": NIKHIL_ID,
            "extracted_text": sample_report_text,
        },
    )
    assert res.status_code == 200, f"AI Pipeline execution failed: {res.text}"
    data = res.json()
    assert data["patient_id"] == NIKHIL_ID
    assert "nlu_findings" in data
    assert "rag_historical_evidence" in data
    assert "doctor_clinical_report" in data
    assert data["review_status"] == "PENDING_DOCTOR_REVIEW"
    assert len(data["recommended_actions"]) > 0
    print("   [PASS] Test 13: Full AI Pipeline executed (OCR/Text -> NLU -> DB Compare -> RAG -> Doctor Report).")


# --------------------------------------------------------------------------
# TEST 14: Integrity Verification Under Break-Glass Access (200 OK)
# --------------------------------------------------------------------------
def test_14_integrity_verification_under_break_glass():
    tokens = get_tokens()
    # Ensure active break-glass on Tanya
    client.post(
        "/emergency/break-glass",
        headers=tokens["doc_headers"],
        json={
            "patient_id": TANYA_ID,
            "reason": "Emergency integrity verification test",
            "duration_hours": 2,
        },
    )

    tanya_event_id = "70000000-0000-0000-0000-000000000012"
    res = client.post(
        f"/integrity/{tanya_event_id}/verify",
        headers=tokens["doc_headers"],
    )
    assert res.status_code == 200, f"Integrity verify under break-glass failed: {res.text}"
    data = res.json()
    assert data["verification_status"] in {"VERIFIED", "HISTORICAL RECORD MISSING", "NOT_ANCHORED", "TAMPERED_OR_MODIFIED"}
    print(f"   [PASS] Test 14: Integrity verification permitted under Break-Glass access (status: {data['verification_status']}).")


# --------------------------------------------------------------------------
# TEST 15: Complete Audit Trail Verification (200 OK & 403 Forbidden checks)
# --------------------------------------------------------------------------
def test_15_complete_audit_trail_verification():
    tokens = get_tokens()

    # 1. Patient self audit log retrieval
    pat_audit_res = client.get("/audit/me", headers=tokens["kabir_headers"])
    assert pat_audit_res.status_code == 200, f"Patient audit retrieval failed: {pat_audit_res.text}"
    pat_data = pat_audit_res.json()
    assert pat_data["patient_id"] == KABIR_ID
    assert pat_data["total_logs"] >= 1
    print(f"   [PASS] Test 15a: Patient self audit logs retrieved: {pat_data['total_logs']} entries.")

    # 2. Authorized Doctor retrieves patient audit logs
    doc_audit_res = client.get(f"/audit/patient/{KABIR_ID}", headers=tokens["doc_headers"])
    assert doc_audit_res.status_code == 200, f"Doctor audit retrieval failed: {doc_audit_res.text}"
    doc_data = doc_audit_res.json()
    assert doc_data["patient_id"] == KABIR_ID
    print(f"   [PASS] Test 15b: Doctor accessed authorized patient audit logs: {doc_data['total_logs']} entries.")

    # 3. Unauthorized Doctor audit retrieval -> 403 Forbidden
    # End break glass on Tanya so doctor has no access
    client.post("/emergency/break-glass/end", headers=tokens["doc_headers"], json={"patient_id": TANYA_ID, "reason": "End test"})
    unauth_audit = client.get(f"/audit/patient/{TANYA_ID}", headers=tokens["doc_headers"])
    assert unauth_audit.status_code == 403, f"Expected 403 for unauthorized audit query, got {unauth_audit.status_code}"
    print("   [PASS] Test 15c: Unauthorized audit query rejected 403 Forbidden.")


def run_all():
    print("=" * 80)
    print("RUNNING BACKEND TASK #6 TEST SUITE: EMERGENCY, OCR, NLU, RAG, PIPELINE & AUDIT")
    print("=" * 80 + "\n")

    test_01_break_glass_initiation_by_doctor()
    test_02_non_doctor_break_glass_forbidden()
    test_03_break_glass_reading_critical_emergency_data()
    test_04_break_glass_write_rejection_document_upload()
    test_05_break_glass_review_rejection()
    test_06_expired_break_glass_access_rejected()
    test_07_break_glass_explicit_termination()
    test_08_explicit_ocr_endpoint()
    test_09_explicit_nlu_endpoint_normalization()
    test_10_nlu_suggestion_only_no_db_mutations()
    test_11_explicit_rag_keyword_extraction_query()
    test_12_rag_patient_isolation()
    test_13_full_ai_pipeline_integration()
    test_14_integrity_verification_under_break_glass()
    test_15_complete_audit_trail_verification()

    print("\n" + "=" * 80)
    print("ALL TASK #6 INTEGRATION TESTS PASSED PERFECTLY (15/15)!")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    run_all()
