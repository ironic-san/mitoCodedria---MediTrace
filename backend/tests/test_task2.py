import sys
from pathlib import Path
from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.main import app

client = TestClient(app)

def run_tests():
    print("=" * 80)
    print("RUNNING BACKEND TASK #2 AUTHENTICATION & AUTHORIZATION TESTS")
    print("=" * 80 + "\n")

    # 1. Login as Doctor (Dr. Aditya Krishnan)
    print("1. Testing Doctor Authentication...")
    doc_login_res = client.post("/auth/login", json={
        "email": "aditya.krishnan@meditrace.demo",
        "password": "Doctor@123!"
    })
    assert doc_login_res.status_code == 200, f"Doctor login failed: {doc_login_res.text}"
    doc_data = doc_login_res.json()
    doc_token = doc_data["access_token"]
    print(f"   [SUCCESS] Doctor logged in. User ID: {doc_data.get('user_id')}, Role: {doc_data.get('role')}")

    # 2. Doctor GET /auth/me
    print("2. Testing Doctor GET /auth/me...")
    doc_me_res = client.get("/auth/me", headers={"Authorization": f"Bearer {doc_token}"})
    assert doc_me_res.status_code == 200, f"/auth/me failed for doctor: {doc_me_res.text}"
    doc_me_data = doc_me_res.json()
    print(f"   [SUCCESS] Doctor /auth/me: Role={doc_me_data['role']}, doctor_id={doc_me_data['doctor_id']}, Name={doc_me_data['full_name']}")
    assert doc_me_data["role"] == "DOCTOR"
    assert doc_me_data["doctor_id"] is not None
    assert doc_me_data["patient_id"] is None

    # 3. Login as Patient (Kabir Malhotra)
    print("3. Testing Patient Authentication...")
    pat_login_res = client.post("/auth/login", json={
        "email": "kabir.malhotra@meditrace.demo",
        "password": "Patient@123!"
    })
    assert pat_login_res.status_code == 200, f"Patient login failed: {pat_login_res.text}"
    pat_data = pat_login_res.json()
    pat_token = pat_data["access_token"]
    print(f"   [SUCCESS] Patient logged in. User ID: {pat_data.get('user_id')}, Role: {pat_data.get('role')}")

    # 4. Patient GET /auth/me
    print("4. Testing Patient GET /auth/me...")
    pat_me_res = client.get("/auth/me", headers={"Authorization": f"Bearer {pat_token}"})
    assert pat_me_res.status_code == 200, f"/auth/me failed for patient: {pat_me_res.text}"
    pat_me_data = pat_me_res.json()
    print(f"   [SUCCESS] Patient /auth/me: Role={pat_me_data['role']}, patient_id={pat_me_data['patient_id']}, Name={pat_me_data['full_name']}")
    assert pat_me_data["role"] == "PATIENT"
    assert pat_me_data["patient_id"] is not None
    assert pat_me_data["doctor_id"] is None

    # 5. Test Missing Token -> 401
    print("5. Testing Missing Authorization Token...")
    no_token_res = client.get("/auth/me")
    print(f"   Response status: {no_token_res.status_code}, detail: {no_token_res.json().get('detail')}")
    assert no_token_res.status_code == 401

    # 6. Test Invalid Token -> 401
    print("6. Testing Invalid Authorization Token...")
    invalid_token_res = client.get("/auth/me", headers={"Authorization": "Bearer invalid.jwt.signature_fake"})
    print(f"   Response status: {invalid_token_res.status_code}, detail: {invalid_token_res.json().get('detail')}")
    assert invalid_token_res.status_code == 401

    # 7. Test Doctor accessing /auth/patient-only -> 403 (Doctor cannot satisfy require_patient)
    print("7. Testing Doctor accessing require_patient() route...")
    doc_pat_only_res = client.get("/auth/patient-only", headers={"Authorization": f"Bearer {doc_token}"})
    print(f"   Response status: {doc_pat_only_res.status_code}, detail: {doc_pat_only_res.json().get('detail')}")
    assert doc_pat_only_res.status_code == 403

    # 8. Test Patient accessing /auth/doctor-only -> 403 (Patient cannot satisfy require_doctor)
    print("8. Testing Patient accessing require_doctor() route...")
    pat_doc_only_res = client.get("/auth/doctor-only", headers={"Authorization": f"Bearer {pat_token}"})
    print(f"   Response status: {pat_doc_only_res.status_code}, detail: {pat_doc_only_res.json().get('detail')}")
    assert pat_doc_only_res.status_code == 403

    # 9. Test Doctor accessing /auth/doctor-only -> 200
    print("9. Testing Doctor accessing require_doctor() route...")
    doc_doc_only_res = client.get("/auth/doctor-only", headers={"Authorization": f"Bearer {doc_token}"})
    assert doc_doc_only_res.status_code == 200
    print(f"   [SUCCESS] Status: {doc_doc_only_res.status_code}, payload: {doc_doc_only_res.json()}")

    # 10. Test Patient accessing /auth/patient-only -> 200
    print("10. Testing Patient accessing require_patient() route...")
    pat_pat_only_res = client.get("/auth/patient-only", headers={"Authorization": f"Bearer {pat_token}"})
    assert pat_pat_only_res.status_code == 200
    print(f"   [SUCCESS] Status: {pat_pat_only_res.status_code}, payload: {pat_pat_only_res.json()}")

    print("\n" + "=" * 80)
    print("ALL TASK #2 TEST SCENARIOS PASSED PERFECTLY!")
    print("=" * 80 + "\n")

if __name__ == "__main__":
    run_tests()
