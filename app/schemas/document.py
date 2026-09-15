from typing import Optional
from pydantic import BaseModel


class DocumentAccessResponse(BaseModel):
    """Document access metadata and download URL."""
    document_id: str
    patient_id: str
    uploaded_by: Optional[str] = None
    title: str
    document_type: str
    document_date: Optional[str] = None
    file_url: str
    download_url: str
    ocr_status: Optional[str] = None
    uploaded_at: Optional[str] = None


class DocumentUploadResponse(BaseModel):
    """Response returned upon successful document upload."""
    document_id: str
    patient_id: str
    uploaded_by: Optional[str] = None
    title: str
    document_type: str
    storage_path: str
    document_date: Optional[str] = None
    uploaded_at: str
    status: str
    download_url: Optional[str] = None
