import { useMemo, useState } from "react"
import { useNavigate } from "react-router-dom"
import DashboardLayout from "../layouts/DashboardLayout.jsx"
import { api } from "../services/api"
import { useApiQuery } from "../hooks/useApiQuery"
import { ErrorState, LoadingState } from "../components/AsyncState"

function DoctorDashboard() {
  const navigate = useNavigate(); const [search, setSearch] = useState("")
  const { data, loading, error, refresh } = useApiQuery(api.doctorPatients, [])
  const patients = useMemo(() => (data || []).map((item) => ({ ...item, id: item.patient_id || item.id, name: item.full_name || item.name || "Patient", condition: item.relationship_type || "Authorized patient", status: item.access_status || "Accessible" })), [data])
  const filtered = patients.filter((item) => `${item.name} ${item.condition}`.toLowerCase().includes(search.toLowerCase()))
  return <DashboardLayout role="doctor" userName="Doctor"><div className="doctor-dashboard-page"><div className="dashboard-page-header"><div><div className="page-eyebrow">CLINICAL WORKSPACE</div><h1>Doctor Dashboard</h1><p>Patients and permissions are supplied by the FastAPI backend.</p></div></div>{loading && <LoadingState label="Loading accessible patients…" />}{error && <ErrorState error={error} onRetry={refresh} />}{!loading && !error && <><div className="stats-grid"><div className="stat-card"><span>👥</span><div><span>Total patients</span><strong>{patients.length}</strong></div></div><div className="stat-card"><span>✓</span><div><span>Normal access</span><strong>{patients.filter((item) => String(item.access_status || "").toUpperCase().includes("NORMAL")).length}</strong></div></div><div className="stat-card"><span>🚨</span><div><span>Emergency tools</span><strong>Read-only</strong></div></div></div><section className="dashboard-panel"><div className="panel-header"><div><div className="section-kicker">PATIENT DIRECTORY</div><h2>Accessible patients</h2></div><input value={search} onChange={(event) => setSearch(event.target.value)} placeholder="Search patients" /></div>{filtered.length === 0 ? <p>No accessible patients found.</p> : <div className="doctor-patient-list">{filtered.map((item) => <button className="doctor-patient-card" type="button" key={item.id} onClick={() => navigate(`/doctor/passport/${item.id}`)}><div><strong>{item.name}</strong><p>{item.condition}</p></div><span>{item.status} →</span></button>)}</div>}</section></>}</div></DashboardLayout>
}
export default DoctorDashboard
