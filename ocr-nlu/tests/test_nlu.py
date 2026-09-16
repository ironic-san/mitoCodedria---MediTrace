import unittest
from ocr.engine import OCRResult
from nlu.pipeline import NLUPipeline
from nlu.models.context import Negation, Certainty, Temporality, Experiencer
from nlu.classifiers.section_detector import SectionDetector
from nlu.models.clinical_fact import EntityType

class NLUIntegrationTests(unittest.TestCase):
    def setUp(self): self.pipeline=NLUPipeline()
    def test_context_and_evidence_are_preserved(self):
        text="Assessment:\nNo evidence of pneumonia.\nPossible pneumonia.\nHistory of diabetes.\nFamily history of diabetes.\nPatient denies chest pain."
        result=self.pipeline.process(OCRResult("d","x",text,None,"COMPLETED",{}))
        pneumonia=[f for f in result.candidate_facts if f.normalized_text.lower()=="pneumonia"]
        self.assertEqual(pneumonia[0].context.negation, Negation.NEGATED)
        self.assertEqual(pneumonia[1].context.certainty, Certainty.POSSIBLE)
        self.assertTrue(all(f.evidence.document_id == "d" for f in result.candidate_facts))
    def test_lab_table_and_json(self):
        text="Laboratory Results\nHbA1c | 7.8 | 4.0 - 5.6 | % | HIGH"
        result=self.pipeline.process(OCRResult("d","x",text,None,"COMPLETED",{}))
        self.assertEqual(result.document.document_type.value,"LABORATORY_REPORT")
        lab=next(f for f in result.candidate_facts if f.entity_type.value=="LAB_RESULT")
        self.assertEqual(lab.attributes["abnormal_flag"],"HIGH")
        self.assertIn("candidate_facts", result.model_dump_json())

    def test_general_section_headings(self):
        text="PATIENT INFORMATION\nName: X\nLABORATORY RESULTS\nHbA1c\nCLINICAL COURSE\nStable\nOPERATIVE SUMMARY\nDone"
        names=[s.name for s in SectionDetector().detect(text)]
        self.assertEqual(names, ["PATIENT_INFORMATION", "LABORATORY", "HOSPITAL_COURSE", "OPERATIVE_SUMMARY"])

    def test_demographics_are_independent_fields(self):
        text="Patient Name: Rohan Iyer\nPatient Identifier: R-123\nDOB: 17-Nov-1997\nGender: Male\nBlood Group: O-"
        facts=self.pipeline.process(OCRResult("d","x",text,None,"COMPLETED",{})).candidate_facts
        demographic=[f for f in facts if f.entity_type==EntityType.PATIENT_DEMOGRAPHIC]
        self.assertEqual({f.attributes["field"] for f in demographic},{"name","patient_identifier","date_of_birth","sex","blood_group"})
        self.assertTrue(all("\n" not in f.original_text for f in demographic))

    def test_bmi_is_dimensionless(self):
        text="Vitals:\nWeight: 73 kg\nBMI: 23.8 kg/m²\nBlood Pressure: 116/72 mmHg"
        facts=self.pipeline.process(OCRResult("d","x",text,None,"COMPLETED",{})).candidate_facts
        measurements=[f for f in facts if f.entity_type==EntityType.MEASUREMENT]
        bmi=next(f for f in measurements if f.attributes["measurement_type"]=="BMI")
        self.assertIsNone(bmi.attributes["unit"])
        self.assertEqual(next(f for f in measurements if f.attributes["measurement_type"]=="WEIGHT").attributes["unit"],"kg")

    def test_repeated_mentions_are_not_contradictions(self):
        text="Chief Complaint:\nRecurrent headaches.\nAssessment:\nHeadache persists.\nFollow-up:\nHeadache diary."
        result=self.pipeline.process(OCRResult("d","x",text,None,"COMPLETED",{}))
        self.assertEqual([i for i in result.validation_issues if i.code=="CONTRADICTORY_CONTEXT"],[])

    def test_relationships_require_local_evidence(self):
        text="Medications:\nLevofloxacin.\nDiagnosis:\nPneumonia."
        result=self.pipeline.process(OCRResult("d","x",text,None,"COMPLETED",{}))
        self.assertEqual(result.relationships,[])

    def test_recommendation_contains_content(self):
        text="Plan:\nRecommend allergy consultation for formal assessment.\nFOLLOW-UP"
        facts=self.pipeline.process(OCRResult("d","x",text,None,"COMPLETED",{})).candidate_facts
        recommendations=[f for f in facts if f.entity_type==EntityType.RECOMMENDATION]
        self.assertEqual(len(recommendations),1)
        self.assertIn("allergy consultation",recommendations[0].original_text.lower())

if __name__ == "__main__": unittest.main()
