import sys
from pathlib import Path
from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.main import app
from app.services.supabase_service import get_supabase_service_client
from app.utils.canonicalization import canonicalize_medical_event, hash_canonical_string, canonicalize_and_hash_event
from app.services.blockchain_service import get_blockchain_service

client = TestClient(app)


def run_tests():
    print("=" * 80)
    print("RUNNING BACKEND TASK #5 TEST SUITE: RAG, INTEGRITY & HYPERLEDGER FABRIC")
    print("=" * 80 + "\n")

    db = get_supabase_service_client()

    # Known Patient IDs from Seed Data:
    # Aarav: 20000000-0000-0000-0000-000000000001
    # Ishita: 20000000-0000-0000-0000-000000000002
    # Nikhil: 20000000-0000-0000-0000-000000000003
    # Diya: 20000000-0000-0000-0000-000000000004
    # Kabir: 20000000-0000-0000-0000-000000000005
    # Tanya: 20000000-0000-0000-0000-000000000006

    # Log in as Doctor (Dr. Aditya Krishnan)
    doc_login_res = client.post("/auth/login", json={
        "email": "aditya.krishnan@meditrace.demo",
        "password": "Doctor@123!"
    })
    assert doc_login_res.status_code == 200, f"Doctor login failed: {doc_login_res.text}"
    doc_data = doc_login_res.json()
    doc_token = doc_data["access_token"]
    doctor_id = doc_data.get("doctor_id") or "10000000-0000-0000-0000-000000000001"
    doc_headers = {"Authorization": f"Bearer {doc_token}"}

    # Log in as Patient (Kabir Malhotra)
    kabir_login_res = client.post("/auth/login", json={
        "email": "kabir.malhotra@meditrace.demo",
        "password": "Patient@123!"
    })
    assert kabir_login_res.status_code == 200
    kabir_data = kabir_login_res.json()
    kabir_token = kabir_data["access_token"]
    kabir_headers = {"Authorization": f"Bearer {kabir_token}"}

    # Grant Dr. Aditya access to Kabir (Patient 5), Nikhil (Patient 3), and Aarav (Patient 1) for testing
    kabir_id = "20000000-0000-0000-0000-000000000005"
    nikhil_id = "20000000-0000-0000-0000-000000000003"
    aarav_id = "20000000-0000-0000-0000-000000000001"
    tanya_id = "20000000-0000-0000-0000-000000000006"

    client.post(f"/patients/{kabir_id}/access", json={"doctor_id": doctor_id, "duration_days": 14}, headers=kabir_headers)
    
    # Direct DB access grant for Nikhil & Aarav (demo setup)
    db.table("doctor_patient").delete().eq("doctor_id", doctor_id).in_("patient_id", [nikhil_id, aarav_id]).execute()
    db.table("doctor_patient").insert([
        {"doctor_id": doctor_id, "patient_id": nikhil_id, "status": "ACTIVE", "relationship_type": "PRIMARY_CARE"},
        {"doctor_id": doctor_id, "patient_id": aarav_id, "status": "ACTIVE", "relationship_type": "PRIMARY_CARE"},
    ]).execute()

    print("--- PART A: HISTORICAL MEDICAL RAG TESTS ---\n")

    # TEST 1: Doctor queries authorized patient's history (Nikhil cardiac intervention)
    print("Test 1: Doctor querying Nikhil's 2023 cardiac intervention...")
    rag_res = client.post("/rag/query", json={
        "patient_id": nikhil_id,
        "question": "What major cardiac intervention did Nikhil undergo in 2023?"
    }, headers=doc_headers)
    assert rag_res.status_code == 200, f"RAG query failed: {rag_res.text}"
    rag_data = rag_res.json()
    print(f"   [PASS] 200 OK. Answer: {rag_data['answer'][:110]}...")
    print(f"   Sources count: {len(rag_data['sources'])}")
    assert rag_data["evidence_found"] is True
    assert len(rag_data["sources"]) > 0
    assert any("angioplasty" in s["title"].lower() or "cardiac" in s["title"].lower() for s in rag_data["sources"])
    assert "angioplasty" in rag_data["answer"].lower() or "myocardial" in rag_data["answer"].lower() or "stent" in rag_data["answer"].lower()

    # TEST 2: Unauthorized doctor query on patient without access (Tanya) -> 403 Forbidden
    print("\nTest 2: Doctor querying Tanya's history without active access...")
    unauth_rag = client.post("/rag/query", json={
        "patient_id": tanya_id,
        "question": "What brain surgery did the patient undergo?"
    }, headers=doc_headers)
    print(f"   Response status: {unauth_rag.status_code}, detail: {unauth_rag.json().get('detail')}")
    assert unauth_rag.status_code == 403, "Expected 403 Forbidden for unauthorized doctor"
    print("   [PASS] 403 Forbidden enforced correctly.")

    # TEST 3: Patient attempting to use doctor RAG endpoint -> 403 Forbidden
    print("\nTest 3: Patient attempting to call doctor /rag/query endpoint...")
    pat_rag = client.post("/rag/query", json={
        "patient_id": kabir_id,
        "question": "What is my allergy history?"
    }, headers=kabir_headers)
    print(f"   Response status: {pat_rag.status_code}, detail: {pat_rag.json().get('detail')}")
    assert pat_rag.status_code == 403, "Expected 403 Forbidden for non-doctor"
    print("   [PASS] 403 Forbidden enforced for non-doctor role.")

    # TEST 4: Patient isolation: Aarav's RAG query MUST NOT return Nikhil's or Tanya's records
    print("\nTest 4: Strict patient isolation (Aarav femur fracture query)...")
    aarav_rag = client.post("/rag/query", json={
        "patient_id": aarav_id,
        "question": "What bone fracture and surgery did Aarav have in 2023?"
    }, headers=doc_headers)
    assert aarav_rag.status_code == 200
    aarav_data = aarav_rag.json()
    print(f"   [PASS] Aarav RAG Answer: {aarav_data['answer'][:110]}...")
    # Verify every returned source belongs STRICTLY to Aarav
    for src in aarav_data["sources"]:
        assert src["patient_id"] == aarav_id, f"Cross-patient leak detected! Source patient_id {src['patient_id']} != {aarav_id}"
        print(f"   Source verified: {src['title']} (patient_id: {src['patient_id']})")
    assert "femur" in aarav_data["answer"].lower() or "fracture" in aarav_data["answer"].lower() or "fixation" in aarav_data["answer"].lower()

    # TEST 5 & 6: Source attribution format
    print("\nTest 5 & 6: Verifying source attribution metadata...")
    top_source = aarav_data["sources"][0]
    assert "document_id" in top_source and top_source["document_id"]
    assert "title" in top_source and top_source["title"]
    assert "chunk_text" in top_source and top_source["chunk_text"]
    assert "similarity_score" in top_source and top_source["similarity_score"] > 0
    print(f"   [PASS] Top source: '{top_source['title']}' | Date: {top_source['document_date']} | Score: {top_source['similarity_score']}")

    # TEST 7: Query with no evidence in records -> does not fabricate facts
    print("\nTest 7: Querying nonexistent medical topic (kidney transplant for Aarav)...")
    no_ev_res = client.post("/rag/query", json={
        "patient_id": aarav_id,
        "question": "When was the patient's bilateral kidney transplant and dialysis performed?"
    }, headers=doc_headers)
    assert no_ev_res.status_code == 200
    no_ev_data = no_ev_res.json()
    print(f"   [PASS] No-evidence response: evidence_found={no_ev_data['evidence_found']}, answer='{no_ev_data['answer']}'")
    assert no_ev_data["evidence_found"] is False or len(no_ev_data["sources"]) == 0 or "no relevant" in no_ev_data["answer"].lower()

    # TEST 8: RAG works independently of live OCR
    print("\nTest 8: RAG standalone query without live document upload...")
    kabir_rag = client.post("/rag/query", json={
        "patient_id": kabir_id,
        "question": "What severe drug allergy does Kabir have?"
    }, headers=doc_headers)
    assert kabir_rag.status_code == 200
    assert "penicillin" in kabir_rag.json()["answer"].lower()
    print(f"   [PASS] Standalone RAG returned: {kabir_rag.json()['answer'][:100]}...")

    print("\n" + "-" * 80)
    print("--- PART B: CRITICAL RECORD INTEGRITY & HYPERLEDGER FABRIC TESTS ---")
    print("-" * 80 + "\n")

    # TEST 9 & 10: Canonicalization & Deterministic SHA-256 Hashing
    print("Test 9 & 10: Canonicalization and SHA-256 deterministic hashing...")
    sample_event = {
        "event_id": "70000000-0000-0000-0000-000000000001",
        "patient_id": "20000000-0000-0000-0000-000000000001",
        "event_type": "DIAGNOSIS",
        "event_date": "2023-06-14T00:00:00+00:00",
        "title": "Left Femur Fracture",
        "description": "Road accident resulted in a closed left femur fracture.",
        "severity": "SEVERE",
        "is_critical": True,
        "version": 1
    }
    canon_str, h1 = canonicalize_and_hash_event(sample_event)
    canon_str2, h2 = canonicalize_and_hash_event(sample_event)
    assert h1 == h2, "Hashing must be 100% deterministic"
    assert len(h1) == 64, "SHA-256 hex digest length must be 64 chars"
    print(f"   [PASS] Canonical SHA-256: {h1}")

    # TEST 11: Blockchain proof creation / anchoring
    print("\nTest 11: Anchoring critical event to Hyperledger Fabric adapter...")
    anchor_res = client.post("/integrity/anchor", json={
        "event_id": "70000000-0000-0000-0000-000000000001",
        "notes": "Verified orthopedic trauma diagnosis"
    }, headers=doc_headers)
    assert anchor_res.status_code == 200, f"Anchor failed: {anchor_res.text}"
    anchor_data = anchor_res.json()
    print(f"   [PASS] Anchored! Tx ID: {anchor_data['blockchain_tx_id']} | Block: {anchor_data['block_number']}")
    assert anchor_data["verification_status"] == "VERIFIED"
    assert anchor_data["blockchain_tx_id"].startswith("fabric-tx-")

    # TEST 12: Matching current record returns VERIFIED
    print("\nTest 12: Verifying anchored event matches current DB record...")
    ver_res = client.post("/integrity/70000000-0000-0000-0000-000000000001/verify", headers=doc_headers)
    assert ver_res.status_code == 200, f"Verify failed: {ver_res.text}"
    ver_data = ver_res.json()
    print(f"   [PASS] Verification status: {ver_data['verification_status']}")
    print(f"   Block Number: {ver_data['block_number']}, Tx ID: {ver_data['blockchain_tx_id']}")
    assert ver_data["verification_status"] == "VERIFIED"
    assert ver_data["current_hash"] is not None

    # TEST 13: Modified / tampered current record fails verification (TAMPERED_OR_MODIFIED)
    print("\nTest 13: Verifying tampered record fails verification...")
    # Temporarily tamper with event title in database
    db.table("medical_events").update({"title": "TAMPERED: Minor Knee Bruise"}).eq("event_id", "70000000-0000-0000-0000-000000000001").execute()
    try:
        tamper_ver = client.post("/integrity/70000000-0000-0000-0000-000000000001/verify", headers=doc_headers)
        assert tamper_ver.status_code == 200
        t_data = tamper_ver.json()
        print(f"   Tampered record verification status: {t_data['verification_status']}")
        assert t_data["verification_status"] == "TAMPERED_OR_MODIFIED"
        print("   [PASS] Detected TAMPERED_OR_MODIFIED correctly.")
    finally:
        # Restore original title and re-anchor
        db.table("medical_events").update({"title": "Left Femur Fracture"}).eq("event_id", "70000000-0000-0000-0000-000000000001").execute()
        client.post("/integrity/anchor", json={"event_id": "70000000-0000-0000-0000-000000000001"}, headers=doc_headers)

    # TEST 14 & 15: Kabir Demo: Simulating tombstoned DB record with anchored Fabric proof...
    # Fabric blockchain history is NOT deleted
    print("\nTest 14 & 15: Kabir Demo: Simulating tombstoned DB record with anchored Fabric proof...")
    kabir_event_id = "70000000-0000-0000-0000-000000000010"
    # Anchor Kabir's Penicillin allergy first
    client.post("/integrity/anchor", json={"event_id": kabir_event_id}, headers=doc_headers)

    # Tombstone Kabir's event in medical_events
    db.table("medical_events").update({"status": "TOMBSTONED"}).eq("event_id", kabir_event_id).execute()

    try:
        miss_res = client.post(f"/integrity/{kabir_event_id}/verify", headers=doc_headers)
        assert miss_res.status_code == 200, f"Missing record verify failed: {miss_res.text}"
        m_data = miss_res.json()
        print(f"   Verification Status: {m_data['verification_status']}")
        print(f"   Message: {m_data['message']}")
        print(f"   Anchored Hash preserved: {m_data['anchored_hash']}")
        print(f"   Blockchain Tx ID preserved: {m_data['blockchain_tx_id']}")
        assert m_data["verification_status"] == "HISTORICAL RECORD MISSING"
        assert m_data["anchored_hash"] is not None
        assert m_data["blockchain_tx_id"] is not None
        print("   [PASS] Verified HISTORICAL RECORD MISSING. Blockchain proof was NOT deleted.")
    finally:
        # Restore Kabir's medical event in DB
        db.table("medical_events").update({"status": "ACTIVE"}).eq("event_id", kabir_event_id).execute()

    # TEST 16: Unauthorized doctor cannot verify another patient's event (Tanya's event) -> 403 Forbidden
    print("\nTest 16: Unauthorized doctor attempting integrity check on Tanya's event...")
    tanya_event_id = "70000000-0000-0000-0000-000000000012"
    unauth_ver = client.post(f"/integrity/{tanya_event_id}/verify", headers=doc_headers)
    print(f"   Response status: {unauth_ver.status_code}, detail: {unauth_ver.json().get('detail')}")
    assert unauth_ver.status_code == 403, "Expected 403 Forbidden for unauthorized doctor"
    print("   [PASS] 403 Forbidden enforced on integrity verification.")

    # TEST 17: Client cannot force VERIFIED result with arbitrary frontend inputs
    print("\nTest 17: Client cannot pass fake hash or override server-side verification...")
    # The endpoint calculates canonical hash strictly on the server; client body is not trusted
    srv_check = client.post("/integrity/70000000-0000-0000-0000-000000000001/verify", json={"force_hash": "fake_hash"}, headers=doc_headers)
    assert srv_check.status_code == 200
    assert srv_check.json()["verification_status"] == "VERIFIED"
    print("   [PASS] Server-side hash generation and verification confirmed.")

    # TEST 18: Blockchain info endpoint
    print("\nTest 18: Checking Hyperledger Fabric channel metadata...")
    bc_info = client.get("/integrity/blockchain/info", headers=doc_headers)
    assert bc_info.status_code == 200
    info_data = bc_info.json()
    print(f"   Channel: {info_data.get('channel')}, Chaincode: {info_data.get('chaincode')}")
    print(f"   Adapter: {info_data.get('adapter')}")
    assert info_data.get("channel") == "meditrace-channel"
    assert info_data.get("chaincode") == "medical_integrity_cc"
    print("   [PASS] Fabric metadata retrieved.")

    # TEST 19: Patient Integrity Overview
    print("\nTest 19: Getting full patient integrity overview for Nikhil...")
    overview_res = client.get(f"/integrity/patient/{nikhil_id}", headers=doc_headers)
    assert overview_res.status_code == 200
    ov_data = overview_res.json()
    print(f"   Total critical events: {ov_data['total_critical_events']}")
    print(f"   Total anchored: {ov_data['total_anchored']}, Total verified: {ov_data['total_verified']}")
    assert ov_data["total_critical_events"] >= 2
    print("   [PASS] Patient integrity summary retrieved.")

    print("\n" + "=" * 80)
    print("ALL TASK #5 TEST SCENARIOS PASSED PERFECTLY!")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    run_tests()
