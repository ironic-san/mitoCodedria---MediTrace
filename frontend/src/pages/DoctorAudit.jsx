import { useState } from "react"
import DashboardLayout from "../layouts/DashboardLayout.jsx"
import { api } from "../services/api"
import { useApiQuery } from "../hooks/useApiQuery"
import { ErrorState, LoadingState } from "../components/AsyncState"

function DoctorAudit() {
  const [patientId, setPatientId] = useState("")
  const directory = useApiQuery(api.doctorPatients, [])
  const audit = useApiQuery(() => patientId ? api.patientAudit(patientId) : Promise.resolve(null), [patientId])
  const logs = audit.data?.logs || audit.data?.audit_logs || audit.data || []
  return <DashboardLayout role="doctor" userName="Doctor"><div className="doctor-page"><div className="dashboard-page-header"><div><div className="page-eyebrow">AUDIT TRAIL</div><h1>Patient activity</h1><p>Audit data is read from the backend and scoped to the selected patient.</p></div></div>{directory.loading && <LoadingState label="Loading accessible patients…" />}{directory.error && <ErrorState error={directory.error} onRetry={directory.refresh} />}{!directory.loading && !directory.error && <section className="dashboard-panel"><h2>Select patient</h2><select value={patientId} onChange={(event) => setPatientId(event.target.value)}><option value="">Select patient</option>{(directory.data || []).map((item) => <option key={item.patient_id || item.id} value={item.patient_id || item.id}>{item.full_name || item.name || item.patient_id}</option>)}</select></section>}{patientId && audit.loading && <LoadingState label="Loading audit trail…" />}{patientId && audit.error && <ErrorState error={audit.error} onRetry={audit.refresh} />}{patientId && !audit.loading && !audit.error && <section className="dashboard-panel"><div className="section-kicker">AUDIT EVENTS</div><h2>{logs.length} events</h2>{logs.length ? <div className="audit-list">{logs.map((log, index) => <article className="audit-row" key={log.audit_id || log.id || index}><strong>{log.action || log.event_type || "Activity"}</strong><span>{log.timestamp || log.created_at || "Date not recorded"}</span><p>{log.reason || log.details?.description || log.entity_type || "No additional details returned."}</p></article>)}</div> : <p>No audit events returned.</p>}</section>}</div></DashboardLayout>
}
export default DoctorAudit
