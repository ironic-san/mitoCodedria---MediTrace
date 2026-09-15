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

  const [confirmDoctor, setConfirmDoctor] = useState(null)
  const [actionMessage, setActionMessage] = useState("")

  const toggleAccess = (id) => {
    const doctor = doctors.find((item) => item.id === id)

    if (!doctor) return

    setDoctors((currentDoctors) =>
      currentDoctors.map((item) => {
        if (item.id !== id) return item

        const newAccess = !item.access

        return {
          ...item,
          access: newAccess,
          grantedOn: newAccess ? "15 Sep 2026" : null,
        }
      })
    )

    setActionMessage(
      doctor.access
        ? `${doctor.name}'s access has been revoked.`
        : `${doctor.name} has been granted access.`
    )

    setConfirmDoctor(null)

    setTimeout(() => {
      setActionMessage("")
    }, 3500)
  }

  const activeDoctors = doctors.filter(
    (doctor) => doctor.access
  ).length

  return (
    <DashboardLayout
      role="patient"
      userName="Kabir Malhotra"
    >
      <div className="patient-access-page">

        {/* =====================================================
            PAGE HEADER
            ===================================================== */}

        <div className="dashboard-page-header">

          <div>
            <div className="page-eyebrow">
              PRIVACY & ACCESS
            </div>

            <h1>
              Access Control
            </h1>

            <p>
              Control which doctors can access your Medi-Trace health
              passport and medical information.
            </p>
          </div>

          <div className="access-control-status">
            <span className="access-control-status-dot"></span>
            Patient Controlled
          </div>

        </div>


        {/* =====================================================
            ACTION MESSAGE
            ===================================================== */}

        {actionMessage && (
          <div className="access-action-message">

            <div className="access-action-icon">
              ✓
            </div>

            <div>
              <strong>
                Access settings updated
              </strong>

              <p>
                {actionMessage}
              </p>
            </div>

          </div>
        )}


        {/* =====================================================
            ACCESS OVERVIEW
            ===================================================== */}

        <div className="stats-grid access-stats">

          <div className="stat-card">

            <div className="stat-icon">
              👨‍⚕️
            </div>

            <div>
              <span>
                Authorized Doctors
              </span>

              <strong>
                {activeDoctors}
              </strong>
            </div>

          </div>


          <div className="stat-card">

            <div className="stat-icon">
              🔐
            </div>

            <div>
              <span>
                Access Type
              </span>

              <strong>
                Normal
              </strong>
            </div>

          </div>


          <div className="stat-card">

            <div className="stat-icon">
              🛡️
            </div>

            <div>
              <span>
                Access Controlled By
              </span>

              <strong>
                You
              </strong>
            </div>

          </div>

        </div>


        {/* =====================================================
            INFORMATION BANNER
            ===================================================== */}

        <div className="info-banner access-info-banner">

          <div className="info-banner-icon">
            🔒
          </div>

          <div>
            <h3>
              You control normal doctor access
            </h3>

            <p>
              Doctors can access your health passport through normal
              access only when you authorize them. You can revoke this
              access at any time.
            </p>
          </div>

        </div>


        {/* =====================================================
            DOCTOR ACCESS
            ===================================================== */}

        <section className="dashboard-panel access-doctors-panel">

          <div className="panel-header">

            <div>
              <div className="section-kicker">
                AUTHORIZED DOCTORS
              </div>

              <h2>
                Doctor Access
              </h2>

              <p>
                Manage doctors who are authorized to access your medical
                information.
              </p>
            </div>

            <div className="doctor-access-count">
              {activeDoctors} active
            </div>

          </div>


          <div className="doctor-access-list">

            {doctors.map((doctor) => (

              <div
                className={`doctor-access-card ${
                  doctor.access
                    ? "doctor-access-active"
                    : ""
                }`}
                key={doctor.id}
              >

                {/* DOCTOR INFORMATION */}

                <div className="doctor-profile">

                  <div className="doctor-avatar">
                    {doctor.name
                      .replace("Dr. ", "")
                      .split(" ")
                      .map((name) => name[0])
                      .join("")
                      .slice(0, 2)
                      .toUpperCase()}
                  </div>

                  <div className="doctor-profile-information">

                    <h3>
                      {doctor.name}
                    </h3>

                    <p>
                      {doctor.specialization}
                    </p>

                    <span>
                      {doctor.hospital}
                    </span>

                  </div>

                </div>


                {/* BOXED ACCESS CONTROL */}

                <div className="doctor-access-control-box">

                  {doctor.access ? (
                    <>
                      <div className="access-active">

                        <span className="status-dot"></span>

                        Access Granted

                      </div>

                      <small>
                        Granted on {doctor.grantedOn}
                      </small>

                      <button
                        type="button"
                        className="revoke-button"
                        onClick={() =>
                          setConfirmDoctor(doctor)
                        }
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

                      <small>
                        Doctor cannot access your passport
                      </small>

                      <button
                        type="button"
                        className="grant-button"
                        onClick={() =>
                          setConfirmDoctor(doctor)
                        }
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


        {/* =====================================================
            NORMAL ACCESS PERMISSIONS
            ===================================================== */}

        <section className="dashboard-panel permissions-panel">

          <div className="panel-header">

            <div>
              <div className="section-kicker">
                NORMAL ACCESS
              </div>

              <h2>
                What does normal access allow?
              </h2>

              <p>
                Authorized doctors can use your health passport as part
                of your care workflow.
              </p>
            </div>

          </div>


          <div className="permission-grid">

            <div className="permission-card">

              <div className="permission-icon">
                📋
              </div>

              <h3>
                View Health Passport
              </h3>

              <p>
                Access structured medical information such as conditions,
                allergies, medications, events and procedures.
              </p>

            </div>


            <div className="permission-card">

              <div className="permission-icon">
                ✏️
              </div>

              <h3>
                Update Medical Information
              </h3>

              <p>
                Authorized doctors can add or correct medical information
                after reviewing it.
              </p>

            </div>


            <div className="permission-card">

              <div className="permission-icon">
                📄
              </div>

              <h3>
                Upload Documents
              </h3>

              <p>
                Relevant medical documents can be uploaded for processing
                and clinical review.
              </p>

            </div>


            <div className="permission-card">

              <div className="permission-icon">
                ✦
              </div>

              <h3>
                AI-Assisted Review
              </h3>

              <p>
                Authorized doctors can use Medi-Trace assistance to review
                historical medical information.
              </p>

            </div>

          </div>

        </section>


        {/* =====================================================
            PATIENT CONTROL PRINCIPLE
            ===================================================== */}

        <section className="access-principle-card">

          <div className="access-principle-icon">
            ✓
          </div>

          <div>

            <span className="access-principle-label">
              PATIENT CONTROL
            </span>

            <h2>
              Normal access requires your authorization
            </h2>

            <p>
              Medi-Trace keeps normal doctor access separate from
              emergency break-glass access. Your authorization controls
              normal read/write access to your health passport.
            </p>

          </div>

        </section>


        {/* =====================================================
            EMERGENCY ACCESS
            ===================================================== */}

        <section className="emergency-access-card">

          <div className="emergency-icon">
            🚨
          </div>

          <div className="emergency-content">

            <span className="emergency-section-label">
              SEPARATE EMERGENCY WORKFLOW
            </span>

            <h2>
              Emergency Access is different
            </h2>

            <p>
              During a genuine emergency, a doctor may use the separate
              break-glass workflow to view critical medical information.
              Emergency access is restricted, auditable and does not
              allow modification of your medical records.
            </p>

          </div>

          <span className="emergency-badge">
            Break-Glass
          </span>

        </section>


        {/* =====================================================
            CONFIRMATION MODAL
            ===================================================== */}

        {confirmDoctor && (

          <div
            className="access-modal-overlay"
            onClick={() => setConfirmDoctor(null)}
          >

            <div
              className="access-confirmation-modal"
              onClick={(event) =>
                event.stopPropagation()
              }
            >

              <div className="confirmation-icon">
                {confirmDoctor.access
                  ? "🔐"
                  : "✓"}
              </div>


              <div className="confirmation-content">

                <span>
                  ACCESS CHANGE
                </span>

                <h2>
                  {confirmDoctor.access
                    ? "Revoke doctor access?"
                    : "Grant doctor access?"}
                </h2>

                <p>
                  {confirmDoctor.access
                    ? `${confirmDoctor.name} will no longer have normal access to your Medi-Trace health passport.`
                    : `${confirmDoctor.name} will be authorized to access your Medi-Trace health passport through normal doctor access.`}
                </p>

              </div>


              {/* SELECTED DOCTOR */}

              <div className="confirmation-doctor">

                <div className="confirmation-avatar">

                  {confirmDoctor.name
                    .replace("Dr. ", "")
                    .split(" ")
                    .map((name) => name[0])
                    .join("")
                    .slice(0, 2)
                    .toUpperCase()}

                </div>

                <div>

                  <strong>
                    {confirmDoctor.name}
                  </strong>

                  <span>
                    {confirmDoctor.specialization}
                  </span>

                </div>

              </div>


              {/* MODAL ACTIONS */}

              <div className="confirmation-actions">

                <button
                  type="button"
                  className="confirmation-cancel"
                  onClick={() =>
                    setConfirmDoctor(null)
                  }
                >
                  Cancel
                </button>

                <button
                  type="button"
                  className={
                    confirmDoctor.access
                      ? "confirmation-revoke"
                      : "confirmation-grant"
                  }
                  onClick={() =>
                    toggleAccess(confirmDoctor.id)
                  }
                >
                  {confirmDoctor.access
                    ? "Revoke Access"
                    : "Grant Access"}
                </button>

              </div>

            </div>

          </div>

        )}

      </div>
    </DashboardLayout>
  )
}

export default PatientAccess