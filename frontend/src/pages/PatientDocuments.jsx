import { useMemo, useRef, useState } from "react"
import DashboardLayout from "../layouts/DashboardLayout.jsx"
import { api, readableError } from "../services/api"
import { useApiQuery } from "../hooks/useApiQuery"
import { ErrorState, LoadingState } from "../components/AsyncState"

function PatientDocuments() {
  const fileInput = useRef(null)
  const { data: summary, loading, error, refresh } = useApiQuery(api.patientMe, [])
  const [message, setMessage] = useState("")
  const [uploading, setUploading] = useState(false)
  const [selected, setSelected] = useState(null)
  const [title, setTitle] = useState("")
  const [documentType, setDocumentType] = useState("OTHER")
  const [documentDate, setDocumentDate] = useState("")
  const documents = useMemo(() => summary?.documents || summary?.medical_documents || [], [summary])

  async function uploadFile(event) {
    const file = event.target.files?.[0]
    event.target.value = ""
    if (!file) return
    setUploading(true); setMessage("")
    const form = new FormData(); form.append("file", file); form.append("document_type", documentType); if (title) form.append("title", title); if (documentDate) form.append("document_date", documentDate)
    try { await api.uploadDocument(form); setMessage("Document uploaded securely."); refresh() }
    catch (requestError) { setMessage(readableError(requestError)) }
    finally { setUploading(false) }
  }

  async function viewDocument(document) {
    try { const access = await api.document(document.document_id || document.id); setSelected({ ...document, url: access?.file_url || access?.download_url || access?.signed_url || access?.url }) }
    catch (requestError) { setMessage(readableError(requestError)) }
  }

  return <DashboardLayout role="patient" userName={summary?.profile?.full_name || "Patient"}>
    <div className="documents-page">
      <div className="dashboard-page-header"><div><div className="page-eyebrow">MEDICAL RECORDS</div><h1>Medical Documents</h1><p>Documents associated with your health passport.</p></div><button className="primary-action-button" type="button" onClick={() => fileInput.current?.click()} disabled={uploading}>{uploading ? "Uploading…" : "+ Add Document"}</button><input ref={fileInput} hidden type="file" accept=".pdf,.png,.jpg,.jpeg,application/pdf,image/png,image/jpeg" onChange={uploadFile} /></div>
      <section className="dashboard-panel"><div className="section-kicker">UPLOAD DETAILS</div><div className="form-group"><label>Title<input value={title} onChange={(event) => setTitle(event.target.value)} placeholder="Optional document title" /></label></div><div className="form-group"><label>Document type<select value={documentType} onChange={(event) => setDocumentType(event.target.value)}><option>OTHER</option><option>LAB_REPORT</option><option>IMAGING</option><option>DISCHARGE_SUMMARY</option><option>ALLERGY_RECORD</option><option>OPERATIVE_REPORT</option></select></label></div><div className="form-group"><label>Document date<input type="date" value={documentDate} onChange={(event) => setDocumentDate(event.target.value)} /></label></div><p>Choose a file above after entering optional metadata. Maximum size: 15 MB.</p></section>
      {message && <div className="document-message" role="status">{message}</div>}
      {loading && <LoadingState label="Loading your documents…" />}{error && <ErrorState error={error} onRetry={refresh} />}
      {!loading && !error && <section className="dashboard-panel documents-panel"><div className="panel-header"><div><div className="section-kicker">YOUR RECORDS</div><h2>Your Documents</h2><p>Securely returned by the MediTrace API.</p></div><div className="document-count">{documents.length} documents</div></div>{documents.length === 0 ? <div className="dashboard-panel">No documents are available yet.</div> : <div className="document-list">{documents.map((document) => { const id = document.document_id || document.id; return <div className="document-card" key={id}><div className="document-icon">📄</div><div className="document-information"><h3>{document.title || document.file_name || document.name || "Medical document"}</h3><p className="document-type">{document.document_type || document.type || "OTHER"}</p><div className="document-meta"><span>📅 {document.document_date || document.created_at || "Date not recorded"}</span></div></div><div className="document-status"><span className="document-status-badge">✓ {document.status || "Available"}</span><button className="document-view-button" type="button" onClick={() => viewDocument(document)}>View</button></div></div> })}</div>}</section>}
      <div className="workflow-note"><span className="workflow-note-icon">ℹ</span><p>Extracted findings remain suggestions until a doctor reviews them. MediTrace does not update your authoritative record from the browser.</p></div>
      {selected && <div className="document-modal-overlay" onClick={() => setSelected(null)}><div className="document-modal" onClick={(event) => event.stopPropagation()}><div className="document-modal-header"><h2>{selected.title || selected.file_name || selected.name || "Document"}</h2><button className="modal-close-button" onClick={() => setSelected(null)}>×</button></div>{selected.url ? <iframe title="Medical document" src={selected.url} style={{ width: "100%", minHeight: 600, border: 0 }} /> : <p>Document URL was not returned by the backend.</p>}</div></div>}
    </div>
  </DashboardLayout>
}

export default PatientDocuments
