import unittest

from app.services.ocr_nlu_adapter import process_text


class OCRNLUAdapterTests(unittest.TestCase):
    def test_process_text_uses_repository_pipeline_and_preserves_evidence(self):
        result = process_text(
            "Patient Name: Rohan Iyer\n"
            "DOB: 1980-01-01\n"
            "BMI: 23.8\n"
            "Headache persists."
        )

        self.assertEqual(result["ocr"]["status"], "COMPLETED")
        facts = result["nlu"]["candidate_facts"]
        self.assertTrue(facts)
        headache = next(fact for fact in facts if fact["normalized_text"] == "Headache")
        self.assertEqual(headache["evidence"]["source_text"], "Headache")
        self.assertEqual(headache["evidence"]["document_id"], "backend-text")

    def test_measurement_semantics_are_not_inferred_from_nearby_text(self):
        result = process_text("BMI: 23.8\nWeight: 72 kg\nHeight: 175 cm")
        measurements = [
            fact for fact in result["nlu"]["candidate_facts"]
            if fact["entity_type"] == "MEASUREMENT"
        ]

        bmi = next(fact for fact in measurements if fact["attributes"].get("measurement_type") == "BMI")
        self.assertEqual(bmi["attributes"]["value"], 23.8)
        self.assertIsNone(bmi["attributes"]["unit"])


if __name__ == "__main__":
    unittest.main()
