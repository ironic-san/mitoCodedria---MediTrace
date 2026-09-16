from nlu.models.output import ValidationIssue
class ContradictionChecker:
    def validate(self, facts):
        issues=[]
        for i,a in enumerate(facts):
            for b in facts[i+1:]:
                if a.entity_type != b.entity_type or a.normalized_text.lower()!=b.normalized_text.lower(): continue
                # Repeated mentions in different sentences/sections are not the same event.
                # Only compare occurrences sharing the exact local context sentence.
                sentence_a=getattr(a, "_context_sentence", "")
                sentence_b=getattr(b, "_context_sentence", "")
                if not sentence_a or sentence_a != sentence_b: continue
                incompatible = a.context.negation != b.context.negation
                incompatible = incompatible or (a.context.certainty != b.context.certainty and {a.context.certainty.value,b.context.certainty.value} & {"POSSIBLE","UNCERTAIN"})
                incompatible = incompatible or ({a.context.temporality.value,b.context.temporality.value} == {"CURRENT","HISTORICAL"})
                if incompatible:
                    issues.append(ValidationIssue(code="CONTRADICTORY_CONTEXT", message=f"Conflicting context for {a.normalized_text} in one occurrence", severity="WARNING", entity_ids=[a.entity_id,b.entity_id]))
        return issues
