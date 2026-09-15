import { useState } from "react"
import DashboardLayout from "../layouts/DashboardLayout.jsx"

function PatientDocuments() {
  const [showUploadMessage, setShowUploadMessage] = useState(false)

  const documents = [
    {
      id: 1,
      name: "Allergy_Records_2019.pdf",
      type: "Allergy Record",
      date: "18 Nov 2019",
      size: "1.2 MB",
      status: "Available",
      icon: "⚠️",
    },
    {
      id: 2,
      name: "Pneumonia_Hospitalization_2024.pdf",
      type: "Hospital Record",
      date: "06 Aug 2024",
      size: "2.8 MB",
      status: "Available",
      icon: "🏥",
    },
    {
      id: 3,
      name: "Emergency_Report_2026.pdf",
      type: "Emergency Record",
      date: "15 Sep 2026",
      size: "1.7 MB",
      status: "Available",
      icon: "🚨",
    },
  ]

  const handleUpload = () => {
    setShowUploadMessage(true)

    setTimeout(() => {
      setShowUploadMessage(false)
    }, 3000)
  }

  return (
    <DashboardLayout
      role="patient"
      userName="Kabir Malhotra"
    >
      <div className="documents-page">

        {/* PAGE HEADER */}

        <div className="dashboard-page-header">

          <div>
            <div className="page-eyebrow">
              MEDICAL RECORDS
            </div>

            <h1>
              Medical Documents
            </h1>

            <p>
              View the medical documents associated with your health passport.
            </p>
          </div>

          <button
            type="button"
            className="primary-action-button"
            onClick={handleUpload}
          >
            + Add Document
          </button>

        </div>


        {/* UPLOAD MESSAGE */}

        {showUploadMessage && (
          <div className="document-message">
            <span>ℹ️</span>

            <div>
              <strong>
                Document upload will be connected to the backend later.
              </strong>

              <p>
                The frontend upload interface is ready for integration.
              </p>
            </div>
          </div>
        )}


        {/* DOCUMENT SUMMARY */}

        <div className="stats-grid">

          <div className="stat-card">

            <div className="stat-icon">
              📄
            </div>

            <div>
              <span>Total Documents</span>
              <strong>{documents.length}</strong>
            </div>

          </div>


          <div className="stat-card">

            <div className="stat-icon">
              🗂️
            </div>

            <div>
              <span>Medical Records</span>
              <strong>3</strong>
            </div>

          </div>


          <div className="stat-card">

            <div className="stat-icon">
              🔐
            </div>

            <div>
              <span>Secure Storage</span>
              <strong>Active</strong>
            </div>

          </div>

        </div>


        {/* DOCUMENT LIST */}

        <section className="dashboard-panel">

          <div className="panel-header">

            <div>
              <h2>
                Your Documents
              </h2>

              <p>
                Medical records associated with your Medi-Trace passport.
              </p>
            </div>

          </div>


          <div className="document-list">

            {documents.map((document) => (

              <div
                className="document-card"
                key={document.id}
              >

                <div className="document-icon">
                  {document.icon}
                </div>


                <div className="document-information">

                  <h3>
                    {document.name}
                  </h3>

                  <p>
                    {document.type}
                  </p>

                  <div className="document-meta">

                    <span>
                      📅 {document.date}
                    </span>

                    <span>
                      •
                    </span>

                    <span>
                      {document.size}
                    </span>

                  </div>

                </div>


                <div className="document-status">

                  <span className="document-status-badge">
                    ✓ {document.status}
                  </span>

                  <button
                    type="button"
                    className="document-view-button"
                    onClick={() =>
                      alert(
                        "Document preview will be connected to the backend later."
                      )
                    }
                  >
                    View
                  </button>

                </div>

              </div>

            ))}

          </div>

        </section>


        {/* DOCUMENT WORKFLOW */}

        <section className="dashboard-panel">

          <div className="panel-header">

            <div>
              <h2>
                How Medi-Trace handles documents
              </h2>

              <p>
                Documents can support the creation and review of your health
                passport.
              </p>
            </div>

          </div>


          <div className="document-workflow">

            <div className="workflow-step">

              <div className="workflow-number">
                1
              </div>

              <div>
                <h3>
                  Document Upload
                </h3>

                <p>
                  A medical document is securely submitted to Medi-Trace.
                </p>
              </div>

            </div>


            <div className="workflow-arrow">
              →
            </div>


            <div className="workflow-step">

              <div className="workflow-number">
                2
              </div>

              <div>
                <h3>
                  Processing
                </h3>

                <p>
                  OCR and medical language processing extract useful
                  information.
                </p>
              </div>

            </div>


            <div className="workflow-arrow">
              →
            </div>


            <div className="workflow-step">

              <div className="workflow-number">
                3
              </div>

              <div>
                <h3>
                  Doctor Review
                </h3>

                <p>
                  Extracted findings are reviewed before becoming authoritative
                  medical information.
                </p>
              </div>

            </div>

          </div>

        </section>


        {/* SECURITY INFORMATION */}

        <div className="document-security">

          <div className="document-security-icon">
            🔒
          </div>

          <div>
            <strong>
              Your documents remain protected
            </strong>

            <p>
              Access to medical documents follows the authorization and
              emergency-access rules of Medi-Trace.
            </p>
          </div>

        </div>

      </div>
    </DashboardLayout>
  )
}

export default PatientDocuments