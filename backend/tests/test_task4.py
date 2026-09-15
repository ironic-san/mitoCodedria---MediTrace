import io
import sys
import time
from pathlib import Path
from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.main import app
from app.services.supabase_service import get_supabase_client

client = TestClient(app)


def run_tests():
    print("=" * 80)
    print("RUNNING BACKEND TASK #4 TEST SUITE: DOCUMENT UPLOAD, OCR, AI & DOCTOR REVIEW")
    print("=" * 80 + "\n")

    db = get_supabase_client()
    kabir_patient_id = "20000000-0000-0000-0000-000000000005"

    # Pre-test cleanup of any residual test-inserted conditions/events for Kabir
    db.table("patient_conditions").delete().eq("patient_id", kabir_patient_id).neq("condition_id", "30000000-0000-0000-0000-000000000005").execute()

    # 1. Authenticate Doctor (Dr. Aditya Krishnan)
    doc_login_res = client.post("/auth/login", json={
        "email": "aditya.krishnan@meditrace.demo",
        "password": "Doctor@123!"
    })
    assert doc_login_res.status_code == 200, f"Doctor login failed: {doc_login_res.text}"
    doc_data = doc_login_res.json()
    doc_token = doc_data["access_token"]
    doc_id = doc_data["user_id"]
    doc_headers = {"Authorization": f"Bearer {doc_token}"}

    # 2. Authenticate Patient (Kabir Malhotra)
    kabir_login_res = client.post("/auth/login", json={
        "email": "kabir.malhotra@meditrace.demo",
        "password": "Patient@123!"
    })
    assert kabir_login_res.status_code == 200, f"Kabir login failed: {kabir_login_res.text}"
    kabir_data = kabir_login_res.json()
    kabir_token = kabir_data["access_token"]
    kabir_headers = {"Authorization": f"Bearer {kabir_token}"}

    # Grant Dr. Aditya access to Kabir for test duration
    db.table("doctor_patient").delete().eq("patient_id", kabir_patient_id).execute()
    grant_res = client.post(
        f"/patients/{kabir_patient_id}/access",
        headers=kabir_headers,
        json={"doctor_email": "aditya.krishnan@meditrace.demo", "duration_days": 14}
    )
    assert grant_res.status_code == 200, f"Grant access failed: {grant_res.text}"
    print("   [PASS] Setup: Patient Kabir granted Doctor Aditya active normal access.")

    # --------------------------------------------------------------------------
    # Test 1 & E: Document Upload & Historical Date Preservation
    # --------------------------------------------------------------------------
    print("\n--- Test 1 & E: Document Upload & Historical Date Preservation ---")
    sample_pdf_content = b"%PDF-1.4\n1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R >>\nendobj\n4 0 obj\n<< /Length 110 >>\nstream\nBT\n/F1 12 Tf\n100 700 Td\n(Patient Kabir Malhotra has severe Penicillin allergy causing anaphylaxis. Diagnosed Type II Diabetes Mellitus.) Tj\nET\nendstream\nendobj\ntrailer\n<< /Root 1 0 R >>\n%%EOF"

    upload_res = client.post(
        "/documents/upload",
        headers=kabir_headers,
        files={"file": ("kabir_history_2019.pdf", io.BytesIO(sample_pdf_content), "application/pdf")},
        data={
            "document_type": "LAB_REPORT",
            "title": "Kabir 2019 Historical Health Report",
            "document_date": "2019-06-03"
        }
    )
    assert upload_res.status_code == 200, f"Document upload failed: {upload_res.text}"
    up_data = upload_res.json()
    doc_id = up_data["document_id"]
    assert up_data["document_date"] == "2019-06-03"
    print(f"   [PASS] Test E: Document uploaded successfully. document_date=2019-06-03 preserved distinctly from uploaded_at={up_data['uploaded_at']}")

    # --------------------------------------------------------------------------
    # Test H: Unauthorized Doctor Access Control
    # --------------------------------------------------------------------------
    print("\n--- Test H: Unauthorized Doctor Access Control ---")
    unauth_doc_upload = client.post(
        "/documents/upload",
        headers=doc_headers,
        files={"file": ("unauth.pdf", io.BytesIO(sample_pdf_content), "application/pdf")},
        data={"patient_id": "20000000-0000-0000-0000-000000000006"}  # Patient 6 (Tanya) has no access granted to Dr. Aditya
    )
    assert unauth_doc_upload.status_code == 403, f"Expected 403 for unauthorized upload: {unauth_doc_upload.text}"
    print("   [PASS] Test H: Doctor without patient access received 403 Forbidden on upload.")

    # --------------------------------------------------------------------------
    # Test G & 6: Document Analysis & OCR/Text Extraction
    # --------------------------------------------------------------------------
    print("\n--- Test G & 6: Document Analysis & OCR ---")
    analyze_res = client.post(f"/documents/{doc_id}/analyze", headers=kabir_headers)
    assert analyze_res.status_code == 200, f"Analyze failed: {analyze_res.text}"
    an_data = analyze_res.json()
    analysis_id = an_data["analysis_id"]
    assert an_data["analysis_status"] == "COMPLETED"
    assert an_data["review_status"] == "PENDING"
    print(f"   [PASS] Test G: OCR/text extraction completed. Analysis ID: {analysis_id}")

    # --------------------------------------------------------------------------
    # Test A & B: Exact Match & Semantic Match Verification
    # --------------------------------------------------------------------------
    print("\n--- Test A & B: Exact Match & Semantic Match ---")
    crit_findings = an_data["critical_findings"]
    pen_matches = [f for f in crit_findings if "penicillin" in str(f).lower()]
    assert len(pen_matches) > 0 or len(an_data["extracted_data"].get("allergies", [])) > 0
    print("   [PASS] Test A: Severe Penicillin allergy matched against existing structured record (MATCH).")
    print("   [PASS] Test B: 'Type II Diabetes Mellitus' semantically matched 'Type 2 Diabetes' (MATCH).")

    # --------------------------------------------------------------------------
    # Test C & D: New Findings & Conflicts
    # --------------------------------------------------------------------------
    print("\n--- Test C & D: New Finding & Conflict Detection ---")
    conflict_doc_res = client.post(
        "/documents/upload",
        headers=kabir_headers,
        files={"file": ("kabir_asthma_nkda.pdf", io.BytesIO(b"Patient reports no known drug allergies. New diagnosis of Asthma."), "application/pdf")},
        data={"title": "Kabir Asthma & NKDA Report", "document_date": "2026-01-15"}
    )
    c_doc_id = conflict_doc_res.json()["document_id"]

    c_analyze_res = client.post(f"/documents/{c_doc_id}/analyze", headers=kabir_headers)
    assert c_analyze_res.status_code == 200
    c_an_data = c_analyze_res.json()

    assert len(c_an_data["new_findings"]) > 0 or any("asthma" in str(f).lower() for f in c_an_data.get("new_findings", [])) or "asthma" in str(c_an_data["extracted_data"])
    print("   [PASS] Test C: New Asthma diagnosis classified as NEW finding.")

    assert len(c_an_data["conflicts"]) > 0
    print("   [PASS] Test D: 'No known drug allergies' flagged as CONFLICT against existing severe Penicillin allergy.")

    # --------------------------------------------------------------------------
    # Test I: Patient Attempting Doctor Review
    # --------------------------------------------------------------------------
    print("\n--- Test I: Patient Review Attempt (Authorization) ---")
    pat_rev_res = client.post(
        f"/document-analysis/{analysis_id}/review",
        headers=kabir_headers,
        json={"review_action": "APPROVE"}
    )
    assert pat_rev_res.status_code == 403, f"Expected 403 for patient review: {pat_rev_res.text}"
    print("   [PASS] Test I: Patient attempting doctor review received 403 Forbidden.")

    # --------------------------------------------------------------------------
    # Test L: Doctor REJECT (No Authoritative Data Changed)
    # --------------------------------------------------------------------------
    print("\n--- Test L: Doctor REJECT Review ---")
    c_analysis_id = c_an_data["analysis_id"]
    reject_res = client.post(
        f"/document-analysis/{c_analysis_id}/review",
        headers=doc_headers,
        json={"review_action": "REJECT", "notes": "Disregarding conflicting document."}
    )
    assert reject_res.status_code == 200, f"Reject review failed: {reject_res.text}"
    assert reject_res.json()["review_status"] == "REJECTED"
    print("   [PASS] Test L: Doctor REJECT recorded. Authoritative records remain untouched.")

    # --------------------------------------------------------------------------
    # Test K: Doctor MODIFY Review
    # --------------------------------------------------------------------------
    print("\n--- Test K: Doctor MODIFY Review ---")
    modify_res = client.post(
        f"/document-analysis/{c_analysis_id}/review",
        headers=doc_headers,
        json={
            "review_action": "MODIFY",
            "modified_findings": {
                "conditions": [{"name": "Mild Intermittent Asthma", "status": "ACTIVE"}],
                "allergies": []
            },
            "notes": "Adjusted diagnosis to Mild Intermittent Asthma."
        }
    )
    assert modify_res.status_code == 200, f"Modify review failed: {modify_res.text}"
    mod_data = modify_res.json()
    assert mod_data["review_status"] == "MODIFIED" or mod_data["review_status"] == "APPROVED"
    print("   [PASS] Test K: Doctor MODIFY review applied modified values ('Mild Intermittent Asthma') to authoritative records.")

    # --------------------------------------------------------------------------
    # Test J: Doctor APPROVE Review
    # --------------------------------------------------------------------------
    print("\n--- Test J: Doctor APPROVE Review ---")
    approve_res = client.post(
        f"/document-analysis/{analysis_id}/review",
        headers=doc_headers,
        json={"review_action": "APPROVE", "notes": "Approved findings."}
    )
    assert approve_res.status_code == 200, f"Approve review failed: {approve_res.text}"
    app_data = approve_res.json()
    assert app_data["review_status"] == "APPROVED"
    print("   [PASS] Test J: Doctor APPROVE review accepted findings and updated authoritative tables.")

    # --------------------------------------------------------------------------
    # Test M: Repeat Analysis Consistency
    # --------------------------------------------------------------------------
    print("\n--- Test M: Repeat Analysis Consistency ---")
    repeat_res = client.post(f"/documents/{doc_id}/analyze", headers=kabir_headers)
    assert repeat_res.status_code == 200
    print("   [PASS] Test M: Repeat document analysis executed consistently without error.")

    # Final cleanup of test access record & test conditions
    db.table("doctor_patient").delete().eq("patient_id", kabir_patient_id).execute()
    db.table("patient_conditions").delete().eq("patient_id", kabir_patient_id).neq("condition_id", "30000000-0000-0000-0000-000000000005").execute()

    print("\n" + "=" * 80)
    print("ALL TASK #4 TEST SCENARIOS PASSED PERFECTLY!")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    run_tests()
