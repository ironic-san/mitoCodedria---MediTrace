import { useState } from "react"
import { useNavigate } from "react-router-dom"
import DashboardLayout from "../layouts/DashboardLayout.jsx"
import { api } from "../services/api"
import { useApiQuery } from "../hooks/useApiQuery"
import { ErrorState, LoadingState } from "../components/AsyncState"

function DoctorPatients() {
  const navigate = useNavigate()

  const [search, setSearch] = useState("")
  const [filter, setFilter] = useState("All")
  const { data, loading, error, refresh } = useApiQuery(api.doctorPatients, [])

  const patients = data?.map((patient) => ({
    id: patient.patient_id,
    name: patient.full_name,
    age: patient.date_of_birth ? new Date().getFullYear() - new Date(patient.date_of_birth).getFullYear() : "—",
    gender: patient.gender || "Not recorded",
    bloodGroup: patient.blood_group || "Not recorded",
    condition: patient.relationship_type || "Authorized patient",
    status: patient.access_status,
    critical: false,
    lastVisit: patient.access_expiry ? `Access until ${new Date(patient.access_expiry).toLocaleDateString()}` : "Active access",
  })) || []
  /* Backend does not provide diagnoses/criticality in the directory response. */
  /*
    {
      id: 1,
      name: "Aarav Mehta",
      age: 24,
      gender: "Male",
      bloodGroup: "O+",
      condition: "Left femur fracture",
      status: "Stable",
      critical: false,
      lastVisit: "12 Sep 2026",
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
      lastVisit: "10 Sep 2026",
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
      lastVisit: "14 Sep 2026",
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
      lastVisit: "08 Sep 2026",
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
      lastVisit: "15 Sep 2026",
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
      lastVisit: "13 Sep 2026",
    },
  ]
  */

  const filteredPatients = patients.filter((patient) => {
    const matchesSearch =
      `${patient.name} ${patient.condition} ${patient.bloodGroup}`
        .toLowerCase()
        .includes(search.toLowerCase())

    const matchesFilter =
      filter === "All" ||
      (filter === "Critical" && patient.critical) ||
      patient.status === filter

    return matchesSearch && matchesFilter
  })

  const openPassport = (patient) => {
    navigate(`/doctor/passport/${patient.id}`)
  }

  return (
    <DashboardLayout
      role="doctor"
      userName="Dr. Arjun Rao"
    >
      <div className="doctor-patients-page">

        {loading && <LoadingState label="Loading authorized patients…" />}
        {error && <ErrorState error={error} onRetry={refresh} />}

        {/* PAGE HEADER */}

        <div className="dashboard-page-header">

          <div>
            <div className="page-eyebrow">
              CLINICAL DIRECTORY
            </div>

            <h1>
              Patient Directory
            </h1>

            <p>
              Search and access health passports for your authorized patients.
            </p>
          </div>

        </div>


        {/* SUMMARY */}

        <div className="stats-grid">

          <div className="stat-card">

            <div className="stat-icon">
              👥
            </div>

            <div>
              <span>Total Patients</span>
              <strong>{patients.length}</strong>
            </div>

          </div>


          <div className="stat-card">

            <div className="stat-icon">
              ⚠️
            </div>

            <div>
              <span>Critical Patients</span>
              <strong>
                {patients.filter((patient) => patient.critical).length}
              </strong>
            </div>

          </div>


          <div className="stat-card">

            <div className="stat-icon">
              🚨
            </div>

            <div>
              <span>Emergency Ready</span>
              <strong>1</strong>
            </div>

          </div>


          <div className="stat-card">

            <div className="stat-icon">
              🔐
            </div>

            <div>
              <span>Access</span>
              <strong>Authorized</strong>
            </div>

          </div>

        </div>


        {/* SEARCH AND FILTER */}

        <section className="dashboard-panel">

          <div className="patient-directory-toolbar">

            <div className="directory-search">

              <span>
                🔍
              </span>

              <input
                type="text"
                placeholder="Search by name, condition or blood group..."
                value={search}
                onChange={(event) => setSearch(event.target.value)}
              />

            </div>


            <div className="directory-filters">

              {[
                "All",
                "Critical",
                "Stable",
                "Monitoring",
                "Follow-up",
              ].map((option) => (

                <button
                  type="button"
                  key={option}
                  className={
                    filter === option
                      ? "directory-filter active"
                      : "directory-filter"
                  }
                  onClick={() => setFilter(option)}
                >
                  {option}
                </button>

              ))}

            </div>

          </div>


          {/* PATIENT COUNT */}

          <div className="directory-result-count">
            Showing <strong>{filteredPatients.length}</strong> of{" "}
            <strong>{patients.length}</strong> patients
          </div>


          {/* PATIENT TABLE */}

          <div className="patient-directory-table">

            <div className="patient-table-header">

              <span>Patient</span>
              <span>Blood Group</span>
              <span>Primary Condition</span>
              <span>Status</span>
              <span>Last Visit</span>
              <span></span>

            </div>


            {filteredPatients.map((patient) => (

              <div
                className="patient-table-row"
                key={patient.id}
                onClick={() => openPassport(patient)}
              >

                <div className="directory-patient">

                  <div className="directory-avatar">
                    {patient.name
                      .split(" ")
                      .map((word) => word[0])
                      .join("")
                      .slice(0, 2)
                      .toUpperCase()}
                  </div>

                  <div>

                    <div className="directory-patient-name">

                      {patient.name}

                      {patient.critical && (
                        <span className="critical-mini-badge">
                          Critical
                        </span>
                      )}

                    </div>

                    <small>
                      {patient.age} years • {patient.gender}
                    </small>

                  </div>

                </div>


                <div className="directory-blood">
                  {patient.bloodGroup}
                </div>


                <div className="directory-condition">
                  {patient.condition}
                </div>


                <div>

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

                </div>


                <div className="directory-last-visit">
                  {patient.lastVisit}
                </div>


                <div className="directory-open">
                  →
                </div>

              </div>

            ))}


            {filteredPatients.length === 0 && (

              <div className="no-patients">

                <div>
                  🔍
                </div>

                <h3>
                  No patients found
                </h3>

                <p>
                  Try changing your search or filter.
                </p>

              </div>

            )}

          </div>

        </section>


        {/* ACCESS INFORMATION */}

        <div className="doctor-directory-info">

          <div className="doctor-directory-info-icon">
            🔐
          </div>

          <div>

            <strong>
              Authorized access only
            </strong>

            <p>
              This directory contains patients who have granted normal access
              to this doctor. Emergency access follows the separate
              break-glass workflow.
            </p>

          </div>

        </div>

      </div>
    </DashboardLayout>
  )
}

export default DoctorPatients
