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
    print("RUNNING BACKEND TASK #3 TEST SUITE: NORMAL PATIENT & DOCTOR ACCESS CONTROL")
    print("=" * 80 + "\n")

    # Clean up residual test access records for clean test run
    db = get_supabase_client()
    db.table("doctor_patient").delete().eq("patient_id", "20000000-0000-0000-0000-000000000005").execute()

    # Log in as Doctor (Dr. Aditya Krishnan)
    doc_login_res = client.post("/auth/login", json={
        "email": "aditya.krishnan@meditrace.demo",
        "password": "Doctor@123!"
    })
    assert doc_login_res.status_code == 200, f"Doctor login failed: {doc_login_res.text}"
    doc_data = doc_login_res.json()
    doc_token = doc_data["access_token"]
    doc_id = doc_data["user_id"]

    # Log in as Patient (Kabir Malhotra)
    kabir_login_res = client.post("/auth/login", json={
        "email": "kabir.malhotra@meditrace.demo",
        "password": "Patient@123!"
    })
    assert kabir_login_res.status_code == 200, f"Kabir login failed: {kabir_login_res.text}"
    kabir_data = kabir_login_res.json()
    kabir_token = kabir_data["access_token"]

    # Get Kabir's patient profile via /auth/me to verify patient_id
    kabir_me_res = client.get("/auth/me", headers={"Authorization": f"Bearer {kabir_token}"})
    assert kabir_me_res.status_code == 200
    kabir_patient_id = kabir_me_res.json()["patient_id"]
    print(f"Kabir Malhotra authenticated. Patient ID: {kabir_patient_id}")

    # Get Doctor Aditya profile via /doctors/me to verify doctor_id
    doc_me_res = client.get("/doctors/me", headers={"Authorization": f"Bearer {doc_token}"})
    assert doc_me_res.status_code == 200
    doctor_aditya_id = doc_me_res.json()["doctor_id"]
    print(f"Dr. Aditya Krishnan authenticated. Doctor ID: {doctor_aditya_id}\n")

    # -------------------------------------------------------------------------
    # TEST 1 & 2: Kabir -> GET /patients/me -> 200 OK & returns Kabir's patient_id
    # -------------------------------------------------------------------------
    print("Test 1 & 2: Kabir calling GET /patients/me...")
    p_me_res = client.get("/patients/me", headers={"Authorization": f"Bearer {kabir_token}"})
    assert p_me_res.status_code == 200, f"Failed GET /patients/me: {p_me_res.text}"
    me_data = p_me_res.json()
    assert me_data["profile"]["patient_id"] == kabir_patient_id
    assert me_data["profile"]["full_name"] == "Kabir Malhotra"
    print(f"   [PASS] 200 OK. Passport retrieved for {me_data['profile']['full_name']} ({me_data['profile']['patient_id']})")
    print(f"   Allergies count: {len(me_data['allergies'])}, Conditions count: {len(me_data['conditions'])}")

    # -------------------------------------------------------------------------
    # TEST 3: Doctor Aditya -> GET /patients/me -> 403 Forbidden
    # -------------------------------------------------------------------------
    print("Test 3: Doctor Aditya calling GET /patients/me...")
    doc_p_me_res = client.get("/patients/me", headers={"Authorization": f"Bearer {doc_token}"})
    assert doc_p_me_res.status_code == 403, f"Expected 403, got {doc_p_me_res.status_code}"
    print(f"   [PASS] 403 Forbidden ({doc_p_me_res.json()['detail']})")

    # -------------------------------------------------------------------------
    # TEST 4: Doctor Aditya without patient access -> GET /patients/{Kabir}/medical-summary -> 403
    # -------------------------------------------------------------------------
    print("Test 4: Doctor Aditya accessing Kabir's medical-summary without access...")
    no_acc_summary = client.get(f"/patients/{kabir_patient_id}/medical-summary", headers={"Authorization": f"Bearer {doc_token}"})
    print(f"   Response status: {no_acc_summary.status_code}, detail: {no_acc_summary.json().get('detail')}")
    assert no_acc_summary.status_code == 403
    print("   [PASS] 403 Forbidden")

    # -------------------------------------------------------------------------
    # TEST 5 & 10: Kabir grants Doctor Aditya normal access with custom duration (e.g. 14 days)
    # -------------------------------------------------------------------------
    print("Test 5 & 10: Kabir granting Doctor Aditya 14 days normal access...")
    grant_res = client.post(
        f"/patients/{kabir_patient_id}/access",
        headers={"Authorization": f"Bearer {kabir_token}"},
        json={"doctor_id": doctor_aditya_id, "duration_days": 14}
    )
    assert grant_res.status_code == 200, f"Failed to grant access: {grant_res.text}"
    grant_data = grant_res.json()
    access_id = grant_data["access_id"]
    print(f"   [PASS] Access granted successfully. Access ID: {access_id}, Status: {grant_data['status']}, Expires: {grant_data['expires_at']}")
    assert grant_data["status"] == "ACTIVE"
    assert grant_data["doctor_id"] == doctor_aditya_id

    # -------------------------------------------------------------------------
    # TEST 6: Doctor Aditya with active access -> GET /patients/{Kabir}/medical-summary -> 200
    # -------------------------------------------------------------------------
    print("Test 6: Doctor Aditya accessing Kabir's medical-summary with active access...")
    has_acc_summary = client.get(f"/patients/{kabir_patient_id}/medical-summary", headers={"Authorization": f"Bearer {doc_token}"})
    assert has_acc_summary.status_code == 200, f"Doctor access failed: {has_acc_summary.text}"
    summary_json = has_acc_summary.json()
    assert summary_json["profile"]["patient_id"] == kabir_patient_id
    print(f"   [PASS] 200 OK. Summary retrieved: {summary_json['profile']['full_name']} (Penicillin Allergy: {any(a['allergen'] == 'Penicillin' for a in summary_json['allergies'])})")

    # -------------------------------------------------------------------------
    # TEST 7: Doctor Aditya sees Kabir in GET /doctors/patients
    # -------------------------------------------------------------------------
    print("Test 7: Doctor Aditya listing accessible patients via GET /doctors/patients...")
    doc_pats_res = client.get("/doctors/patients", headers={"Authorization": f"Bearer {doc_token}"})
    assert doc_pats_res.status_code == 200
    pats_list = doc_pats_res.json()
    kabir_found = any(p["patient_id"] == kabir_patient_id for p in pats_list)
    assert kabir_found, f"Kabir not found in doctor's accessible list: {pats_list}"
    print(f"   [PASS] 200 OK. Doctor's accessible patient list contains Kabir ({len(pats_list)} total active patients)")

    # -------------------------------------------------------------------------
    # TEST 18 & 20: Document Access (Patient & Authorized Doctor)
    # -------------------------------------------------------------------------
    print("Test 18 & 20: Testing Document Access for Patient & Authorized Doctor...")
    kabir_docs = summary_json.get("medical_events", [])
    doc_id_to_test = None
    for ev in kabir_docs:
        if ev.get("source_document_id"):
            doc_id_to_test = ev["source_document_id"]
            break

    if not doc_id_to_test:
        doc_id_to_test = "60000000-0000-0000-0000-000000000005"

    print(f"   Testing document_id: {doc_id_to_test}")
    # Patient access own document
    pat_doc_acc = client.get(f"/documents/{doc_id_to_test}/access", headers={"Authorization": f"Bearer {kabir_token}"})
    assert pat_doc_acc.status_code == 200, f"Patient document access failed: {pat_doc_acc.text}"
    print(f"   [PASS] Test 20: Patient accessed own document 200 OK ({pat_doc_acc.json()['title']})")

    # Authorized Doctor access patient's document
    doc_doc_acc = client.get(f"/documents/{doc_id_to_test}/access", headers={"Authorization": f"Bearer {doc_token}"})
    assert doc_doc_acc.status_code == 200, f"Authorized doctor document access failed: {doc_doc_acc.text}"
    print(f"   [PASS] Test 18: Authorized Doctor accessed patient document 200 OK")

    # -------------------------------------------------------------------------
    # TEST 8: Kabir revokes Aditya's access -> Aditya immediately receives 403
    # -------------------------------------------------------------------------
    print("Test 8: Kabir revoking Doctor Aditya's access...")
    revoke_res = client.delete(f"/patients/{kabir_patient_id}/access/{access_id}", headers={"Authorization": f"Bearer {kabir_token}"})
    assert revoke_res.status_code == 200, f"Revocation failed: {revoke_res.text}"
    print(f"   [PASS] Revoked. {revoke_res.json()['message']}")

    print("   Verifying immediate 403 for Doctor Aditya after revocation...")
    post_revoke_summary = client.get(f"/patients/{kabir_patient_id}/medical-summary", headers={"Authorization": f"Bearer {doc_token}"})
    assert post_revoke_summary.status_code == 403, f"Expected 403 after revocation, got {post_revoke_summary.status_code}"
    print(f"   [PASS] 403 Forbidden after revocation ({post_revoke_summary.json()['detail']})")

    # -------------------------------------------------------------------------
    # TEST 19: Unauthorized doctor accessing document after revocation -> 403
    # -------------------------------------------------------------------------
    print("Test 19: Doctor Aditya accessing document after revocation...")
    doc_doc_acc_rev = client.get(f"/documents/{doc_id_to_test}/access", headers={"Authorization": f"Bearer {doc_token}"})
    assert doc_doc_acc_rev.status_code == 403
    print("   [PASS] 403 Forbidden")

    # -------------------------------------------------------------------------
    # TEST 11 & 12: Doctor cannot grant himself access or extend access
    # -------------------------------------------------------------------------
    print("Test 11 & 12: Doctor trying to grant himself access via POST /patients/{Kabir}/access...")
    doc_self_grant = client.post(
        f"/patients/{kabir_patient_id}/access",
        headers={"Authorization": f"Bearer {doc_token}"},
        json={"doctor_id": doctor_aditya_id, "duration_days": 30}
    )
    assert doc_self_grant.status_code == 403, f"Expected 403 for doctor self grant, got {doc_self_grant.status_code}"
    print(f"   [PASS] 403 Forbidden ({doc_self_grant.json()['detail']})")

    # -------------------------------------------------------------------------
    # TEST 13: Patient cannot grant access for another patient
    # -------------------------------------------------------------------------
    print("Test 13: Kabir trying to grant access for another patient (Aarav)...")
    aarav_id = "20000000-0000-0000-0000-000000000001"
    kabir_grant_aarav = client.post(
        f"/patients/{aarav_id}/access",
        headers={"Authorization": f"Bearer {kabir_token}"},
        json={"doctor_id": doctor_aditya_id, "duration_days": 7}
    )
    assert kabir_grant_aarav.status_code == 403
    print(f"   [PASS] 403 Forbidden ({kabir_grant_aarav.json()['detail']})")

    # -------------------------------------------------------------------------
    # TEST 14 & 15: Patient cannot access another patient's data & Doctor without access cannot
    # -------------------------------------------------------------------------
    print("Test 14: Kabir trying to access Aarav's medical-summary...")
    kabir_view_aarav = client.get(f"/patients/{aarav_id}/medical-summary", headers={"Authorization": f"Bearer {kabir_token}"})
    assert kabir_view_aarav.status_code == 403
    print("   [PASS] 403 Forbidden")

    print("Test 15: Doctor Aditya trying to access Tanya's medical-summary without access...")
    tanya_id = "20000000-0000-0000-0000-000000000006"
    doc_view_tanya = client.get(f"/patients/{tanya_id}/medical-summary", headers={"Authorization": f"Bearer {doc_token}"})
    assert doc_view_tanya.status_code == 403
    print("   [PASS] 403 Forbidden")

    # -------------------------------------------------------------------------
    # TEST 16: Unauthenticated requests -> 401
    # -------------------------------------------------------------------------
    print("Test 16: Unauthenticated request to /patients/me...")
    unauth_res = client.get("/patients/me")
    assert unauth_res.status_code == 401
    print("   [PASS] 401 Unauthorized")

    # -------------------------------------------------------------------------
    # TEST 17: Nonexistent patient -> 404
    # -------------------------------------------------------------------------
    print("Test 17: Accessing non-existent patient ID...")
    bogus_id = "00000000-0000-0000-0000-000000000000"
    nonexist_res = client.get(f"/patients/{bogus_id}/medical-summary", headers={"Authorization": f"Bearer {kabir_token}"})
    assert nonexist_res.status_code == 404
    print(f"   [PASS] 404 Not Found ({nonexist_res.json()['detail']})")

    # -------------------------------------------------------------------------
    # TEST 21: Verify /patients/me cannot be manipulated with URL parameters
    # -------------------------------------------------------------------------
    print("Test 21: Verifying /patients/me ignores URL parameter manipulation...")
    manip_res = client.get(f"/patients/me?patient_id={aarav_id}", headers={"Authorization": f"Bearer {kabir_token}"})
    assert manip_res.status_code == 200
    assert manip_res.json()["profile"]["patient_id"] == kabir_patient_id
    print("   [PASS] 200 OK. Returned authenticated user's profile (Kabir), ignoring query parameter")

    # Clean up test access record
    db.table("doctor_patient").delete().eq("patient_id", "20000000-0000-0000-0000-000000000005").execute()

    print("\n" + "=" * 80)
    print("ALL TASK #3 TEST SCENARIOS PASSED PERFECTLY!")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    run_tests()
