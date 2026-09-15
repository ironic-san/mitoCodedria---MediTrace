from typing import Any, Dict, Optional
from pydantic import BaseModel, Field


class OCRProcessResponse(BaseModel):
    extracted_text: str
    filename: str
    content_type: str
    char_count: int
    word_count: int
    ocr_status: str = "COMPLETED"
    confidence_score: float = 0.95
    document_date: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
