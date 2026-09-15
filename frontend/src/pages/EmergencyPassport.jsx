import { Link } from "react-router-dom"
import DashboardLayout from "../layouts/DashboardLayout.jsx"

function EmergencyPassport() {
  return (
    <DashboardLayout
      role="patient"
      userName="Kabir Malhotra"
    >
      <div className="patient-passport-page">

        {/* =====================================================
            PAGE HEADER
        ====================================================== */}

        <section className="patient-passport-header">

          <div>
            <span className="passport-page-kicker">
              EMERGENCY HEALTH PASSPORT
            </span>

            <h1>
              Kabir's Medical Passport
            </h1>

            <p>
              Essential medical information organized for
              rapid access during an emergency.
            </p>
          </div>

          <div className="patient-passport-actions">

            <button
              type="button"
              className="patient-passport-print"
              onClick={() => window.print()}
            >
              <span>▣</span>
              Print Passport
            </button>

            <Link
              to="/patient/dashboard"
              className="patient-passport-back"
            >
              ← Dashboard
            </Link>

          </div>

        </section>


        {/* =====================================================
            EMERGENCY STATUS
        ====================================================== */}

        <section className="passport-ready-banner">

          <div className="passport-ready-icon">
            ✓
          </div>

          <div className="passport-ready-content">

            <span>
              EMERGENCY READY
            </span>

            <h2>
              Your critical information is organized
            </h2>

            <p>
              Essential health information can be quickly
              reviewed by authorized healthcare professionals.
            </p>

          </div>

          <div className="passport-ready-badge">
            READY
          </div>

        </section>


        {/* =====================================================
            PATIENT IDENTITY
        ====================================================== */}

        <section className="passport-identity">

          <div className="passport-avatar-large">
            KM
          </div>

          <div className="passport-patient-details">

            <span className="passport-label">
              PATIENT
            </span>

            <h2>
              Kabir Malhotra
            </h2>

            <p>
              Male <span>•</span> 52 years old
            </p>

            <div className="passport-patient-id">
              Patient ID: MT-KM-0005
            </div>

          </div>


          <div className="passport-blood-group">

            <span>
              BLOOD GROUP
            </span>

            <strong>
              O−
            </strong>

            <small>
              Registered
            </small>

          </div>


          <div className="passport-emergency-status">
            <span></span>
            Emergency Ready
          </div>

        </section>


        {/* =====================================================
            CRITICAL INFORMATION
        ====================================================== */}

        <section className="passport-critical-block">

          <div className="passport-block-heading">

            <div className="passport-heading-icon critical">
              !
            </div>

            <div>
              <span>
                CRITICAL INFORMATION
              </span>

              <h2>
                Allergies
              </h2>
            </div>

          </div>


          <div className="passport-allergy-card">

            <div className="passport-allergy-icon">
              !
            </div>

            <div className="passport-allergy-main">

              <span>
                SEVERE ALLERGY
              </span>

              <h3>
                Penicillin
              </h3>

              <p>
                Severe allergic reaction with potential
                life-threatening consequences.
              </p>

            </div>

            <div className="passport-severity">

              <span>
                SEVERITY
              </span>

              <strong>
                CRITICAL
              </strong>

            </div>

          </div>

        </section>


        {/* =====================================================
            MEDICAL INFORMATION
        ====================================================== */}

        <div className="passport-information-grid">


          {/* CONDITIONS */}

          <section className="passport-info-panel">

            <div className="passport-info-header">

              <div className="passport-info-icon blue">
                +
              </div>

              <div>
                <h2>
                  Medical Conditions
                </h2>

                <span>
                  Current conditions
                </span>
              </div>

            </div>


            <div className="passport-info-content">

              <div className="passport-empty-state">

                <div className="passport-check">
                  ✓
                </div>

                <div>
                  <strong>
                    No major conditions recorded
                  </strong>

                  <p>
                    No active critical conditions are
                    currently listed.
                  </p>
                </div>

              </div>

            </div>

          </section>


          {/* MEDICATIONS */}

          <section className="passport-info-panel">

            <div className="passport-info-header">

              <div className="passport-info-icon green">
                +
              </div>

              <div>
                <h2>
                  Current Medications
                </h2>

                <span>
                  Active medication information
                </span>
              </div>

            </div>


            <div className="passport-info-content">

              <div className="passport-empty-state">

                <div className="passport-info-symbol">
                  i
                </div>

                <div>
                  <strong>
                    No medication information specified
                  </strong>

                  <p>
                    The current demo dataset does not
                    specify medications for this patient.
                  </p>
                </div>

              </div>

            </div>

          </section>


          {/* CARDIAC HISTORY */}

          <section className="passport-info-panel">

            <div className="passport-info-header">

              <div className="passport-info-icon red">
                ♥
              </div>

              <div>
                <h2>
                  Cardiac History
                </h2>

                <span>
                  Major cardiac events
                </span>
              </div>

            </div>


            <div className="passport-info-content">

              <div className="passport-empty-state">

                <div className="passport-check">
                  ✓
                </div>

                <div>
                  <strong>
                    No major cardiac events
                  </strong>

                  <p>
                    No major cardiac events are currently
                    recorded in available history.
                  </p>
                </div>

              </div>

            </div>

          </section>


          {/* SURGERIES */}

          <section className="passport-info-panel">

            <div className="passport-info-header">

              <div className="passport-info-icon purple">
                +
              </div>

              <div>
                <h2>
                  Major Surgeries
                </h2>

                <span>
                  Surgical history
                </span>
              </div>

            </div>


            <div className="passport-info-content">

              <div className="passport-empty-state">

                <div className="passport-check">
                  ✓
                </div>

                <div>
                  <strong>
                    No major surgeries recorded
                  </strong>

                  <p>
                    No major surgical procedures are
                    currently listed.
                  </p>
                </div>

              </div>

            </div>

          </section>


          {/* MEDICAL DEVICES */}

          <section className="passport-info-panel">

            <div className="passport-info-header">

              <div className="passport-info-icon orange">
                ⚙
              </div>

              <div>
                <h2>
                  Medical Devices
                </h2>

                <span>
                  Implanted or critical devices
                </span>
              </div>

            </div>


            <div className="passport-info-content">

              <div className="passport-empty-state">

                <div className="passport-check">
                  ✓
                </div>

                <div>
                  <strong>
                    No medical devices recorded
                  </strong>

                  <p>
                    No implanted medical devices are
                    currently listed.
                  </p>
                </div>

              </div>

            </div>

          </section>


          {/* EMERGENCY CONTACT */}

          <section className="passport-info-panel">

            <div className="passport-info-header">

              <div className="passport-info-icon teal">
                ☎
              </div>

              <div>
                <h2>
                  Emergency Contact
                </h2>

                <span>
                  Contact in case of emergency
                </span>
              </div>

            </div>


            <div className="passport-info-content">

              <div className="passport-contact">

                <div className="passport-contact-avatar">
                  RM
                </div>

                <div className="passport-contact-details">

                  <strong>
                    Riya Malhotra
                  </strong>

                  <span>
                    Emergency Contact
                  </span>

                </div>

                <div className="passport-contact-number">
                  +91 XXXXX XXXXX
                </div>

              </div>

            </div>

          </section>

        </div>


        {/* =====================================================
            MEDICAL TIMELINE CTA
        ====================================================== */}

        <section className="passport-timeline-cta">

          <div className="passport-timeline-icon">
            ◷
          </div>

          <div>

            <span>
              MEDICAL HISTORY
            </span>

            <h2>
              View your complete medical timeline
            </h2>

            <p>
              Review recorded medical events and your
              longitudinal health history.
            </p>

          </div>

          <Link
            to="/patient/timeline"
            className="passport-timeline-button"
          >
            Open Timeline
            <span>→</span>
          </Link>

        </section>


        {/* =====================================================
            ACCESS & PRIVACY
        ====================================================== */}

        <section className="passport-access-section">

          <div className="passport-access-icon">
            🔐
          </div>

          <div className="passport-access-content">

            <span>
              PRIVACY & ACCESS
            </span>

            <h2>
              You control who can access your health information
            </h2>

            <p>
              Review doctor permissions and see access
              activity from your Access Control and
              Access History sections.
            </p>

          </div>

          <div className="passport-access-actions">

            <Link to="/patient/access">
              Manage Access
            </Link>

            <Link to="/patient/access-history">
              View History
            </Link>

          </div>

        </section>


        {/* =====================================================
            FOOTER
        ====================================================== */}

        <footer className="passport-page-footer">

          <span>
            Medi-Trace Emergency Health Passport
          </span>

          <span>
            Patient information • Verify clinically before treatment
          </span>

        </footer>

      </div>
    </DashboardLayout>
  )
}

export default EmergencyPassport