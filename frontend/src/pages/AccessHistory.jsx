import DashboardLayout from "../layouts/DashboardLayout.jsx"

function AccessHistory() {
  const accessLogs = [
    {
      id: 1,
      doctor: "Dr. Arjun Rao",
      hospital: "Apollo Hospitals, Chennai",
      specialization: "Emergency Medicine",
      date: "15 Sep 2026",
      time: "09:18 AM",
      accessType: "Emergency",
      status: "Break-Glass",
      reason: "Emergency treatment for suspected anaphylaxis.",
      icon: "🚨",
    },
    {
      id: 2,
      doctor: "Dr. Priya Menon",
      hospital: "MIOT International",
      specialization: "Cardiology",
      date: "12 Sep 2026",
      time: "02:45 PM",
      accessType: "Normal",
      status: "Completed",
      reason: "Reviewed medication history before consultation.",
      icon: "👨‍⚕️",
    },
    {
      id: 3,
      doctor: "Dr. Rahul Sharma",
      hospital: "Fortis Hospital",
      specialization: "General Medicine",
      date: "05 Sep 2026",
      time: "11:20 AM",
      accessType: "Normal",
      status: "Completed",
      reason: "Routine outpatient consultation.",
      icon: "👨‍⚕️",
    },
    {
      id: 4,
      doctor: "Dr. Sneha Iyer",
      hospital: "Apollo Hospitals",
      specialization: "Internal Medicine",
      date: "28 Aug 2026",
      time: "04:15 PM",
      accessType: "Normal",
      status: "Revoked",
      reason: "Temporary consultation access expired.",
      icon: "👩‍⚕️",
    },
  ]

  const normalAccesses = accessLogs.filter(
    (log) => log.accessType === "Normal"
  ).length

  const emergencyAccesses = accessLogs.filter(
    (log) => log.accessType === "Emergency"
  ).length

  return (
    <DashboardLayout
      role="patient"
      userName="Kabir Malhotra"
    >
      <div className="patient-history-page">

        {/* PAGE HEADER */}

        <div className="dashboard-page-header">

          <div>
            <div className="page-eyebrow">
              PRIVACY & TRANSPARENCY
            </div>

            <h1>
              Access History
            </h1>

            <p>
              Review when doctors accessed your Medi-Trace health passport
              and why the access occurred.
            </p>
          </div>

          <div className="history-secure-status">
            <span className="history-secure-dot"></span>
            Audit Protected
          </div>

        </div>


        {/* TRANSPARENCY BANNER */}

        <div className="audit-banner patient-audit-banner">

          <div className="audit-banner-icon">
            🛡
          </div>

          <div>
            <span className="audit-banner-label">
              PATIENT TRANSPARENCY
            </span>

            <h3>
              Every access is recorded
            </h3>

            <p>
              Medi-Trace records normal doctor access and emergency
              break-glass access so you can review how your medical
              information was accessed.
            </p>
          </div>

        </div>


        {/* SUMMARY */}

        <div className="health-summary-grid access-history-stats">

          <div className="health-card">

            <div className="health-card-icon">
              👨‍⚕️
            </div>

            <div className="health-card-label">
              TOTAL ACCESSES
            </div>

            <div className="health-card-value">
              24
            </div>

            <div className="health-card-description">
              Since account creation
            </div>

          </div>


          <div className="health-card">

            <div className="health-card-icon">
              🔐
            </div>

            <div className="health-card-label">
              NORMAL ACCESS
            </div>

            <div className="health-card-value">
              {normalAccesses}
            </div>

            <div className="health-card-description">
              Recorded consultation events
            </div>

          </div>


          <div className="health-card">

            <div className="health-card-icon">
              🚨
            </div>

            <div className="health-card-label">
              BREAK-GLASS EVENTS
            </div>

            <div className="health-card-value">
              {emergencyAccesses}
            </div>

            <div className="health-card-description">
              Emergency access events
            </div>

          </div>


          <div className="health-card">

            <div className="health-card-icon">
              ◷
            </div>

            <div className="health-card-label">
              LAST ACCESS
            </div>

            <div className="health-card-value">
              Today
            </div>

            <div className="health-card-description">
              09:18 AM
            </div>

          </div>

        </div>


        {/* ACCESS TIMELINE */}

        <section className="dashboard-panel access-history-panel">

          <div className="panel-header">

            <div>
              <div className="section-kicker">
                AUDIT HISTORY
              </div>

              <h2>
                Access Timeline
              </h2>

              <p>
                A chronological record of access to your health passport.
              </p>
            </div>

            <div className="history-record-count">
              {accessLogs.length} recent records
            </div>

          </div>


          <div className="patient-audit-timeline">

            {accessLogs.map((log, index) => (

              <div
                className={`patient-audit-entry ${
                  log.accessType === "Emergency"
                    ? "patient-audit-emergency"
                    : ""
                }`}
                key={log.id}
              >

                {/* DATE */}

                <div className="patient-audit-date">

                  <strong>
                    {log.date}
                  </strong>

                  <span>
                    {log.time}
                  </span>

                </div>


                {/* TIMELINE NODE */}

                <div className="patient-audit-track">

                  <div className="patient-audit-node">
                    {log.icon}
                  </div>

                  {index !== accessLogs.length - 1 && (
                    <div className="patient-audit-connector"></div>
                  )}

                </div>


                {/* DETAILS */}

                <div className="patient-audit-details">

                  <div className="patient-audit-top">

                    <div>

                      <div className="patient-audit-doctor">
                        <h3>
                          {log.doctor}
                        </h3>

                        <span
                          className={`patient-access-type ${
                            log.accessType === "Emergency"
                              ? "emergency"
                              : "normal"
                          }`}
                        >
                          {log.accessType === "Emergency"
                            ? "BREAK-GLASS"
                            : "NORMAL ACCESS"}
                        </span>
                      </div>

                      <p className="patient-audit-specialization">
                        {log.specialization}
                        <span>•</span>
                        {log.hospital}
                      </p>

                    </div>

                  </div>


                  <div className="patient-audit-reason-box">

                    <span>
                      ACCESS REASON
                    </span>

                    <p>
                      {log.reason}
                    </p>

                  </div>


                  <div className="patient-audit-footer">

                    <span
                      className={`patient-audit-status ${
                        log.status === "Break-Glass"
                          ? "status-emergency"
                          : log.status === "Revoked"
                          ? "status-revoked"
                          : "status-completed"
                      }`}
                    >
                      {log.status}
                    </span>

                    <span className="patient-visible-label">
                      <span>✓</span>
                      Patient Visible
                    </span>

                  </div>

                </div>

              </div>

            ))}

          </div>

        </section>


        {/* ACCESS TYPES */}

        <section className="dashboard-panel access-types-panel">

          <div className="panel-header">

            <div>
              <div className="section-kicker">
                ACCESS TYPES
              </div>

              <h2>
                Understanding your access history
              </h2>

              <p>
                Different access workflows have different permissions.
              </p>
            </div>

          </div>


          <div className="access-type-grid">

            <div className="access-type-card">

              <div className="access-type-icon normal-icon">
                🔐
              </div>

              <div>
                <h3>
                  Normal Access
                </h3>

                <p>
                  Access granted by you to an authorized doctor. Normal
                  access can support viewing, updating and reviewing your
                  health passport.
                </p>
              </div>

              <span className="access-type-badge normal-badge">
                Patient Authorized
              </span>

            </div>


            <div className="access-type-card emergency-type-card">

              <div className="access-type-icon emergency-icon-small">
                🚨
              </div>

              <div>
                <h3>
                  Break-Glass Access
                </h3>

                <p>
                  A separate emergency workflow that allows restricted
                  access to critical information. It does not allow
                  modification of your records.
                </p>
              </div>

              <span className="access-type-badge emergency-badge-small">
                Emergency Only
              </span>

            </div>

          </div>

        </section>


        {/* AUDIT PROTECTION */}

        <div className="audit-protection-card">

          <div className="audit-protection-icon">
            🔒
          </div>

          <div>

            <span>
              AUDIT PROTECTION
            </span>

            <strong>
              Your access history is recorded for transparency
            </strong>

            <p>
              Access events are maintained as part of the Medi-Trace audit
              trail and are visible to you.
            </p>

          </div>

          <div className="audit-protection-status">
            <span></span>
            Protected
          </div>

        </div>

      </div>
    </DashboardLayout>
  )
}

export default AccessHistory