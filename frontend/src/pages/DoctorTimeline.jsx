import { useState } from "react"
import DashboardLayout from "../layouts/DashboardLayout.jsx"
import { api } from "../services/api"
import { useApiQuery } from "../hooks/useApiQuery"
import { ErrorState, LoadingState } from "../components/AsyncState"

function DoctorTimeline() {
  const [patientId, setPatientId] = useState("")
  const directory = useApiQuery(api.doctorPatients, [])
  const timeline = useApiQuery(() => patientId ? api.patientSummary(patientId) : Promise.resolve(null), [patientId])
  const events = timeline.data?.medical_events || []
  return <DashboardLayout role="doctor" userName="Doctor"><div className="doctor-timeline-page"><div className="dashboard-page-header"><div><div className="page-eyebrow">MEDICAL TIMELINE</div><h1>Patient timeline</h1><p>Clinical events are loaded from the authorized patient summary.</p></div></div>{directory.loading && <LoadingState label="Loading accessible patients…" />}{directory.error && <ErrorState error={directory.error} onRetry={directory.refresh} />}{!directory.loading && !directory.error && <section className="dashboard-panel"><h2>Select patient</h2><select value={patientId} onChange={(event) => setPatientId(event.target.value)}><option value="">Select patient</option>{(directory.data || []).map((item) => <option key={item.patient_id || item.id} value={item.patient_id || item.id}>{item.full_name || item.name || item.patient_id}</option>)}</select></section>}{patientId && timeline.loading && <LoadingState label="Loading timeline…" />}{patientId && timeline.error && <ErrorState error={timeline.error} onRetry={timeline.refresh} />}{patientId && !timeline.loading && !timeline.error && <section className="dashboard-panel"><div className="section-kicker">AUTHORITATIVE EVENTS</div><h2>{events.length} events</h2>{events.length ? <div className="doctor-timeline">{events.map((event, index) => <article className="doctor-timeline-item" key={event.event_id || event.id || index}><time>{event.event_date || "Date not recorded"}</time><div><h3>{event.title || event.event_type || "Medical event"}</h3><p>{event.description || "No description recorded."}</p><small>{event.doctor_name || "MediTrace record"} · {event.status || "Recorded"}</small></div></article>)}</div> : <p>No medical events returned.</p>}</section>}</div></DashboardLayout>
}
export default DoctorTimeline
