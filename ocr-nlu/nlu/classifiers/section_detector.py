import re
from nlu.models.document import Section

class SectionDetector:
    """Detect common clinical headings, including numbered/OCR-formatted headings."""
    HEADERS = {
        "chief complaint":"CHIEF_COMPLAINT", "presenting complaint":"CHIEF_COMPLAINT",
        "history of present illness":"HPI", "hpi":"HPI", "history":"HISTORY",
        "past medical history":"PMH", "pmh":"PMH", "past surgical history":"PSH", "psh":"PSH",
        "allergies":"ALLERGIES", "medications":"MEDICATIONS", "current medications":"MEDICATIONS",
        "discharge medication":"DISCHARGE_MEDICATIONS", "discharge medications":"DISCHARGE_MEDICATIONS",
        "family history":"FAMILY_HISTORY", "social history":"SOCIAL_HISTORY",
        "physical examination":"EXAMINATION", "examination":"EXAMINATION",
        "investigations":"INVESTIGATIONS", "laboratory":"LABORATORY", "laboratory results":"LABORATORY",
        "lab results":"LABORATORY", "specimen details":"SPECIMEN_DETAILS", "imaging":"IMAGING",
        "findings":"FINDINGS", "impression":"IMPRESSION", "assessment":"ASSESSMENT",
        "diagnosis":"DIAGNOSIS", "pre-operative diagnosis":"PREOPERATIVE_DIAGNOSIS",
        "post-operative diagnosis":"POSTOPERATIVE_DIAGNOSIS", "procedure":"PROCEDURE",
        "operative findings":"OPERATIVE_FINDINGS", "operative summary":"OPERATIVE_SUMMARY",
        "hospital course":"HOSPITAL_COURSE", "clinical course":"HOSPITAL_COURSE",
        "discharge diagnosis":"DISCHARGE_DIAGNOSIS", "plan":"PLAN", "recommendations":"RECOMMENDATIONS",
        "follow-up":"FOLLOW_UP", "follow up":"FOLLOW_UP", "patient information":"PATIENT_INFORMATION",
        "document metadata":"DOCUMENT_METADATA", "clinical team":"CLINICAL_TEAM", "pathologist notes":"NOTES",
        "signature":"SIGNATURE", "immediate post-operative condition":"POSTOPERATIVE_CONDITION",
        "post-operative orders":"POSTOPERATIVE_ORDERS", "intraoperative neuromonitoring":"INTRAOPERATIVE_MONITORING",
    }
    def _key(self, heading: str) -> str:
        key = heading.lower().replace("–", "-").replace("—", "-")
        key = re.sub(r"^\s*(?:\(?[0-9ivx]+[.)]|[-*])\s*", "", key)
        key = re.sub(r"[^a-z- ]", "", key)
        return re.sub(r"\s+", " ", key).strip(" -")

    def detect(self, text: str) -> list[Section]:
        # A heading is a mostly standalone line. This handles uppercase OCR headings,
        # optional numbering, divider punctuation, and a trailing colon.
        lines = list(re.finditer(r"(?im)^\s*([^\n:]{2,80})\s*:?[ \t]*$", text))
        hits=[]
        for m in lines:
            key=self._key(m.group(1))
            if key in self.HEADERS:
                hits.append((m, self.HEADERS[key], m.group(1).strip()))
        out=[]
        for i,(m,name,heading) in enumerate(hits):
            start=m.end(); end=hits[i+1][0].start() if i+1<len(hits) else len(text)
            out.append(Section(name=name, heading=heading, text=text[start:end].strip(), start=start, end=end))
        return out
