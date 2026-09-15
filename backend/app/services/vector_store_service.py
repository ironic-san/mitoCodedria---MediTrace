import logging
from typing import Any, Dict, List, Optional
from pydantic import BaseModel

from app.schemas.rag import RAGSourceItem
from app.services.embedding_service import compute_cosine_similarity, expand_tokens, tokenize

logger = logging.getLogger(__name__)


class IndexedDocumentChunk(BaseModel):
    chunk_id: str
    patient_id: str
    document_id: str
    title: str
    document_date: Optional[str] = None
    chunk_text: str
    chunk_index: int
    term_vector: Dict[str, float]


class PatientVectorStore:
    """
    Patient-scoped in-memory vector store for historical medical document retrieval.
    Strictly guarantees that vector searches are filtered by patient_id.
    """
    def __init__(self):
        # Maps patient_id -> List[IndexedDocumentChunk]
        self._patient_chunks: Dict[str, List[IndexedDocumentChunk]] = {}

    def index_documents_for_patient(self, patient_id: str, documents: List[Dict[str, Any]]) -> int:
        """
        Chunks and indexes all documents belonging to a single patient.
        Replaces any previous index for this patient.
        """
        chunks: List[IndexedDocumentChunk] = []

        for doc in documents:
            doc_id = str(doc.get("document_id", ""))
            doc_patient_id = str(doc.get("patient_id", ""))
            # Hard enforcement: skip document if it does not belong to this patient
            if doc_patient_id != patient_id:
                continue

            title = doc.get("title") or "Medical Document"
            doc_date = doc.get("document_date")
            text = (doc.get("extracted_text") or doc.get("title") or "").strip()

            if not text:
                continue

            # Split document into coherent paragraphs / sentences (max 300 words per chunk)
            paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
            if not paragraphs:
                paragraphs = [text]

            for idx, para in enumerate(paragraphs):
                chunk_id = f"{doc_id}_chunk_{idx}"
                # Combine title and text for rich context representation
                content_for_embedding = f"{title}. Date: {doc_date or 'Unknown'}. {para}"
                tokens = tokenize(content_for_embedding)
                term_vec = expand_tokens(tokens)

                chunks.append(
                    IndexedDocumentChunk(
                        chunk_id=chunk_id,
                        patient_id=patient_id,
                        document_id=doc_id,
                        title=title,
                        document_date=doc_date,
                        chunk_text=para,
                        chunk_index=idx,
                        term_vector=term_vec,
                    )
                )

        self._patient_chunks[patient_id] = chunks
        return len(chunks)

    def search_patient_scoped(
        self,
        patient_id: str,
        query: str,
        top_k: int = 5,
        min_score: float = 0.08,
    ) -> List[RAGSourceItem]:
        """
        Strict patient-scoped similarity search.
        Evaluates ONLY chunks belonging to patient_id.
        """
        patient_chunks = self._patient_chunks.get(patient_id, [])
        if not patient_chunks:
            return []

        query_tokens = tokenize(query)
        if not query_tokens:
            return []

        query_vec = expand_tokens(query_tokens)

        scored_chunks = []
        for chunk in patient_chunks:
            # Double safety check: patient isolation
            if chunk.patient_id != patient_id:
                continue

            sim = compute_cosine_similarity(query_vec, chunk.term_vector)
            if sim >= min_score:
                scored_chunks.append((sim, chunk))

        # Sort descending by similarity score
        scored_chunks.sort(key=lambda x: x[0], reverse=True)

        results: List[RAGSourceItem] = []
        for sim, chunk in scored_chunks[:top_k]:
            results.append(
                RAGSourceItem(
                    document_id=chunk.document_id,
                    title=chunk.title,
                    document_date=chunk.document_date,
                    chunk_text=chunk.chunk_text,
                    similarity_score=round(float(sim), 4),
                    patient_id=chunk.patient_id,
                )
            )

        return results

    def similarity_search(
        self,
        query: str,
        top_k: int = 5,
        patient_id: Optional[str] = None,
    ) -> List[RAGSourceItem]:
        """Patient-scoped similarity search or alias for search_patient_scoped."""
        if patient_id:
            return self.search_patient_scoped(patient_id=patient_id, query=query, top_k=top_k)
        return []


# Global singleton instance
_vector_store_instance = PatientVectorStore()


def get_patient_vector_store(client: Optional[Any] = None, patient_id: Optional[str] = None) -> PatientVectorStore:
    """
    Returns the singleton patient-scoped vector store.
    If client and patient_id are provided, automatically loads and indexes the patient's documents from Supabase.
    """
    if client is not None and patient_id is not None:
        if patient_id not in _vector_store_instance._patient_chunks or not _vector_store_instance._patient_chunks[patient_id]:
            try:
                docs_res = client.table("medical_documents").select("*").eq("patient_id", patient_id).execute()
                if docs_res.data:
                    _vector_store_instance.index_documents_for_patient(patient_id, docs_res.data)
            except Exception as e:
                logger.warning(f"Failed to auto-index documents for patient {patient_id}: {e}")
    return _vector_store_instance
