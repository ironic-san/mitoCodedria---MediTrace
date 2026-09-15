import { Link } from "react-router-dom"
import DashboardLayout from "../layouts/DashboardLayout.jsx"

function EmergencyPassport() {
  return (
    <DashboardLayout
      role="patient"
      userName="Kabir Malhotra"
    >

      <div className="passport-page">

        {/* =========================
            PAGE HEADER
        ========================== */}

        <div className="passport-page-header">

          <div>
            <div className="page-eyebrow">
              EMERGENCY HEALTH PASSPORT
            </div>

            <h1>
              Kabir's Medical Passport
            </h1>

            <p>
              Critical medical information designed for
              rapid access during emergencies.
            </p>
          </div>


          <div className="passport-header-actions">

            <button
              type="button"
              className="passport-print-button"
            >
              🖨 Print Passport
            </button>

            <Link
              to="/patient/dashboard"
              className="passport-back-button"
            >
              ← Dashboard
            </Link>

          </div>

        </div>


        {/* =========================
            VERIFICATION BANNER
        ========================== */}

        <div className="passport-verification-banner">

          <div className="verification-icon">
            ✓
          </div>

          <div className="verification-content">

            <strong>
              Critical History Verified
            </strong>

            <p>
              Available critical medical history matches
              its historical cryptographic proof.
            </p>

          </div>

          <div className="verification-status">
            VERIFIED
          </div>

        </div>


        {/* =========================
            PATIENT IDENTITY CARD
        ========================== */}

        <section className="passport-identity-card">

          <div className="passport-avatar">
            KM
          </div>

          <div className="passport-identity">

            <div className="identity-label">
              PATIENT
            </div>

            <h2>
              Kabir Malhotra
            </h2>

            <p>
              Male • 52 years old
            </p>

            <div className="identity-id">
              Patient ID: MT-KM-0005
            </div>

          </div>


          <div className="identity-blood">

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


          <div className="identity-status">

            <span className="status-dot"></span>

            Emergency Ready

          </div>

        </section>


        {/* =========================
            CRITICAL ALERT
        ========================== */}

        <section className="passport-critical-section">

          <div className="passport-section-heading">

            <div className="heading-icon critical-heading-icon">
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


          <div className="allergy-card">

            <div className="allergy-warning-icon">
              ⚠
            </div>

            <div className="allergy-information">

              <div className="allergy-label">
                SEVERE ALLERGY
              </div>

              <h3>
                Penicillin
              </h3>

              <p>
                Severe allergic reaction. Potentially
                life-threatening.
              </p>

            </div>

            <div className="allergy-severity">
              <span>
                SEVERITY
              </span>

              <strong>
                CRITICAL
              </strong>
            </div>

          </div>

        </section>


        {/* =========================
            MEDICAL INFORMATION GRID
        ========================== */}

        <div className="passport-info-grid">


          {/* =========================
              CONDITIONS
          ========================== */}

          <section className="passport-info-card">

            <div className="info-card-header">

              <div className="info-card-icon">
                🩺
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


            <div className="info-card-body">

              <div className="condition-item">

                <div className="condition-status">
                  ●
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


          {/* =========================
              MEDICATIONS
          ========================== */}

          <section className="passport-info-card">

            <div className="info-card-header">

              <div className="info-card-icon">
                💊
              </div>

              <div>

                <h2>
                  Current Medications
                </h2>

                <span>
                  Active medications
                </span>

              </div>

            </div>


            <div className="info-card-body">

              <div className="medication-item">

                <div className="medication-number">
                  01
                </div>

                <div>

                  <strong>
                    Metformin
                  </strong>

                  <p>
                    500 mg • Twice daily
                  </p>

                </div>

              </div>


              <div className="medication-item">

                <div className="medication-number">
                  02
                </div>

                <div>

                  <strong>
                    Atorvastatin
                  </strong>

                  <p>
                    20 mg • Once daily
                  </p>

                </div>

              </div>

            </div>

          </section>


          {/* =========================
              CARDIAC HISTORY
          ========================== */}

          <section className="passport-info-card">

            <div className="info-card-header">

              <div className="info-card-icon">
                ❤️
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


            <div className="info-card-body">

              <div className="history-clear">

                <div className="history-check">
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


          {/* =========================
              SURGERIES
          ========================== */}

          <section className="passport-info-card">

            <div className="info-card-header">

              <div className="info-card-icon">
                🏥
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


            <div className="info-card-body">

              <div className="history-clear">

                <div className="history-check">
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


          {/* =========================
              MEDICAL DEVICES
          ========================== */}

          <section className="passport-info-card">

            <div className="info-card-header">

              <div className="info-card-icon">
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


            <div className="info-card-body">

              <div className="history-clear">

                <div className="history-check">
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


          {/* =========================
              EMERGENCY CONTACT
          ========================== */}

          <section className="passport-info-card">

            <div className="info-card-header">

              <div className="info-card-icon">
                📞
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


            <div className="info-card-body">

              <div className="emergency-contact">

                <div className="contact-avatar">
                  RM
                </div>

                <div>

                  <strong>
                    Riya Malhotra
                  </strong>

                  <p>
                    Emergency Contact
                  </p>

                </div>

                <div className="contact-phone">
                  +91 XXXXX XXXXX
                </div>

              </div>

            </div>

          </section>

        </div>


        {/* =========================
            AI SUMMARY
        ========================== */}

        <section className="passport-ai-section">

          <div className="passport-ai-header">

            <div className="passport-ai-icon">
              ✦
            </div>

            <div>

              <span>
                AI MEDICAL INTELLIGENCE
              </span>

              <h2>
                Emergency Summary
              </h2>

            </div>

            <div className="ai-generated-badge">
              AI GENERATED
            </div>

          </div>


          <div className="passport-ai-content">

            <p>

              <strong>
                Critical allergy:
              </strong>{" "}

              Kabir Malhotra has a documented severe
              Penicillin allergy that may result in a
              potentially life-threatening reaction.

            </p>

            <p>

              <strong>
                Current history:
              </strong>{" "}

              Two active medications are recorded.
              No major cardiac events, major surgeries,
              or medical devices are currently listed.

            </p>

            <div className="ai-disclaimer">

              ⚠ AI-generated summary. Healthcare
              professionals must verify information
              clinically before treatment.

            </div>

          </div>

        </section>


        {/* =========================
            BLOCKCHAIN INTEGRITY
        ========================== */}

        <section className="passport-blockchain-section">

          <div className="blockchain-main">

            <div className="blockchain-icon">
              ⛓
            </div>

            <div>

              <span>
                INTEGRITY VERIFICATION
              </span>

              <h2>
                Blockchain Integrity Verified
              </h2>

              <p>
                Critical medical history has a matching
                historical cryptographic proof.
              </p>

            </div>

          </div>


          <div className="blockchain-details">

            <div>

              <span>
                STATUS
              </span>

              <strong className="verified-text">
                ✓ VERIFIED
              </strong>

            </div>

            <div>

              <span>
                HASH ALGORITHM
              </span>

              <strong>
                SHA-256
              </strong>

            </div>

            <div>

              <span>
                PROOF
              </span>

              <strong>
                Historical Match
              </strong>

            </div>

          </div>

        </section>


        {/* =========================
            FOOTNOTE
        ========================== */}

        <div className="passport-footnote">

          <span>
            Last updated: Demo data • 15 September 2026
          </span>

          <span>
            Medi-Trace • Verify clinically before treatment
          </span>

        </div>

      </div>

    </DashboardLayout>
  )
}

export default EmergencyPassport