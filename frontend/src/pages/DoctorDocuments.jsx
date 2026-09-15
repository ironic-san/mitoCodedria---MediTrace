import { useRef, useState } from "react"
import DashboardLayout from "../layouts/DashboardLayout"

const patients = [
  {
    id: "PT-AARAV-001",
    name: "Aarav Mehta",
    age: 24,
    gender: "Male",
    bloodGroup: "O+",
    summary: "Road accident with left femur fracture",
  },
  {
    id: "PT-ISHITA-002",
    name: "Ishita Kapoor",
    age: 46,
    gender: "Female",
    bloodGroup: "B+",
    summary: "Type 2 diabetes and hypertension",
  },
  {
    id: "PT-NIKHIL-003",
    name: "Nikhil Varma",
    age: 61,
    gender: "Male",
    bloodGroup: "A+",
    summary: "Previous MI with angioplasty and stent",
  },
  {
    id: "PT-DIYA-004",
    name: "Diya Srinivasan",
    age: 38,
    gender: "Female",
    bloodGroup: "AB+",
    summary: "Osteosarcoma with chemotherapy and surgery",
  },
  {
    id: "PT-KABIR-005",
    name: "Kabir Malhotra",
    age: 52,
    gender: "Male",
    bloodGroup: "O-",
    summary: "Severe Penicillin allergy and pneumonia history",
  },
  {
    id: "PT-TANYA-006",
    name: "Tanya Bose",
    age: 34,
    gender: "Female",
    bloodGroup: "A-",
    summary: "Intracranial lesion with brain surgery",
  },
]

const initialDocuments = {
  "PT-AARAV-001": [
    {
      id: 1,
      name: "Accident_Hospital_Record.pdf",
      type: "Hospital Record",
      date: "2023",
      size: "2.4 MB",
      status: "Processed",
      findings: 3,
    },
    {
      id: 2,
      name: "Femur_Fixation_Report.pdf",
      type: "Procedure Report",
      date: "2023",
      size: "1.8 MB",
      status: "Processed",
      findings: 2,
    },
    {
      id: 3,
      name: "Follow_Up_Report.pdf",
      type: "Follow-up",
      date: "2023",
      size: "1.1 MB",
      status: "Processed",
      findings: 1,
    },
  ],

  "PT-ISHITA-002": [
    {
      id: 4,
      name: "Diabetes_Clinical_Record.pdf",
      type: "Clinical Record",
      date: "Current",
      size: "1.7 MB",
      status: "Processed",
      findings: 3,
    },
    {
      id: 5,
      name: "Hypertension_Record.pdf",
      type: "Clinical Record",
      date: "Current",
      size: "1.3 MB",
      status: "Processed",
      findings: 2,
    },
  ],

  "PT-NIKHIL-003": [
    {
      id: 6,
      name: "MI_Hospitalization_Record.pdf",
      type: "Hospital Record",
      date: "2023",
      size: "3.2 MB",
      status: "Processed",
      findings: 4,
    },
    {
      id: 7,
      name: "Angiography_Report.pdf",
      type: "Investigation",
      date: "2023",
      size: "2.1 MB",
      status: "Processed",
      findings: 2,
    },
    {
      id: 8,
      name: "Angioplasty_Stent_Report.pdf",
      type: "Procedure Report",
      date: "2023",
      size: "2.7 MB",
      status: "Processed",
      findings: 3,
    },
  ],

  "PT-DIYA-004": [
    {
      id: 9,
      name: "Osteosarcoma_Report.pdf",
      type: "Diagnosis",
      date: "Historical",
      size: "2.8 MB",
      status: "Processed",
      findings: 3,
    },
    {
      id: 10,
      name: "Chemotherapy_Record.pdf",
      type: "Treatment",
      date: "Historical",
      size: "3.4 MB",
      status: "Processed",
      findings: 4,
    },
    {
      id: 11,
      name: "Limb_Sparing_Surgery.pdf",
      type: "Procedure Report",
      date: "Historical",
      size: "2.5 MB",
      status: "Processed",
      findings: 2,
    },
  ],

  "PT-KABIR-005": [
    {
      id: 12,
      name: "Penicillin_Allergy_Record.pdf",
      type: "Allergy Record",
      date: "2019",
      size: "1.2 MB",
      status: "Processed",
      findings: 2,
      critical: true,
    },
    {
      id: 13,
      name: "Pneumonia_Hospitalization.pdf",
      type: "Hospital Record",
      date: "2024",
      size: "2.6 MB",
      status: "Processed",
      findings: 2,
    },
    {
      id: 14,
      name: "Emergency_Presentation_2026.pdf",
      type: "Emergency Record",
      date: "2026",
      size: "1.9 MB",
      status: "Processed",
      findings: 2,
      critical: true,
    },
  ],

  "PT-TANYA-006": [
    {
      id: 15,
      name: "Neurological_Evaluation.pdf",
      type: "Clinical Record",
      date: "2024",
      size: "2.0 MB",
      status: "Processed",
      findings: 2,
    },
    {
      id: 16,
      name: "Intracranial_Lesion_Report.pdf",
      type: "Diagnosis",
      date: "2025",
      size: "2.9 MB",
      status: "Processed",
      findings: 3,
    },
    {
      id: 17,
      name: "Brain_Surgery_Report.pdf",
      type: "Procedure Report",
      date: "2025",
      size: "3.1 MB",
      status: "Processed",
      findings: 3,
      conflict: true,
    },
    {
      id: 18,
      name: "2026_Follow_Up.pdf",
      type: "Follow-up",
      date: "2026",
      size: "1.5 MB",
      status: "Processed",
      findings: 1,
    },
  ],
}

function DoctorDocuments() {
  const [selectedPatientId, setSelectedPatientId] =
    useState("PT-KABIR-005")

  const [documents, setDocuments] =
    useState(initialDocuments)

  const [selectedDocument, setSelectedDocument] =
    useState(null)

  const [uploading, setUploading] =
    useState(false)

  const [uploadMessage, setUploadMessage] =
    useState("")

  const fileInputRef = useRef(null)

  const selectedPatient = patients.find(
    (patient) => patient.id === selectedPatientId
  )

  const patientDocuments =
    documents[selectedPatientId] || []

  function handlePatientChange(event) {
    setSelectedPatientId(event.target.value)
    setSelectedDocument(null)
    setUploadMessage("")
  }

  function handleUploadClick() {
    if (fileInputRef.current) {
      fileInputRef.current.click()
    }
  }

  function handleFileChange(event) {
    const file = event.target.files?.[0]

    if (!file) {
      return
    }

    setUploading(true)
    setUploadMessage("")

    // Demo processing simulation.
    // This will later be replaced by the FastAPI upload endpoint.
    setTimeout(() => {
      const newDocument = {
        id: Date.now(),
        name: file.name,
        type: "New Medical Document",
        date: new Date().getFullYear().toString(),
        size: `${(file.size / (1024 * 1024)).toFixed(2)} MB`,
        status: "AI Processing",
        findings: 0,
      }

      setDocuments((current) => ({
        ...current,
        [selectedPatientId]: [
          newDocument,
          ...(current[selectedPatientId] || []),
        ],
      }))

      setUploading(false)
      setUploadMessage(
        "Document uploaded. OCR and AI processing started."
      )

      event.target.value = ""
    }, 1200)
  }

  function simulateReview(document) {
    setDocuments((current) => ({
      ...current,
      [selectedPatientId]: current[selectedPatientId].map(
        (item) =>
          item.id === document.id
            ? {
                ...item,
                status: "Reviewed",
              }
            : item
      ),
    }))

    setSelectedDocument({
      ...document,
      status: "Reviewed",
    })
  }

  return (
    <DashboardLayout
      role="doctor"
      userName="Dr. Meera Iyer"
    >
      <div className="doctor-documents-page">

        {/* =====================================================
            HEADER
        ===================================================== */}

        <div className="page-header doctor-documents-header">
          <div>
            <div className="page-eyebrow">
              CLINICAL DOCUMENTS
            </div>

            <h1>Medical Documents</h1>

            <p>
              Review patient documents, upload new medical
              records and inspect AI-extracted findings.
            </p>
          </div>

          <button
            type="button"
            className="primary-action-button"
            onClick={handleUploadClick}
            disabled={uploading}
          >
            {uploading ? "Processing..." : "+ Upload Document"}
          </button>

          <input
            ref={fileInputRef}
            type="file"
            accept=".pdf,.png,.jpg,.jpeg"
            onChange={handleFileChange}
            style={{ display: "none" }}
          />
        </div>


        {/* =====================================================
            PATIENT SELECTOR
        ===================================================== */}

        <div className="doctor-document-patient-selector card">

          <div className="document-selector-left">

            <div className="document-selector-icon">
              ♙
            </div>

            <div>
              <label htmlFor="document-patient-select">
                SELECT PATIENT
              </label>

              <select
                id="document-patient-select"
                value={selectedPatientId}
                onChange={handlePatientChange}
              >
                {patients.map((patient) => (
                  <option
                    key={patient.id}
                    value={patient.id}
                  >
                    {patient.name} — {patient.id}
                  </option>
                ))}
              </select>
            </div>

          </div>

          <div className="document-selected-patient">

            <strong>
              {selectedPatient.name}
            </strong>

            <span>
              {selectedPatient.age} yrs ·{" "}
              {selectedPatient.gender} ·{" "}
              Blood Group {selectedPatient.bloodGroup}
            </span>

          </div>

        </div>


        {/* =====================================================
            UPLOAD MESSAGE
        ===================================================== */}

        {uploadMessage && (
          <div className="document-upload-message">
            <span>✓</span>
            {uploadMessage}
          </div>
        )}


        {/* =====================================================
            PATIENT SUMMARY
        ===================================================== */}

        <div className="document-patient-summary card">

          <div className="document-avatar">
            {selectedPatient.name
              .split(" ")
              .map((word) => word[0])
              .join("")
              .slice(0, 2)
              .toUpperCase()}
          </div>

          <div className="document-patient-info">

            <strong>
              {selectedPatient.name}
            </strong>

            <span>
              {selectedPatient.id}
            </span>

            <p>
              {selectedPatient.summary}
            </p>

          </div>

          <div className="document-stats">

            <div>
              <strong>
                {patientDocuments.length}
              </strong>

              <span>
                Documents
              </span>
            </div>

            <div>
              <strong>
                {
                  patientDocuments.filter(
                    (doc) => doc.status === "Processed"
                  ).length
                }
              </strong>

              <span>
                Processed
              </span>
            </div>

            <div>
              <strong>
                {
                  patientDocuments.filter(
                    (doc) =>
                      doc.conflict ||
                      doc.status === "AI Processing"
                  ).length
                }
              </strong>

              <span>
                Review
              </span>
            </div>

          </div>

        </div>


        {/* =====================================================
            DOCUMENT LIST
        ===================================================== */}

        <div className="documents-section">

          <div className="documents-section-header">

            <div>
              <h2>
                Patient Documents
              </h2>

              <p>
                Historical and current medical evidence
                available for clinical review.
              </p>
            </div>

            <span className="documents-count">
              {patientDocuments.length} files
            </span>

          </div>


          <div className="documents-list">

            {patientDocuments.map((document) => (

              <div
                key={document.id}
                className={`doctor-document-card card ${
                  document.conflict
                    ? "document-conflict"
                    : ""
                } ${
                  document.critical
                    ? "document-critical"
                    : ""
                }`}
              >

                <div className="document-file-icon">
                  PDF
                </div>

                <div className="document-main">

                  <div className="document-title-row">

                    <h3>
                      {document.name}
                    </h3>

                    <span
                      className={`document-status ${
                        document.status ===
                        "AI Processing"
                          ? "processing"
                          : document.status ===
                            "Reviewed"
                          ? "reviewed"
                          : ""
                      }`}
                    >
                      {document.status}
                    </span>

                  </div>

                  <div className="document-meta">

                    <span>
                      {document.type}
                    </span>

                    <span>
                      •
                    </span>

                    <span>
                      {document.date}
                    </span>

                    <span>
                      •
                    </span>

                    <span>
                      {document.size}
                    </span>

                  </div>

                  <div className="document-findings">

                    <span>
                      ✦ {document.findings} extracted
                      findings
                    </span>

                    {document.critical && (
                      <span className="document-critical-label">
                        ⚠ Critical information
                      </span>
                    )}

                    {document.conflict && (
                      <span className="document-conflict-label">
                        ⚠ Date discrepancy detected
                      </span>
                    )}

                  </div>

                </div>


                <div className="document-actions">

                  <button
                    type="button"
                    className="secondary-action-button"
                    onClick={() =>
                      setSelectedDocument(document)
                    }
                  >
                    Review
                  </button>

                  <button
                    type="button"
                    className="document-more-button"
                    title="Document options"
                  >
                    ⋮
                  </button>

                </div>

              </div>

            ))}

          </div>

        </div>


        {/* =====================================================
            UPLOAD WORKFLOW
        ===================================================== */}

        <div className="document-workflow card">

          <div className="workflow-header">

            <div className="workflow-icon">
              ✦
            </div>

            <div>
              <h2>
                Document Processing Workflow
              </h2>

              <p>
                Uploaded documents move through AI-assisted
                processing before doctor approval.
              </p>
            </div>

          </div>

          <div className="workflow-steps">

            <div className="workflow-step active">
              <span>1</span>
              <strong>Upload</strong>
              <small>Medical document</small>
            </div>

            <div className="workflow-connector"></div>

            <div className="workflow-step">
              <span>2</span>
              <strong>OCR</strong>
              <small>Extract text</small>
            </div>

            <div className="workflow-connector"></div>

            <div className="workflow-step">
              <span>3</span>
              <strong>NLU</strong>
              <small>Find clinical data</small>
            </div>

            <div className="workflow-connector"></div>

            <div className="workflow-step">
              <span>4</span>
              <strong>Review</strong>
              <small>Doctor validates</small>
            </div>

            <div className="workflow-connector"></div>

            <div className="workflow-step">
              <span>5</span>
              <strong>DB</strong>
              <small>Approved record</small>
            </div>

          </div>

          <div className="workflow-note">
            <span>ⓘ</span>
            AI extraction assists the doctor but does not
            automatically create authoritative medical facts.
          </div>

        </div>


        {/* =====================================================
            REVIEW MODAL
        ===================================================== */}

        {selectedDocument && (

          <div
            className="document-modal-overlay"
            onClick={() => setSelectedDocument(null)}
          >

            <div
              className="document-review-modal"
              onClick={(event) =>
                event.stopPropagation()
              }
            >

              <div className="review-modal-header">

                <div>
                  <div className="page-eyebrow">
                    DOCUMENT REVIEW
                  </div>

                  <h2>
                    {selectedDocument.name}
                  </h2>

                  <p>
                    {selectedDocument.type} ·{" "}
                    {selectedDocument.date}
                  </p>
                </div>

                <button
                  type="button"
                  className="modal-close-button"
                  onClick={() =>
                    setSelectedDocument(null)
                  }
                >
                  ×
                </button>

              </div>


              <div className="review-status-box">

                <span className="review-status-icon">
                  ✦
                </span>

                <div>
                  <strong>
                    AI Extraction Summary
                  </strong>

                  <p>
                    {selectedDocument.findings} potential
                    clinical findings were extracted from
                    this document. Doctor review is required
                    before any finding is added or modified
                    in the authoritative record.
                  </p>
                </div>

              </div>


              {selectedDocument.conflict && (

                <div className="review-warning">

                  <span>⚠</span>

                  <div>
                    <strong>
                      Potential discrepancy detected
                    </strong>

                    <p>
                      This document contains information that
                      may differ from the current database
                      record. Compare the source document
                      with the authoritative record before
                      approving any change.
                    </p>
                  </div>

                </div>

              )}


              {selectedDocument.critical && (

                <div className="review-critical">

                  <span>!</span>

                  <div>
                    <strong>
                      Critical medical information
                    </strong>

                    <p>
                      This document contains information that
                      may be important during emergency care.
                    </p>
                  </div>

                </div>

              )}


              <div className="review-findings">

                <h3>
                  Extracted Findings
                </h3>

                <div className="finding-item">
                  <span>✓</span>
                  <div>
                    <strong>
                      Structured clinical information
                    </strong>
                    <small>
                      Extracted by the AI processing pipeline
                    </small>
                  </div>
                </div>

                <div className="finding-item">
                  <span>✓</span>
                  <div>
                    <strong>
                      Source document preserved
                    </strong>
                    <small>
                      Original evidence remains available
                      for verification
                    </small>
                  </div>
                </div>

                <div className="finding-item">
                  <span>✓</span>
                  <div>
                    <strong>
                      Doctor approval required
                    </strong>
                    <small>
                      AI findings are not automatically treated
                      as authoritative facts
                    </small>
                  </div>
                </div>

              </div>


              <div className="review-modal-actions">

                <button
                  type="button"
                  className="secondary-action-button"
                  onClick={() =>
                    setSelectedDocument(null)
                  }
                >
                  Close
                </button>

                <button
                  type="button"
                  className="primary-action-button"
                  onClick={() => {
                    simulateReview(selectedDocument)
                  }}
                >
                  ✓ Mark as Reviewed
                </button>

              </div>

            </div>

          </div>

        )}

      </div>
    </DashboardLayout>
  )
}

export default DoctorDocuments