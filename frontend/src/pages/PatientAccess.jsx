import { useState } from "react"
import DashboardLayout from "../layouts/DashboardLayout.jsx"

function PatientAccess() {
  const [doctors, setDoctors] = useState([
    {
      id: 1,
      name: "Dr. Arjun Rao",
      specialization: "Emergency Medicine",
      hospital: "Apollo Hospitals",
      access: true,
      grantedOn: "12 Sep 2026",
    },
    {
      id: 2,
      name: "Dr. Priya Menon",
      specialization: "Cardiology",
      hospital: "MIOT International",
      access: false,
      grantedOn: null,
    },
    {
      id: 3,
      name: "Dr. Rahul Sharma",
      specialization: "General Medicine",
      hospital: "Fortis Hospital",
      access: false,
      grantedOn: null,
    },
  ])

  const toggleAccess = (id) => {
    setDoctors((currentDoctors) =>
      currentDoctors.map((doctor) => {
        if (doctor.id !== id) return doctor

        const newAccess = !doctor.access

        return {
          ...doctor,
          access: newAccess,
          grantedOn: newAccess ? "15 Sep 2026" : null,
        }
      })
    )
  }

  const activeDoctors = doctors.filter((doctor) => doctor.access).length

  return (
    <DashboardLayout userType="patient">
      <div className="page-header">
        <div>
          <h1>Access Control</h1>
          <p>
            Control which doctors can access your Medi-Trace health passport.
          </p>
        </div>
      </div>

      {/* Access Overview */}
      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-icon">👨‍⚕️</div>
          <div>
            <span>Authorized Doctors</span>
            <strong>{activeDoctors}</strong>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">🔐</div>
          <div>
            <span>Access Type</span>
            <strong>Normal</strong>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">🛡️</div>
          <div>
            <span>Your Control</span>
            <strong>Patient</strong>
          </div>
        </div>
      </div>

      {/* Important Information */}
      <div className="info-banner">
        <div className="info-banner-icon">🔒</div>

        <div>
          <h3>You control normal doctor access</h3>
          <p>
            Doctors can access your health passport only when you authorize
            them. You can revoke normal access at any time.
          </p>
        </div>
      </div>

      {/* Doctor List */}
      <section className="dashboard-section">
        <div className="section-header">
          <div>
            <h2>Doctor Access</h2>
            <p>Manage doctors who can access your medical information.</p>
          </div>
        </div>

        <div className="doctor-access-list">
          {doctors.map((doctor) => (
            <div className="doctor-access-card" key={doctor.id}>
              <div className="doctor-profile">
                <div className="doctor-avatar">
                  {doctor.name
                    .replace("Dr. ", "")
                    .split(" ")
                    .map((name) => name[0])
                    .join("")
                    .slice(0, 2)}
                </div>

                <div>
                  <h3>{doctor.name}</h3>
                  <p>{doctor.specialization}</p>
                  <span>{doctor.hospital}</span>
                </div>
              </div>

              <div className="doctor-access-status">
                {doctor.access ? (
                  <>
                    <div className="access-active">
                      <span className="status-dot"></span>
                      Access Granted
                    </div>

                    <small>Granted on {doctor.grantedOn}</small>

                    <button
                      className="revoke-button"
                      onClick={() => toggleAccess(doctor.id)}
                    >
                      Revoke Access
                    </button>
                  </>
                ) : (
                  <>
                    <div className="access-inactive">
                      <span className="status-dot"></span>
                      No Access
                    </div>

                    <small>Doctor cannot access your passport</small>

                    <button
                      className="grant-button"
                      onClick={() => toggleAccess(doctor.id)}
                    >
                      Grant Access
                    </button>
                  </>
                )}
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* What normal access allows */}
      <section className="dashboard-section">
        <div className="section-header">
          <div>
            <h2>What does normal access allow?</h2>
            <p>Authorized doctors can use your health passport for care.</p>
          </div>
        </div>

        <div className="permission-grid">
          <div className="permission-card">
            <div className="permission-icon">📋</div>
            <h3>View Health Passport</h3>
            <p>
              Access your structured medical information, conditions,
              allergies, medications and medical events.
            </p>
          </div>

          <div className="permission-card">
            <div className="permission-icon">✏️</div>
            <h3>Update Medical Information</h3>
            <p>
              Authorized doctors can add or correct medical information after
              reviewing it.
            </p>
          </div>

          <div className="permission-card">
            <div className="permission-icon">📄</div>
            <h3>Upload Documents</h3>
            <p>
              Doctors can upload relevant medical documents for processing and
              review.
            </p>
          </div>

          <div className="permission-card">
            <div className="permission-icon">🤖</div>
            <h3>AI-Assisted Analysis</h3>
            <p>
              Doctors can use Medi-Trace AI tools to analyze historical
              medical information.
            </p>
          </div>
        </div>
      </section>

      {/* Emergency Access */}
      <section className="emergency-access-card">
        <div className="emergency-icon">🚨</div>

        <div className="emergency-content">
          <h2>Emergency Access is different</h2>
          <p>
            During a genuine emergency, a doctor may use the separate
            break-glass emergency workflow to view critical medical
            information. Emergency access is restricted and does not allow
            modification of your records.
          </p>
        </div>

        <span className="emergency-badge">Break-Glass</span>
      </section>
    </DashboardLayout>
  )
}

export default PatientAccess