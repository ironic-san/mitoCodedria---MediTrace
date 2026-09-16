import unittest
from datetime import datetime, timedelta, timezone

from app.services.ai_service import deterministic_compare_findings
from app.services.emergency_service import get_doctor_access_mode
from app.services.patient_service import has_valid_doctor_access
from app.schemas.integrity import IntegrityVerifyResponse


class _Response:
    def __init__(self, data):
        self.data = data


class _Query:
    def __init__(self, rows):
        self.rows = rows
        self.filters = []

    def select(self, *_args, **_kwargs):
        return self

    def eq(self, key, value):
        self.filters.append((key, value))
        return self

    def execute(self):
        rows = [row for row in self.rows if all(row.get(key) == value for key, value in self.filters if key in row)]
        return _Response(rows)


class _Client:
    def __init__(self, rows):
        self.rows = rows
        self.queries = []

    def table(self, _name):
        query = _Query(self.rows)
        self.queries.append(query)
        return query


class ScopedBackendTests(unittest.TestCase):
    def test_normal_access_requires_relationship_type(self):
        client = _Client([
            {
                "relationship_type": "BREAK_GLASS",
                "status": "ACTIVE",
                "ended_at": (datetime.now(timezone.utc) + timedelta(hours=1)).isoformat(),
            }
        ])
        self.assertFalse(has_valid_doctor_access(client, "doctor", "patient"))
        self.assertIn(("relationship_type", "NORMAL_ACCESS"), client.queries[0].filters)

    def test_access_mode_does_not_treat_unknown_relationship_as_normal(self):
        client = _Client([{
            "relationship_type": "UNKNOWN",
            "status": "ACTIVE",
            "ended_at": (datetime.now(timezone.utc) + timedelta(hours=1)).isoformat(),
        }])
        self.assertIsNone(get_doctor_access_mode(client, "doctor", "patient"))

    def test_malformed_expiry_fails_closed_for_normal_access(self):
        client = _Client([{
            "relationship_type": "NORMAL_ACCESS",
            "status": "ACTIVE",
            "ended_at": "not-a-timestamp",
        }])
        self.assertFalse(has_valid_doctor_access(client, "doctor", "patient"))

    def test_deterministic_comparison_distinguishes_match_and_new(self):
        result = deterministic_compare_findings(
            {
                "conditions": [{"name": "Hypertension"}, {"name": "Asthma"}],
                "allergies": [],
                "medications": [],
                "events": [],
            },
            {
                "conditions": [{"condition_name": "Hypertension"}],
                "allergies": [],
                "medications": [],
                "medical_events": [],
            },
        )
        self.assertEqual(len(result["matches"]), 1)
        self.assertEqual(result["new_findings"][0]["finding"], "Asthma")

    def test_integrity_contract_exposes_verification_result(self):
        response = IntegrityVerifyResponse(
            event_id="event-1",
            verification_status="VERIFIED",
            message="verified",
        )
        self.assertEqual(response.verification_status, "VERIFIED")
        self.assertEqual(response.event_id, "event-1")


if __name__ == "__main__":
    unittest.main()
