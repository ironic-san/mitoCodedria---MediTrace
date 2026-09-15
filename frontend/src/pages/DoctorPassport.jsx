import { useState } from "react"
import { useNavigate, useParams } from "react-router-dom"
import DashboardLayout from "../layouts/DashboardLayout.jsx"

function DoctorPassport() {
  const { id } = useParams()
  const navigate = useNavigate()

  const [activeTab, setActiveTab] = useState("overview")
  const [showEditMessage, setShowEditMessage] = useState(false)

  const patients = {
    1: {
      name: "Aarav Mehta",
      age: 24,
      gender: "Male",
      bloodGroup: "O+",
      condition: "Left femur fracture",
      status: "Stable",
      critical: false,
      allergies: ["No known allergies"],
      medications: ["Post-operative medications — historical record"],
      conditions: ["Left femur fracture"],
      events: [
        {
          date: "2023",
          title: "Road Accident",
          description:
            "Patient sustained a left femur fracture following a road accident.",
        },
        {
          date: "2023",
          title: "Surgical Fixation",
          description:
            "Surgical fixation procedure performed for the left femur fracture.",
        },
        {
          date: "2023",
          title: "Follow-up",
          description:
            "Post-operative follow-up and recovery monitoring documented.",
        },
      ],
      documents: 3,
    },

    2: {
      name: "Ishita Kapoor",
      age: 46,
      gender: "Female",
      bloodGroup: "B+",
      condition: "Type 2 Diabetes + Hypertension",
      status: "Stable",
      critical: false,
      allergies: ["No documented allergies"],
      medications: [
        "Metformin 500 mg — BID",
        "Amlodipine 5 mg — OD",
      ],
      conditions: [
        "Type 2 Diabetes Mellitus",
        "Hypertension",
      ],
      events: [
        {
          date: "2024",
          title: "Diabetes Diagnosis",
          description:
            "Type 2 Diabetes Mellitus documented following clinical evaluation.",
        },
        {
          date: "2024",
          title: "Hypertension Documented",
          description:
            "Hypertension added to the patient's medical history.",
        },
        {
          date: "2026",
          title: "Routine Follow-up",
          description:
            "Ongoing monitoring of diabetes and blood pressure documented.",
        },
      ],
      documents: 3,
    },

    3: {
      name: "Nikhil Varma",
      age: 61,
      gender: "Male",
      bloodGroup: "A+",
      condition: "Previous MI / Angioplasty + Stent",
      status: "Monitoring",
      critical: true,
      allergies: ["No documented allergies"],
      medications: [
        "Aspirin",
        "Clopidogrel",
        "Atorvastatin",
        "Metoprolol",
      ],
      conditions: [
        "Previous Myocardial Infarction",
        "Coronary Artery Disease",
      ],
      events: [
        {
          date: "2023",
          title: "Myocardial Infarction",
          description:
            "Patient hospitalized following myocardial infarction.",
        },
        {
          date: "2023",
          title: "Angiography",
          description:
            "Coronary angiography performed during hospitalization.",
        },
        {
          date: "2023",
          title: "Angioplasty + Stent",
          description:
            "Angioplasty and coronary stent placement documented.",
        },
        {
          date: "2024–2026",
          title: "Cardiology Follow-ups",
          description:
            "Ongoing cardiology follow-ups and medication management.",
        },
      ],
      documents: 5,
    },

    4: {
      name: "Diya Srinivasan",
      age: 38,
      gender: "Female",
      bloodGroup: "AB+",
      condition: "Osteosarcoma",
      status: "Follow-up",
      critical: false,
      allergies: ["No documented allergies"],
      medications: ["Chemotherapy-related medications — historical record"],
      conditions: ["Osteosarcoma"],
      events: [
        {
          date: "2024",
          title: "Osteosarcoma Diagnosis",
          description:
            "Osteosarcoma diagnosis documented following evaluation.",
        },
        {
          date: "2024–2025",
          title: "Chemotherapy",
          description:
            "Patient underwent documented chemotherapy treatment.",
        },
        {
          date: "2025",
          title: "Limb-Sparing Surgery",
          description:
            "Limb-sparing surgical procedure documented.",
        },
        {
          date: "2026",
          title: "Surveillance",
          description:
            "Post-treatment surveillance and follow-up documented.",
        },
      ],
      documents: 4,
    },

    5: {
      name: "Kabir Malhotra",
      age: 52,
      gender: "Male",
      bloodGroup: "O-",
      condition: "Severe Penicillin Allergy",
      status: "Emergency Ready",
      critical: true,
      allergies: [
        "Penicillin — Severe",
      ],
      medications: [
        "No medication information specified in current demo dataset",
      ],
      conditions: [
        "Severe Penicillin Allergy",
      ],
      events: [
        {
          date: "2019",
          title: "Severe Penicillin Allergy Identified",
          description:
            "Severe Penicillin allergy documented with anaphylaxis as the recorded reaction.",
        },
        {
          date: "2024",
          title: "Bacterial Pneumonia Hospitalization",
          description:
            "Hospitalization for bacterial pneumonia documented.",
        },
        {
          date: "2026",
          title: "Emergency Presentation",
          description:
            "Emergency presentation documented for current emergency workflow demonstration.",
        },
      ],
      documents: 3,
    },

    6: {
      name: "Tanya Bose",
      age: 34,
      gender: "Female",
      bloodGroup: "A-",
      condition: "Intracranial lesion / Post-surgery",
      status: "Follow-up",
      critical: true,
      allergies: ["No documented allergies"],
      medications: [
        "Post-surgical medications — historical record",
      ],
      conditions: [
        "Intracranial lesion",
      ],
      events: [
        {
          date: "2024",
          title: "Neurological Symptoms",
          description:
            "Neurological symptoms documented during clinical evaluation.",
        },
        {
          date: "2025",
          title: "Intracranial Lesion",
          description:
            "Intracranial lesion documented following investigation.",
        },
        {
          date: "2025",
          title: "Brain Surgery",
          description:
            "Brain surgery documented. Current database records 10 Sep 2025 while a medical document records 14 Sep 2025, requiring doctor review.",
        },
        {
          date: "2026",
          title: "Follow-up",
          description:
            "Post-surgical follow-up documented.",
        },
      ],
      documents: 4,
    },
  }

  const patient = patients[id] || patients[5]

  const showEdit = () => {
    setShowEditMessage(true)

    setTimeout(() => {
      setShowEditMessage(false)
    }, 3000)
  }

  return (
    <DashboardLayout
      role="doctor"
      userName="Dr. Arjun Rao"
    >
      <div className="doctor-passport-page">

        {/* BACK */}

        <button
          type="button"
          className="back-button"
          onClick={() => navigate("/doctor/patients")}
        >
          ← Back to Patients
        </button>


        {/* PATIENT HEADER */}

        <section className="passport-patient-header">

          <div className="passport-patient-main">

            <div className="large-patient-avatar">
              {patient.name
                .split(" ")
                .map((word) => word[0])
                .join("")
                .slice(0, 2)
                .toUpperCase()}
            </div>

            <div>

              <div className="passport-label">
                HEALTH PASSPORT
              </div>

              <h1>
                {patient.name}
              </h1>

              <p>
                {patient.age} years • {patient.gender}
              </p>

            </div>

          </div>


          <div className="passport-header-meta">

            <div className="passport-blood-group">
              <span>Blood Group</span>
              <strong>{patient.bloodGroup}</strong>
            </div>

            <div
              className={`passport-status ${
                patient.status === "Emergency Ready"
                  ? "emergency"
                  : patient.status === "Monitoring"
                    ? "monitoring"
                    : "stable"
              }`}
            >
              {patient.status}
            </div>

          </div>

        </section>


        {/* CRITICAL ALERT */}

        {patient.critical && (

          <div className="doctor-critical-alert">

            <div className="doctor-critical-icon">
              ⚠️
            </div>

            <div>

              <strong>
                Critical Medical Information
              </strong>

              <p>
                {patient.name === "Kabir Malhotra"
                  ? "Severe Penicillin allergy — recorded reaction: anaphylaxis."
                  : patient.name === "Tanya Bose"
                    ? "Potential medical record discrepancy detected. Doctor review required."
                    : "Patient has clinically important historical information requiring attention."}
              </p>

            </div>

          </div>

        )}


        {/* EDIT MESSAGE */}

        {showEditMessage && (

          <div className="doctor-edit-message">

            <span>✏️</span>

            <div>
              <strong>
                Edit workflow ready
              </strong>

              <p>
                Changes will be connected to the FastAPI backend later.
              </p>
            </div>

          </div>

        )}


        {/* NAVIGATION TABS */}

        <div className="passport-tabs">

          {[
            ["overview", "Overview"],
            ["timeline", "Medical Timeline"],
            ["documents", "Documents"],
          ].map(([value, label]) => (

            <button
              type="button"
              key={value}
              className={
                activeTab === value
                  ? "passport-tab active"
                  : "passport-tab"
              }
              onClick={() => setActiveTab(value)}
            >
              {label}
            </button>

          ))}

        </div>


        {/* OVERVIEW */}

        {activeTab === "overview" && (

          <div className="passport-content-grid">

            {/* LEFT */}

            <div>

              {/* CONDITIONS */}

              <section className="dashboard-panel passport-panel">

                <div className="panel-header">

                  <div>
                    <h2>Conditions</h2>
                    <p>Current structured medical conditions.</p>
                  </div>

                  <button
                    type="button"
                    className="small-edit-button"
                    onClick={showEdit}
                  >
                    ✏ Edit
                  </button>

                </div>

                <div className="passport-item-list">

                  {patient.conditions.map((condition) => (

                    <div
                      className="passport-list-item"
                      key={condition}
                    >
                      <span className="passport-list-icon">
                        ●
                      </span>

                      <span>
                        {condition}
                      </span>
                    </div>

                  ))}

                </div>

              </section>


              {/* ALLERGIES */}

              <section className="dashboard-panel passport-panel">

                <div className="panel-header">

                  <div>
                    <h2>Allergies</h2>
                    <p>Known allergies and recorded reactions.</p>
                  </div>

                  <button
                    type="button"
                    className="small-edit-button"
                    onClick={showEdit}
                  >
                    ✏ Edit
                  </button>

                </div>

                <div className="passport-item-list">

                  {patient.allergies.map((allergy) => (

                    <div
                      className={
                        allergy.includes("Penicillin")
                          ? "passport-list-item allergy-critical"
                          : "passport-list-item"
                      }
                      key={allergy}
                    >

                      <span className="passport-list-icon">
                        ⚠️
                      </span>

                      <span>
                        {allergy}
                      </span>

                    </div>

                  ))}

                </div>

                {patient.name === "Kabir Malhotra" && (

                  <div className="reaction-box">

                    <span>
                      Recorded reaction
                    </span>

                    <strong>
                      Anaphylaxis
                    </strong>

                  </div>

                )}

              </section>

            </div>


            {/* RIGHT */}

            <div>

              {/* MEDICATIONS */}

              <section className="dashboard-panel passport-panel">

                <div className="panel-header">

                  <div>
                    <h2>Medications</h2>
                    <p>Medication information currently documented.</p>
                  </div>

                  <button
                    type="button"
                    className="small-edit-button"
                    onClick={showEdit}
                  >
                    ✏ Edit
                  </button>

                </div>

                <div className="passport-item-list">

                  {patient.medications.map((medication) => (

                    <div
                      className="passport-list-item"
                      key={medication}
                    >

                      <span className="passport-list-icon">
                        💊
                      </span>

                      <span>
                        {medication}
                      </span>

                    </div>

                  ))}

                </div>

              </section>


              {/* MEDICAL EVENTS */}

              <section className="dashboard-panel passport-panel">

                <div className="panel-header">

                  <div>
                    <h2>Recent Medical Events</h2>
                    <p>Key events from the patient's history.</p>
                  </div>

                  <button
                    type="button"
                    className="small-edit-button"
                    onClick={showEdit}
                  >
                    + Add
                  </button>

                </div>

                <div className="passport-events">

                  {patient.events.slice(-3).map((event) => (

                    <div
                      className="passport-event"
                      key={`${event.date}-${event.title}`}
                    >

                      <div className="passport-event-date">
                        {event.date}
                      </div>

                      <div className="passport-event-marker">
                        ●
                      </div>

                      <div>

                        <h3>
                          {event.title}
                        </h3>

                        <p>
                          {event.description}
                        </p>

                      </div>

                    </div>

                  ))}

                </div>

              </section>

            </div>

          </div>

        )}


        {/* TIMELINE */}

        {activeTab === "timeline" && (

          <section className="dashboard-panel passport-panel full-width-panel">

            <div className="panel-header">

              <div>
                <h2>
                  Medical Timeline
                </h2>

                <p>
                  Chronological clinical history for {patient.name}.
                </p>
              </div>

              <button
                type="button"
                className="small-edit-button"
                onClick={showEdit}
              >
                + Add Event
              </button>

            </div>


            <div className="doctor-passport-timeline">

              {patient.events.map((event, index) => (

                <div
                  className="doctor-passport-event"
                  key={`${event.date}-${event.title}`}
                >

                  <div className="doctor-event-date">
                    {event.date}
                  </div>

                  <div className="doctor-event-marker-wrapper">

                    <div className="doctor-event-marker">
                      ●
                    </div>

                    {index !== patient.events.length - 1 && (
                      <div className="doctor-event-line"></div>
                    )}

                  </div>

                  <div className="doctor-event-content">

                    <h3>
                      {event.title}
                    </h3>

                    <p>
                      {event.description}
                    </p>

                  </div>

                </div>

              ))}

            </div>

          </section>

        )}


        {/* DOCUMENTS */}

        {activeTab === "documents" && (

          <section className="dashboard-panel passport-panel full-width-panel">

            <div className="panel-header">

              <div>
                <h2>
                  Medical Documents
                </h2>

                <p>
                  {patient.documents} documents associated with this patient.
                </p>
              </div>

              <button
                type="button"
                className="primary-action-button"
                onClick={showEdit}
              >
                + Upload Document
              </button>

            </div>


            <div className="passport-document-list">

              {Array.from(
                { length: patient.documents },
                (_, index) => (
                  <div
                    className="passport-document"
                    key={index}
                  >

                    <div className="passport-document-icon">
                      📄
                    </div>

                    <div>

                      <h3>
                        {index === 0
                          ? "Clinical Medical Record.pdf"
                          : index === 1
                            ? "Hospital Follow-up Record.pdf"
                            : "Medical History Document.pdf"}
                      </h3>

                      <p>
                        Medical document • Available for review
                      </p>

                    </div>

                    <span className="document-status-badge">
                      ✓ Available
                    </span>

                    <button
                      type="button"
                      className="document-view-button"
                      onClick={() =>
                        alert(
                          "Document preview will be connected to the backend later."
                        )
                      }
                    >
                      View
                    </button>

                  </div>
                )
              )}

            </div>

          </section>

        )}


        {/* CLINICAL TOOLS */}

        <section className="doctor-passport-tools">

          <div className="doctor-tool-card">

            <span>🤖</span>

            <div>
              <strong>
                AI Clinical Review
              </strong>

              <p>
                Review AI-assisted findings and historical evidence.
              </p>
            </div>

            <button
              type="button"
              onClick={() => navigate("/doctor/ai-reviews")}
            >
              Open
            </button>

          </div>


          <div className="doctor-tool-card">

            <span>🔗</span>

            <div>
              <strong>
                Integrity Verification
              </strong>

              <p>
                Verify provenance of critical historical events.
              </p>
            </div>

            <button
              type="button"
              onClick={() => navigate("/doctor/integrity")}
            >
              Verify
            </button>

          </div>

        </section>


        {/* DOCTOR RESPONSIBILITY */}

        <div className="doctor-review-notice">

          <span>
            🩺
          </span>

          <div>

            <strong>
              Doctor review required
            </strong>

            <p>
              Medi-Trace assists with extraction, retrieval and summarization.
              The treating doctor remains the final decision-maker for
              clinical information.
            </p>

          </div>

        </div>

      </div>
    </DashboardLayout>
  )
}

export default DoctorPassport