from pydantic import BaseModel, Field
class Evidence(BaseModel):
    document_id: str
    source_text: str = Field(min_length=1)
    page_number: int | None = None
    character_start: int | None = None
    character_end: int | None = None
    section: str | None = None
    ocr_confidence: float | None = None
