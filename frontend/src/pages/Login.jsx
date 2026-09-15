import { Link, useNavigate } from "react-router-dom"
import { useState } from "react"

function Login() {
  const navigate = useNavigate()

  const [role, setRole] = useState("patient")
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [error, setError] = useState("")

  const handleLogin = (event) => {
    event.preventDefault()

    setError("")

    // Temporary frontend demo authentication

    if (
      role === "patient" &&
      email === "kabir@meditrace.demo" &&
      password === "kabir123"
    ) {
      navigate("/patient/dashboard")
      return
    }

    if (
      role === "doctor" &&
      email === "doctor@meditrace.demo" &&
      password === "doctor123"
    ) {
      navigate("/doctor/dashboard")
      return
    }

    setError(
      "Invalid demo credentials. Please check the email, password, and selected role."
    )
  }

  return (
    <div className="login-page">

      <div className="login-container">

        {/* LEFT SIDE */}

        <div className="login-info">

          <Link to="/" className="login-logo">
            Medi<span>-</span>Trace
          </Link>

          <div className="login-info-content">

            <div className="login-badge">
              🛡️ SECURE HEALTHCARE ACCESS
            </div>

            <h1>
              Your medical history,
              <br />
              <span>when it matters.</span>
            </h1>

            <p>
              Securely access your emergency health passport,
              medical history, and verified critical information.
            </p>

            <div className="login-features">

              <div>
                <span>✓</span>

                <p>
                  <strong>Secure Access</strong>
                  <br />
                  Protected healthcare information
                </p>
              </div>

              <div>
                <span>✓</span>

                <p>
                  <strong>Verified History</strong>
                  <br />
                  Cryptographic integrity protection
                </p>
              </div>

              <div>
                <span>✓</span>

                <p>
                  <strong>Emergency Ready</strong>
                  <br />
                  Critical information at your fingertips
                </p>
              </div>

            </div>

          </div>

          <p className="login-footer-text">
            © 2026 Medi-Trace
          </p>

        </div>


        {/* RIGHT SIDE */}

        <div className="login-form-section">

          <div className="login-card">

            <div className="login-card-header">

              <h2>
                Welcome back
              </h2>

              <p>
                Sign in to access your Medi-Trace account
              </p>

            </div>


            {/* ROLE */}

            <div className="role-selection">

              <label>
                I am a
              </label>

              <div className="role-buttons">

                <button
                  type="button"
                  className={`role-button ${
                    role === "patient" ? "active" : ""
                  }`}
                  onClick={() => {
                    setRole("patient")
                    setError("")
                  }}
                >
                  👤 Patient
                </button>


                <button
                  type="button"
                  className={`role-button ${
                    role === "doctor" ? "active" : ""
                  }`}
                  onClick={() => {
                    setRole("doctor")
                    setError("")
                  }}
                >
                  🩺 Doctor
                </button>

              </div>

            </div>


            {/* LOGIN FORM */}

            <form onSubmit={handleLogin}>

              {/* EMAIL */}

              <div className="form-group">

                <label htmlFor="email">
                  Email Address
                </label>

                <input
                  id="email"
                  type="email"
                  placeholder="Enter your email"
                  value={email}
                  onChange={(event) =>
                    setEmail(event.target.value)
                  }
                  required
                />

              </div>


              {/* PASSWORD */}

              <div className="form-group">

                <div className="password-label">

                  <label htmlFor="password">
                    Password
                  </label>

                  <button
                    type="button"
                    className="forgot-password-button"
                    onClick={() => {
                      setError(
                        "Password recovery will be connected to Supabase later."
                      )
                    }}
                  >
                    Forgot password?
                  </button>

                </div>

                <input
                  id="password"
                  type="password"
                  placeholder="Enter your password"
                  value={password}
                  onChange={(event) =>
                    setPassword(event.target.value)
                  }
                  required
                />

              </div>


              {/* ERROR */}

              {error && (
                <div className="login-error">
                  ⚠ {error}
                </div>
              )}


              {/* SIGN IN */}

              <button
                type="submit"
                className="login-submit"
              >
                Sign In
              </button>

            </form>


            {/* DIVIDER */}

            <div className="login-divider">
              <span>DEMO ACCESS</span>
            </div>


            {/* DEMO CREDENTIALS */}

            <div className="demo-credentials">

              <div className="demo-title">
                🧪 Frontend Demo Accounts
              </div>

              <div className="demo-account">

                <strong>
                  👤 Patient
                </strong>

                <span>
                  kabir@meditrace.demo
                </span>

                <span>
                  Password: kabir123
                </span>

              </div>

              <div className="demo-account">

                <strong>
                  🩺 Doctor
                </strong>

                <span>
                  doctor@meditrace.demo
                </span>

                <span>
                  Password: doctor123
                </span>

              </div>

            </div>


            {/* SIGN UP */}

            <p className="signup-text">

              Don't have an account?

              <button
                type="button"
                className="signup-button"
                onClick={() =>
                  setError(
                    "Account creation will be connected to Supabase later."
                  )
                }
              >
                Create an account
              </button>

            </p>


            {/* SECURITY */}

            <div className="security-note">
              🔒 Your healthcare information is securely protected.
            </div>

          </div>

        </div>

      </div>

    </div>
  )
}

export default Login