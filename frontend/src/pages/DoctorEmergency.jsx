import { useState } from "react"
import DashboardLayout from "../layouts/DashboardLayout"

const patients = [
  {
    id: "PT-KABIR-005",
    name: "Kabir Malhotra",
    age: 52,
    gender: "Male",
    bloodGroup: "O-",
    allergy: "Severe Penicillin Allergy",
    reaction: "Anaphylaxis",
    criticalConditions: ["Severe Penicillin Allergy"],
    medications: "No medication information specified in current demo dataset",
    emergencyEvents: [
      {
        date: "18 Jan 2024",
        title: "Bacterial Pneumonia Hospitalization",
        description:
          "Hospitalization for bacterial pneumonia documented in historical records.",
      },
      {
        date: "06 Sep 2026",
        title: "Emergency Presentation",
        description:
          "Emergency presentation requiring immediate access to critical medical history.",
      },
    ],
  },
  {
    id: "PT-NIKHIL-003",
    name: "Nikhil Varma",
    age: 61,
    gender: "Male",
    bloodGroup: "A+",
    allergy: "No known allergies",
    reaction: null,
    criticalConditions: ["Previous Myocardial Infarction"],
    medications:
      "Aspirin, Clopidogrel, Atorvastatin, Metoprolol",
    emergencyEvents: [
      {
        date: "11 Feb 2023",
        title: "Myocardial Infarction",
        description:
          "Hospitalization followed by angiography and angioplasty with stent placement.",
      },
      {
        date: "2024–2026",
        title: "Cardiology Follow-ups",
        description:
          "Longitudinal cardiology follow-up records available.",
      },
    ],
  },
  {
    id: "PT-TANYA-006",
    name: "Tanya Bose",
    age: 34,
    gender: "Female",
    bloodGroup: "A-",
    allergy: "No known allergies",
    reaction: null,
    criticalConditions: ["Intracranial Lesion"],
    medications: "Not specified in emergency summary",
    emergencyEvents: [
      {
        date: "10 Sep 2025",
        title: "Brain Surgery",
        description:
          "Surgical treatment for intracranial lesion.",
      },
      {
        date: "2026",
        title: "Neurological Follow-up",
        description:
          "Post-operative neurological follow-up documented.",
      },
    ],
  },
]

function DoctorEmergency() {
  const [selectedPatient, setSelectedPatient] = useState(null)
  const [reason, setReason] = useState("")
  const [authorized, setAuthorized] = useState(false)
  const [showConfirmation, setShowConfirmation] = useState(false)

  const openEmergencyAccess = () => {
    if (!selectedPatient || !reason.trim()) {
      return
    }

    setShowConfirmation(true)
  }

  const confirmEmergencyAccess = () => {
    setAuthorized(true)
    setShowConfirmation(false)
  }

  const resetEmergency = () => {
    setSelectedPatient(null)
    setReason("")
    setAuthorized(false)
    setShowConfirmation(false)
  }

  return (
    <DashboardLayout
      role="doctor"
      userName="Dr. Priya Sharma"
    >
      <div className="doctor-page">

        {/* HEADER */}
        <div className="doctor-page-header emergency-page-header">
          <div>
            <div className="doctor-eyebrow">
              EMERGENCY ACCESS
            </div>

            <h1>Break-Glass Emergency Access</h1>

            <p>
              Access critical patient information when normal
              authorization is unavailable.
            </p>
          </div>

          {authorized && (
            <div className="emergency-active-badge">
              <span></span>
              Emergency Access Active
            </div>
          )}
        </div>

        {/* WARNING */}
        <div className="emergency-warning-banner">
          <div className="emergency-warning-icon">
            !
          </div>

          <div>
            <strong>
              Break-glass access is intended for genuine emergencies
            </strong>

            <p>
              Every emergency access event is recorded in the audit
              trail. This mode provides emergency read access only
              and does not allow modification of medical records.
            </p>
          </div>
        </div>

        {!authorized ? (
          <>
            {/* ACCESS FORM */}
            <div className="emergency-access-card">

              <div className="emergency-card-header">
                <div>
                  <h2>Request Emergency Access</h2>
                  <p>
                    Select the patient and provide a clinical reason
                    for accessing their emergency passport.
                  </p>
                </div>

                <div className="emergency-lock-icon">
                  🔐
                </div>
              </div>

              {/* PATIENT SELECT */}
              <div className="emergency-section">

                <label>
                  Select Patient
                </label>

                <div className="emergency-patient-grid">

                  {patients.map((patient) => (
                    <button
                      type="button"
                      key={patient.id}
                      className={
                        selectedPatient?.id === patient.id
                          ? "emergency-patient-option selected"
                          : "emergency-patient-option"
                      }
                      onClick={() => setSelectedPatient(patient)}
                    >

                      <div className="emergency-patient-avatar">
                        {patient.name
                          .split(" ")
                          .map((word) => word[0])
                          .join("")
                          .slice(0, 2)}
                      </div>

                      <div className="emergency-patient-info">
                        <strong>{patient.name}</strong>
                        <span>
                          {patient.age} years • {patient.gender}
                        </span>
                        <small>{patient.id}</small>
                      </div>

                      <div className="emergency-radio">
                        {selectedPatient?.id === patient.id
                          ? "✓"
                          : ""}
                      </div>

                    </button>
                  ))}

                </div>

              </div>

              {/* REASON */}
              <div className="emergency-section">

                <label htmlFor="emergency-reason">
                  Reason for Emergency Access
                </label>

                <textarea
                  id="emergency-reason"
                  value={reason}
                  onChange={(e) => setReason(e.target.value)}
                  placeholder="Example: Patient is unconscious and previous medical history is required to identify critical allergies and medications."
                  rows="4"
                />

                <div className="emergency-character-count">
                  {reason.length} / 500
                </div>

              </div>

              {/* PERMISSIONS */}
              <div className="emergency-permission-box">

                <div className="permission-title">
                  <span>🛡</span>
                  Emergency Access Permissions
                </div>

                <div className="permission-grid">

                  <div className="permission-item allowed">
                    <span>✓</span>
                    <div>
                      <strong>Critical Information</strong>
                      <small>
                        Allergies, medications, conditions,
                        blood group and relevant events
                      </small>
                    </div>
                  </div>

                  <div className="permission-item allowed">
                    <span>✓</span>
                    <div>
                      <strong>Integrity Verification</strong>
                      <small>
                        Verify available blockchain provenance
                      </small>
                    </div>
                  </div>

                  <div className="permission-item denied">
                    <span>×</span>
                    <div>
                      <strong>Modify Medical Records</strong>
                      <small>
                        Database modifications are disabled
                      </small>
                    </div>
                  </div>

                  <div className="permission-item denied">
                    <span>×</span>
                    <div>
                      <strong>Approve AI Findings</strong>
                      <small>
                        AI findings cannot be approved in this mode
                      </small>
                    </div>
                  </div>

                </div>

              </div>

              {/* ACTION */}
              <div className="emergency-form-footer">

                <span>
                  🔒 This action will be recorded in the audit trail.
                </span>

                <button
                  type="button"
                  className="emergency-request-button"
                  disabled={
                    !selectedPatient ||
                    !reason.trim()
                  }
                  onClick={openEmergencyAccess}
                >
                  🚨 Request Emergency Access
                </button>

              </div>

            </div>

            {/* RECENT EMERGENCY ACCESS */}
            <div className="emergency-history-card">

              <div className="emergency-history-header">
                <div>
                  <h2>Recent Emergency Access</h2>
                  <p>
                    Previous break-glass events recorded by Medi-Trace
                  </p>
                </div>
              </div>

              <div className="emergency-history-row">

                <div className="history-status-dot"></div>

                <div className="history-main">
                  <strong>
                    Dr. Priya Sharma accessed Kabir Malhotra
                  </strong>

                  <span>
                    Critical allergy information required during
                    emergency presentation
                  </span>
                </div>

                <div className="history-time">
                  Today, 14:32
                </div>

              </div>

              <div className="emergency-history-row">

                <div className="history-status-dot"></div>

                <div className="history-main">
                  <strong>
                    Dr. Rahul Menon accessed Nikhil Varma
                  </strong>

                  <span>
                    Emergency cardiac history review
                  </span>
                </div>

                <div className="history-time">
                  Yesterday, 19:08
                </div>

              </div>

            </div>
          </>
        ) : (

          /* =====================================================
             EMERGENCY PASSPORT
             ===================================================== */

          <div className="emergency-passport-card">

            <div className="emergency-passport-header">

              <div>
                <span>EMERGENCY PASSPORT</span>
                <h2>{selectedPatient.name}</h2>

                <p>
                  Emergency read-only access granted
                </p>
              </div>

              <button
                type="button"
                className="emergency-end-button"
                onClick={resetEmergency}
              >
                End Emergency Access
              </button>

            </div>

            {/* PATIENT BASIC INFO */}
            <div className="emergency-basic-info">

              <div>
                <span>Patient ID</span>
                <strong>{selectedPatient.id}</strong>
              </div>

              <div>
                <span>Age</span>
                <strong>{selectedPatient.age} years</strong>
              </div>

              <div>
                <span>Gender</span>
                <strong>{selectedPatient.gender}</strong>
              </div>

              <div>
                <span>Blood Group</span>
                <strong className="blood-group-value">
                  {selectedPatient.bloodGroup}
                </strong>
              </div>

            </div>

            {/* CRITICAL INFO */}
            <div className="emergency-critical-grid">

              <div className="critical-emergency-card allergy-card">

                <div className="critical-card-title">
                  <span>⚠</span>
                  Critical Allergy
                </div>

                <strong>
                  {selectedPatient.allergy}
                </strong>

                {selectedPatient.reaction && (
                  <p>
                    Reaction:{" "}
                    <strong>{selectedPatient.reaction}</strong>
                  </p>
                )}

              </div>

              <div className="critical-emergency-card condition-card">

                <div className="critical-card-title">
                  <span>♥</span>
                  Critical Conditions
                </div>

                {selectedPatient.criticalConditions.map(
                  (condition) => (
                    <strong key={condition}>
                      {condition}
                    </strong>
                  )
                )}

              </div>

              <div className="critical-emergency-card medication-card">

                <div className="critical-card-title">
                  <span>✚</span>
                  Current Medications
                </div>

                <strong>
                  {selectedPatient.medications}
                </strong>

              </div>

            </div>

            {/* EVENTS */}
            <div className="emergency-events-section">

              <div className="emergency-events-title">
                <div>
                  <h3>Relevant Medical History</h3>
                  <p>
                    Historical events available for emergency review
                  </p>
                </div>

                <span className="readonly-badge">
                  READ ONLY
                </span>
              </div>

              <div className="emergency-event-list">

                {selectedPatient.emergencyEvents.map(
                  (event, index) => (

                    <div
                      className="emergency-event-row"
                      key={`${event.date}-${index}`}
                    >

                      <div className="emergency-event-date">
                        {event.date}
                      </div>

                      <div className="emergency-event-line">
                        <span></span>
                      </div>

                      <div className="emergency-event-content">
                        <strong>{event.title}</strong>
                        <p>{event.description}</p>
                      </div>

                    </div>

                  )
                )}

              </div>

            </div>

            {/* VERIFICATION */}
            <div className="emergency-verification-panel">

              <div className="verification-panel-icon">
                ✓
              </div>

              <div>
                <strong>
                  Integrity verification available
                </strong>

                <p>
                  Critical events can be checked against available
                  blockchain provenance. Verification does not
                  determine medical truth.
                </p>
              </div>

              <button
                type="button"
                className="emergency-verify-button"
                onClick={() => alert("Demo: Integrity verification requested.")}
              >
                Verify Integrity
              </button>

            </div>

            {/* READ ONLY NOTICE */}
            <div className="emergency-readonly-notice">
              <span>🔒</span>

              <div>
                <strong>
                  Read-only emergency session
                </strong>

                <p>
                  Medical records cannot be edited, deleted,
                  approved, or otherwise modified while using
                  break-glass access.
                </p>
              </div>
            </div>

          </div>
        )}

      </div>

      {/* CONFIRMATION MODAL */}
      {showConfirmation && selectedPatient && (

        <div
          className="emergency-modal-overlay"
          onClick={() => setShowConfirmation(false)}
        >

          <div
            className="emergency-confirm-modal"
            onClick={(e) => e.stopPropagation()}
          >

            <div className="confirm-warning-icon">
              🚨
            </div>

            <h2>Confirm Emergency Access</h2>

            <p>
              You are requesting break-glass access to the
              emergency health passport of:
            </p>

            <div className="confirm-patient">
              <strong>{selectedPatient.name}</strong>
              <span>{selectedPatient.id}</span>
            </div>

            <div className="confirm-reason">

              <span>Recorded reason</span>

              <p>
                {reason}
              </p>

            </div>

            <div className="confirm-audit-note">
              ⚠ This access will be permanently recorded in the
              audit trail.
            </div>

            <div className="confirm-actions">

              <button
                type="button"
                className="confirm-cancel-button"
                onClick={() => setShowConfirmation(false)}
              >
                Cancel
              </button>

              <button
                type="button"
                className="confirm-access-button"
                onClick={confirmEmergencyAccess}
              >
                Confirm Emergency Access
              </button>

            </div>

          </div>

        </div>

      )}

    </DashboardLayout>
  )
}

export default DoctorEmergency