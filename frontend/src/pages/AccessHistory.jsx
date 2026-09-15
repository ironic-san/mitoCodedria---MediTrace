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
    },
  ]

  return (
    <DashboardLayout role="patient" userName="Kabir Malhotra">
      <div className="audit-page">

        <div className="dashboard-page-header">
          <div>
            <div className="page-eyebrow">PATIENT AUDIT LOG</div>
            <h1>Access History</h1>
            <p>
              Every access to your medical records is recorded and visible to you.
            </p>
          </div>
        </div>

        {/* Transparency Banner */}

        <div className="audit-banner">
          <div className="audit-banner-icon">🛡️</div>

          <div>
            <h3>Full Transparency</h3>
            <p>
              Medi-Trace records every authorized and emergency access to your
              health passport. Patients can review these logs anytime.
            </p>
          </div>
        </div>

        {/* Summary Cards */}

        <div className="health-summary-grid">

          <div className="health-card">
            <div className="health-card-icon">👨‍⚕️</div>
            <div className="health-card-label">TOTAL ACCESSES</div>
            <div className="health-card-value">24</div>
            <div className="health-card-description">
              Since account creation
            </div>
          </div>

          <div className="health-card">
            <div className="health-card-icon">🔐</div>
            <div className="health-card-label">AUTHORIZED DOCTORS</div>
            <div className="health-card-value">3</div>
            <div className="health-card-description">
              Currently active
            </div>
          </div>

          <div className="health-card">
            <div className="health-card-icon">🚨</div>
            <div className="health-card-label">BREAK-GLASS EVENTS</div>
            <div className="health-card-value">1</div>
            <div className="health-card-description">
              Emergency access events
            </div>
          </div>

          <div className="health-card">
            <div className="health-card-icon">📋</div>
            <div className="health-card-label">LAST ACCESS</div>
            <div className="health-card-value">Today</div>
            <div className="health-card-description">
              09:18 AM
            </div>
          </div>

        </div>

        {/* Timeline */}

        <section className="dashboard-panel">

          <div className="panel-header">
            <div>
              <h2>Access Timeline</h2>
              <p>Chronological history of record access.</p>
            </div>
          </div>

          <div className="audit-timeline">

            {accessLogs.map((log) => (
              <div className="audit-entry" key={log.id}>

                <div className="audit-date">
                  <strong>{log.date}</strong>
                  <span>{log.time}</span>
                </div>

                <div className="audit-line"></div>

                <div className="audit-details">

                  <div className="audit-header">

                    <div>
                      <h3>{log.doctor}</h3>

                      <p>
                        {log.specialization} • {log.hospital}
                      </p>
                    </div>

                    <span
                      className={`audit-status ${
                        log.accessType === "Emergency"
                          ? "emergency"
                          : "normal"
                      }`}
                    >
                      {log.accessType}
                    </span>

                  </div>

                  <p className="audit-reason">
                    {log.reason}
                  </p>

                  <div className="audit-footer">

                    <span className="audit-badge">
                      {log.status}
                    </span>

                    <span>
                      Patient Visible
                    </span>

                  </div>

                </div>

              </div>
            ))}

          </div>

        </section>

        {/* Info Card */}

        <section className="dashboard-panel audit-info-panel">

          <div className="panel-header">
            <div>
              <h2>Why do I see these logs?</h2>
            </div>
          </div>

          <div className="audit-info-content">

            <div className="audit-info-item">
              <strong>Normal Access</strong>
              <p>
                Doctors you authorize can view and update your medical records.
              </p>
            </div>

            <div className="audit-info-item">
              <strong>Break-Glass Access</strong>
              <p>
                Emergency doctors may temporarily access only critical medical
                information during a verified emergency.
              </p>
            </div>

            <div className="audit-info-item">
              <strong>Audit Protection</strong>
              <p>
                Audit history cannot be edited or deleted by patients or doctors.
              </p>
            </div>

          </div>

        </section>

      </div>
    </DashboardLayout>
  )
}

export default AccessHistory