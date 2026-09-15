from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.analysis import router as analysis_router
from app.api.audit import router as audit_router
from app.api.auth import router as auth_router
from app.api.doctors import router as doctors_router
from app.api.documents import router as documents_router
from app.api.emergency import router as emergency_router
from app.api.integrity import router as integrity_router
from app.api.nlu import router as nlu_router
from app.api.ocr import router as ocr_router
from app.api.patients import router as patients_router
from app.api.rag import router as rag_router
from app.core.config import get_settings

settings = get_settings()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="MediTrace Emergency Health Passport & Access Control API",
)

# Configure CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API Routers
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(patients_router, prefix="/patients", tags=["Patients & Passport"])
app.include_router(doctors_router, prefix="/doctors", tags=["Doctors & Access Discovery"])
app.include_router(documents_router, prefix="/documents", tags=["Document Access & Upload"])
app.include_router(emergency_router, prefix="/emergency", tags=["Emergency & Break-Glass"])
app.include_router(ocr_router, prefix="/ocr", tags=["OCR Text Extraction"])
app.include_router(nlu_router, prefix="/nlu", tags=["NLU Medical Extraction"])
app.include_router(rag_router, prefix="/rag", tags=["Historical Medical RAG"])
app.include_router(integrity_router, prefix="/integrity", tags=["Integrity & Hyperledger Fabric"])
app.include_router(analysis_router, prefix="/document-analysis", tags=["Document Analysis & Review"])
app.include_router(audit_router, prefix="/audit", tags=["Audit Logging"])


@app.get("/health", tags=["Health"])
def health_check():
    """Health check endpoint to verify backend service status."""
    return {
        "status": "ok",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
