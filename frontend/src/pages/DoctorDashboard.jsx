import { useState } from "react"
import { useNavigate } from "react-router-dom"
import DashboardLayout from "../layouts/DashboardLayout.jsx"

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
    "aria-hidden": "true",
  }

  const icons = {
    patients: (
      <svg {...common}>
        <path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2" />
        <circle cx="9" cy="7" r="4" />
        <path d="M22 21v-2a4 4 0 0 0-3-3.87" />
        <path d="M16 3.13a4 4 0 0 1 0 7.75" />
      </svg>
    ),

    alert: (
      <svg {...common}>
        <path d="M10.3 3.4 2.7 17a2 2 0 0 0 1.75 3h15.1a2 2 0 0 0 1.75-3L13.7 3.4a2 2 0 0 0-3.4 0z" />
        <path d="M12 9v4" />
        <path d="M12 17h.01" />
      </svg>
    ),

    review: (
      <svg {...common}>
        <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
        <path d="M14 2v6h6" />
        <path d="M8 13h8" />
        <path d="M8 17h5" />
      </svg>
    ),

    shield: (
      <svg {...common}>
        <path d="M12 3l7 3v5c0 4.5-3 8.2-7 10-4-1.8-7-5.5-7-10V6l7-3z" />
        <path d="M9 12l2 2 4-4" />
      </svg>
    ),

    search: (
      <svg {...common}>
        <circle cx="11" cy="11" r="7" />
        <path d="m20 20-4-4" />
      </svg>
    ),

    arrow: (
      <svg {...common}>
        <path d="M5 12h13" />
        <path d="m13 6 6 6-6 6" />
      </svg>
    ),

    warning: (
      <svg {...common}>
        <path d="M10.3 3.4 2.7 17a2 2 0 0 0 1.75 3h15.1a2 2 0 0 0 1.75-3L13.7 3.4a2 2 0 0 0-3.4 0z" />
        <path d="M12 9v4" />
        <path d="M12 17h.01" />
      </svg>
    ),

    info: (
      <svg {...common}>
        <circle cx="12" cy="12" r="9" />
        <path d="M12 11v5" />
        <path d="M12 8h.01" />
      </svg>
    ),

    folder: (
      <svg {...common}>
        <path d="M3 6a2 2 0 0 1 2-2h5l2 2h7a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z" />
      </svg>
    ),

    sparkles: (
      <svg {...common}>
        <path d="m12 3-1.4 5.6L5 10l5.6 1.4L12 17l1.4-5.6L19 10l-5.6-1.4z" />
        <path d="m19 16-.7 2.3L16 19l2.3.7L19 22l.7-2.3L22 19l-2.3-.7z" />
      </svg>
    ),

    check: (
      <svg {...common}>
        <path d="m5 12 4 4L19 6" />
      </svg>
    ),
  }

  return icons[name] || null
}

function DoctorDashboard() {
  const navigate = useNavigate()

  const [search, setSearch] = useState("")

  const patients = [
    {
      id: 1,
      name: "Aarav Mehta",
      age: 24,
      gender: "Male",
      bloodGroup: "O+",
      condition: "Left femur fracture",
      status: "Stable",
      critical: false,
    },
    {
      id: 2,
      name: "Ishita Kapoor",
      age: 46,
      gender: "Female",
      bloodGroup: "B+",
      condition: "Type 2 Diabetes + Hypertension",
      status: "Stable",
      critical: false,
    },
    {
      id: 3,
      name: "Nikhil Varma",
      age: 61,
      gender: "Male",
      bloodGroup: "A+",
      condition: "Previous MI / Angioplasty + Stent",
      status: "Monitoring",
      critical: true,
    },
    {
      id: 4,
      name: "Diya Srinivasan",
      age: 38,
      gender: "Female",
      bloodGroup: "AB+",
      condition: "Osteosarcoma",
      status: "Follow-up",
      critical: false,
    },
    {
      id: 5,
      name: "Kabir Malhotra",
      age: 52,
      gender: "Male",
      bloodGroup: "O-",
      condition: "Severe Penicillin Allergy",
      status: "Emergency Ready",
      critical: true,
    },
    {
      id: 6,
      name: "Tanya Bose",
      age: 34,
      gender: "Female",
      bloodGroup: "A-",
      condition: "Intracranial lesion / Post-surgery",
      status: "Follow-up",
      critical: true,
    },
  ]

  const filteredPatients = patients.filter((patient) =>
    `${patient.name} ${patient.condition}`
      .toLowerCase()
      .includes(search.toLowerCase())
  )

  const openPatient = (patient) => {
    navigate(`/doctor/passport/${patient.id}`)
  }

  return (
    <DashboardLayout
      role="doctor"
      userName="Dr. Arjun Rao"
    >
      <div className="doctor-dashboard-page">

        {/* =========================
            PAGE HEADER
            ========================= */}

        <div className="dashboard-page-header">

          <div>
            <div className="page-eyebrow">
              CLINICAL WORKSPACE
            </div>

            <h1>
              Doctor Dashboard
            </h1>

            <p>
              Access authorized patient health passports and clinical tools.
            </p>
          </div>

          <div className="doctor-ready-badge">
            <span className="status-dot"></span>
            Emergency Ready
          </div>

        </div>


        {/* =========================
            SUMMARY CARDS
            ========================= */}

        <div className="stats-grid">

          {/* Authorized Patients */}

          <div className="stat-card polished-stat-card">

            <div className="stat-icon stat-icon-patients">
              <Icon
                name="patients"
                size={21}
              />
            </div>

            <div className="stat-content">
              <span className="stat-label">
                Authorized Patients
              </span>

              <strong>
                {patients.length}
              </strong>

              <small>
                Active clinical access
              </small>
            </div>

            <div className="stat-accent">
              <Icon
                name="arrow"
                size={15}
              />
            </div>

          </div>


          {/* Critical Alerts */}

          <div className="stat-card polished-stat-card stat-card-alert">

            <div className="stat-icon stat-icon-alert">
              <Icon
                name="alert"
                size={21}
              />
            </div>

            <div className="stat-content">
              <span className="stat-label">
                Critical Alerts
              </span>

              <strong>
                3
              </strong>

              <small>
                Require clinical attention
              </small>
            </div>

            <div className="stat-accent">
              <Icon
                name="arrow"
                size={15}
              />
            </div>

          </div>


          {/* Pending Reviews */}

          <div className="stat-card polished-stat-card">

            <div className="stat-icon stat-icon-review">
              <Icon
                name="review"
                size={21}
              />
            </div>

            <div className="stat-content">
              <span className="stat-label">
                Pending Reviews
              </span>

              <strong>
                2
              </strong>

              <small>
                Awaiting doctor review
              </small>
            </div>

            <div className="stat-accent">
              <Icon
                name="arrow"
                size={15}
              />
            </div>

          </div>


          {/* Integrity */}

          <div className="stat-card polished-stat-card">

            <div className="stat-icon stat-icon-integrity">
              <Icon
                name="shield"
                size={21}
              />
            </div>

            <div className="stat-content">
              <span className="stat-label">
                Integrity Checks
              </span>

              <strong>
                8
              </strong>

              <small>
                Provenance checks recorded
              </small>
            </div>

            <div className="stat-accent">
              <Icon
                name="arrow"
                size={15}
              />
            </div>

          </div>

        </div>


        {/* =========================
            PATIENT SEARCH
            ========================= */}

        <section className="dashboard-panel doctor-patient-panel">

          <div className="panel-header">

            <div>
              <h2>
                Patient Health Passports
              </h2>

              <p>
                Search patients you are authorized to access.
              </p>
            </div>

            <button
              type="button"
              className="panel-action-button"
              onClick={() => navigate("/doctor/patients")}
            >
              View all
              <Icon
                name="arrow"
                size={14}
              />
            </button>

          </div>


          <div className="patient-search-wrapper">

            <span className="patient-search-icon">
              <Icon
                name="search"
                size={18}
              />
            </span>

            <input
              type="text"
              placeholder="Search by patient name or condition..."
              value={search}
              onChange={(event) =>
                setSearch(event.target.value)
              }
            />

          </div>


          <div className="doctor-patient-list">

            {filteredPatients.map((patient) => (

              <div
                className="doctor-patient-card"
                key={patient.id}
                onClick={() => openPatient(patient)}
                role="button"
                tabIndex={0}
                onKeyDown={(event) => {
                  if (event.key === "Enter") {
                    openPatient(patient)
                  }
                }}
              >

                <div className="patient-avatar">
                  {patient.name
                    .split(" ")
                    .map((word) => word[0])
                    .join("")
                    .slice(0, 2)
                    .toUpperCase()}
                </div>


                <div className="doctor-patient-info">

                  <div className="doctor-patient-name-row">

                    <h3>
                      {patient.name}
                    </h3>

                    {patient.critical && (
                      <span className="critical-mini-badge">
                        Critical
                      </span>
                    )}

                  </div>

                  <p>
                    {patient.age} years • {patient.gender}
                  </p>

                  <span>
                    {patient.condition}
                  </span>

                </div>


                <div className="doctor-patient-meta">

                  <span className="blood-group">
                    {patient.bloodGroup}
                  </span>

                  <span
                    className={`patient-status ${
                      patient.status === "Emergency Ready"
                        ? "emergency"
                        : patient.status === "Monitoring"
                          ? "monitoring"
                          : "stable"
                    }`}
                  >
                    {patient.status}
                  </span>

                  <span className="patient-arrow">
                    <Icon
                      name="arrow"
                      size={15}
                    />
                  </span>

                </div>

              </div>

            ))}


            {filteredPatients.length === 0 && (

              <div className="no-patients">

                <div className="empty-search-icon">
                  <Icon
                    name="search"
                    size={25}
                  />
                </div>

                <h3>
                  No patients found
                </h3>

                <p>
                  Try searching with a different name or condition.
                </p>

              </div>

            )}

          </div>

        </section>


        {/* =========================
            CRITICAL ALERTS
            ========================= */}

        <section className="dashboard-panel">

          <div className="panel-header">

            <div>
              <h2>
                Critical Patient Alerts
              </h2>

              <p>
                Information requiring clinical attention.
              </p>
            </div>

            <div className="panel-count">
              3 alerts
            </div>

          </div>


          <div className="doctor-alert-list">

            {/* Kabir */}

            <div className="doctor-alert critical">

              <div className="doctor-alert-icon">
                <Icon
                  name="warning"
                  size={20}
                />
              </div>

              <div>
                <strong>
                  Kabir Malhotra
                </strong>

                <p>
                  Severe Penicillin allergy — reaction recorded as anaphylaxis.
                </p>
              </div>

              <button
                type="button"
                onClick={() => openPatient(patients[4])}
              >
                View
                <Icon
                  name="arrow"
                  size={13}
                />
              </button>

            </div>


            {/* Tanya */}

            <div className="doctor-alert warning">

              <div className="doctor-alert-icon">
                <Icon
                  name="warning"
                  size={20}
                />
              </div>

              <div>
                <strong>
                  Tanya Bose
                </strong>

                <p>
                  Potential discrepancy detected between medical document and current surgery date.
                </p>
              </div>

              <button
                type="button"
                onClick={() => openPatient(patients[5])}
              >
                Review
                <Icon
                  name="arrow"
                  size={13}
                />
              </button>

            </div>


            {/* Nikhil */}

            <div className="doctor-alert info">

              <div className="doctor-alert-icon">
                <Icon
                  name="info"
                  size={20}
                />
              </div>

              <div>
                <strong>
                  Nikhil Varma
                </strong>

                <p>
                  Longitudinal cardiac history available for historical review.
                </p>
              </div>

              <button
                type="button"
                onClick={() => openPatient(patients[2])}
              >
                Open
                <Icon
                  name="arrow"
                  size={13}
                />
              </button>

            </div>

          </div>

        </section>


        {/* =========================
            QUICK ACTIONS
            ========================= */}

        <section className="dashboard-panel">

          <div className="panel-header">

            <div>
              <h2>
                Clinical Tools
              </h2>

              <p>
                Quick access to Medi-Trace clinical workflows.
              </p>
            </div>

          </div>


          <div className="clinical-tools-grid">

            <button
              type="button"
              className="clinical-tool"
              onClick={() => navigate("/doctor/patients")}
            >
              <span className="clinical-tool-icon">
                <Icon
                  name="patients"
                  size={21}
                />
              </span>

              <strong>
                Patient Directory
              </strong>

              <small>
                Browse authorized patients
              </small>

              <span className="clinical-tool-arrow">
                <Icon
                  name="arrow"
                  size={14}
                />
              </span>

            </button>


            <button
              type="button"
              className="clinical-tool"
              onClick={() => navigate("/doctor/documents")}
            >
              <span className="clinical-tool-icon">
                <Icon
                  name="folder"
                  size={21}
                />
              </span>

              <strong>
                Document Review
              </strong>

              <small>
                Upload and review medical documents
              </small>

              <span className="clinical-tool-arrow">
                <Icon
                  name="arrow"
                  size={14}
                />
              </span>

            </button>


            <button
              type="button"
              className="clinical-tool"
              onClick={() => navigate("/doctor/ai-reviews")}
            >
              <span className="clinical-tool-icon">
                <Icon
                  name="sparkles"
                  size={21}
                />
              </span>

              <strong>
                AI Reviews
              </strong>

              <small>
                Review AI-extracted findings
              </small>

              <span className="clinical-tool-arrow">
                <Icon
                  name="arrow"
                  size={14}
                />
              </span>

            </button>


            <button
              type="button"
              className="clinical-tool"
              onClick={() => navigate("/doctor/integrity")}
            >
              <span className="clinical-tool-icon">
                <Icon
                  name="check"
                  size={21}
                />
              </span>

              <strong>
                Integrity Verification
              </strong>

              <small>
                Verify historical record provenance
              </small>

              <span className="clinical-tool-arrow">
                <Icon
                  name="arrow"
                  size={14}
                />
              </span>

            </button>

          </div>

        </section>

      </div>
    </DashboardLayout>
  )
}

export default DoctorDashboard