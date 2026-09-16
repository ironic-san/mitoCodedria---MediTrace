import { useRef, useState } from "react"
import DashboardLayout from "../layouts/DashboardLayout.jsx"
import { api, readableError } from "../services/api"
import { useApiQuery } from "../hooks/useApiQuery"
import { ErrorState, LoadingState } from "../components/AsyncState"

function DoctorAIReviews() {
  const input = useRef(null)
  const { data: directory, loading, error, refresh } = useApiQuery(api.doctorPatients, [])
  const [patientId, setPatientId] = useState("")
  const [documentId, setDocumentId] = useState("")
  const [ocr, setOcr] = useState(null); const [retrievals, setRetrievals] = useState([]); const [analysis, setAnalysis] = useState(null)
  const [busy, setBusy] = useState(""); const [message, setMessage] = useState("")
  const patients = directory || []

  async function runWorkflow(event) {
    const file = event.target.files?.[0]; event.target.value = ""
    if (!file || !patientId) { setMessage("Select an accessible patient first."); return }
    setBusy("upload"); setMessage("")
    try {
      const form = new FormData(); form.append("file", file); form.append("patient_id", patientId)
      const uploaded = await api.uploadDocument(form); const uploadedId = uploaded?.document_id || uploaded?.id
      setDocumentId(uploadedId || "")
      const ocrForm = new FormData(); ocrForm.append("file", file); ocrForm.append("patient_id", patientId); if (uploadedId) ocrForm.append("document_id", uploadedId)
      const result = await api.ocr(ocrForm); setOcr(result); setDocumentId(result.document_id || uploadedId || "")
      setBusy("")
    } catch (requestError) { setMessage(readableError(requestError)); setBusy("") }
  }

  async function retrieve() {
    if (!patientId) return setMessage("Select an accessible patient first.")
    setBusy("rag"); setMessage("")
    try { const result = await api.rag({ patient_id: patientId, query: "What previous postoperative and preoperative history is documented?", max_sources: 5 }); setRetrievals(result?.retrievals || result?.sources || result || []) }
    catch (requestError) { setMessage(readableError(requestError)) } finally { setBusy("") }
  }

  async function generate() {
    if (!patientId || !documentId || !ocr) return setMessage("Upload and extract a document before generating the report.")
    setBusy("response"); setMessage("")
    try { setAnalysis(await api.response({ patient_id: patientId, document_id: documentId, doctor_query: "Compare the new report with the previous history.", ocr_findings: ocr, rag_retrievals: retrievals })) }
    catch (requestError) { setMessage(readableError(requestError)) } finally { setBusy("") }
  }

  async function runPipeline() {
    if (!patientId || !documentId) return setMessage("Upload a document before running the full pipeline.")
    setBusy("pipeline"); setMessage("")
    try { setAnalysis(await api.pipeline({ patient_id: patientId, document_id: documentId, extracted_text: ocr?.ocr?.extracted_text || "" })) }
    catch (requestError) { setMessage(readableError(requestError)) } finally { setBusy("") }
  }

  async function review(action) {
    if (!analysis?.analysis_id) return
    setBusy("review"); setMessage("")
    try { const result = await api.review({ analysis_id: analysis.analysis_id, review_action: action, notes: `Reviewed by doctor: ${action}.` }); setAnalysis((current) => ({ ...current, ...result, review_status: result?.review_status || action })); }
    catch (requestError) { setMessage(readableError(requestError)); if (requestError.status === 409) refresh() } finally { setBusy("") }
  }

  return <DashboardLayout role="doctor" userName="Doctor"><div className="ai-review-page polished-ai-page"><div className="dashboard-page-header"><div><div className="page-eyebrow">AI-ASSISTED CLINICAL REVIEW</div><h1>Clinical review workflow</h1><p>OCR, deterministic NLU, historical RAG, and Gemini are executed by the backend.</p></div></div>
    {loading && <LoadingState label="Loading accessible patients…" />}{error && <ErrorState error={error} onRetry={refresh} />}{message && <div className="document-message" role="alert">{message}</div>}
    {!loading && !error && <><section className="dashboard-panel"><div className="panel-header"><div><div className="section-kicker">1 · DOCUMENT</div><h2>Upload and select patient</h2></div></div><select value={patientId} onChange={(event) => { setPatientId(event.target.value); setOcr(null); setAnalysis(null) }}><option value="">Select an accessible patient</option>{patients.map((item) => <option key={item.patient_id || item.id} value={item.patient_id || item.id}>{item.full_name || item.name || item.patient_id}</option>)}</select><button type="button" className="primary-action-button" disabled={!patientId || busy === "upload"} onClick={() => input.current?.click()}>{busy === "upload" ? "Processing…" : "Upload document"}</button><input ref={input} hidden type="file" accept=".pdf,.png,.jpg,.jpeg" onChange={runWorkflow} />{documentId && <p>Document: {documentId}</p>}</section>
      {ocr && <section className="dashboard-panel"><div className="section-kicker">2 · OCR + NLU</div><h2>Extraction result</h2><p>Status: {ocr.ocr?.ocr_status || "Returned"} · Confidence: {ocr.ocr?.confidence_score ?? "—"}</p><pre className="clinical-output">{ocr.ocr?.extracted_text || "No extracted text returned."}</pre><details><summary>Structured NLU findings</summary><pre className="clinical-output">{JSON.stringify(ocr.nlu || {}, null, 2)}</pre></details></section>}
      {ocr && <section className="dashboard-panel"><div className="section-kicker">3 · HISTORICAL RAG</div><h2>Patient-scoped retrieval</h2><button type="button" className="secondary-action-button" onClick={retrieve} disabled={busy === "rag"}>{busy === "rag" ? "Retrieving…" : "Retrieve history"}</button>{retrievals.map((item, index) => <article className="retrieval-card" key={index}><strong>{item.title || "Historical source"}</strong><small>{item.date || "Date not recorded"} · {item.section || ""} · similarity {item.similarity_score ?? item.score ?? "—"}</small><p>{item.text || item.content || ""}</p></article>)}</section>}
      {ocr && <section className="dashboard-panel"><div className="section-kicker">4 · CLINICAL COMPARISON</div><h2>Backend-generated report</h2><button type="button" className="primary-action-button" onClick={generate} disabled={busy === "response" || !documentId}>{busy === "response" ? "Generating…" : "Generate grounded response"}</button><button type="button" className="secondary-action-button" onClick={runPipeline} disabled={busy === "pipeline" || !documentId}>{busy === "pipeline" ? "Running pipeline…" : "Run full AI pipeline"}</button>{analysis && <><div className="clinical-advisory"><strong>Advisory information — doctor review required</strong><p>{analysis.response || analysis.report || JSON.stringify(analysis)}</p></div><p>Review status: <strong>{analysis.review_status || "PENDING"}</strong></p>{String(analysis.review_status || "PENDING").toUpperCase() === "PENDING" && <div className="review-actions"><button type="button" className="secondary-action-button" disabled={busy === "review"} onClick={() => review("REJECT")}>Reject</button><button type="button" className="primary-action-button" disabled={busy === "review"} onClick={() => review("APPROVE")}>Approve</button></div>}</>}</section>}</>}
  </div></DashboardLayout>
}
export default DoctorAIReviews
