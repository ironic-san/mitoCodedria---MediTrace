import { Link } from "react-router-dom"

function Home() {
  return (
    <div className="home-page">

      {/* Navbar */}
      <nav className="navbar">
        <div className="logo">
          Medi<span>-</span>Trace
        </div>

        <div className="nav-links">
          <a href="#features">Features</a>
          <a href="#how-it-works">How It Works</a>
          <a href="#about">About</a>
        </div>

        <div className="nav-buttons">
          <Link to="/login" className="login-btn">
            Login
          </Link>

          <Link to="/login" className="get-started-btn">
            Get Started
          </Link>
        </div>
      </nav>


      {/* Hero Section */}
      <section className="hero">

        <div className="hero-content">
          <div className="hero-badge">
            🛡️ AI + Blockchain Healthcare
          </div>

          <h1>
            Your Medical History.
            <br />
            <span>Ready When It Matters.</span>
          </h1>

          <p>
            Medi-Trace is an AI-powered emergency health passport
            that helps doctors access, understand, and verify critical
            medical history when every second counts.
          </p>

          <div className="hero-buttons">
            <Link to="/login" className="primary-btn">
              Get Started →
            </Link>

            <a href="#how-it-works" className="secondary-btn">
              See How It Works
            </a>
          </div>

          <div className="hero-stats">
            <div>
              <strong>AI</strong>
              <span>Medical Intelligence</span>
            </div>

            <div>
              <strong>✓</strong>
              <span>Verified History</span>
            </div>

            <div>
              <strong>24/7</strong>
              <span>Emergency Ready</span>
            </div>
          </div>
        </div>


        {/* Passport Preview */}
        <div className="passport-wrapper">
          <div className="passport-card">

            <div className="passport-header">
              <div>
                <small>EMERGENCY HEALTH PASSPORT</small>
                <h3>Patient Profile</h3>
              </div>

              <div className="verified-badge">
                ✓ VERIFIED
              </div>
            </div>

            <div className="patient-info">
              <div className="patient-avatar">
                KM
              </div>

              <div>
                <h2>Kabir Malhotra</h2>
                <p>52 years • Male</p>
              </div>

              <div className="blood-group">
                <small>Blood Group</small>
                <strong>O−</strong>
              </div>
            </div>

            <div className="critical-alert">
              <div className="alert-icon">!</div>

              <div>
                <small>CRITICAL ALLERGY</small>
                <strong>Severe Penicillin Allergy</strong>
                <p>Potentially life-threatening</p>
              </div>
            </div>

            <div className="passport-section">
              <div className="section-title">
                Critical Medical History
              </div>

              <div className="history-item">
                <span>❤️</span>
                <div>
                  <strong>Cardiac History</strong>
                  <p>No major cardiac events recorded</p>
                </div>
              </div>

              <div className="history-item">
                <span>💊</span>
                <div>
                  <strong>Current Medications</strong>
                  <p>2 active medications</p>
                </div>
              </div>
            </div>

            <div className="blockchain-status">
              <div className="chain-icon">⛓</div>

              <div>
                <strong>Blockchain Integrity Verified</strong>
                <p>Critical history matches historical proof</p>
              </div>

              <span>✓</span>
            </div>

          </div>
        </div>

      </section>


      {/* Features */}
      <section id="features" className="features-section">

        <div className="section-heading">
          <span>WHY MEDI-TRACE</span>

          <h2>
            Critical information,
            <br />
            exactly when you need it.
          </h2>

          <p>
            We don't just show doctors what's in the record —
            we help identify when something critical may be missing.
          </p>
        </div>

        <div className="features-grid">

          <div className="feature-card">
            <div className="feature-icon">🏥</div>
            <h3>Emergency Passport</h3>
            <p>
              A concise view of allergies, medications, conditions,
              surgeries, devices, and other critical medical history.
            </p>
          </div>

          <div className="feature-card">
            <div className="feature-icon">🧠</div>
            <h3>AI Medical Intelligence</h3>
            <p>
              AI extracts important information from medical documents
              and creates an understandable emergency summary.
            </p>
          </div>

          <div className="feature-card">
            <div className="feature-icon">🔐</div>
            <h3>Verified History</h3>
            <p>
              Critical medical events can be backed by cryptographic
              proofs to help detect missing or inconsistent history.
            </p>
          </div>

          <div className="feature-card">
            <div className="feature-icon">🚨</div>
            <h3>Emergency Access</h3>
            <p>
              Designed for emergency workflows where authorized
              doctors may need rapid access to critical information.
            </p>
          </div>

        </div>

      </section>


      {/* How It Works */}
      <section id="how-it-works" className="how-section">

        <div className="section-heading">
          <span>HOW IT WORKS</span>

          <h2>
            Access → Understand → Verify → Alert
          </h2>
        </div>

        <div className="steps">

          <div className="step">
            <div className="step-number">01</div>
            <h3>Access</h3>
            <p>
              Authorized healthcare professionals access the patient's
              emergency health passport.
            </p>
          </div>

          <div className="step">
            <div className="step-number">02</div>
            <h3>Understand</h3>
            <p>
              AI converts complex medical information into a concise
              emergency-focused summary.
            </p>
          </div>

          <div className="step">
            <div className="step-number">03</div>
            <h3>Verify</h3>
            <p>
              Critical history can be compared against cryptographic
              historical proofs.
            </p>
          </div>

          <div className="step">
            <div className="step-number">04</div>
            <h3>Alert</h3>
            <p>
              Potentially missing or inconsistent critical information
              is highlighted for clinical review.
            </p>
          </div>

        </div>

      </section>


      {/* About */}
      <section id="about" className="about-section">

        <div className="about-content">

          <span>ABOUT MEDI-TRACE</span>

          <h2>
            Making medical history
            <br />
            trustworthy in emergencies.
          </h2>

          <p>
            Medi-Trace combines electronic medical records, AI-powered
            document intelligence, cryptographic integrity verification,
            and emergency access workflows into one healthcare platform.
          </p>

          <p>
            The goal is simple: help healthcare professionals find
            critical information faster and recognize when important
            historical information may be missing or inconsistent.
          </p>

        </div>

      </section>


      {/* Footer */}
      <footer className="footer">

        <div className="footer-logo">
          Medi<span>-</span>Trace
        </div>

        <p>
          AI-Powered Emergency Health Passport
        </p>

        <div className="footer-bottom">
          © 2026 Medi-Trace. Built for safer emergency healthcare.
        </div>

      </footer>

    </div>
  )
}

export default Home