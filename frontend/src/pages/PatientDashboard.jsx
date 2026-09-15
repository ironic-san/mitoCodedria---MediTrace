import { Link } from "react-router-dom"
import DashboardLayout from "../layouts/DashboardLayout.jsx"

function PatientDashboard() {
  return (
    <DashboardLayout
      role="patient"
      userName="Kabir Malhotra"
    >
      <div className="patient-dashboard">

        {/* =====================================================
            PAGE HEADER
        ====================================================== */}

        <section className="patient-welcome-section">
          <div className="patient-welcome-content">
            <div className="page-eyebrow">
              PATIENT DASHBOARD
            </div>

            <h1>
              Good afternoon, Kabir
            </h1>

            <p>
              Your essential health information is organized,
              accessible, and ready when you need it.
            </p>
          </div>

          <Link
            to="/patient/passport"
            className="patient-primary-button"
          >
            <span>View Emergency Passport</span>
            <span className="button-arrow">→</span>
          </Link>
        </section>


        {/* =====================================================
            CRITICAL MEDICAL ALERT
        ====================================================== */}

        <section className="patient-critical-alert">

          <div className="patient-critical-icon">
            !
          </div>

          <div className="patient-critical-content">

            <div className="patient-alert-label">
              CRITICAL MEDICAL ALERT
            </div>

            <h2>
              Severe Penicillin Allergy
            </h2>

            <p>
              A severe Penicillin allergy is recorded in your
              medical history and should be communicated to
              healthcare professionals during treatment.
            </p>

          </div>

          <Link
            to="/patient/passport"
            className="patient-alert-button"
          >
            View Details
            <span>→</span>
          </Link>

        </section>


        {/* =====================================================
            HEALTH SNAPSHOT
        ====================================================== */}

        <section className="patient-health-section">

          <div className="patient-section-heading">
            <div>
              <span className="section-kicker">
                HEALTH SNAPSHOT
              </span>

              <h2>
                Your essential information
              </h2>
            </div>

            <Link to="/patient/passport">
              View Passport →
            </Link>
          </div>


          <div className="patient-health-grid">

            {/* Blood Group */}
            <div className="patient-health-card">

              <div className="patient-health-card-top">
                <div className="patient-health-icon blood">
                  +
                </div>

                <span className="patient-health-status">
                  Recorded
                </span>
              </div>

              <div className="patient-health-label">
                BLOOD GROUP
              </div>

              <div className="patient-health-value">
                O−
              </div>

              <p>
                Registered blood type
              </p>

            </div>


            {/* Allergies */}
            <div className="patient-health-card critical">

              <div className="patient-health-card-top">
                <div className="patient-health-icon allergy">
                  !
                </div>

                <span className="patient-health-status warning">
                  Critical
                </span>
              </div>

              <div className="patient-health-label">
                ALLERGIES
              </div>

              <div className="patient-health-value">
                1
              </div>

              <p>
                Critical allergy recorded
              </p>

            </div>


            {/* Medications */}
            <div className="patient-health-card">

              <div className="patient-health-card-top">
                <div className="patient-health-icon medication">
                  +
                </div>

                <span className="patient-health-status">
                  Current
                </span>
              </div>

              <div className="patient-health-label">
                ACTIVE MEDICATIONS
              </div>

              <div className="patient-health-value">
                2
              </div>

              <p>
                Current medications
              </p>

            </div>


            {/* Medical Events */}
            <div className="patient-health-card">

              <div className="patient-health-card-top">
                <div className="patient-health-icon events">
                  ◷
                </div>

                <span className="patient-health-status">
                  Updated
                </span>
              </div>

              <div className="patient-health-label">
                MEDICAL EVENTS
              </div>

              <div className="patient-health-value">
                4
              </div>

              <p>
                Recorded medical events
              </p>

            </div>

          </div>

        </section>


        {/* =====================================================
            MAIN CONTENT GRID
        ====================================================== */}

        <div className="patient-dashboard-grid">


          {/* =================================================
              RECENT MEDICAL HISTORY
          ================================================== */}

          <section className="patient-panel patient-history-panel">

            <div className="patient-panel-header">

              <div>
                <span className="section-kicker">
                  MEDICAL HISTORY
                </span>

                <h2>
                  Recent medical events
                </h2>

                <p>
                  Your latest recorded health activity
                </p>
              </div>

              <Link to="/patient/timeline">
                View Timeline →
              </Link>

            </div>


            <div className="patient-events-list">

              {/* Event 1 */}

              <div className="patient-event">

                <div className="patient-event-date">
                  <strong>18</strong>
                  <span>JUN</span>
                </div>

                <div className="patient-event-marker">
                  <span></span>
                </div>

                <div className="patient-event-content">

                  <div className="patient-event-meta">
                    <span className="patient-event-type allergy">
                      ALLERGY
                    </span>

                    <span className="patient-event-verified">
                      ✓ Verified
                    </span>
                  </div>

                  <h3>
                    Severe Penicillin Allergy Recorded
                  </h3>

                  <p>
                    Marked as a critical allergy with
                    potential life-threatening reaction.
                  </p>

                </div>

              </div>


              {/* Event 2 */}

              <div className="patient-event">

                <div className="patient-event-date">
                  <strong>04</strong>
                  <span>MAY</span>
                </div>

                <div className="patient-event-marker">
                  <span></span>
                </div>

                <div className="patient-event-content">

                  <div className="patient-event-meta">
                    <span className="patient-event-type">
                      CONSULTATION
                    </span>

                    <span className="patient-event-verified">
                      ✓ Verified
                    </span>
                  </div>

                  <h3>
                    General Medical Consultation
                  </h3>

                  <p>
                    Routine clinical assessment and
                    medication review.
                  </p>

                </div>

              </div>


              {/* Event 3 */}

              <div className="patient-event">

                <div className="patient-event-date">
                  <strong>12</strong>
                  <span>FEB</span>
                </div>

                <div className="patient-event-marker">
                  <span></span>
                </div>

                <div className="patient-event-content">

                  <div className="patient-event-meta">
                    <span className="patient-event-type medication">
                      MEDICATION
                    </span>

                    <span className="patient-event-verified">
                      ✓ Verified
                    </span>
                  </div>

                  <h3>
                    Medication Updated
                  </h3>

                  <p>
                    Active medication list updated after
                    clinical review.
                  </p>

                </div>

              </div>

            </div>


            <Link
              to="/patient/timeline"
              className="patient-history-footer"
            >
              <span>
                View complete medical timeline
              </span>

              <span>→</span>
            </Link>

          </section>


          {/* =================================================
              RIGHT COLUMN
          ================================================== */}

          <aside className="patient-dashboard-side">


            {/* =============================================
                HEALTH PASSPORT CARD
            ============================================== */}

            <section className="patient-panel passport-preview">

              <div className="passport-preview-top">

                <div className="passport-card-icon">
                  +
                </div>

                <div>
                  <span className="section-kicker">
                    EMERGENCY READY
                  </span>

                  <h2>
                    Health Passport
                  </h2>
                </div>

              </div>

              <p>
                Your critical medical information is
                organized in one place for authorized
                healthcare professionals.
              </p>


              <div className="passport-mini-info">

                <div>
                  <span>
                    BLOOD GROUP
                  </span>

                  <strong>
                    O−
                  </strong>
                </div>

                <div>
                  <span>
                    ALLERGY
                  </span>

                  <strong>
                    Penicillin
                  </strong>
                </div>

              </div>


              <Link
                to="/patient/passport"
                className="passport-view-button"
              >
                Open Emergency Passport
                <span>→</span>
              </Link>

            </section>


            {/* =============================================
                ACCESS STATUS
            ============================================== */}

            <section className="patient-panel access-preview">

              <div className="patient-panel-header compact">

                <div>
                  <span className="section-kicker">
                    ACCESS CONTROL
                  </span>

                  <h2>
                    Doctor access
                  </h2>
                </div>

                <Link to="/patient/access">
                  Manage
                </Link>

              </div>


              <div className="access-status-row">

                <div className="access-status-icon">
                  ✓
                </div>

                <div>
                  <strong>
                    Access permissions
                  </strong>

                  <p>
                    Control who can access your
                    medical information.
                  </p>
                </div>

              </div>


              <Link
                to="/patient/access-history"
                className="access-history-link"
              >
                View access history
                <span>→</span>
              </Link>

            </section>


            {/* =============================================
                DOCUMENTS
            ============================================== */}

            <section className="patient-panel documents-preview">

              <div className="patient-panel-header compact">

                <div>
                  <span className="section-kicker">
                    DOCUMENTS
                  </span>

                  <h2>
                    Medical documents
                  </h2>
                </div>

                <Link to="/patient/documents">
                  View All
                </Link>

              </div>


              <div className="document-preview-item">

                <div className="document-icon">
                  ▤
                </div>

                <div>
                  <strong>
                    Medical Records
                  </strong>

                  <span>
                    Stored health documents
                  </span>
                </div>

                <span className="document-arrow">
                  →
                </span>

              </div>

            </section>

          </aside>

        </div>


        {/* =====================================================
            TRANSPARENCY / EMERGENCY SECTION
        ====================================================== */}

        <section className="patient-emergency-section">

          <div className="patient-emergency-symbol">
            !
          </div>

          <div className="patient-emergency-content">

            <span>
              EMERGENCY ACCESS
            </span>

            <h2>
              Your critical health information is ready.
            </h2>

            <p>
              Authorized healthcare professionals can
              quickly access essential information during
              an emergency, subject to the access controls
              you've configured.
            </p>

          </div>

          <Link
            to="/patient/passport"
            className="patient-emergency-button"
          >
            View Emergency Passport
            <span>→</span>
          </Link>

        </section>


        {/* =====================================================
            PRIVACY / TRANSPARENCY NOTE
        ====================================================== */}

        <div className="patient-privacy-note">

          <div className="privacy-note-icon">
            🔐
          </div>

          <div>
            <strong>
              You control your medical access
            </strong>

            <p>
              Review doctor access permissions and see
              when your medical information has been accessed
              from the Access Control and Access History
              sections.
            </p>
          </div>

          <Link to="/patient/access">
            Manage Access →
          </Link>

        </div>

      </div>
    </DashboardLayout>
  )
}

export default PatientDashboard