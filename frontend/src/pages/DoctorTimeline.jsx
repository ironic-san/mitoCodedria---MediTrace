import { useMemo, useState } from "react"
import DashboardLayout from "../layouts/DashboardLayout"

const patients = [
  {
    id: "PT-AARAV-001",
    name: "Aarav Mehta",
    age: 24,
    gender: "Male",
    bloodGroup: "O+",
    summary: "Road accident with left femur fracture",
  },
  {
    id: "PT-ISHITA-002",
    name: "Ishita Kapoor",
    age: 46,
    gender: "Female",
    bloodGroup: "B+",
    summary: "Type 2 diabetes and hypertension",
  },
  {
    id: "PT-NIKHIL-003",
    name: "Nikhil Varma",
    age: 61,
    gender: "Male",
    bloodGroup: "A+",
    summary: "Previous MI with angioplasty and stent",
  },
  {
    id: "PT-DIYA-004",
    name: "Diya Srinivasan",
    age: 38,
    gender: "Female",
    bloodGroup: "AB+",
    summary: "Osteosarcoma with chemotherapy and surgery",
  },
  {
    id: "PT-KABIR-005",
    name: "Kabir Malhotra",
    age: 52,
    gender: "Male",
    bloodGroup: "O-",
    summary: "Severe Penicillin allergy and pneumonia history",
  },
  {
    id: "PT-TANYA-006",
    name: "Tanya Bose",
    age: 34,
    gender: "Female",
    bloodGroup: "A-",
    summary: "Intracranial lesion with brain surgery",
  },
]

const timelineData = {
  "PT-AARAV-001": [
    {
      date: "2023",
      title: "Road Accident",
      type: "Emergency",
      icon: "🚨",
      description:
        "Patient involved in a road accident resulting in a left femur fracture.",
      source: "Medical history",
      status: "Verified",
    },
    {
      date: "2023",
      title: "Left Femur Fracture",
      type: "Diagnosis",
      icon: "🦴",
      description:
        "Left femur fracture documented following the road accident.",
      source: "Clinical record",
      status: "Verified",
    },
    {
      date: "2023",
      title: "Fracture Fixation",
      type: "Procedure",
      icon: "⚕",
      description:
        "Surgical fixation performed for the left femur fracture.",
      source: "Procedure record",
      status: "Verified",
    },
    {
      date: "2023",
      title: "Follow-up",
      type: "Follow-up",
      icon: "◷",
      description:
        "Post-procedure follow-up documented after fracture treatment.",
      source: "Follow-up record",
      status: "Verified",
    },
  ],

  "PT-ISHITA-002": [
    {
      date: "Current",
      title: "Type 2 Diabetes",
      type: "Condition",
      icon: "◆",
      description:
        "Type 2 diabetes mellitus is part of the patient's current medical history.",
      source: "Current medical record",
      status: "Active",
    },
    {
      date: "Current",
      title: "Hypertension",
      type: "Condition",
      icon: "♥",
      description:
        "Hypertension is documented as a current medical condition.",
      source: "Current medical record",
      status: "Active",
    },
    {
      date: "Current",
      title: "Metformin 500 mg BID",
      type: "Medication",
      icon: "💊",
      description:
        "Metformin 500 mg twice daily is documented in the patient's medication history.",
      source: "Medication record",
      status: "Active",
    },
    {
      date: "Current",
      title: "Amlodipine 5 mg OD",
      type: "Medication",
      icon: "💊",
      description:
        "Amlodipine 5 mg once daily is documented in the patient's medication history.",
      source: "Medication record",
      status: "Active",
    },
  ],

  "PT-NIKHIL-003": [
    {
      date: "2023",
      title: "Myocardial Infarction",
      type: "Emergency",
      icon: "🚨",
      description:
        "Patient experienced a myocardial infarction followed by hospitalization.",
      source: "Historical medical record",
      status: "Verified",
    },
    {
      date: "2023",
      title: "Hospitalization",
      type: "Hospital",
      icon: "🏥",
      description:
        "Hospitalization documented as part of the patient's cardiac event.",
      source: "Hospital record",
      status: "Verified",
    },
    {
      date: "2023",
      title: "Angiography",
      type: "Investigation",
      icon: "⌁",
      description:
        "Coronary angiography was performed during the cardiac treatment episode.",
      source: "Procedure record",
      status: "Verified",
    },
    {
      date: "2023",
      title: "Angioplasty + Stent",
      type: "Procedure",
      icon: "⚕",
      description:
        "Angioplasty with stent placement was documented.",
      source: "Procedure record",
      status: "Verified",
    },
    {
      date: "Follow-up",
      title: "Cardiology Follow-ups",
      type: "Follow-up",
      icon: "◷",
      description:
        "Subsequent cardiology follow-ups are documented in the patient's history.",
      source: "Clinical record",
      status: "Verified",
    },
  ],

  "PT-DIYA-004": [
    {
      date: "Historical",
      title: "Osteosarcoma",
      type: "Diagnosis",
      icon: "◆",
      description:
        "Osteosarcoma documented in the patient's medical history.",
      source: "Historical medical record",
      status: "Verified",
    },
    {
      date: "Historical",
      title: "Chemotherapy",
      type: "Treatment",
      icon: "✦",
      description:
        "Chemotherapy documented as part of the patient's cancer treatment.",
      source: "Treatment record",
      status: "Verified",
    },
    {
      date: "Historical",
      title: "Limb-Sparing Surgery",
      type: "Procedure",
      icon: "⚕",
      description:
        "Limb-sparing surgery documented as part of treatment.",
      source: "Procedure record",
      status: "Verified",
    },
    {
      date: "Current",
      title: "Surveillance",
      type: "Follow-up",
      icon: "◷",
      description:
        "Surveillance follow-up documented after treatment.",
      source: "Follow-up record",
      status: "Active",
    },
  ],

  "PT-KABIR-005": [
    {
      date: "2019",
      title: "Severe Penicillin Allergy",
      type: "Allergy",
      icon: "⚠",
      description:
        "Severe Penicillin allergy documented with an anaphylaxis reaction.",
      source: "Historical medical record",
      status: "Verified",
      critical: true,
    },
    {
      date: "2024",
      title: "Bacterial Pneumonia",
      type: "Diagnosis",
      icon: "◆",
      description:
        "Hospitalization for bacterial pneumonia documented.",
      source: "Hospital record",
      status: "Verified",
    },
    {
      date: "2026",
      title: "Emergency Presentation",
      type: "Emergency",
      icon: "🚨",
      description:
        "Patient presented for an emergency episode. Current allergy information is available for emergency review.",
      source: "Emergency record",
      status: "Verified",
      critical: true,
    },
  ],

  "PT-TANYA-006": [
    {
      date: "2024",
      title: "Neurological Symptoms",
      type: "Clinical Event",
      icon: "◆",
      description:
        "Neurological symptoms documented during clinical evaluation.",
      source: "Clinical record",
      status: "Verified",
    },
    {
      date: "2025",
      title: "Intracranial Lesion",
      type: "Diagnosis",
      icon: "◆",
      description:
        "Intracranial lesion documented in the patient's medical history.",
      source: "Clinical record",
      status: "Verified",
    },
    {
      date: "10 Sep 2025",
      title: "Brain Surgery",
      type: "Procedure",
      icon: "⚕",
      description:
        "Brain surgery is recorded in the current database.",
      source: "Current DB record",
      status: "Review",
      conflict: true,
    },
    {
      date: "14 Sep 2025",
      title: "Document Date Conflict",
      type: "AI Flag",
      icon: "⚠",
      description:
        "A medical document contains a surgery date of 14 Sep 2025, while the current database records 10 Sep 2025. Doctor review is required.",
      source: "Document + DB comparison",
      status: "Needs review",
      conflict: true,
    },
    {
      date: "2026",
      title: "Follow-up",
      type: "Follow-up",
      icon: "◷",
      description:
        "Follow-up documented after the intracranial lesion treatment.",
      source: "Follow-up record",
      status: "Verified",
    },
  ],
}

function DoctorTimeline() {
  const [selectedPatientId, setSelectedPatientId] =
    useState("PT-KABIR-005")

  const selectedPatient = patients.find(
    (patient) => patient.id === selectedPatientId
  )

  const events = useMemo(
    () => timelineData[selectedPatientId] || [],
    [selectedPatientId]
  )

  return (
    <DashboardLayout
      role="doctor"
      userName="Dr. Meera Iyer"
    >
      <div className="doctor-timeline-page">

        {/* Page Header */}
        <div className="page-header doctor-timeline-header">
          <div>
            <div className="page-eyebrow">CLINICAL RECORD</div>
            <h1>Medical Timeline</h1>
            <p>
              Review a patient's longitudinal medical history,
              events, procedures and flagged discrepancies.
            </p>
          </div>

          <div className="timeline-header-status">
            <span className="status-dot"></span>
            Clinical View
          </div>
        </div>

        {/* Patient Selector */}
        <div className="doctor-patient-selector card">
          <div className="selector-left">
            <div className="selector-icon">♙</div>

            <div>
              <label htmlFor="patient-select">
                SELECT PATIENT
              </label>

              <select
                id="patient-select"
                value={selectedPatientId}
                onChange={(event) =>
                  setSelectedPatientId(event.target.value)
                }
              >
                {patients.map((patient) => (
                  <option
                    key={patient.id}
                    value={patient.id}
                  >
                    {patient.name} — {patient.id}
                  </option>
                ))}
              </select>
            </div>
          </div>

          <div className="selected-patient-summary">
            <strong>{selectedPatient.name}</strong>
            <span>
              {selectedPatient.age} yrs ·{" "}
              {selectedPatient.gender} ·{" "}
              Blood Group {selectedPatient.bloodGroup}
            </span>
          </div>
        </div>

        {/* Patient Summary */}
        <div className="timeline-patient-banner card">
          <div className="timeline-avatar">
            {selectedPatient.name
              .split(" ")
              .map((word) => word[0])
              .join("")
              .slice(0, 2)
              .toUpperCase()}
          </div>

          <div className="timeline-patient-info">
            <div className="timeline-patient-name">
              {selectedPatient.name}
            </div>

            <div className="timeline-patient-id">
              {selectedPatient.id}
            </div>

            <p>{selectedPatient.summary}</p>
          </div>

          <div className="timeline-summary-stats">
            <div>
              <strong>{events.length}</strong>
              <span>Recorded Events</span>
            </div>

            <div>
              <strong>
                {events.filter((event) => event.critical).length}
              </strong>
              <span>Critical</span>
            </div>

            <div>
              <strong>
                {events.filter((event) => event.conflict).length}
              </strong>
              <span>Needs Review</span>
            </div>
          </div>
        </div>

        {/* Timeline */}
        <div className="timeline-section">

          <div className="section-heading-row">
            <div>
              <h2>Clinical History</h2>
              <p>
                Chronological view of documented patient events.
              </p>
            </div>

            <span className="event-count">
              {events.length} events
            </span>
          </div>

          <div className="doctor-timeline">

            {events.map((event, index) => (
              <div
                className={`doctor-timeline-item ${
                  event.conflict ? "timeline-conflict" : ""
                } ${
                  event.critical ? "timeline-critical" : ""
                }`}
                key={`${event.title}-${index}`}
              >

                {/* Timeline line */}
                <div className="timeline-marker-column">
                  <div className="timeline-marker">
                    {event.icon}
                  </div>

                  {index < events.length - 1 && (
                    <div className="timeline-line"></div>
                  )}
                </div>

                {/* Event Card */}
                <div className="timeline-event-card card">

                  <div className="timeline-event-top">
                    <div>
                      <span className="timeline-date">
                        {event.date}
                      </span>

                      <h3>{event.title}</h3>
                    </div>

                    <span
                      className={`timeline-status ${
                        event.status === "Needs review"
                          ? "review"
                          : event.status === "Review"
                          ? "review"
                          : event.status === "Active"
                          ? "active"
                          : ""
                      }`}
                    >
                      {event.status}
                    </span>
                  </div>

                  <div className="timeline-event-type">
                    {event.type}
                  </div>

                  <p className="timeline-event-description">
                    {event.description}
                  </p>

                  <div className="timeline-event-footer">
                    <span>
                      Source: <strong>{event.source}</strong>
                    </span>

                    {event.critical && (
                      <span className="critical-label">
                        ⚠ Critical information
                      </span>
                    )}

                    {event.conflict && (
                      <span className="conflict-label">
                        ⚠ Doctor review required
                      </span>
                    )}
                  </div>

                </div>
              </div>
            ))}

          </div>
        </div>

        {/* Clinical note */}
        <div className="timeline-ai-note card">
          <div className="ai-note-icon">✦</div>

          <div>
            <strong>AI-assisted timeline</strong>

            <p>
              Medi-Trace organizes available medical evidence
              into a chronological view. AI-generated findings
              and discrepancies require doctor review before
              becoming authoritative medical records.
            </p>
          </div>
        </div>

      </div>
    </DashboardLayout>
  )
}

export default DoctorTimeline