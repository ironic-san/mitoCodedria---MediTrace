from nlu.models.output import ValidationIssue
class EvidenceValidator:
    def validate(self, facts):
        return [ValidationIssue(code="MISSING_EVIDENCE", message="Fact has no source evidence", severity="ERROR", entity_ids=[f.entity_id]) for f in facts if not f.evidence or not f.evidence.source_text]
