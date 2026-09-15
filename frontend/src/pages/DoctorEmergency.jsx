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

function Icon({ name, size = 20 }) {
  const common = {
    width: size,
    height: size,
    viewBox: "0 0 24 24",
    fill: "none",
    stroke: "currentColor",
    strokeWidth: 1.8,
    strokeLinecap: "round",
    strokeLinejoin: "round",
  }

  const icons = {
    alert: (
      <>
        <path d="M10.3 3.8 2.2 18a2 2 0 0 0 1.7 3h16.2a2 2 0 0 0 1.7-3L13.7 3.8a2 2 0 0 0-3.4 0z" />
        <path d="M12 9v4M12 17h.01" />
      </>
    ),

    shield: (
      <>
        <path d="M12 3l8 3v5c0 5.2-3.4 8.5-8 10-4.6-1.5-8-4.8-8-10V6l8-3z" />
        <path d="m9 12 2 2 4-4" />
      </>
    ),

    lock: (
      <>
        <rect x="5" y="10" width="14" height="11" rx="2" />
        <path d="M8 10V7a4 4 0 0 1 8 0v3" />
        <path d="M12 14v3" />
      </>
    ),

    unlock: (
      <>
        <rect x="5" y="10" width="14" height="11" rx="2" />
        <path d="M8 10V7a4 4 0 0 1 7.5-1.8" />
      </>
    ),

    user: (
      <>
        <circle cx="12" cy="8" r="3.5" />
        <path d="M5 21a7 7 0 0 1 14 0" />
      </>
    ),

    check: <path d="m5 12 4 4L19 6" />,

    close: (
      <>
        <path d="m6 6 12 12M18 6 6 18" />
      </>
    ),

    file: (
      <>
        <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
        <path d="M14 2v6h6" />
        <path d="M8 13h8M8 17h5" />
      </>
    ),

    link: (
      <>
        <path d="M10 13a5 5 0 0 0 7.1.1l2-2a5 5 0 0 0-7.1-7.1l-1.1 1.1" />
        <path d="M14 11a5 5 0 0 0-7.1-.1l-2 2A5 5 0 0 0 12 20l1.1-1.1" />
      </>
    ),

    clock: (
      <>
        <circle cx="12" cy="12" r="9" />
        <path d="M12 7v5l3 2" />
      </>
    ),

    arrow: (
      <>
        <path d="M5 12h14" />
        <path d="m13 6 6 6-6 6" />
      </>
    ),

    back: (
      <>
        <path d="M19 12H5" />
        <path d="m11 18-6-6 6-6" />
      </>
    ),
  }

  return <svg {...common}>{icons[name]}</svg>
}

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
      <div className="doctor-page polished-emergency-page">

        {/* HEADER */}
        <div className="doctor-page-header emergency-polished-header">
          <div>
            <div className="doctor-eyebrow emergency-eyebrow">
              <span>
                <Icon name="alert" size={14} />
              </span>
              EMERGENCY ACCESS
            </div>

            <h1>Break-Glass Emergency Access</h1>

            <p>
              Access critical patient information when normal authorization
              is unavailable.
            </p>
          </div>

          {authorized && (
            <div className="emergency-active-badge polished-active-badge">
              <span className="active-dot"></span>
              <div>
                <strong>Emergency Access Active</strong>
                <small>Read-only session</small>
              </div>
            </div>
          )}
        </div>

        {/* WARNING */}
        <div className="emergency-warning-banner polished-emergency-warning">
          <div className="emergency-warning-icon">
            <Icon name="alert" size={21} />
          </div>

          <div className="emergency-warning-content">
            <strong>
              Break-glass access is intended for genuine emergencies
            </strong>

            <p>
              Every emergency access event is recorded in the audit trail.
              This mode provides emergency read access only and does not
              allow modification of medical records.
            </p>
          </div>

          <span className="emergency-warning-tag">
            AUDITED ACCESS
          </span>
        </div>

        {!authorized ? (
          <>
            {/* ACCESS REQUEST */}
            <div className="emergency-access-card polished-emergency-card">

              <div className="emergency-card-header polished-emergency-header">
                <div>
                  <span className="emergency-section-label">
                    STEP 01
                  </span>

                  <h2>Request Emergency Access</h2>

                  <p>
                    Select the patient and provide a clinical reason for
                    accessing their emergency passport.
                  </p>
                </div>

                <div className="emergency-lock-icon polished-lock-icon">
                  <Icon name="lock" size={23} />
                </div>
              </div>

              {/* PATIENT */}
              <div className="emergency-section polished-emergency-section">

                <div className="emergency-section-heading">
                  <div>
                    <label>Select Patient</label>
                    <span>
                      Choose the patient requiring emergency review.
                    </span>
                  </div>

                  {selectedPatient && (
                    <span className="selected-patient-indicator">
                      <Icon name="check" size={12} />
                      Selected
                    </span>
                  )}
                </div>

                <div className="emergency-patient-grid polished-patient-grid">

                  {patients.map((patient) => (
                    <button
                      type="button"
                      key={patient.id}
                      className={
                        selectedPatient?.id === patient.id
                          ? "emergency-patient-option selected polished-patient-option"
                          : "emergency-patient-option polished-patient-option"
                      }
                      onClick={() => setSelectedPatient(patient)}
                    >
                      <div className="emergency-patient-avatar polished-emergency-avatar">
                        {patient.name
                          .split(" ")
                          .map((word) => word[0])
                          .join("")
                          .slice(0, 2)}
                      </div>

                      <div className="emergency-patient-info">
                        <strong>{patient.name}</strong>

                        <span>
                          {patient.age} years · {patient.gender}
                        </span>

                        <small>{patient.id}</small>
                      </div>

                      <div className="emergency-radio polished-emergency-radio">
                        {selectedPatient?.id === patient.id && (
                          <Icon name="check" size={12} />
                        )}
                      </div>
                    </button>
                  ))}

                </div>
              </div>

              {/* REASON */}
              <div className="emergency-section polished-emergency-section">

                <div className="emergency-section-heading">
                  <div>
                    <label htmlFor="emergency-reason">
                      Reason for Emergency Access
                    </label>

                    <span>
                      This reason will be permanently recorded in the audit trail.
                    </span>
                  </div>

                  <span className="reason-required">
                    REQUIRED
                  </span>
                </div>

                <div className="reason-input-wrapper">
                  <textarea
                    id="emergency-reason"
                    value={reason}
                    onChange={(e) => {
                      if (e.target.value.length <= 500) {
                        setReason(e.target.value)
                      }
                    }}
                    placeholder="Example: Patient is unconscious and previous medical history is required to identify critical allergies and medications."
                    rows="4"
                  />

                  <div className="emergency-character-count">
                    {reason.length} / 500
                  </div>
                </div>

              </div>

              {/* PERMISSIONS */}
              <div className="emergency-permission-box polished-permission-box">

                <div className="permission-title polished-permission-title">
                  <div className="permission-title-icon">
                    <Icon name="shield" size={17} />
                  </div>

                  <div>
                    <strong>Emergency Access Permissions</strong>
                    <span>Restricted break-glass scope</span>
                  </div>
                </div>

                <div className="permission-grid polished-permission-grid">

                  <div className="permission-item allowed polished-permission-item">
                    <div className="permission-check allowed-check">
                      <Icon name="check" size={12} />
                    </div>

                    <div>
                      <strong>Critical Information</strong>
                      <small>
                        Allergies, medications, conditions, blood group
                        and relevant events
                      </small>
                    </div>
                  </div>

                  <div className="permission-item allowed polished-permission-item">
                    <div className="permission-check allowed-check">
                      <Icon name="check" size={12} />
                    </div>

                    <div>
                      <strong>Integrity Verification</strong>
                      <small>
                        Verify available blockchain provenance
                      </small>
                    </div>
                  </div>

                  <div className="permission-item denied polished-permission-item">
                    <div className="permission-check denied-check">
                      <Icon name="close" size={12} />
                    </div>

                    <div>
                      <strong>Modify Medical Records</strong>
                      <small>
                        Database modifications are disabled
                      </small>
                    </div>
                  </div>

                  <div className="permission-item denied polished-permission-item">
                    <div className="permission-check denied-check">
                      <Icon name="close" size={12} />
                    </div>

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
              <div className="emergency-form-footer polished-emergency-footer">

                <div className="audit-reminder">
                  <Icon name="clock" size={14} />

                  <span>
                    This action will be recorded in the audit trail.
                  </span>
                </div>

                <button
                  type="button"
                  className="emergency-request-button polished-emergency-button"
                  disabled={
                    !selectedPatient ||
                    !reason.trim()
                  }
                  onClick={openEmergencyAccess}
                >
                  <Icon name="unlock" size={17} />
                  Request Emergency Access
                </button>

              </div>

            </div>

            {/* RECENT ACCESS */}
            <div className="emergency-history-card polished-history-card">

              <div className="emergency-history-header polished-history-header">
                <div>
                  <span className="emergency-section-label">
                    AUDIT HISTORY
                  </span>

                  <h2>Recent Emergency Access</h2>

                  <p>
                    Previous break-glass events recorded by Medi-Trace
                  </p>
                </div>

                <div className="history-count">
                  2 events
                </div>
              </div>

              <div className="emergency-history-row polished-history-row">

                <div className="history-status-dot"></div>

                <div className="history-main">
                  <strong>
                    Dr. Priya Sharma accessed Kabir Malhotra
                  </strong>

                  <span>
                    Critical allergy information required during emergency
                    presentation
                  </span>
                </div>

                <div className="history-time">
                  <Icon name="clock" size={12} />
                  Today, 14:32
                </div>

              </div>

              <div className="emergency-history-row polished-history-row">

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
                  <Icon name="clock" size={12} />
                  Yesterday, 19:08
                </div>

              </div>

            </div>
          </>
        ) : (

          /* =====================================================
             EMERGENCY PASSPORT
             ===================================================== */

          <div className="emergency-passport-card polished-emergency-passport">

            {/* PASSPORT HEADER */}
            <div className="emergency-passport-header polished-passport-header">

              <div className="passport-patient-heading">
                <div className="passport-active-icon">
                  <Icon name="unlock" size={21} />
                </div>

                <div>
                  <span>EMERGENCY PASSPORT</span>
                  <h2>{selectedPatient.name}</h2>

                  <p>
                    Emergency read-only access granted
                  </p>
                </div>
              </div>

              <button
                type="button"
                className="emergency-end-button polished-end-button"
                onClick={resetEmergency}
              >
                <Icon name="close" size={15} />
                End Emergency Access
              </button>

            </div>

            {/* ACCESS STRIP */}
            <div className="emergency-session-strip">
              <div>
                <span className="session-dot"></span>
                <strong>Emergency session active</strong>
              </div>

              <span>
                WRITE ACCESS DISABLED
              </span>
            </div>

            {/* BASIC INFO */}
            <div className="emergency-basic-info polished-basic-info">

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
            <div className="emergency-critical-grid polished-critical-grid">

              <div className="critical-emergency-card allergy-card polished-critical-card">

                <div className="critical-card-title">
                  <span className="critical-card-icon">
                    <Icon name="alert" size={15} />
                  </span>

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

              <div className="critical-emergency-card condition-card polished-critical-card">

                <div className="critical-card-title">
                  <span className="critical-card-icon">
                    <Icon name="shield" size={15} />
                  </span>

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

              <div className="critical-emergency-card medication-card polished-critical-card">

                <div className="critical-card-title">
                  <span className="critical-card-icon">
                    <Icon name="file" size={15} />
                  </span>

                  Current Medications
                </div>

                <strong>
                  {selectedPatient.medications}
                </strong>

              </div>

            </div>

            {/* EVENTS */}
            <div className="emergency-events-section polished-events-section">

              <div className="emergency-events-title polished-events-title">
                <div>
                  <span className="emergency-section-label">
                    HISTORICAL EVIDENCE
                  </span>

                  <h3>Relevant Medical History</h3>

                  <p>
                    Historical events available for emergency review
                  </p>
                </div>

                <span className="readonly-badge polished-readonly-badge">
                  <Icon name="lock" size={11} />
                  READ ONLY
                </span>
              </div>

              <div className="emergency-event-list polished-event-list">

                {selectedPatient.emergencyEvents.map(
                  (event, index) => (
                    <div
                      className="emergency-event-row polished-event-row"
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
            <div className="emergency-verification-panel polished-verification-panel">

              <div className="verification-panel-icon">
                <Icon name="shield" size={20} />
              </div>

              <div>
                <strong>
                  Integrity verification available
                </strong>

                <p>
                  Critical events can be checked against available blockchain
                  provenance. Verification does not determine medical truth.
                </p>
              </div>

              <button
                type="button"
                className="emergency-verify-button polished-verify-button"
                onClick={() =>
                  alert(
                    "Demo: Integrity verification requested."
                  )
                }
              >
                <Icon name="check" size={15} />
                Verify Integrity
              </button>

            </div>

            {/* READ ONLY */}
            <div className="emergency-readonly-notice polished-readonly-notice">

              <div className="readonly-notice-icon">
                <Icon name="lock" size={16} />
              </div>

              <div>
                <strong>
                  Read-only emergency session
                </strong>

                <p>
                  Medical records cannot be edited, deleted, approved,
                  or otherwise modified while using break-glass access.
                </p>
              </div>

            </div>

          </div>
        )}

      </div>

      {/* CONFIRMATION MODAL */}
      {showConfirmation && selectedPatient && (
        <div
          className="emergency-modal-overlay polished-emergency-overlay"
          onClick={() => setShowConfirmation(false)}
        >
          <div
            className="emergency-confirm-modal polished-confirm-modal"
            onClick={(e) => e.stopPropagation()}
          >

            <div className="confirm-warning-icon polished-confirm-icon">
              <Icon name="alert" size={25} />
            </div>

            <span className="confirm-eyebrow">
              BREAK-GLASS AUTHORIZATION
            </span>

            <h2>Confirm Emergency Access</h2>

            <p>
              You are requesting emergency read-only access to the
              patient's emergency health passport.
            </p>

            <div className="confirm-patient polished-confirm-patient">
              <div className="confirm-avatar">
                {selectedPatient.name
                  .split(" ")
                  .map((word) => word[0])
                  .join("")
                  .slice(0, 2)}
              </div>

              <div>
                <strong>{selectedPatient.name}</strong>
                <span>{selectedPatient.id}</span>
              </div>
            </div>

            <div className="confirm-reason polished-confirm-reason">
              <span>Recorded reason</span>

              <p>
                {reason}
              </p>
            </div>

            <div className="confirm-audit-note polished-audit-note">
              <Icon name="clock" size={15} />

              <span>
                This access will be permanently recorded in the audit trail.
              </span>
            </div>

            <div className="confirm-permission-summary">
              <span>
                <Icon name="check" size={12} />
                Emergency Read
              </span>

              <span>
                <Icon name="check" size={12} />
                Integrity Verification
              </span>

              <span className="blocked">
                <Icon name="close" size={12} />
                Write Access
              </span>
            </div>

            <div className="confirm-actions">

              <button
                type="button"
                className="confirm-cancel-button polished-cancel-button"
                onClick={() => setShowConfirmation(false)}
              >
                Cancel
              </button>

              <button
                type="button"
                className="confirm-access-button polished-confirm-button"
                onClick={confirmEmergencyAccess}
              >
                <Icon name="unlock" size={16} />
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