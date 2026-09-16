import DashboardLayout from "../layouts/DashboardLayout.jsx"
import { api } from "../services/api"
import { useApiQuery } from "../hooks/useApiQuery"
import { ErrorState, LoadingState } from "../components/AsyncState"

function EmergencyPassport() {
  // Patient passport data comes from the patient-owned endpoint. The
  // emergency summary endpoint is reserved for doctor normal/break-glass
  // access and returns 403 for a patient session.
  const { data, loading, error, refresh } = useApiQuery(api.patientMe, [])
  const profile = data?.profile || data?.patient || {}
  const allergies = data?.allergies || []; const conditions = data?.conditions || []; const medications = data?.medications || []
  return <DashboardLayout role="patient" userName={profile.full_name || "Patient"}><div className="patient-passport-page"><div className="dashboard-page-header"><div><div className="page-eyebrow">EMERGENCY PASSPORT</div><h1>{profile.full_name || "Your emergency health passport"}</h1><p>Critical information returned directly from MediTrace.</p></div><span className="verified-badge">BACKEND RECORD</span></div>{loading && <LoadingState label="Loading emergency summary…" />}{error && <ErrorState error={error} onRetry={refresh} />}{!loading && !error && <><section className="patient-critical-alert"><div className="patient-critical-icon">!</div><div><div className="patient-alert-label">ALLERGIES</div><h2>{allergies.length ? allergies.map((item) => item.allergen || item.name).join(", ") : "No allergies recorded"}</h2><p>{allergies.length ? "Share this information with your treating clinician." : "No allergy information is currently recorded."}</p></div></section><div className="passport-section"><h2>Conditions</h2>{conditions.length ? <ul>{conditions.map((item, index) => <li key={index}>{item.condition_name || item.name || item}</li>)}</ul> : <p>No conditions recorded.</p>}</div><div className="passport-section"><h2>Medications</h2>{medications.length ? <ul>{medications.map((item, index) => <li key={index}>{[item.medication_name || item.name, item.dosage, item.frequency].filter(Boolean).join(" — ")}</li>)}</ul> : <p>No medications recorded.</p>}</div><div className="passport-section"><h2>Emergency notes</h2><pre className="clinical-output">{JSON.stringify(data?.critical_history || data?.emergency_notes || [], null, 2)}</pre></div></>}</div></DashboardLayout>
}
export default EmergencyPassport
