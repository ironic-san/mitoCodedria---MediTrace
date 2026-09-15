import { useState } from "react"
import DashboardLayout from "../layouts/DashboardLayout.jsx"

function PatientDocuments() {
  const [showUploadMessage, setShowUploadMessage] = useState(false)
  const [selectedDocument, setSelectedDocument] = useState(null)

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
    }, 3500)
  }

  const handleView = (document) => {
    setSelectedDocument(document)
  }

  const closePreview = () => {
    setSelectedDocument(null)
  }

  return (
    <DashboardLayout
      role="patient"
      userName="Kabir Malhotra"
    >
      <div className="documents-page">

        {/* =====================================================
            PAGE HEADER
            ===================================================== */}

        <div className="dashboard-page-header">

          <div>
            <div className="page-eyebrow">
              MEDICAL RECORDS
            </div>

            <h1>
              Medical Documents
            </h1>

            <p>
              View and manage the medical documents associated with your
              Medi-Trace health passport.
            </p>
          </div>

          <button
            type="button"
            className="primary-action-button"
            onClick={handleUpload}
          >
            <span className="button-plus">
              +
            </span>

            Add Document
          </button>

        </div>


        {/* =====================================================
            UPLOAD MESSAGE
            ===================================================== */}

        {showUploadMessage && (

          <div className="document-message">

            <div className="document-message-icon">
              ↑
            </div>

            <div className="document-message-content">

              <strong>
                Document upload interface ready
              </strong>

              <p>
                Backend document storage and processing will be connected
                during integration.
              </p>

            </div>

            <button
              type="button"
              className="message-close"
              onClick={() => setShowUploadMessage(false)}
            >
              ×
            </button>

          </div>

        )}


        {/* =====================================================
            DOCUMENT SUMMARY
            ===================================================== */}

        <div className="document-summary-grid">

          {/* TOTAL DOCUMENTS */}

          <div className="document-summary-card documents-card-blue">

            <div className="document-summary-icon">
              📄
            </div>

            <div className="document-summary-content">

              <span>
                TOTAL DOCUMENTS
              </span>

              <strong>
                {documents.length}
              </strong>

              <p>
                Records in your passport
              </p>

            </div>

          </div>


          {/* MEDICAL RECORDS */}

          <div className="document-summary-card documents-card-green">

            <div className="document-summary-icon">
              🗂️
            </div>

            <div className="document-summary-content">

              <span>
                MEDICAL RECORDS
              </span>

              <strong>
                {documents.length}
              </strong>

              <p>
                Available medical documents
              </p>

            </div>

          </div>


          {/* DOCUMENT ACCESS */}

          <div className="document-summary-card documents-card-purple">

            <div className="document-summary-icon">
              🔐
            </div>

            <div className="document-summary-content">

              <span>
                DOCUMENT ACCESS
              </span>

              <strong>
                Protected
              </strong>

              <p>
                Access follows authorization rules
              </p>

            </div>

          </div>

        </div>


        {/* =====================================================
            YOUR DOCUMENTS
            ===================================================== */}

        <section className="dashboard-panel documents-panel">

          <div className="panel-header">

            <div>

              <div className="section-kicker">
                YOUR RECORDS
              </div>

              <h2>
                Your Documents
              </h2>

              <p>
                Medical records currently associated with your health
                passport.
              </p>

            </div>

            <div className="document-count">
              {documents.length} documents
            </div>

          </div>


          <div className="document-list">

            {documents.map((document) => (

              <div
                className="document-card"
                key={document.id}
              >

                {/* DOCUMENT ICON */}

                <div className="document-icon">
                  {document.icon}
                </div>


                {/* DOCUMENT INFORMATION */}

                <div className="document-information">

                  <h3>
                    {document.name}
                  </h3>

                  <p className="document-type">
                    {document.type}
                  </p>

                  <div className="document-meta">

                    <span>
                      📅 {document.date}
                    </span>

                    <span className="document-meta-divider">
                      •
                    </span>

                    <span>
                      {document.size}
                    </span>

                  </div>

                </div>


                {/* DOCUMENT CONTROLS */}

                <div className="document-status">

                  <span className="document-status-badge">

                    <span className="status-check">
                      ✓
                    </span>

                    {document.status}

                  </span>

                  <button
                    type="button"
                    className="document-view-button"
                    onClick={() => handleView(document)}
                  >
                    View
                  </button>

                </div>

              </div>

            ))}

          </div>

        </section>


        {/* =====================================================
            DOCUMENT PROCESS
            ===================================================== */}

        <section className="dashboard-panel document-process-panel">

          <div className="panel-header">

            <div>

              <div className="section-kicker">
                DOCUMENT PROCESSING
              </div>

              <h2>
                How your documents are handled
              </h2>

              <p>
                Uploaded records can support the review and maintenance
                of your health passport.
              </p>

            </div>

          </div>


          <div className="document-workflow">

            <div className="workflow-step">

              <div className="workflow-number">
                1
              </div>

              <div className="workflow-step-content">

                <span className="workflow-label">
                  INPUT
                </span>

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

              <div className="workflow-step-content">

                <span className="workflow-label">
                  PROCESSING
                </span>

                <h3>
                  Information Extraction
                </h3>

                <p>
                  Document content can be processed to identify useful
                  medical information.
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

              <div className="workflow-step-content">

                <span className="workflow-label">
                  REVIEW
                </span>

                <h3>
                  Doctor Review
                </h3>

                <p>
                  Extracted findings are reviewed before becoming
                  authoritative medical information.
                </p>

              </div>

            </div>

          </div>


          <div className="workflow-note">

            <span className="workflow-note-icon">
              ℹ
            </span>

            <p>
              Information extracted from a document does not automatically
              become part of your authoritative medical record. Doctor
              review is required.
            </p>

          </div>

        </section>


        {/* =====================================================
            SECURITY
            ===================================================== */}

        <div className="document-security">

          <div className="document-security-icon">
            🔒
          </div>

          <div>

            <strong>
              Your documents remain protected
            </strong>

            <p>
              Document access follows the authorization and emergency-access
              rules of Medi-Trace.
            </p>

          </div>

          <div className="security-status">

            <span className="security-dot"></span>

            Protected

          </div>

        </div>


        {/* =====================================================
            DOCUMENT PREVIEW
            ===================================================== */}

        {selectedDocument && (

          <div
            className="document-modal-overlay"
            onClick={closePreview}
          >

            <div
              className="document-modal"
              onClick={(event) =>
                event.stopPropagation()
              }
            >

              <div className="document-modal-header">

                <div className="document-modal-title">

                  <div className="document-modal-icon">
                    {selectedDocument.icon}
                  </div>

                  <div>

                    <span>
                      {selectedDocument.type}
                    </span>

                    <h2>
                      {selectedDocument.name}
                    </h2>

                  </div>

                </div>


                <button
                  type="button"
                  className="modal-close-button"
                  onClick={closePreview}
                >
                  ×
                </button>

              </div>


              <div className="document-preview">

                <div className="preview-paper">

                  <div className="preview-paper-icon">
                    📄
                  </div>

                  <h3>
                    Document Preview
                  </h3>

                  <p>
                    Secure document preview will be connected to backend
                    storage later.
                  </p>

                  <span>
                    {selectedDocument.name}
                  </span>

                </div>

              </div>


              <div className="document-modal-footer">

                <div>

                  <span>
                    Document date
                  </span>

                  <strong>
                    {selectedDocument.date}
                  </strong>

                </div>


                <div>

                  <span>
                    File size
                  </span>

                  <strong>
                    {selectedDocument.size}
                  </strong>

                </div>


                <div>

                  <span>
                    Status
                  </span>

                  <strong className="modal-status">
                    ✓ {selectedDocument.status}
                  </strong>

                </div>

              </div>

            </div>

          </div>

        )}

      </div>
    </DashboardLayout>
  )
}

export default PatientDocuments