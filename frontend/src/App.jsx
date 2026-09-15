import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom"

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

function App() {
  return (
    <BrowserRouter>
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
          element={<PatientDashboard />}
        />

        <Route
          path="/patient/passport"
          element={<EmergencyPassport />}
        />

        <Route
          path="/patient/timeline"
          element={<PatientTimeline />}
        />

        <Route
          path="/patient/documents"
          element={<PatientDocuments />}
        />

        <Route
          path="/patient/access"
          element={<PatientAccess />}
        />

        <Route
          path="/patient/access-history"
          element={<AccessHistory />}
        />


        {/* =====================================================
            DOCTOR ROUTES
        ===================================================== */}

        <Route
          path="/doctor/dashboard"
          element={<DoctorDashboard />}
        />

        <Route
          path="/doctor/patients"
          element={<DoctorPatients />}
        />

        {/* Doctor Emergency Passport */}

        <Route
          path="/doctor/passport"
          element={
            <Navigate
              to="/doctor/passport/PT-KABIR-005"
              replace
            />
          }
        />

        <Route
          path="/doctor/passport/:id"
          element={<DoctorPassport />}
        />

        {/* Doctor Medical Timeline */}

        <Route
          path="/doctor/timeline"
          element={<DoctorTimeline />}
        />

        {/* Doctor Documents */}

        <Route
          path="/doctor/documents"
          element={<DoctorDocuments />}
        />

        {/* Doctor AI Reviews */}

        <Route
          path="/doctor/ai-reviews"
          element={<DoctorAIReviews />}
        />

        {/* Doctor Integrity */}

        <Route
          path="/doctor/integrity"
          element={<DoctorIntegrity />}
        />

        {/* Doctor Emergency / Break-Glass */}

        <Route
          path="/doctor/emergency"
          element={<DoctorEmergency />}
        />

        {/* Doctor Audit Trail */}

        <Route
          path="/doctor/audit"
          element={<DoctorAudit />}
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
    </BrowserRouter>
  )
}

export default App