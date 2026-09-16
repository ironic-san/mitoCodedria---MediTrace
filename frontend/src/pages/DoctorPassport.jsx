import { useState } from "react"
import { useNavigate, useParams } from "react-router-dom"
import DashboardLayout from "../layouts/DashboardLayout.jsx"
import { api } from "../services/api"
import { useApiQuery } from "../hooks/useApiQuery"
import { ErrorState, LoadingState } from "../components/AsyncState"

function Icon({ name, size = 19 }) {
  const common = {
    width: size,
    height: size,
    viewBox: "0 0 24 24",
    fill: "none",
    stroke: "currentColor",
    strokeWidth: 1.8,
    strokeLinecap: "round",
    strokeLinejoin: "round",
    "aria-hidden": "true",
  }

  const icons = {
    back: (
      <svg {...common}>
        <path d="M19 12H5" />
        <path d="m12 19-7-7 7-7" />
      </svg>
    ),

    user: (
      <svg {...common}>
        <circle cx="12" cy="8" r="4" />
        <path d="M4 21a8 8 0 0 1 16 0" />
      </svg>
    ),

    blood: (
      <svg {...common}>
        <path d="M12 3s-6 6.5-6 11a6 6 0 0 0 12 0c0-4.5-6-11-6-11z" />
      </svg>
    ),

    alert: (
      <svg {...common}>
        <path d="M10.3 3.4 2.7 17a2 2 0 0 0 1.75 3h15.1a2 2 0 0 0 1.75-3L13.7 3.4a2 2 0 0 0-3.4 0z" />
        <path d="M12 9v4" />
        <path d="M12 17h.01" />
      </svg>
    ),

    condition: (
      <svg {...common}>
        <path d="M4 19V5" />
        <path d="M4 6h12l-2 3 2 3H4" />
      </svg>
    ),

    allergy: (
      <svg {...common}>
        <path d="M12 3v18" />
        <path d="M5 8c2.5 0 4 1.5 7 4s4.5 4 7 4" />
        <path d="M5 16c2.5 0 4-1.5 7-4s4.5-4 7-4" />
      </svg>
    ),

    medicine: (
      <svg {...common}>
        <path d="m8 4 12 12" />
        <path d="M16 3a4 4 0 0 1 0 6l-7 7a4 4 0 0 1-6-6l7-7a4 4 0 0 1 6 0z" />
        <path d="m6 12 6 6" />
      </svg>
    ),

    calendar: (
      <svg {...common}>
        <rect x="3" y="4" width="18" height="17" rx="2" />
        <path d="M16 2v4" />
        <path d="M8 2v4" />
        <path d="M3 10h18" />
      </svg>
    ),

    document: (
      <svg {...common}>
        <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
        <path d="M14 2v6h6" />
        <path d="M8 13h8" />
        <path d="M8 17h5" />
      </svg>
    ),

    ai: (
      <svg {...common}>
        <path d="m12 3-1.4 5.6L5 10l5.6 1.4L12 17l1.4-5.6L19 10l-5.6-1.4z" />
        <path d="m19 16-.7 2.3L16 19l2.3.7L19 22l.7-2.3L22 19l-2.3-.7z" />
      </svg>
    ),

    shield: (
      <svg {...common}>
        <path d="M12 3l7 3v5c0 4.5-3 8.2-7 10-4-1.8-7-5.5-7-10V6l7-3z" />
        <path d="m9 12 2 2 4-4" />
      </svg>
    ),

    edit: (
      <svg {...common}>
        <path d="M12 20h9" />
        <path d="M16.5 3.5a2.1 2.1 0 0 1 3 3L8 18l-4 1 1-4z" />
      </svg>
    ),

    plus: (
      <svg {...common}>
        <path d="M12 5v14" />
        <path d="M5 12h14" />
      </svg>
    ),

    eye: (
      <svg {...common}>
        <path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7S2 12 2 12z" />
        <circle cx="12" cy="12" r="3" />
      </svg>
    ),

    arrow: (
      <svg {...common}>
        <path d="M5 12h13" />
        <path d="m13 6 6 6-6 6" />
      </svg>
    ),

    check: (
      <svg {...common}>
        <path d="m5 12 4 4L19 6" />
      </svg>
    ),

    clock: (
      <svg {...common}>
        <circle cx="12" cy="12" r="9" />
        <path d="M12 7v5l3 2" />
      </svg>
    ),

    file: (
      <svg {...common}>
        <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
        <path d="M14 2v6h6" />
      </svg>
    ),

    info: (
      <svg {...common}>
        <circle cx="12" cy="12" r="9" />
        <path d="M12 11v5" />
        <path d="M12 8h.01" />
      </svg>
    ),
  }

  return icons[name] || null
}

function DoctorPassport() {
  const { id } = useParams()
  const navigate = useNavigate()
  const { data: summary, loading, error, refresh } = useApiQuery(() => api.patientSummary(id), [id])

  const [activeTab, setActiveTab] = useState("overview")
  const [showEditMessage, setShowEditMessage] = useState(false)

  const _demoPatients = {
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
      allergies: ["Penicillin — Severe"],
      medications: [
        "No medication information specified in current demo dataset",
      ],
      conditions: ["Severe Penicillin Allergy"],
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
      conditions: ["Intracranial lesion"],
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

  const patient = summary ? {
    name: summary.profile.full_name,
    age: summary.profile.age ?? "—",
    gender: summary.profile.gender || "Not recorded",
    bloodGroup: summary.profile.blood_group || "Not recorded",
    condition: summary.conditions?.map((condition) => condition.condition_name).join(", ") || "No conditions recorded",
    status: "Authorized access",
    critical: summary.critical_history?.length > 0,
    allergies: summary.allergies?.map((allergy) => allergy.allergen) || [],
    medications: summary.medications?.map((medication) => [medication.medication_name, medication.dosage, medication.frequency].filter(Boolean).join(" — ")) || [],
    conditions: summary.conditions?.map((condition) => condition.condition_name) || [],
    events: summary.medical_events?.map((event) => ({ date: event.event_date || "Date not recorded", title: event.title, description: event.description || "No description recorded." })) || [],
    documents: "Not available", // The API has no list-documents endpoint.
  } : null

  if (!patient) return <DashboardLayout role="doctor" userName="Doctor">{loading ? <LoadingState label="Loading authorized patient passport…" /> : <ErrorState error={error || "Patient record is unavailable."} onRetry={refresh} />}</DashboardLayout>

  const showEdit = () => {
    setShowEditMessage(true)

    setTimeout(() => {
      setShowEditMessage(false)
    }, 3000)
  }

  const initials = patient.name
    .split(" ")
    .map((word) => word[0])
    .join("")
    .slice(0, 2)
    .toUpperCase()

  return (
    <DashboardLayout
      role="doctor"
      userName="Dr. Arjun Rao"
    >
      <div className="doctor-passport-page">

        {/* =========================
            BACK NAVIGATION
            ========================= */}

        <button
          type="button"
          className="passport-back-link"
          onClick={() => navigate("/doctor/patients")}
        >
          <Icon name="back" size={16} />
          Back to Patients
        </button>


        {/* =========================
            PATIENT HERO
            ========================= */}

        <section className="doctor-passport-hero">

          <div className="doctor-passport-identity">

            <div className="doctor-passport-avatar">
              {initials}
            </div>

            <div className="doctor-passport-name">

              <div className="passport-label">
                EMERGENCY HEALTH PASSPORT
              </div>

              <h1>
                {patient.name}
              </h1>

              <p>
                {patient.age} years
                <span>•</span>
                {patient.gender}
                <span>•</span>
                Patient ID: PT-{String(id || 5).padStart(3, "0")}
              </p>

            </div>

          </div>


          <div className="doctor-passport-hero-right">

            <div className="doctor-blood-card">

              <span className="doctor-blood-icon">
                <Icon name="blood" size={18} />
              </span>

              <div>
                <small>Blood Group</small>
                <strong>{patient.bloodGroup}</strong>
              </div>

            </div>


            <div
              className={`doctor-passport-status ${
                patient.status === "Emergency Ready"
                  ? "emergency"
                  : patient.status === "Monitoring"
                    ? "monitoring"
                    : "stable"
              }`}
            >
              <span></span>
              {patient.status}
            </div>

          </div>

        </section>


        {/* =========================
            CRITICAL ALERT
            ========================= */}

        {patient.critical && (

          <section
            className={`doctor-passport-critical ${
              patient.name === "Kabir Malhotra"
                ? "allergy-alert"
                : "review-alert"
            }`}
          >

            <div className="doctor-passport-critical-icon">
              <Icon name="alert" size={21} />
            </div>

            <div className="doctor-passport-critical-content">

              <div className="critical-title-row">

                <strong>
                  {patient.name === "Kabir Malhotra"
                    ? "Critical Allergy Alert"
                    : "Clinical Review Alert"}
                </strong>

                <span>
                  {patient.name === "Kabir Malhotra"
                    ? "HIGH PRIORITY"
                    : "REVIEW REQUIRED"}
                </span>

              </div>

              <p>
                {patient.name === "Kabir Malhotra"
                  ? "Severe Penicillin allergy — recorded reaction: anaphylaxis."
                  : patient.name === "Tanya Bose"
                    ? "Potential medical record discrepancy detected. Current database and medical document contain different surgery dates."
                    : "Patient has clinically important historical information requiring attention."}
              </p>

            </div>

          </section>

        )}


        {/* =========================
            EDIT MESSAGE
            ========================= */}

        {showEditMessage && (

          <div className="doctor-edit-message">

            <span>
              <Icon name="check" size={18} />
            </span>

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


        {/* =========================
            TABS
            ========================= */}

        <div className="doctor-passport-tabs">

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
                  ? "doctor-passport-tab active"
                  : "doctor-passport-tab"
              }
              onClick={() => setActiveTab(value)}
            >
              {label}
            </button>

          ))}

        </div>


        {/* =========================
            OVERVIEW
            ========================= */}

        {activeTab === "overview" && (

          <div className="doctor-passport-overview">

            {/* =====================
                CONDITIONS
                ===================== */}

            <section className="doctor-passport-card">

              <div className="doctor-passport-card-header">

                <div className="doctor-section-heading">

                  <span className="doctor-section-icon condition">
                    <Icon name="condition" size={18} />
                  </span>

                  <div>
                    <h2>Medical Conditions</h2>
                    <p>Current structured medical conditions.</p>
                  </div>

                </div>

                <button
                  type="button"
                  className="passport-edit-button"
                  onClick={showEdit}
                >
                  <Icon name="edit" size={14} />
                  Edit
                </button>

              </div>


              <div className="doctor-passport-list">

                {patient.conditions.map((condition) => (

                  <div
                    className="doctor-passport-list-item"
                    key={condition}
                  >

                    <span className="list-check">
                      <Icon name="check" size={13} />
                    </span>

                    <span>{condition}</span>

                  </div>

                ))}

              </div>

            </section>


            {/* =====================
                ALLERGIES
                ===================== */}

            <section
              className={`doctor-passport-card ${
                patient.name === "Kabir Malhotra"
                  ? "allergy-card-highlight"
                  : ""
              }`}
            >

              <div className="doctor-passport-card-header">

                <div className="doctor-section-heading">

                  <span className="doctor-section-icon allergy">
                    <Icon name="allergy" size={18} />
                  </span>

                  <div>
                    <h2>Allergies</h2>
                    <p>Known allergies and recorded reactions.</p>
                  </div>

                </div>

                <button
                  type="button"
                  className="passport-edit-button"
                  onClick={showEdit}
                >
                  <Icon name="edit" size={14} />
                  Edit
                </button>

              </div>


              <div className="doctor-passport-list">

                {patient.allergies.map((allergy) => (

                  <div
                    className={
                      allergy.includes("Penicillin")
                        ? "doctor-passport-list-item allergy-critical"
                        : "doctor-passport-list-item"
                    }
                    key={allergy}
                  >

                    <span className="allergy-list-icon">
                      <Icon name="alert" size={14} />
                    </span>

                    <span>{allergy}</span>

                  </div>

                ))}

              </div>


              {patient.name === "Kabir Malhotra" && (

                <div className="reaction-box">

                  <span>Recorded reaction</span>

                  <strong>
                    Anaphylaxis
                  </strong>

                </div>

              )}

            </section>


            {/* =====================
                MEDICATIONS
                ===================== */}

            <section className="doctor-passport-card">

              <div className="doctor-passport-card-header">

                <div className="doctor-section-heading">

                  <span className="doctor-section-icon medication">
                    <Icon name="medicine" size={18} />
                  </span>

                  <div>
                    <h2>Medications</h2>
                    <p>Medication information currently documented.</p>
                  </div>

                </div>

                <button
                  type="button"
                  className="passport-edit-button"
                  onClick={showEdit}
                >
                  <Icon name="edit" size={14} />
                  Edit
                </button>

              </div>


              <div className="doctor-passport-medications">

                {patient.medications.map((medication) => (

                  <div
                    className="doctor-medication-row"
                    key={medication}
                  >

                    <span className="medication-dot"></span>

                    <span>
                      {medication}
                    </span>

                  </div>

                ))}

              </div>

            </section>


            {/* =====================
                RECENT EVENTS
                ===================== */}

            <section className="doctor-passport-card">

              <div className="doctor-passport-card-header">

                <div className="doctor-section-heading">

                  <span className="doctor-section-icon event">
                    <Icon name="calendar" size={18} />
                  </span>

                  <div>
                    <h2>Recent Medical Events</h2>
                    <p>Key events from the patient's history.</p>
                  </div>

                </div>

                <button
                  type="button"
                  className="passport-edit-button"
                  onClick={showEdit}
                >
                  <Icon name="plus" size={14} />
                  Add
                </button>

              </div>


              <div className="doctor-recent-events">

                {patient.events.slice(-3).map((event) => (

                  <div
                    className="doctor-recent-event"
                    key={`${event.date}-${event.title}`}
                  >

                    <div className="doctor-event-year">
                      {event.date}
                    </div>

                    <div className="doctor-event-point">
                      <span></span>
                    </div>

                    <div className="doctor-event-details">

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

        )}


        {/* =========================
            TIMELINE
            ========================= */}

        {activeTab === "timeline" && (

          <section className="doctor-passport-card doctor-full-width-card">

            <div className="doctor-passport-card-header">

              <div className="doctor-section-heading">

                <span className="doctor-section-icon event">
                  <Icon name="clock" size={18} />
                </span>

                <div>
                  <h2>Medical Timeline</h2>
                  <p>
                    Chronological clinical history for {patient.name}.
                  </p>
                </div>

              </div>

              <button
                type="button"
                className="passport-primary-small"
                onClick={showEdit}
              >
                <Icon name="plus" size={14} />
                Add Event
              </button>

            </div>


            <div className="doctor-passport-timeline-new">

              {patient.events.map((event, index) => (

                <div
                  className="doctor-timeline-row"
                  key={`${event.date}-${event.title}`}
                >

                  <div className="doctor-timeline-date">
                    {event.date}
                  </div>

                  <div className="doctor-timeline-track">

                    <div className="doctor-timeline-dot">
                      <span></span>
                    </div>

                    {index !== patient.events.length - 1 && (
                      <div className="doctor-timeline-line"></div>
                    )}

                  </div>

                  <div className="doctor-timeline-body">

                    <div className="doctor-timeline-title-row">

                      <h3>
                        {event.title}
                      </h3>

                      <span>
                        <Icon name="check" size={11} />
                        Recorded
                      </span>

                    </div>

                    <p>
                      {event.description}
                    </p>

                  </div>

                </div>

              ))}

            </div>

          </section>

        )}


        {/* =========================
            DOCUMENTS
            ========================= */}

        {activeTab === "documents" && (

          <section className="doctor-passport-card doctor-full-width-card">

            <div className="doctor-passport-card-header">

              <div className="doctor-section-heading">

                <span className="doctor-section-icon document">
                  <Icon name="document" size={18} />
                </span>

                <div>
                  <h2>Medical Documents</h2>
                  <p>
                    {patient.documents} documents associated with this patient.
                  </p>
                </div>

              </div>

              <button
                type="button"
                className="passport-primary-small"
                onClick={showEdit}
              >
                <Icon name="plus" size={14} />
                Upload Document
              </button>

            </div>


            <div className="doctor-passport-document-list">

              {Array.from(
                { length: patient.documents },
                (_, index) => (

                  <div
                    className="doctor-document-row"
                    key={index}
                  >

                    <div className="doctor-document-icon">
                      <Icon name="file" size={20} />
                    </div>

                    <div className="doctor-document-info">

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

                    <span className="doctor-document-status">
                      <Icon name="check" size={11} />
                      Available
                    </span>

                    <button
                      type="button"
                      className="doctor-document-view"
                      onClick={() =>
                        alert(
                          "Document preview will be connected to the backend later."
                        )
                      }
                    >
                      <Icon name="eye" size={14} />
                      View
                    </button>

                  </div>

                )
              )}

            </div>

          </section>

        )}


        {/* =========================
            CLINICAL TOOLS
            ========================= */}

        <section className="doctor-passport-tools-new">

          <button
            type="button"
            className="doctor-passport-tool"
            onClick={() => navigate("/doctor/ai-reviews")}
          >

            <span className="tool-icon ai">
              <Icon name="ai" size={20} />
            </span>

            <span className="tool-copy">
              <strong>AI Clinical Review</strong>
              <small>
                Review AI-assisted findings and historical evidence.
              </small>
            </span>

            <Icon name="arrow" size={16} />

          </button>


          <button
            type="button"
            className="doctor-passport-tool"
            onClick={() => navigate("/doctor/integrity")}
          >

            <span className="tool-icon integrity">
              <Icon name="shield" size={20} />
            </span>

            <span className="tool-copy">
              <strong>Integrity Verification</strong>
              <small>
                Verify provenance of critical historical events.
              </small>
            </span>

            <Icon name="arrow" size={16} />

          </button>

        </section>


        {/* =========================
            DOCTOR RESPONSIBILITY
            ========================= */}

        <section className="doctor-review-notice-new">

          <span className="review-notice-icon">
            <Icon name="info" size={19} />
          </span>

          <div>

            <strong>
              Doctor review required
            </strong>

            <p>
              Medi-Trace assists with extraction, retrieval and summarization.
              The treating doctor remains the final decision-maker for clinical information.
            </p>

          </div>

        </section>

      </div>
    </DashboardLayout>
  )
}

export default DoctorPassport
