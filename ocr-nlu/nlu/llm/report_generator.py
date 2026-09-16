import json
from .prompts import SYSTEM_PROMPT
class ReportGenerator:
    def __init__(self, client=None): self.client=client
    def build_payload(self, result, *, db_context=None, rag_evidence=None):
        return {"document":result.document.model_dump(), "facts":[f.model_dump() for f in result.candidate_facts], "relationships":[r.model_dump() for r in result.relationships], "validation_issues":[i.model_dump() for i in result.validation_issues], "db_context":db_context, "rag_evidence":rag_evidence}
    def generate(self, result, *, db_context=None, rag_evidence=None):
        payload=self.build_payload(result, db_context=db_context, rag_evidence=rag_evidence)
        if self.client is None: return {"prompt":SYSTEM_PROMPT, "structured_input":payload}
        return self.client.complete(SYSTEM_PROMPT+"\n"+json.dumps(payload, default=str), json_mode=True)
