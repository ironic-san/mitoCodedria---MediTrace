import { useState } from "react"
import { useNavigate } from "react-router-dom"
import DashboardLayout from "../layouts/DashboardLayout.jsx"

function DoctorAIReviews() {
  const navigate = useNavigate()

  const [selectedPatient, setSelectedPatient] = useState("Kabir Malhotra")
  const [reviewStatus, setReviewStatus] = useState("Pending Review")

  const patients = [
    {
      name: "Kabir Malhotra",
      document: "Emergency_Report_2026.pdf",
      type: "Emergency Record",
      date: "15 Sep 2026",
    },
    {
      name: "Tanya Bose",
      document: "Brain_Surgery_Followup_2025.pdf",
      type: "Surgical Record",
      date: "14 Sep 2025",
    },
    {
      name: "Nikhil Varma",
      document: "Cardiology_Followup_2026.pdf",
      type: "Cardiology Record",
      date: "14 Sep 2026",
    },
  ]

  const currentPatient =
    patients.find(
      (patient) => patient.name === selectedPatient
    ) || patients[0]

  const handleReview = (status) => {
    setReviewStatus(status)
  }

  return (
    <DashboardLayout
      role="doctor"
      userName="Dr. Arjun Rao"
    >
      <div className="ai-review-page">

        {/* PAGE HEADER */}

        <div className="dashboard-page-header">

          <div>

            <div className="page-eyebrow">
              AI-ASSISTED CLINICAL REVIEW
            </div>

            <h1>
              AI Reviews
            </h1>

            <p>
              Review extracted findings and historical evidence before updating
              the patient's health passport.
            </p>

          </div>

          <div className="ai-review-status">
            <span className="ai-status-dot"></span>
            AI Assistance Active
          </div>

        </div>


        {/* PATIENT SELECTOR */}

        <section className="dashboard-panel">

          <div className="ai-patient-selector">

            <div>

              <label>
                PATIENT
              </label>

              <select
                value={selectedPatient}
                onChange={(event) => {
                  setSelectedPatient(event.target.value)
                  setReviewStatus("Pending Review")
                }}
              >

                {patients.map((patient) => (
                  <option
                    key={patient.name}
                    value={patient.name}
                  >
                    {patient.name}
                  </option>
                ))}

              </select>

            </div>


            <div className="ai-document-summary">

              <span className="ai-document-icon">
                📄
              </span>

              <div>

                <strong>
                  {currentPatient.document}
                </strong>

                <p>
                  {currentPatient.type} • {currentPatient.date}
                </p>

              </div>

            </div>

          </div>

        </section>


        {/* REVIEW STATUS */}

        <div
          className={`review-status-banner ${
            reviewStatus === "Approved"
              ? "approved"
              : reviewStatus === "Rejected"
                ? "rejected"
                : "pending"
          }`}
        >

          <span>
            {reviewStatus === "Approved"
              ? "✓"
              : reviewStatus === "Rejected"
                ? "✕"
                : "⏳"}
          </span>

          <div>

            <strong>
              {reviewStatus}
            </strong>

            <p>
              {reviewStatus === "Pending Review"
                ? "AI-generated findings are waiting for doctor review."
                : reviewStatus === "Approved"
                  ? "The reviewed findings have been marked as approved in this demo."
                  : "The AI findings have been marked as rejected in this demo."}
            </p>

          </div>

        </div>


        {/* MAIN REVIEW GRID */}

        <div className="ai-review-grid">

          {/* DOCUMENT / OCR */}

          <section className="dashboard-panel ai-panel">

            <div className="panel-header">

              <div>

                <h2>
                  Document & OCR
                </h2>

                <p>
                  Extracted text from the uploaded medical document.
                </p>

              </div>

              <span className="processing-badge">
                OCR Complete
              </span>

            </div>


            <div className="ocr-document">

              <div className="ocr-document-header">

                <span>
                  📄
                </span>

                <div>

                  <strong>
                    {currentPatient.document}
                  </strong>

                  <small>
                    Medical document
                  </small>

                </div>

              </div>


              <div className="ocr-text">

                <p>
                  <strong>Patient:</strong> {currentPatient.name}
                </p>

                <p>
                  <strong>Clinical Record:</strong>
                </p>

                {currentPatient.name === "Kabir Malhotra" ? (
                  <>
                    <p>
                      Patient presented for emergency evaluation.
                    </p>

                    <p>
                      Known severe allergy to Penicillin documented.
                    </p>

                    <p>
                      Previous reaction recorded as anaphylaxis.
                    </p>

                    <p>
                      Emergency medical history reviewed during presentation.
                    </p>
                  </>
                ) : currentPatient.name === "Tanya Bose" ? (
                  <>
                    <p>
                      Follow-up after intracranial lesion surgery.
                    </p>

                    <p>
                      Surgical date documented in this medical document as
                      14 September 2025.
                    </p>

                    <p>
                      Continued post-operative follow-up recommended.
                    </p>
                  </>
                ) : (
                  <>
                    <p>
                      Cardiology follow-up documented.
                    </p>

                    <p>
                      Previous myocardial infarction and coronary intervention
                      noted in the medical history.
                    </p>

                    <p>
                      Continued medication and cardiology follow-up documented.
                    </p>
                  </>
                )}

              </div>

            </div>

          </section>


          {/* NLU FINDINGS */}

          <section className="dashboard-panel ai-panel">

            <div className="panel-header">

              <div>

                <h2>
                  Structured Findings
                </h2>

                <p>
                  Information extracted by medical language processing.
                </p>

              </div>

              <span className="processing-badge">
                NLU Complete
              </span>

            </div>


            <div className="finding-list">

              {currentPatient.name === "Kabir Malhotra" && (
                <>
                  <div className="finding-card critical">

                    <div className="finding-icon">
                      ⚠️
                    </div>

                    <div>

                      <span className="finding-type">
                        ALLERGY
                      </span>

                      <strong>
                        Penicillin
                      </strong>

                      <p>
                        Severity: Severe
                      </p>

                    </div>

                    <span className="finding-confidence">
                      98%
                    </span>

                  </div>


                  <div className="finding-card critical">

                    <div className="finding-icon">
                      🚨
                    </div>

                    <div>

                      <span className="finding-type">
                        REACTION
                      </span>

                      <strong>
                        Anaphylaxis
                      </strong>

                      <p>
                        Associated with Penicillin allergy
                      </p>

                    </div>

                    <span className="finding-confidence">
                      97%
                    </span>

                  </div>
                </>
              )}


              {currentPatient.name === "Tanya Bose" && (
                <>

                  <div className="finding-card warning">

                    <div className="finding-icon">
                      ⚠️
                    </div>

                    <div>

                      <span className="finding-type">
                        DATE
                      </span>

                      <strong>
                        14 Sep 2025
                      </strong>

                      <p>
                        Surgery date extracted from document.
                      </p>

                    </div>

                    <span className="finding-confidence">
                      96%
                    </span>

                  </div>


                  <div className="finding-card">

                    <div className="finding-icon">
                      🧠
                    </div>

                    <div>

                      <span className="finding-type">
                        PROCEDURE
                      </span>

                      <strong>
                        Brain Surgery
                      </strong>

                      <p>
                        Surgical procedure identified in document.
                      </p>

                    </div>

                    <span className="finding-confidence">
                      95%
                    </span>

                  </div>

                </>
              )}


              {currentPatient.name === "Nikhil Varma" && (
                <>

                  <div className="finding-card">

                    <div className="finding-icon">
                      ❤️
                    </div>

                    <div>

                      <span className="finding-type">
                        CARDIAC EVENT
                      </span>

                      <strong>
                        Previous MI
                      </strong>

                      <p>
                        Historical myocardial infarction referenced.
                      </p>

                    </div>

                    <span className="finding-confidence">
                      96%
                    </span>

                  </div>


                  <div className="finding-card">

                    <div className="finding-icon">
                      🩺
                    </div>

                    <div>

                      <span className="finding-type">
                        PROCEDURE
                      </span>

                      <strong>
                        Angioplasty + Stent
                      </strong>

                      <p>
                        Previous coronary intervention identified.
                      </p>

                    </div>

                    <span className="finding-confidence">
                      94%
                    </span>

                  </div>

                </>
              )}

            </div>

          </section>

        </div>


        {/* RAG EVIDENCE */}

        <section className="dashboard-panel ai-panel">

          <div className="panel-header">

            <div>

              <h2>
                Historical Evidence
              </h2>

              <p>
                Relevant evidence retrieved from the patient's historical
                medical corpus.
              </p>

            </div>

            <span className="rag-badge">
              RAG Evidence
            </span>

          </div>


          <div className="rag-evidence-list">

            {currentPatient.name === "Kabir Malhotra" && (
              <>
                <div className="rag-evidence">

                  <div className="rag-number">
                    01
                  </div>

                  <div>

                    <strong>
                      Allergy Record — 2019
                    </strong>

                    <p>
                      Historical record identifies severe Penicillin allergy
                      with anaphylaxis as the documented reaction.
                    </p>

                    <span>
                      Source: Allergy_Records_2019.pdf
                    </span>

                  </div>

                </div>


                <div className="rag-evidence">

                  <div className="rag-number">
                    02
                  </div>

                  <div>

                    <strong>
                      Emergency History
                    </strong>

                    <p>
                      Historical medical evidence supports the presence of a
                      critical Penicillin allergy in the patient's record.
                    </p>

                    <span>
                      Patient-scoped historical evidence
                    </span>

                  </div>

                </div>
              </>
            )}


            {currentPatient.name === "Tanya Bose" && (
              <div className="rag-evidence">

                <div className="rag-number">
                  01
                </div>

                <div>

                  <strong>
                    Surgical History — 2025
                  </strong>

                  <p>
                    Historical document contains a surgery date of
                    14 September 2025.
                  </p>

                  <span>
                    Source: Brain_Surgery_Followup_2025.pdf
                  </span>

                </div>

              </div>
            )}


            {currentPatient.name === "Nikhil Varma" && (
              <>
                <div className="rag-evidence">

                  <div className="rag-number">
                    01
                  </div>

                  <div>

                    <strong>
                      Cardiology Hospitalization — 2023
                    </strong>

                    <p>
                      Historical evidence describes myocardial infarction,
                      hospitalization and coronary intervention.
                    </p>

                    <span>
                      Patient-scoped historical evidence
                    </span>

                  </div>

                </div>


                <div className="rag-evidence">

                  <div className="rag-number">
                    02
                  </div>

                  <div>

                    <strong>
                      Cardiology Follow-up
                    </strong>

                    <p>
                      Historical follow-up records reference ongoing cardiac
                      treatment and medication management.
                    </p>

                    <span>
                      Patient-scoped historical evidence
                    </span>

                  </div>

                </div>
              </>
            )}

          </div>

        </section>


        {/* AI SUMMARY */}

        <section className="ai-summary-card">

          <div className="ai-summary-header">

            <div className="ai-brain-icon">
              ✦
            </div>

            <div>

              <span>
                AI-ASSISTED SUMMARY
              </span>

              <h2>
                Clinical Interpretation
              </h2>

            </div>

            <span className="ai-generated-badge">
              AI Generated
            </span>

          </div>


          <div className="ai-summary-body">

            {currentPatient.name === "Kabir Malhotra" && (
              <>
                <p>
                  The uploaded emergency document identifies a severe
                  Penicillin allergy with a recorded reaction of anaphylaxis.
                </p>

                <div className="ai-highlight">
                  <strong>
                    Possible allergy-related finding detected.
                  </strong>

                  <span>
                    Compare with the current structured patient record before
                    making any modification.
                  </span>
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

                <div className="ai-highlight warning">
                  <strong>
                    Potential date discrepancy detected.
                  </strong>

                  <span>
                    Doctor review is required before modifying the authoritative
                    medical record.
                  </span>
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

                <div className="ai-highlight">
                  <strong>
                    Longitudinal history available.
                  </strong>

                  <span>
                    Review the retrieved evidence alongside the current
                    structured record.
                  </span>
                </div>
              </>
            )}

          </div>

        </section>


        {/* REVIEW ACTIONS */}

        <section className="ai-review-actions">

          <div>

            <strong>
              Doctor Review Required
            </strong>

            <p>
              AI findings do not automatically modify the patient's medical
              record.
            </p>

          </div>


          <div className="review-action-buttons">

            <button
              type="button"
              className="reject-review-button"
              onClick={() => handleReview("Rejected")}
            >
              ✕ Reject Findings
            </button>


            <button
              type="button"
              className="edit-review-button"
              onClick={() => alert(
                "Edit workflow will be connected to the FastAPI backend later."
              )}
            >
              ✏ Edit Findings
            </button>


            <button
              type="button"
              className="approve-review-button"
              onClick={() => handleReview("Approved")}
            >
              ✓ Approve Findings
            </button>

          </div>

        </section>


        {/* NAVIGATION */}

        <div className="ai-review-navigation">

          <button
            type="button"
            onClick={() => navigate("/doctor/patients")}
          >
            ← Patient Directory
          </button>

          <button
            type="button"
            onClick={() => navigate("/doctor/integrity")}
          >
            Continue to Integrity →
          </button>

        </div>

      </div>
    </DashboardLayout>
  )
}

export default DoctorAIReviews