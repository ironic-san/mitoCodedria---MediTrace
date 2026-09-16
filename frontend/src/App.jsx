import { BrowserRouter, Routes, Route, Navigate, useLocation } from "react-router-dom"
import { session } from "./services/api"

import Home from "./pages/Home"
import Login from "./pages/Login"

// Patient pages
import PatientDashboard from "./pages/PatientDashboard"
import EmergencyPassport from "./pages/EmergencyPassport.jsx"
import PatientAccess from "./pages/PatientAccess.jsx"
import AccessHistory from "./pages/AccessHistory.jsx"
import PatientTimeline from "./pages/PatientTimeline.jsx"
import PatientDocuments from "./pages/PatientDocuments.jsx"

// Doctor pages
import DoctorDashboard from "./pages/DoctorDashboard.jsx"
import DoctorPatients from "./pages/DoctorPatients.jsx"
import DoctorPassport from "./pages/DoctorPassport.jsx"
import DoctorTimeline from "./pages/DoctorTimeline.jsx"
import DoctorDocuments from "./pages/DoctorDocuments.jsx"
import DoctorAIReviews from "./pages/DoctorAIReviews.jsx"
import DoctorIntegrity from "./pages/DoctorIntegrity.jsx"
import DoctorEmergency from "./pages/DoctorEmergency.jsx"
import DoctorAudit from "./pages/DoctorAudit.jsx"

function AppRoutes() {
  useLocation()
  const activeSession = session.get()
  const role = String(activeSession?.user?.role || "").toUpperCase()
  const patientRoute = (element) => activeSession?.access_token && role === "PATIENT" ? element : <Navigate to="/login" replace />
  const doctorRoute = (element) => activeSession?.access_token && role === "DOCTOR" ? element : <Navigate to="/login" replace />
  return (
      <Routes>

        {/* =====================================================
            PUBLIC ROUTES
        ===================================================== */}

        <Route
          path="/"
          element={<Home />}
        />

        <Route
          path="/login"
          element={<Login />}
        />


        {/* =====================================================
            PATIENT ROUTES
        ===================================================== */}

        <Route
          path="/patient/dashboard"
          element={patientRoute(<PatientDashboard />)}
        />

        <Route
          path="/patient/passport"
          element={patientRoute(<EmergencyPassport />)}
        />

        <Route
          path="/patient/timeline"
          element={patientRoute(<PatientTimeline />)}
        />

        <Route
          path="/patient/documents"
          element={patientRoute(<PatientDocuments />)}
        />

        <Route
          path="/patient/access"
          element={patientRoute(<PatientAccess />)}
        />

        <Route
          path="/patient/access-history"
          element={patientRoute(<AccessHistory />)}
        />


        {/* =====================================================
            DOCTOR ROUTES
        ===================================================== */}

        <Route
          path="/doctor/dashboard"
          element={doctorRoute(<DoctorDashboard />)}
        />

        <Route
          path="/doctor/patients"
          element={doctorRoute(<DoctorPatients />)}
        />

        {/* Doctor Emergency Passport */}

        <Route
          path="/doctor/passport"
          element={
            doctorRoute(<Navigate
              to="/doctor/patients"
              replace
            />)
          }
        />

        <Route
          path="/doctor/passport/:id"
          element={doctorRoute(<DoctorPassport />)}
        />

        {/* Doctor Medical Timeline */}

        <Route
          path="/doctor/timeline"
          element={doctorRoute(<DoctorTimeline />)}
        />

        {/* Doctor Documents */}

        <Route
          path="/doctor/documents"
          element={doctorRoute(<DoctorDocuments />)}
        />

        {/* Doctor AI Reviews */}

        <Route
          path="/doctor/ai-reviews"
          element={doctorRoute(<DoctorAIReviews />)}
        />

        {/* Doctor Integrity */}

        <Route
          path="/doctor/integrity"
          element={doctorRoute(<DoctorIntegrity />)}
        />

        {/* Doctor Emergency / Break-Glass */}

        <Route
          path="/doctor/emergency"
          element={doctorRoute(<DoctorEmergency />)}
        />

        {/* Doctor Audit Trail */}

        <Route
          path="/doctor/audit"
          element={doctorRoute(<DoctorAudit />)}
        />


        {/* =====================================================
            FALLBACK
        ===================================================== */}

        <Route
          path="*"
          element={
            <Navigate
              to="/"
              replace
            />
          }
        />

      </Routes>
  )
}

function App() {
  return <BrowserRouter><AppRoutes /></BrowserRouter>
}

export default App
