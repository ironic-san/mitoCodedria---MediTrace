import { Link } from "react-router-dom"
import DashboardLayout from "../layouts/DashboardLayout.jsx"

function PatientDashboard() {
  return (
    <DashboardLayout
      role="patient"
      userName="Kabir Malhotra"
    >
      <div className="patient-dashboard">

        {/* =========================
            PAGE HEADER
        ========================== */}

        <div className="dashboard-page-header">

          <div>
            <div className="page-eyebrow">
              PATIENT DASHBOARD
            </div>

            <h1>
              Good afternoon, Kabir
            </h1>

            <p>
              Here's your emergency health overview.
            </p>
          </div>

          <Link
            to="/patient/passport"
            className="dashboard-primary-button"
          >
            View Emergency Passport →
          </Link>

        </div>


        {/* =========================
            CRITICAL MEDICAL ALERT
        ========================== */}

        <div className="dashboard-critical-alert">

          <div className="critical-alert-icon">
            !
          </div>

          <div className="critical-alert-content">

            <div className="critical-alert-label">
              CRITICAL MEDICAL ALERT
            </div>

            <h3>
              Severe Penicillin Allergy
            </h3>

            <p>
              This allergy is marked as potentially
              life-threatening and should be clearly
              communicated during emergency treatment.
            </p>

          </div>

          <Link
            to="/patient/passport"
            className="alert-action"
          >
            View Details
          </Link>

        </div>


        {/* =========================
            HEALTH SUMMARY CARDS
        ========================== */}

        <div className="health-summary-grid">

          {/* Blood Group */}

          <div className="health-card">

            <div className="health-card-icon blood-icon">
              🩸
            </div>

            <div className="health-card-label">
              BLOOD GROUP
            </div>

            <div className="health-card-value">
              O−
            </div>

            <div className="health-card-description">
              Registered blood type
            </div>

          </div>


          {/* Allergies */}

          <div className="health-card">

            <div className="health-card-icon allergy-icon">
              ⚠
            </div>

            <div className="health-card-label">
              ALLERGIES
            </div>

            <div className="health-card-value">
              1
            </div>

            <div className="health-card-description">
              Critical allergy recorded
            </div>

          </div>


          {/* Active Medications */}

          <div className="health-card">

            <div className="health-card-icon medication-icon">
              💊
            </div>

            <div className="health-card-label">
              ACTIVE MEDICATIONS
            </div>

            <div className="health-card-value">
              2
            </div>

            <div className="health-card-description">
              Current medications
            </div>

          </div>


          {/* Medical Events */}

          <div className="health-card">

            <div className="health-card-icon event-icon">
              ◷
            </div>

            <div className="health-card-label">
              MEDICAL EVENTS
            </div>

            <div className="health-card-value">
              4
            </div>

            <div className="health-card-description">
              Recorded medical events
            </div>

          </div>

        </div>


        {/* =========================
            MAIN DASHBOARD GRID
        ========================== */}

        <div className="dashboard-main-grid">


          {/* =========================
              RECENT MEDICAL EVENTS
          ========================== */}

          <section className="dashboard-panel">

            <div className="panel-header">

              <div>
                <h2>
                  Recent Medical Events
                </h2>

                <p>
                  Your latest recorded medical history
                </p>
              </div>

              <Link to="/patient/timeline">
                View Timeline →
              </Link>

            </div>


            <div className="medical-events">

              {/* Event 1 */}

              <div className="medical-event">

                <div className="event-date">
                  <strong>
                    18
                  </strong>

                  <span>
                    JUN
                  </span>
                </div>

                <div className="event-line"></div>

                <div className="event-details">

                  <div className="event-type">
                    ALLERGY
                  </div>

                  <h3>
                    Severe Penicillin Allergy Recorded
                  </h3>

                  <p>
                    Marked as a critical allergy with
                    potential life-threatening reaction.
                  </p>

                  <span className="event-verified">
                    ✓ Verified
                  </span>

                </div>

              </div>


              {/* Event 2 */}

              <div className="medical-event">

                <div className="event-date">
                  <strong>
                    04
                  </strong>

                  <span>
                    MAY
                  </span>
                </div>

                <div className="event-line"></div>

                <div className="event-details">

                  <div className="event-type">
                    CONSULTATION
                  </div>

                  <h3>
                    General Medical Consultation
                  </h3>

                  <p>
                    Routine clinical assessment and
                    medication review.
                  </p>

                  <span className="event-verified">
                    ✓ Verified
                  </span>

                </div>

              </div>


              {/* Event 3 */}

              <div className="medical-event">

                <div className="event-date">
                  <strong>
                    12
                  </strong>

                  <span>
                    FEB
                  </span>
                </div>

                <div className="event-line"></div>

                <div className="event-details">

                  <div className="event-type">
                    MEDICATION
                  </div>

                  <h3>
                    Medication Updated
                  </h3>

                  <p>
                    Active medication list updated after
                    clinical review.
                  </p>

                  <span className="event-verified">
                    ✓ Verified
                  </span>

                </div>

              </div>

            </div>

          </section>


          {/* =========================
              RIGHT COLUMN
          ========================== */}

          <div className="dashboard-side-column">


            {/* =========================
                AI EMERGENCY SUMMARY
            ========================== */}

            <section className="dashboard-panel ai-summary-panel">

              <div className="ai-summary-header">

                <div className="ai-icon">
                  ✦
                </div>

                <div>

                  <h2>
                    AI Emergency Summary
                  </h2>

                  <span>
                    Generated from medical history
                  </span>

                </div>

              </div>


              <div className="ai-summary-content">

                <p>
                  <strong>Critical:</strong> Severe
                  Penicillin allergy is documented and
                  should be considered before medication
                  administration.
                </p>

                <p>
                  No major cardiac events are currently
                  recorded in the available history.
                </p>

              </div>


              <Link
                to="/patient/passport"
                className="ai-summary-button"
              >
                View Full Summary →
              </Link>

            </section>


            {/* =========================
                HISTORY INTEGRITY
            ========================== */}

            <section className="dashboard-panel integrity-panel">

              <div className="panel-header">

                <div>

                  <h2>
                    History Integrity
                  </h2>

                  <p>
                    Critical history verification
                  </p>

                </div>

              </div>


              <div className="integrity-status">

                <div className="integrity-check">
                  ✓
                </div>

                <div>

                  <strong>
                    VERIFIED
                  </strong>

                  <p>
                    Critical history matches
                    historical proof.
                  </p>

                </div>

              </div>


              <Link
                to="/patient/passport"
                className="integrity-link"
              >
                View Verification Details →
              </Link>

            </section>


            {/* =========================
                QUICK ACTIONS
            ========================== */}

            <section className="dashboard-panel quick-actions-panel">

              <div className="panel-header">

                <div>

                  <h2>
                    Quick Actions
                  </h2>

                </div>

              </div>


              <div className="quick-actions">

                <Link to="/patient/passport">

                  <span>
                    🪪
                  </span>

                  Emergency Passport

                </Link>


                <Link to="/patient/timeline">

                  <span>
                    ◷
                  </span>

                  Medical Timeline

                </Link>


                <Link to="/patient/documents">

                  <span>
                    ▤
                  </span>

                  Medical Documents

                </Link>

              </div>

            </section>

          </div>

        </div>


        {/* =========================
            EMERGENCY ACCESS
        ========================== */}

        <section className="emergency-dashboard-card">

          <div className="emergency-dashboard-icon">
            🚨
          </div>


          <div className="emergency-dashboard-content">

            <span>
              EMERGENCY ACCESS
            </span>

            <h2>
              Need emergency medical assistance?
            </h2>

            <p>
              Your critical health information is
              organized and ready for authorized
              healthcare professionals.
            </p>

          </div>


          <button
            type="button"
            className="emergency-button"
          >
            Emergency Mode
          </button>

        </section>

      </div>
    </DashboardLayout>
  )
}

export default PatientDashboard