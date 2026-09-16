import DashboardLayout from "../layouts/DashboardLayout.jsx"
import { api } from "../services/api"
import { useApiQuery } from "../hooks/useApiQuery"
import { ErrorState, LoadingState } from "../components/AsyncState"

function PatientTimeline() {
  const { data: summary, loading, error, refresh } = useApiQuery(api.patientMe, [])
  const events = summary?.medical_events?.map((event) => ({
    year: event.event_date ? new Date(event.event_date).getFullYear() : "—",
    date: event.event_date ? new Date(event.event_date).toLocaleDateString() : "Date not recorded",
    title: event.title,
    type: event.event_type || "Medical event",
    icon: event.is_critical ? "!" : "+",
    hospital: event.doctor_name || "MediTrace record",
    description: event.description || "No additional description recorded.",
    details: [event.severity && `Severity: ${event.severity}`, event.status && `Status: ${event.status}`].filter(Boolean),
    status: event.status || "Recorded",
    tone: event.is_critical ? "critical" : "completed",
  })) || []
  /* Demo timeline retained below as a visual reference only; backend data is displayed. */
  /*
    {
      year: "2019",
      date: "18 Nov 2019",
      title: "Severe Penicillin Allergy Identified",
      type: "Allergy",
      icon: "!",
      hospital: "Apollo Hospitals, Chennai",
      description:
        "A severe allergic reaction to Penicillin was documented, with the reaction recorded as anaphylaxis.",
      details: [
        "Allergen: Penicillin",
        "Severity: Severe",
        "Reaction: Anaphylaxis",
      ],
      status: "Critical",
      tone: "critical",
    },
    {
      year: "2024",
      date: "06 Aug 2024",
      title: "Bacterial Pneumonia Hospitalization",
      type: "Hospitalization",
      icon: "+",
      hospital: "Apollo Hospitals, Chennai",
      description:
        "Hospital admission for bacterial pneumonia with treatment and clinical monitoring.",
      details: [
        "Diagnosis: Bacterial pneumonia",
        "Hospital admission recorded",
        "Treatment and follow-up documented",
      ],
      status: "Completed",
      tone: "completed",
    },
    {
      year: "2026",
      date: "15 Sep 2026",
      title: "Emergency Presentation",
      type: "Emergency",
      icon: "!",
      hospital: "Emergency Department",
      description:
        "Emergency evaluation initiated. Critical allergy information is available through the Emergency Health Passport.",
      details: [
        "Emergency workflow initiated",
        "Critical allergy information available",
        "Emergency access requires authorization",
      ],
      status: "Current",
      tone: "current",
    },
  ] */

  return (
    <DashboardLayout
      role="patient"
      userName="Kabir Malhotra"
    >
      <div className="patient-timeline-page">
        {loading && <LoadingState label="Loading your medical timeline…" />}
        {error && <ErrorState error={error} onRetry={refresh} />}

        {/* =====================================================
            PAGE HEADER
        ====================================================== */}

        <section className="patient-timeline-header">

          <div>
            <span className="timeline-page-kicker">
              MEDICAL HISTORY
            </span>

            <h1>
              Medical Timeline
            </h1>

            <p>
              A chronological view of your documented medical history.
            </p>
          </div>

          <div className="timeline-header-summary">

            <div className="timeline-summary-number">
              {events.length}
            </div>

            <div>
              <span>
                DOCUMENTED
              </span>

              <strong>
                Medical Events
              </strong>
            </div>

          </div>

        </section>


        {/* =====================================================
            INFORMATION NOTICE
        ====================================================== */}

        <section className="patient-timeline-notice">

          <div className="timeline-notice-icon">
            i
          </div>

          <div>
            <strong>
              Your medical history
            </strong>

            <p>
              This timeline presents structured medical information
              recorded in your Medi-Trace health passport.
            </p>
          </div>

        </section>


        {/* =====================================================
            TIMELINE PANEL
        ====================================================== */}

        <section className="patient-timeline-panel">

          <div className="patient-timeline-panel-header">

            <div>
              <span>
                HEALTH HISTORY
              </span>

              <h2>
                Medical Events
              </h2>

              <p>
                Chronological history of documented events.
              </p>
            </div>

            <div className="timeline-event-count">
              {events.length} EVENTS
            </div>

          </div>


          {/* =================================================
              TIMELINE
          ================================================== */}

          <div className="patient-medical-timeline">

            {events.map((event, index) => (

              <article
                className={`patient-timeline-event ${event.tone}`}
                key={event.date}
              >

                {/* DATE */}

                <div className="patient-timeline-date">

                  <strong>
                    {event.year}
                  </strong>

                  <span>
                    {event.date}
                  </span>

                </div>


                {/* MARKER */}

                <div className="patient-timeline-track">

                  <div className="patient-timeline-marker">
                    {event.icon}
                  </div>

                  {index !== events.length - 1 && (
                    <div className="patient-timeline-line"></div>
                  )}

                </div>


                {/* EVENT CARD */}

                <div className="patient-timeline-card">

                  <div className="patient-timeline-card-top">

                    <div className="patient-timeline-card-title">

                      <span className="patient-event-category">
                        {event.type}
                      </span>

                      <h3>
                        {event.title}
                      </h3>

                    </div>

                    <span
                      className={`patient-event-status ${event.tone}`}
                    >
                      {event.status}
                    </span>

                  </div>


                  <p className="patient-event-description">
                    {event.description}
                  </p>


                  <div className="patient-event-location">
                    <span className="location-icon">
                      +
                    </span>

                    {event.hospital}
                  </div>


                  <div className="patient-event-details">

                    {event.details.map((detail) => (

                      <div
                        className="patient-event-detail"
                        key={detail}
                      >
                        <span>
                          ✓
                        </span>

                        {detail}
                      </div>

                    ))}

                  </div>

                </div>

              </article>

            ))}

          </div>

        </section>


        {/* =====================================================
            CRITICAL INFORMATION
        ====================================================== */}

        <section className="patient-timeline-critical">

          <div className="timeline-critical-icon">
            !
          </div>

          <div className="timeline-critical-content">

            <span>
              CRITICAL MEDICAL INFORMATION
            </span>

            <h2>
              Severe Penicillin Allergy
            </h2>

            <p>
              Reaction recorded as{" "}
              <strong>
                anaphylaxis
              </strong>
              . This information should be considered during
              emergency care.
            </p>

          </div>

          <div className="timeline-critical-badge">
            SEVERE
          </div>

        </section>


        {/* =====================================================
            EMERGENCY PASSPORT CTA
        ====================================================== */}

        <section className="timeline-passport-cta">

          <div className="timeline-passport-icon">
            +
          </div>

          <div>
            <span>
              EMERGENCY READY
            </span>

            <h2>
              Need your critical information quickly?
            </h2>

            <p>
              Open your Emergency Health Passport for a
              concise view of essential medical information.
            </p>
          </div>

          <a
            href="/patient/passport"
            className="timeline-passport-button"
          >
            Open Passport
            <span>→</span>
          </a>

        </section>


        {/* =====================================================
            FOOTER NOTE
        ====================================================== */}

        <div className="patient-timeline-footer">

          <span>
            🔐 Your medical information is protected
          </span>

          <span>
            Medi-Trace • Only authorized healthcare workflows
            can modify records.
          </span>

        </div>

      </div>
    </DashboardLayout>
  )
}

export default PatientTimeline
