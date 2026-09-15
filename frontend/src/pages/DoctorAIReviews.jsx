import { useState } from "react"
import { useNavigate } from "react-router-dom"
import DashboardLayout from "../layouts/DashboardLayout.jsx"

function Icon({ name, size = 20 }) {
  const common = {
    width: size,
    height: size,
    viewBox: "0 0 24 24",
    fill: "none",
    stroke: "currentColor",
    strokeWidth: 1.8,
    strokeLinecap: "round",
    strokeLinejoin: "round",
  }

  const icons = {
    sparkle: (
      <>
        <path d="M12 3l1.6 5.4L19 10l-5.4 1.6L12 17l-1.6-5.4L5 10l5.4-1.6L12 3z" />
        <path d="M19 16l.7 2.3L22 19l-2.3.7L19 22l-.7-2.3L16 19l2.3-.7L19 16z" />
      </>
    ),
    file: (
      <>
        <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
        <path d="M14 2v6h6" />
        <path d="M8 13h8M8 17h6" />
      </>
    ),
    brain: (
      <>
        <path d="M9.5 4.5a3 3 0 0 0-5 2.2A3.5 3.5 0 0 0 5 13a3.5 3.5 0 0 0 2.5 5.9A3 3 0 0 0 13 17V7a3 3 0 0 0-3.5-2.5z" />
        <path d="M14.5 4.5a3 3 0 0 1 5 2.2A3.5 3.5 0 0 1 19 13a3.5 3.5 0 0 1-2.5 5.9A3 3 0 0 1 11 17V7a3 3 0 0 1 3.5-2.5z" />
        <path d="M8 8h2M14 8h2M8 13h2M14 13h2" />
      </>
    ),
    search: (
      <>
        <circle cx="11" cy="11" r="7" />
        <path d="m20 20-4-4" />
      </>
    ),
    shield: (
      <>
        <path d="M12 3l8 3v5c0 5.2-3.4 8.5-8 10-4.6-1.5-8-4.8-8-10V6l8-3z" />
        <path d="m9 12 2 2 4-4" />
      </>
    ),
    alert: (
      <>
        <path d="M10.3 3.8 2.2 18a2 2 0 0 0 1.7 3h16.2a2 2 0 0 0 1.7-3L13.7 3.8a2 2 0 0 0-3.4 0z" />
        <path d="M12 9v4M12 17h.01" />
      </>
    ),
    check: <path d="m5 12 4 4L19 6" />,
    x: (
      <>
        <path d="m6 6 12 12M18 6 6 18" />
      </>
    ),
    edit: (
      <>
        <path d="M12 20h9" />
        <path d="M16.5 3.5a2.1 2.1 0 0 1 3 3L8 18l-4 1 1-4z" />
      </>
    ),
    database: (
      <>
        <ellipse cx="12" cy="5" rx="8" ry="3" />
        <path d="M4 5v7c0 1.7 3.6 3 8 3s8-1.3 8-3V5" />
        <path d="M4 12v7c0 1.7 3.6 3 8 3s8-1.3 8-3v-7" />
      </>
    ),
    arrow: (
      <>
        <path d="M5 12h14" />
        <path d="m13 6 6 6-6 6" />
      </>
    ),
    back: (
      <>
        <path d="M19 12H5" />
        <path d="m11 18-6-6 6-6" />
      </>
    ),
  }

  return <svg {...common}>{icons[name]}</svg>
}

function DoctorAIReviews() {
  const navigate = useNavigate()

  const [selectedPatient, setSelectedPatient] = useState("Kabir Malhotra")
  const [reviewStatus, setReviewStatus] = useState("Pending Review")
  const [activeEvidence, setActiveEvidence] = useState(0)

  const patients = [
    {
      name: "Kabir Malhotra",
      id: "PT-KABIR-005",
      document: "Emergency_Report_2026.pdf",
      type: "Emergency Record",
      date: "15 Sep 2026",
      findingCount: 2,
      priority: "Critical",
    },
    {
      name: "Tanya Bose",
      id: "PT-TANYA-006",
      document: "Brain_Surgery_Followup_2025.pdf",
      type: "Surgical Record",
      date: "14 Sep 2025",
      findingCount: 2,
      priority: "Review Required",
    },
    {
      name: "Nikhil Varma",
      id: "PT-NIKHIL-003",
      document: "Cardiology_Followup_2026.pdf",
      type: "Cardiology Record",
      date: "14 Sep 2026",
      findingCount: 2,
      priority: "Historical",
    },
  ]

  const currentPatient =
    patients.find((patient) => patient.name === selectedPatient) || patients[0]

  const handlePatientChange = (event) => {
    setSelectedPatient(event.target.value)
    setReviewStatus("Pending Review")
    setActiveEvidence(0)
  }

  const handleReview = (status) => {
    setReviewStatus(status)
  }

  const isApproved = reviewStatus === "Approved"
  const isRejected = reviewStatus === "Rejected"

  return (
    <DashboardLayout role="doctor" userName="Dr. Arjun Rao">
      <div className="ai-review-page polished-ai-page">

        {/* HEADER */}
        <div className="dashboard-page-header ai-polished-header">
          <div>
            <div className="page-eyebrow">
              <span className="eyebrow-icon">
                <Icon name="sparkle" size={14} />
              </span>
              AI-ASSISTED CLINICAL REVIEW
            </div>

            <h1>AI Reviews</h1>

            <p>
              Review AI-extracted findings and historical evidence before
              updating the patient's authoritative health record.
            </p>
          </div>

          <div className="ai-active-indicator">
            <span className="ai-active-pulse"></span>
            <div>
              <strong>AI Assistance Active</strong>
              <small>OCR · NLU · RAG ready</small>
            </div>
          </div>
        </div>

        {/* WORKFLOW */}
        <section className="ai-workflow">
          <div className="workflow-step completed">
            <div className="workflow-number">
              <Icon name="file" size={17} />
            </div>
            <div>
              <strong>Document</strong>
              <span>Uploaded</span>
            </div>
          </div>

          <div className="workflow-line active"></div>

          <div className="workflow-step completed">
            <div className="workflow-number">
              <Icon name="search" size={17} />
            </div>
            <div>
              <strong>OCR</strong>
              <span>Extracted</span>
            </div>
          </div>

          <div className="workflow-line active"></div>

          <div className="workflow-step completed">
            <div className="workflow-number">
              <Icon name="brain" size={17} />
            </div>
            <div>
              <strong>NLU</strong>
              <span>Structured</span>
            </div>
          </div>

          <div className="workflow-line active"></div>

          <div className="workflow-step current">
            <div className="workflow-number">
              <Icon name="sparkle" size={17} />
            </div>
            <div>
              <strong>Doctor Review</strong>
              <span>Decision required</span>
            </div>
          </div>
        </section>

        {/* PATIENT CONTEXT */}
        <section className="dashboard-panel ai-patient-context">
          <div className="ai-context-left">
            <div className="ai-patient-avatar">
              {currentPatient.name
                .split(" ")
                .map((word) => word[0])
                .join("")
                .slice(0, 2)}
            </div>

            <div>
              <span className="context-label">CURRENT PATIENT</span>
              <h2>{currentPatient.name}</h2>
              <p>
                {currentPatient.id} · {currentPatient.type}
              </p>
            </div>
          </div>

          <div className="ai-context-right">
            <div className="context-document">
              <div className="context-document-icon">
                <Icon name="file" size={19} />
              </div>
              <div>
                <span>Source document</span>
                <strong>{currentPatient.document}</strong>
              </div>
            </div>

            <div className="context-select">
              <label>CHANGE PATIENT</label>
              <select
                value={selectedPatient}
                onChange={handlePatientChange}
              >
                {patients.map((patient) => (
                  <option key={patient.name} value={patient.name}>
                    {patient.name}
                  </option>
                ))}
              </select>
            </div>
          </div>
        </section>

        {/* REVIEW STATUS */}
        <div
          className={`review-status-banner polished-review-status ${
            isApproved
              ? "approved"
              : isRejected
                ? "rejected"
                : "pending"
          }`}
        >
          <div className="review-status-icon">
            {isApproved ? (
              <Icon name="check" size={21} />
            ) : isRejected ? (
              <Icon name="x" size={21} />
            ) : (
              <Icon name="alert" size={21} />
            )}
          </div>

          <div className="review-status-content">
            <strong>{reviewStatus}</strong>
            <p>
              {reviewStatus === "Pending Review"
                ? "AI-generated findings are waiting for doctor validation."
                : reviewStatus === "Approved"
                  ? "Findings have been approved for this demonstration. Authoritative database updates still require the backend workflow."
                  : "These AI findings have been rejected in this demonstration."}
            </p>
          </div>

          <span className="status-tag">
            {isApproved
              ? "REVIEWED"
              : isRejected
                ? "REJECTED"
                : "ACTION REQUIRED"}
          </span>
        </div>

        {/* TOP GRID */}
        <div className="ai-review-grid polished-ai-grid">

          {/* OCR */}
          <section className="dashboard-panel ai-panel polished-ai-card">
            <div className="panel-header polished-panel-header">
              <div className="panel-title-group">
                <div className="panel-title-icon document-icon">
                  <Icon name="file" size={19} />
                </div>

                <div>
                  <h2>Document & OCR</h2>
                  <p>Text extracted from the uploaded medical record.</p>
                </div>
              </div>

              <span className="processing-badge polished-success-badge">
                <Icon name="check" size={13} />
                OCR Complete
              </span>
            </div>

            <div className="ocr-document polished-ocr-document">
              <div className="ocr-document-header polished-document-header">
                <div className="document-file-icon">
                  <Icon name="file" size={22} />
                </div>

                <div>
                  <strong>{currentPatient.document}</strong>
                  <small>
                    {currentPatient.type} · {currentPatient.date}
                  </small>
                </div>

                <span className="document-confidence">
                  99% extraction
                </span>
              </div>

              <div className="ocr-text polished-ocr-text">
                <div className="ocr-line">
                  <span>01</span>
                  <p>
                    <strong>Patient:</strong> {currentPatient.name}
                  </p>
                </div>

                <div className="ocr-line">
                  <span>02</span>
                  <p>
                    <strong>Clinical Record:</strong>
                  </p>
                </div>

                {currentPatient.name === "Kabir Malhotra" ? (
                  <>
                    <div className="ocr-line">
                      <span>03</span>
                      <p>Patient presented for emergency evaluation.</p>
                    </div>

                    <div className="ocr-line highlighted">
                      <span>04</span>
                      <p>
                        Known severe allergy to <strong>Penicillin</strong>{" "}
                        documented.
                      </p>
                    </div>

                    <div className="ocr-line highlighted">
                      <span>05</span>
                      <p>
                        Previous reaction recorded as{" "}
                        <strong>anaphylaxis</strong>.
                      </p>
                    </div>

                    <div className="ocr-line">
                      <span>06</span>
                      <p>
                        Emergency medical history reviewed during presentation.
                      </p>
                    </div>
                  </>
                ) : currentPatient.name === "Tanya Bose" ? (
                  <>
                    <div className="ocr-line">
                      <span>03</span>
                      <p>Follow-up after intracranial lesion surgery.</p>
                    </div>

                    <div className="ocr-line highlighted warning">
                      <span>04</span>
                      <p>
                        Surgical date documented as{" "}
                        <strong>14 September 2025</strong>.
                      </p>
                    </div>

                    <div className="ocr-line">
                      <span>05</span>
                      <p>Continued post-operative follow-up recommended.</p>
                    </div>
                  </>
                ) : (
                  <>
                    <div className="ocr-line">
                      <span>03</span>
                      <p>Cardiology follow-up documented.</p>
                    </div>

                    <div className="ocr-line">
                      <span>04</span>
                      <p>
                        Previous myocardial infarction and coronary
                        intervention noted.
                      </p>
                    </div>

                    <div className="ocr-line">
                      <span>05</span>
                      <p>
                        Continued medication and cardiology follow-up documented.
                      </p>
                    </div>
                  </>
                )}
              </div>
            </div>
          </section>

          {/* NLU */}
          <section className="dashboard-panel ai-panel polished-ai-card">
            <div className="panel-header polished-panel-header">
              <div className="panel-title-group">
                <div className="panel-title-icon nlu-icon">
                  <Icon name="brain" size={19} />
                </div>

                <div>
                  <h2>Structured Findings</h2>
                  <p>Medical concepts identified by NLU processing.</p>
                </div>
              </div>

              <span className="processing-badge polished-success-badge">
                <Icon name="check" size={13} />
                NLU Complete
              </span>
            </div>

            <div className="finding-list polished-finding-list">

              {currentPatient.name === "Kabir Malhotra" && (
                <>
                  <div className="finding-card polished-finding critical">
                    <div className="finding-icon critical-icon">
                      <Icon name="alert" size={18} />
                    </div>

                    <div className="finding-main">
                      <span className="finding-type">ALLERGY</span>
                      <strong>Penicillin</strong>
                      <p>Severity: Severe</p>
                    </div>

                    <div className="confidence-column">
                      <span>Confidence</span>
                      <strong>98%</strong>
                    </div>
                  </div>

                  <div className="finding-card polished-finding critical">
                    <div className="finding-icon critical-icon">
                      <Icon name="alert" size={18} />
                    </div>

                    <div className="finding-main">
                      <span className="finding-type">REACTION</span>
                      <strong>Anaphylaxis</strong>
                      <p>Associated with Penicillin allergy</p>
                    </div>

                    <div className="confidence-column">
                      <span>Confidence</span>
                      <strong>97%</strong>
                    </div>
                  </div>
                </>
              )}

              {currentPatient.name === "Tanya Bose" && (
                <>
                  <div className="finding-card polished-finding warning">
                    <div className="finding-icon warning-icon">
                      <Icon name="alert" size={18} />
                    </div>

                    <div className="finding-main">
                      <span className="finding-type">DATE</span>
                      <strong>14 Sep 2025</strong>
                      <p>Surgery date extracted from document</p>
                    </div>

                    <div className="confidence-column">
                      <span>Confidence</span>
                      <strong>96%</strong>
                    </div>
                  </div>

                  <div className="finding-card polished-finding">
                    <div className="finding-icon procedure-icon">
                      <Icon name="sparkle" size={18} />
                    </div>

                    <div className="finding-main">
                      <span className="finding-type">PROCEDURE</span>
                      <strong>Brain Surgery</strong>
                      <p>Surgical procedure identified in document</p>
                    </div>

                    <div className="confidence-column">
                      <span>Confidence</span>
                      <strong>95%</strong>
                    </div>
                  </div>
                </>
              )}

              {currentPatient.name === "Nikhil Varma" && (
                <>
                  <div className="finding-card polished-finding">
                    <div className="finding-icon cardiac-icon">
                      <span>+</span>
                    </div>

                    <div className="finding-main">
                      <span className="finding-type">CARDIAC EVENT</span>
                      <strong>Previous MI</strong>
                      <p>Historical myocardial infarction referenced</p>
                    </div>

                    <div className="confidence-column">
                      <span>Confidence</span>
                      <strong>96%</strong>
                    </div>
                  </div>

                  <div className="finding-card polished-finding">
                    <div className="finding-icon procedure-icon">
                      <Icon name="sparkle" size={18} />
                    </div>

                    <div className="finding-main">
                      <span className="finding-type">PROCEDURE</span>
                      <strong>Angioplasty + Stent</strong>
                      <p>Previous coronary intervention identified</p>
                    </div>

                    <div className="confidence-column">
                      <span>Confidence</span>
                      <strong>94%</strong>
                    </div>
                  </div>
                </>
              )}

            </div>

            <div className="finding-footer">
              <Icon name="shield" size={16} />
              <span>AI findings require doctor validation before becoming authoritative.</span>
            </div>
          </section>
        </div>

        {/* HISTORICAL EVIDENCE */}
        <section className="dashboard-panel ai-panel polished-ai-card evidence-panel">
          <div className="panel-header polished-panel-header">
            <div className="panel-title-group">
              <div className="panel-title-icon rag-icon">
                <Icon name="search" size={19} />
              </div>

              <div>
                <h2>Historical Evidence</h2>
                <p>
                  Relevant patient-scoped evidence retrieved from the historical
                  medical corpus.
                </p>
              </div>
            </div>

            <span className="rag-badge polished-rag-badge">
              <Icon name="database" size={13} />
              RAG Evidence
            </span>
          </div>

          <div className="rag-evidence-list polished-rag-list">

            {currentPatient.name === "Kabir Malhotra" && (
              <>
                <button
                  type="button"
                  className={`rag-evidence polished-rag-evidence ${
                    activeEvidence === 0 ? "active" : ""
                  }`}
                  onClick={() => setActiveEvidence(0)}
                >
                  <div className="rag-number">01</div>

                  <div className="rag-evidence-content">
                    <div className="rag-evidence-top">
                      <strong>Allergy Record — 2019</strong>
                      <span>Historical</span>
                    </div>

                    <p>
                      Historical record identifies severe Penicillin allergy
                      with anaphylaxis as the documented reaction.
                    </p>

                    <small>
                      Source: Allergy_Records_2019.pdf
                    </small>
                  </div>

                  <Icon name="arrow" size={18} />
                </button>

                <button
                  type="button"
                  className={`rag-evidence polished-rag-evidence ${
                    activeEvidence === 1 ? "active" : ""
                  }`}
                  onClick={() => setActiveEvidence(1)}
                >
                  <div className="rag-number">02</div>

                  <div className="rag-evidence-content">
                    <div className="rag-evidence-top">
                      <strong>Emergency History</strong>
                      <span>Patient-scoped</span>
                    </div>

                    <p>
                      Historical medical evidence supports the presence of a
                      critical Penicillin allergy in the patient's record.
                    </p>

                    <small>Patient-scoped historical evidence</small>
                  </div>

                  <Icon name="arrow" size={18} />
                </button>
              </>
            )}

            {currentPatient.name === "Tanya Bose" && (
              <button
                type="button"
                className="rag-evidence polished-rag-evidence active"
              >
                <div className="rag-number">01</div>

                <div className="rag-evidence-content">
                  <div className="rag-evidence-top">
                    <strong>Surgical History — 2025</strong>
                    <span>Potential conflict</span>
                  </div>

                  <p>
                    Historical document contains a surgery date of
                    14 September 2025.
                  </p>

                  <small>
                    Source: Brain_Surgery_Followup_2025.pdf
                  </small>
                </div>

                <Icon name="arrow" size={18} />
              </button>
            )}

            {currentPatient.name === "Nikhil Varma" && (
              <>
                <button
                  type="button"
                  className={`rag-evidence polished-rag-evidence ${
                    activeEvidence === 0 ? "active" : ""
                  }`}
                  onClick={() => setActiveEvidence(0)}
                >
                  <div className="rag-number">01</div>

                  <div className="rag-evidence-content">
                    <div className="rag-evidence-top">
                      <strong>Cardiology Hospitalization — 2023</strong>
                      <span>Historical</span>
                    </div>

                    <p>
                      Historical evidence describes myocardial infarction,
                      hospitalization and coronary intervention.
                    </p>

                    <small>Patient-scoped historical evidence</small>
                  </div>

                  <Icon name="arrow" size={18} />
                </button>

                <button
                  type="button"
                  className={`rag-evidence polished-rag-evidence ${
                    activeEvidence === 1 ? "active" : ""
                  }`}
                  onClick={() => setActiveEvidence(1)}
                >
                  <div className="rag-number">02</div>

                  <div className="rag-evidence-content">
                    <div className="rag-evidence-top">
                      <strong>Cardiology Follow-up</strong>
                      <span>Historical</span>
                    </div>

                    <p>
                      Historical follow-up records reference ongoing cardiac
                      treatment and medication management.
                    </p>

                    <small>Patient-scoped historical evidence</small>
                  </div>

                  <Icon name="arrow" size={18} />
                </button>
              </>
            )}

          </div>
        </section>

        {/* AI INTERPRETATION */}
        <section className="ai-summary-card polished-ai-summary">
          <div className="ai-summary-header polished-summary-header">
            <div className="ai-brain-icon polished-ai-brain">
              <Icon name="sparkle" size={21} />
            </div>

            <div>
              <span>AI-ASSISTED SUMMARY</span>
              <h2>Clinical Interpretation</h2>
            </div>

            <span className="ai-generated-badge">
              AI Generated
            </span>
          </div>

          <div className="ai-summary-body polished-summary-body">

            {currentPatient.name === "Kabir Malhotra" && (
              <>
                <p>
                  The uploaded emergency document identifies a severe
                  Penicillin allergy with a recorded reaction of anaphylaxis.
                  This finding should be compared against the current
                  structured patient record before any modification is made.
                </p>

                <div className="ai-highlight polished-ai-highlight critical-highlight">
                  <div className="highlight-icon">
                    <Icon name="alert" size={18} />
                  </div>

                  <div>
                    <strong>
                      Possible allergy-related finding detected.
                    </strong>
                    <span>
                      Doctor review is required before modifying the
                      authoritative medical record.
                    </span>
                  </div>
                </div>
              </>
            )}

            {currentPatient.name === "Tanya Bose" && (
              <>
                <p>
                  The uploaded surgical document contains a brain surgery date
                  of 14 September 2025, while the current structured database
                  record contains 10 September 2025.
                </p>

                <div className="ai-highlight polished-ai-highlight warning-highlight">
                  <div className="highlight-icon">
                    <Icon name="alert" size={18} />
                  </div>

                  <div>
                    <strong>Potential date discrepancy detected.</strong>
                    <span>
                      Doctor review is required before modifying the
                      authoritative medical record.
                    </span>
                  </div>
                </div>
              </>
            )}

            {currentPatient.name === "Nikhil Varma" && (
              <>
                <p>
                  Historical evidence supports a previous myocardial infarction
                  followed by angiography, angioplasty and stent placement.
                  Cardiology follow-up records indicate ongoing management.
                </p>

                <div className="ai-highlight polished-ai-highlight">
                  <div className="highlight-icon">
                    <Icon name="search" size={18} />
                  </div>

                  <div>
                    <strong>Longitudinal history available.</strong>
                    <span>
                      Review the retrieved evidence alongside the current
                      structured record.
                    </span>
                  </div>
                </div>
              </>
            )}

          </div>
        </section>

        {/* RESPONSIBILITY NOTICE */}
        <div className="ai-responsibility-strip">
          <div className="responsibility-icon">
            <Icon name="shield" size={20} />
          </div>

          <div>
            <strong>Doctor remains the final decision-maker</strong>
            <p>
              Medi-Trace assists with extraction, retrieval and summarization.
              AI does not diagnose, approve findings automatically, or directly
              modify the authoritative medical record.
            </p>
          </div>
        </div>

        {/* ACTIONS */}
        <section className="ai-review-actions polished-review-actions">
          <div className="review-action-copy">
            <span className="action-eyebrow">FINAL REVIEW</span>
            <strong>Doctor Review Required</strong>
            <p>
              Validate the evidence and findings before approving any update.
            </p>
          </div>

          <div className="review-action-buttons polished-action-buttons">
            <button
              type="button"
              className="reject-review-button polished-action-button reject"
              onClick={() => handleReview("Rejected")}
            >
              <Icon name="x" size={17} />
              Reject Findings
            </button>

            <button
              type="button"
              className="edit-review-button polished-action-button edit"
              onClick={() =>
                alert(
                  "Edit workflow will be connected to the FastAPI backend later."
                )
              }
            >
              <Icon name="edit" size={17} />
              Edit Findings
            </button>

            <button
              type="button"
              className="approve-review-button polished-action-button approve"
              onClick={() => handleReview("Approved")}
            >
              <Icon name="check" size={17} />
              Approve Findings
            </button>
          </div>
        </section>

        {/* NAVIGATION */}
        <div className="ai-review-navigation polished-navigation">
          <button
            type="button"
            onClick={() => navigate("/doctor/patients")}
          >
            <Icon name="back" size={17} />
            Patient Directory
          </button>

          <button
            type="button"
            onClick={() => navigate("/doctor/integrity")}
          >
            Continue to Integrity
            <Icon name="arrow" size={17} />
          </button>
        </div>

      </div>
    </DashboardLayout>
  )
}

export default DoctorAIReviews