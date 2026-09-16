from pydantic import BaseModel, Field
class Relationship(BaseModel):
    relationship_id: str
    source_entity_id: str
    relationship_type: str
    target_entity_id: str
    evidence: list[str] = Field(default_factory=list)
    confidence: float | None = None
