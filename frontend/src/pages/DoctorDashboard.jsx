import { useState } from "react"
import { useNavigate } from "react-router-dom"
import DashboardLayout from "../layouts/DashboardLayout.jsx"

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

        {/* PAGE HEADER */}

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


        {/* SUMMARY CARDS */}

        <div className="stats-grid">

          <div className="stat-card">

            <div className="stat-icon">
              👥
            </div>

            <div>
              <span>Authorized Patients</span>
              <strong>{patients.length}</strong>
            </div>

          </div>


          <div className="stat-card">

            <div className="stat-icon">
              🚨
            </div>

            <div>
              <span>Critical Alerts</span>
              <strong>3</strong>
            </div>

          </div>


          <div className="stat-card">

            <div className="stat-icon">
              📄
            </div>

            <div>
              <span>Pending Reviews</span>
              <strong>2</strong>
            </div>

          </div>


          <div className="stat-card">

            <div className="stat-icon">
              ✓
            </div>

            <div>
              <span>Integrity Checks</span>
              <strong>8</strong>
            </div>

          </div>

        </div>


        {/* PATIENT SEARCH */}

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

          </div>


          <div className="patient-search-wrapper">

            <span className="patient-search-icon">
              🔍
            </span>

            <input
              type="text"
              placeholder="Search by patient name or condition..."
              value={search}
              onChange={(event) => setSearch(event.target.value)}
            />

          </div>


          <div className="doctor-patient-list">

            {filteredPatients.map((patient) => (

              <div
                className="doctor-patient-card"
                key={patient.id}
                onClick={() => openPatient(patient)}
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
                    →
                  </span>

                </div>

              </div>

            ))}


            {filteredPatients.length === 0 && (

              <div className="no-patients">
                <div>🔍</div>

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


        {/* CRITICAL ALERTS */}

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

          </div>


          <div className="doctor-alert-list">

            <div className="doctor-alert critical">

              <div className="doctor-alert-icon">
                ⚠️
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
              </button>

            </div>


            <div className="doctor-alert warning">

              <div className="doctor-alert-icon">
                ⚠️
              </div>

              <div>
                <strong>
                  Tanya Bose
                </strong>

                <p>
                  Potential discrepancy detected between medical document and
                  current surgery date.
                </p>
              </div>

              <button
                type="button"
                onClick={() => openPatient(patients[5])}
              >
                Review
              </button>

            </div>


            <div className="doctor-alert info">

              <div className="doctor-alert-icon">
                ℹ️
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
              </button>

            </div>

          </div>

        </section>


        {/* QUICK ACTIONS */}

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
              <span>👥</span>
              <strong>Patient Directory</strong>
              <small>Browse authorized patients</small>
            </button>


            <button
              type="button"
              className="clinical-tool"
              onClick={() => navigate("/doctor/documents")}
            >
              <span>📄</span>
              <strong>Document Review</strong>
              <small>Upload and review medical documents</small>
            </button>


            <button
              type="button"
              className="clinical-tool"
              onClick={() => navigate("/doctor/ai-reviews")}
            >
              <span>✦</span>
              <strong>AI Reviews</strong>
              <small>Review AI-extracted findings</small>
            </button>


            <button
              type="button"
              className="clinical-tool"
              onClick={() => navigate("/doctor/integrity")}
            >
              <span>✓</span>
              <strong>Integrity Verification</strong>
              <small>Verify historical record provenance</small>
            </button>

          </div>

        </section>

      </div>
    </DashboardLayout>
  )
}

export default DoctorDashboard