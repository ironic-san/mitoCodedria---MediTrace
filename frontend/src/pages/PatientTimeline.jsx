import DashboardLayout from "../layouts/DashboardLayout.jsx"

function PatientTimeline() {
  const events = [
    {
      year: "2019",
      date: "18 Nov 2019",
      title: "Severe Penicillin Allergy Identified",
      type: "Allergy",
      icon: "⚠️",
      hospital: "Apollo Hospitals, Chennai",
      description:
        "Severe allergic reaction to Penicillin documented. Reaction recorded as anaphylaxis.",
      details: [
        "Allergen: Penicillin",
        "Severity: Severe",
        "Reaction: Anaphylaxis",
      ],
      status: "Critical",
    },
    {
      year: "2024",
      date: "06 Aug 2024",
      title: "Bacterial Pneumonia Hospitalization",
      type: "Hospitalization",
      icon: "🏥",
      hospital: "Apollo Hospitals, Chennai",
      description:
        "Hospital admission for bacterial pneumonia with treatment and clinical monitoring.",
      details: [
        "Diagnosis: Bacterial pneumonia",
        "Hospital admission recorded",
        "Treatment and follow-up documented",
      ],
      status: "Completed",
    },
    {
      year: "2026",
      date: "15 Sep 2026",
      title: "Emergency Presentation",
      type: "Emergency",
      icon: "🚨",
      hospital: "Emergency Department",
      description:
        "Patient presented for emergency evaluation. Critical allergy information is available through the emergency health passport.",
      details: [
        "Emergency workflow initiated",
        "Critical allergy information available",
        "Emergency access requires break-glass authorization",
      ],
      status: "Current",
    },
  ]

  return (
    <DashboardLayout
      role="patient"
      userName="Kabir Malhotra"
    >
      <div className="timeline-page">

        {/* PAGE HEADER */}

        <div className="dashboard-page-header">
          <div>
            <div className="page-eyebrow">
              MEDICAL HISTORY
            </div>

            <h1>
              Medical Timeline
            </h1>

            <p>
              A chronological view of your documented medical history.
            </p>
          </div>
        </div>


        {/* IMPORTANT NOTICE */}

        <div className="timeline-notice">

          <div className="timeline-notice-icon">
            ℹ️
          </div>

          <div>
            <h3>
              Your medical history
            </h3>

            <p>
              This timeline presents structured medical information recorded
              in your Medi-Trace health passport.
            </p>
          </div>

        </div>


        {/* TIMELINE */}

        <section className="dashboard-panel">

          <div className="panel-header">

            <div>
              <h2>
                Medical Events
              </h2>

              <p>
                Chronological history of documented events.
              </p>
            </div>

            <div className="timeline-count">
              {events.length} Events
            </div>

          </div>


          <div className="medical-timeline">

            {events.map((event, index) => (

              <div
                className="timeline-event"
                key={event.date}
              >

                {/* DATE */}

                <div className="timeline-date">

                  <strong>
                    {event.year}
                  </strong>

                  <span>
                    {event.date}
                  </span>

                </div>


                {/* TIMELINE MARKER */}

                <div className="timeline-marker-wrapper">

                  <div className="timeline-marker">
                    {event.icon}
                  </div>

                  {index !== events.length - 1 && (
                    <div className="timeline-connector"></div>
                  )}

                </div>


                {/* EVENT CONTENT */}

                <div className="timeline-content">

                  <div className="timeline-content-header">

                    <div>

                      <span className="timeline-type">
                        {event.type}
                      </span>

                      <h3>
                        {event.title}
                      </h3>

                    </div>

                    <span
                      className={`timeline-status ${
                        event.status === "Critical"
                          ? "critical"
                          : event.status === "Current"
                            ? "current"
                            : "completed"
                      }`}
                    >
                      {event.status}
                    </span>

                  </div>


                  <p className="timeline-description">
                    {event.description}
                  </p>


                  <div className="timeline-hospital">
                    🏥 {event.hospital}
                  </div>


                  <div className="timeline-details">

                    {event.details.map((detail) => (

                      <div
                        className="timeline-detail"
                        key={detail}
                      >
                        <span>✓</span>
                        {detail}
                      </div>

                    ))}

                  </div>

                </div>

              </div>

            ))}

          </div>

        </section>


        {/* CRITICAL INFORMATION */}

        <section className="timeline-critical-card">

          <div className="critical-card-icon">
            ⚠️
          </div>

          <div className="critical-card-content">

            <div className="critical-card-label">
              CRITICAL MEDICAL INFORMATION
            </div>

            <h2>
              Severe Penicillin Allergy
            </h2>

            <p>
              Reaction recorded as <strong>anaphylaxis</strong>.
              This information should be considered during emergency care.
            </p>

          </div>

          <div className="critical-card-badge">
            SEVERE
          </div>

        </section>


        {/* FOOTER INFORMATION */}

        <div className="timeline-footer">

          <span>
            🔐 Your medical information is protected
          </span>

          <span>
            •
          </span>

          <span>
            Only authorized healthcare workflows can modify records.
          </span>

        </div>

      </div>
    </DashboardLayout>
  )
}

export default PatientTimeline