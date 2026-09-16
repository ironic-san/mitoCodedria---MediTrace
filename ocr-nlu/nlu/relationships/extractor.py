from nlu.models.relationships import Relationship
class RelationshipExtractor:
    def extract(self, facts):
        out=[]
        meds=[f for f in facts if f.entity_type.value=="MEDICATION"]; cond=[f for f in facts if f.entity_type.value=="CONDITION"]
        for m in meds:
            for c in cond:
                if c.context.negation.value == "NEGATED": continue
                ms=getattr(m, "_context_sentence", ""); cs=getattr(c, "_context_sentence", "")
                if not ms or ms != cs: continue
                if not any(token in ms.lower() for token in ("treat", "for", "manage", "prescrib", "due to", "given")): continue
                out.append(Relationship(relationship_id=f"rel-{m.entity_id}-{c.entity_id}", source_entity_id=m.entity_id, relationship_type="TREATS", target_entity_id=c.entity_id, evidence=[ms], confidence=.65))
        return out
