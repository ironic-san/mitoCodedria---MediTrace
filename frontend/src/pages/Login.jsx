import { Link, useNavigate } from "react-router-dom"
import { useState } from "react"
import { api, readableError, session } from "../services/api"

function Login() {
  const navigate = useNavigate()

  const [role, setRole] = useState("patient")
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [error, setError] = useState("")

  const [submitting, setSubmitting] = useState(false)
  const handleLogin = async (event) => {
    event.preventDefault()

    setError("")

    setSubmitting(true)
    try {
      const login = await api.login(email, password)
      session.set(login)
      const user = await api.me()
      if (user.role !== role.toUpperCase()) throw new Error(`This account is registered as a ${user.role.toLowerCase()}. Choose the matching sign-in role.`)
      session.set({ ...login, user })
      navigate(user.role === "DOCTOR" ? "/doctor/dashboard" : "/patient/dashboard", { replace: true })
    } catch (requestError) {
      session.clear()
      setError(readableError(requestError))
    } finally { setSubmitting(false) }
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
                {submitting ? "Signing in…" : "Sign In"}
              </button>

            </form>




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
