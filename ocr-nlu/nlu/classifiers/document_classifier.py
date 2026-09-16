from nlu.models.document import DocumentType
class DocumentClassifier:
    RULES = {
        DocumentType.LABORATORY_REPORT: ("laboratory", "lab results", "reference range", "specimen"),
        DocumentType.MRI_REPORT: ("mri", "magnetic resonance"),
        DocumentType.CT_REPORT: ("ct scan", "computed tomography"),
        DocumentType.RADIOLOGY_REPORT: ("radiology", "impression", "technique"),
        DocumentType.OPERATIVE_REPORT: ("operative", "operation performed", "postoperative diagnosis"),
        DocumentType.DISCHARGE_SUMMARY: ("discharge", "hospital course", "discharge medications"),
        DocumentType.FOLLOW_UP: ("follow-up", "follow up", "return in"),
        DocumentType.CONSULTATION: ("consultation", "consulting", "neurology consultation"),
        DocumentType.ALLERGY_ASSESSMENT: ("allergy assessment", "allergies"),
        DocumentType.MEDICATION_HISTORY: ("medication history", "current medications"),
        DocumentType.NEUROLOGY_REPORT: ("neurology", "neurological"),
        DocumentType.PREOPERATIVE_ASSESSMENT: ("preoperative", "pre-operative"),
        DocumentType.POSTOPERATIVE_FOLLOWUP: ("postoperative follow-up", "post-operative follow-up"),
    }
    def classify(self, text: str):
        low = text.lower(); scores = {k: sum(low.count(x) for x in v) for k,v in self.RULES.items()}
        header = low[:600]
        if "discharge summary" in header or "emergency discharge" in header:
            return DocumentType.DISCHARGE_SUMMARY, 0.95, ["matched explicit discharge heading"]
        if "follow-up" in header or "follow up" in header:
            return DocumentType.FOLLOW_UP, 0.9, ["matched explicit follow-up heading"]
        if "neurology consultation" in header or "consultation" in header:
            return DocumentType.CONSULTATION, 0.85, ["matched consultation heading"]
        best, score = max(scores.items(), key=lambda x:x[1])
        if score == 0: return DocumentType.UNKNOWN, 0.0, []
        return best, min(0.99, 0.55 + 0.1 * score), [f"matched: {', '.join(x for x in self.RULES[best] if x in low)}"]
