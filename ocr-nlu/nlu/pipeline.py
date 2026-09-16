"""Deterministic, evidence-preserving NLU pipeline for OCRResult inputs."""
import re
from uuid import uuid4
from ocr.engine import OCRResult
from .models.clinical_fact import ClinicalFact, EntityType
from .models.context import Context, Negation, Certainty, Temporality, Experiencer, FactStatus
from .models.document import DocumentStructure
from .models.evidence import Evidence
from .models.output import NLUResult, ValidationIssue
from .classifiers import DocumentClassifier, SectionDetector
from .context import detect_negation, detect_certainty, detect_temporality, detect_experiencer
from .normalizers import normalize_abbreviation, normalize_date, normalize_unit, terminology_code
from .relationships import RelationshipExtractor
from .validators import EvidenceValidator, ContradictionChecker

class NLUPipeline:
    """Transform OCR text into candidate facts; never silently asserts clinical truth."""
    def __init__(self):
        self.classifier=DocumentClassifier(); self.sections=SectionDetector(); self.relationships=RelationshipExtractor()

    def process(self, ocr_result: OCRResult) -> NLUResult:
        text=ocr_result.extracted_text or ""
        dtype, confidence, reasoning=self.classifier.classify(text)
        structure=DocumentStructure(document_id=ocr_result.document_id, file_path=ocr_result.file_path, document_type=dtype, classification_confidence=confidence, classification_reasoning=reasoning, sections=self.sections.detect(text), metadata=ocr_result.metadata)
        facts=[]
        patterns=[
            (EntityType.SYMPTOM, r"\b(chest pain|headache|dizziness|weakness|nausea|vomiting|seizure|fever|shortness of breath|dyspnea)\b"),
            (EntityType.CONDITION, r"\b(type 2 diabetes mellitus|t2dm|diabetes mellitus|diabetes|hypertension|htn|pneumonia|pneurnonia|epilepsy|migraine|stroke|asthma|fracture)\b"),
            (EntityType.PROCEDURE, r"\b(craniotomy|surgery|surgical resection|biopsy|appendectomy|angioplasty|pci|operation|procedure)\b"),
            (EntityType.ANATOMICAL_SITE, r"\b(left|right|bilateral)?\s*(frontal|parietal|temporal|occipital|brain|lung|heart|knee|abdomen|chest)\b"),
            (EntityType.DEVICE, r"\b(shunt|pacemaker|stent|implant)\b"),
        ]
        for typ, pat in patterns:
            for m in re.finditer(pat,text,re.I):
                original = next((g for g in m.groups() if g), m.group(0))
                facts.append(self._fact(ocr_result, text, m, typ, original, structure))
        facts.extend(self._demographics(ocr_result,text,structure)); facts.extend(self._recommendations(ocr_result,text,structure)); facts.extend(self._medications(ocr_result,text,structure)); facts.extend(self._allergies(ocr_result,text,structure)); facts.extend(self._labs(ocr_result,text,structure)); facts.extend(self._dates(ocr_result,text,structure)); facts.extend(self._measurements(ocr_result,text,structure)); facts.extend(self._vitals(ocr_result,text,structure))
        facts=self._dedupe(facts)
        issues=EvidenceValidator().validate(facts)+ContradictionChecker().validate(facts)
        if any(f.extraction_confidence is not None and f.extraction_confidence < .5 for f in facts): issues.append(ValidationIssue(code="LOW_CONFIDENCE", message="One or more facts were extracted with low OCR confidence", severity="WARNING"))
        for f in facts:
            if f.context.certainty != Certainty.CERTAIN or f.context.negation == Negation.NEGATED: f.status=FactStatus.NEEDS_REVIEW
            else: f.status=FactStatus.NORMALIZED
        return NLUResult(document=structure,candidate_facts=facts,verified_facts=[],relationships=self.relationships.extract(facts),validation_issues=issues)

    def _fact(self, ocr, text, match, typ, original, structure, attrs=None, evidence_span=None):
        start,end=evidence_span or match.span()
        left=max(text.rfind("\n",0,start), text.rfind(".",0,start), text.rfind("!",0,start), text.rfind("?",0,start))
        right_candidates=[x for x in (text.find("\n",end), text.find(".",end), text.find("!",end), text.find("?",end)) if x >= 0]
        right=min(right_candidates) if right_candidates else len(text)
        sentence=text[left+1:right].strip()
        sentence=sentence or original; normalized=normalize_abbreviation(original); neg=detect_negation(sentence,original)
        ctx=Context(negation=Negation(neg), certainty=Certainty(detect_certainty(sentence)), temporality=Temporality(detect_temporality(sentence)), experiencer=Experiencer(detect_experiencer(sentence)))
        section=next((s.name for s in structure.sections if s.start<=start<=s.end),None)
        fact=ClinicalFact(entity_id=str(uuid4()),entity_type=typ,original_text=original,normalized_text=normalized,terminology_code=terminology_code(normalized),context=ctx,evidence=Evidence(document_id=ocr.document_id,source_text=original,character_start=start,character_end=end,section=section,ocr_confidence=ocr.confidence),extraction_confidence=(ocr.confidence/100 if ocr.confidence is not None else None),attributes=dict(attrs or {}))
        fact._context_sentence=sentence
        return fact

    def _demographics(self, ocr, text, structure):
        fields=(("name", r"(?:patient\s+name|name)[ \t]*:[ \t]*([A-Z][A-Za-z]+(?:[ \t]+[A-Z][A-Za-z]+){1,3})"), ("patient_identifier", r"(?:patient[ \t]*(?:id|identifier)|mrn)[ \t]*[^:]*:[ \t]*([^\n|]+)"), ("date_of_birth", r"(?:dob|date[ \t]+of[ \t]+birth)[ \t]*:[ \t]*([^\n|]+)"), ("sex", r"(?:gender|sex)[ \t]*:[ \t]*([^\n|]+)"), ("blood_group", r"blood[ \t]+group[ \t]*:[ \t]*([^\n|]+)"))
        out=[]
        for field, pat in fields:
            for m in re.finditer(pat,text,re.I):
                value=m.group(1).strip(); attrs={"field":field}
                if field=="date_of_birth": attrs["iso_date"]=normalize_date(value.split("(")[0].strip())
                out.append(self._fact(ocr,text,m,EntityType.PATIENT_DEMOGRAPHIC,value,structure,attrs,m.span(1)))
        return out

    def _recommendations(self, ocr, text, structure):
        out=[]
        for m in re.finditer(r"\b((?:recommend(?:ed|ation)?|return|schedule|plan)\b[^.\n]{8,}|follow[- ]?up\s+(?:with|in|for)\b[^.\n]+)",text,re.I):
            out.append(self._fact(ocr,text,m,EntityType.RECOMMENDATION,m.group(1).strip(),structure))
        return out

    def _find(self, ocr,text,structure,pat,typ,group=1,attrs=None):
        return [self._fact(ocr,text,m,typ,m.group(group),structure,attrs) for m in re.finditer(pat,text,re.I)]
    def _medications(self, ocr,text,s):
        pat=r"\b(levofloxacin|amoxicillin|penicillin|penicillln|aspirin|metformin|levetiracetam|paracetamol|acetaminophen|ibuprofen|atorvastatin|insulin|cetirizine|salbutamol)\b(?:\s+(\d+(?:\.\d+)?)\s*(mg|g|mcg))?(?:\s+(once daily|twice daily|three times daily|od|bid|tid|prn|qid))?(?:\s+(oral|po|iv|im|neb))?"
        out=[]
        for m in re.finditer(pat,text,re.I):
            context=text[max(0,m.start()-90):min(len(text),m.end()+90)].lower()
            if "allerg" in context or "reaction" in context or "penicillin-class" in context:
                continue
            attrs={"dose":m.group(2),"unit":normalize_unit(m.group(3)) if m.group(3) else None,"frequency":normalize_abbreviation(m.group(4)) if m.group(4) else None,"route":normalize_abbreviation(m.group(5)) if m.group(5) else None}
            out.append(self._fact(ocr,text,m,EntityType.MEDICATION,normalize_abbreviation(m.group(1)),s,attrs))
        return out
    def _allergies(self,ocr,text,s):
        out=[]
        for m in re.finditer(r"\bno known (?:drug )?allerg(?:y|ies)\b", text, re.I):
            fact=self._fact(ocr,text,m,EntityType.ALLERGY,m.group(0),s,{"criticality":"NONE"})
            fact.context.negation=Negation.NEGATED
            out.append(fact)
        allergy_patterns=(
            r"(?:severe\s+)?(penicill(?:in|ln)|amoxicillin)\s+allergy\s*\(([^)]*)\)",
            r"possible\s+(amoxicillin)-related\s+reaction",
        )
        for pat in allergy_patterns:
            for m in re.finditer(pat,text,re.I):
                allergen=normalize_abbreviation(m.group(1))
                fact=self._fact(ocr,text,m,EntityType.ALLERGY,allergen,s,{"reaction":m.group(2) if m.lastindex and m.lastindex > 1 else "reaction", "severity":"SEVERE" if "severe" in m.group(0).lower() else None, "confirmed":False if "possible" in m.group(0).lower() else True})
                out.append(fact)
        for m in re.finditer(r"(?:allerg(?:y|ies)\s*:\s*|allergic to\s+)([A-Za-z]+)(?:\s*\(([^)]+)\))?",text,re.I): out.append(self._fact(ocr,text,m,EntityType.ALLERGY,m.group(1),s,{"reaction":m.group(2),"severity":"SEVERE" if m.group(2) and "anaphyl" in m.group(2).lower() else None}))
        return out
    def _labs(self,ocr,text,s):
        out=[]; pat=r"\b(hemoglobin|haemoglobin|glucose|creatinine|sodium|potassium|wbc|white blood cell(?: count)?)\b\s*[:=]?\s*(\d+(?:\.\d+)?)\s*(mg/dL|g/dL|mmol/L|mL|%)?(?:\s*\((high|low|critical)\))?"
        for m in re.finditer(pat,text,re.I): out.append(self._fact(ocr,text,m,EntityType.LAB_RESULT,m.group(0),s,{"test_name":m.group(1),"value":float(m.group(2)),"unit":normalize_unit(m.group(3)) if m.group(3) else None,"abnormal_flag":m.group(4)}))
        table=r"^\s*([^|\n-][^|\n]*?)\s*\|\s*([<>]?\d+(?:\.\d+)?)\s*\|\s*([^|\n]+?)\s*\|\s*([^|\n]+?)\s*\|\s*(HIGH|LOW|NORMAL|CRITICAL)\s*$"
        for m in re.finditer(table,text,re.I|re.M):
            attrs={"test_name":m.group(1).strip(),"value":float(m.group(2)),"reference_range":m.group(3).strip(),"unit":normalize_unit(m.group(4)),"abnormal_flag":m.group(5).upper()}
            out.append(self._fact(ocr,text,m,EntityType.LAB_RESULT,m.group(0).strip(),s,attrs))
        return out
    def _dates(self,ocr,text,s):
        out=[]
        pat=r"\b(?:\d{1,2}[/-]\d{1,2}[/-]\d{4}|\d{4}-\d{2}-\d{2}|(?:January|February|March|April|May|June|July|August|September|October|November|December) \d{1,2} \d{4}|\d{1,2} (?:January|February|March|April|May|June|July|August|September|October|November|December) \d{4})\b"
        for m in re.finditer(pat,text,re.I): out.append(self._fact(ocr,text,m,EntityType.DATE_TIME,m.group(0),s,{"iso_date":normalize_date(m.group(0))}))
        return out
    def _measurements(self,ocr,text,s):
        out=[]; covered=[]
        labeled=(("BMI",r"\bBMI\s*[:=]?\s*(\d+(?:\.\d+)?)\s*(?:kg\s*/\s*m[²2])?"), ("WEIGHT",r"\bWeight\s*[:=]?\s*(\d+(?:\.\d+)?)\s*(kg|g)\b"), ("HEIGHT",r"\bHeight\s*[:=]?\s*(\d+(?:\.\d+)?)\s*(cm|m)\b"))
        for kind,pat in labeled:
            for m in re.finditer(pat,text,re.I):
                covered.append(m.span()); unit=None if kind=="BMI" else normalize_unit(m.group(2))
                out.append(self._fact(ocr,text,m,EntityType.MEASUREMENT,m.group(0),s,{"value":float(m.group(1)),"measurement_type":kind,"unit":unit}))
        for m in re.finditer(r"\b(\d+(?:\.\d+)?)\s*(mmHg|bpm|kg|cm|mm|mg/dL|g/dL|mmol/L|%)\b(?!\s*/)",text,re.I):
            if any(a<=m.start()<b for a,b in covered): continue
            out.append(self._fact(ocr,text,m,EntityType.MEASUREMENT,m.group(0),s,{"value":float(m.group(1)),"measurement_type":"MEASUREMENT","unit":normalize_unit(m.group(2))}))
        return out
    def _vitals(self,ocr,text,s):
        out=[]
        for m in re.finditer(r"\b(blood pressure|bp|heart rate|pulse|temperature|oxygen saturation|spo2)\s*[:=]?\s*([\d./]+)\s*(mmHg|bpm|°?C|%)?",text,re.I): out.append(self._fact(ocr,text,m,EntityType.VITAL_SIGN,m.group(0),s,{"name":m.group(1),"value":m.group(2),"unit":normalize_unit(m.group(3)) if m.group(3) else None}))
        return out
    def _dedupe(self,facts):
        seen=set(); out=[]
        for f in facts:
            key=(f.entity_type,f.normalized_text.lower(),f.evidence.character_start)
            if key not in seen: seen.add(key); out.append(f)
        return out
