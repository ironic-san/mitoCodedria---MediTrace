import { useState } from "react"
import DashboardLayout from "../layouts/DashboardLayout"

const auditRecords = [
  {
    id: "AUD-001",
    type: "BREAK_GLASS",
    title: "Emergency access granted",
    description:
      "Emergency access to critical medical information was granted for Kabir Malhotra.",
    doctor: "Dr. Priya Sharma",
    patient: "Kabir Malhotra",
    patientId: "PT-KABIR-005",
    timestamp: "15 Sep 2026 • 14:32",
    reason: "Critical allergy information required during emergency presentation.",
    severity: "HIGH",
  },
  {
    id: "AUD-002",
    type: "INTEGRITY",
    title: "Integrity verification completed",
    description:
      "Blockchain provenance was checked for the severe Penicillin allergy record.",
    doctor: "Dr. Priya Sharma",
    patient: "Kabir Malhotra",
    patientId: "PT-KABIR-005",
    timestamp: "15 Sep 2026 • 14:28",
    reason: "Verification of critical allergy provenance.",
    severity: "NORMAL",
  },
  {
    id: "AUD-003",
    type: "AI_REVIEW",
    title: "AI finding reviewed",
    description:
      "A possible allergy-related finding extracted from a medical document was reviewed.",
    doctor: "Dr. Priya Sharma",
    patient: "Kabir Malhotra",
    patientId: "PT-KABIR-005",
    timestamp: "15 Sep 2026 • 13:55",
    reason: "Doctor review of AI-generated finding.",
    severity: "NORMAL",
  },
  {
    id: "AUD-004",
    type: "DOCUMENT",
    title: "Medical document uploaded",
    description:
      "A historical medical document was uploaded for patient record processing.",
    doctor: "Dr. Priya Sharma",
    patient: "Tanya Bose",
    patientId: "PT-TANYA-006",
    timestamp: "15 Sep 2026 • 12:41",
    reason: "Historical neurological records uploaded for review.",
    severity: "NORMAL",
  },
  {
    id: "AUD-005",
    type: "MODIFICATION",
    title: "Medical record updated",
    description:
      "A structured medical event was edited after doctor review.",
    doctor: "Dr. Rahul Menon",
    patient: "Nikhil Varma",
    patientId: "PT-NIKHIL-003",
    timestamp: "14 Sep 2026 • 18:22",
    reason: "Correction to historical cardiology information.",
    severity: "NORMAL",
  },
  {
    id: "AUD-006",
    type: "HISTORICAL_QUERY",
    title: "Historical medical query executed",
    description:
      "A longitudinal question was answered using historical medical evidence.",
    doctor: "Dr. Priya Sharma",
    patient: "Nikhil Varma",
    patientId: "PT-NIKHIL-003",
    timestamp: "14 Sep 2026 • 17:05",
    reason: "Review of long-term cardiac history.",
    severity: "NORMAL",
  },
  {
    id: "AUD-007",
    type: "ACCESS",
    title: "Patient record accessed",
    description:
      "Authorized doctor access was used to open the patient's health passport.",
    doctor: "Dr. Rahul Menon",
    patient: "Aarav Mehta",
    patientId: "PT-AARAV-001",
    timestamp: "14 Sep 2026 • 15:36",
    reason: "Routine clinical review.",
    severity: "NORMAL",
  },
  {
    id: "AUD-008",
    type: "INTEGRITY",
    title: "Integrity mismatch detected",
    description:
      "A discrepancy was identified between the current record and historical evidence.",
    doctor: "Dr. Priya Sharma",
    patient: "Tanya Bose",
    patientId: "PT-TANYA-006",
    timestamp: "14 Sep 2026 • 11:18",
    reason: "Brain surgery date requires doctor review.",
    severity: "HIGH",
  },
]

const typeConfig = {
  ACCESS: {
    icon: "↗",
    label: "Record Access",
  },
  BREAK_GLASS: {
    icon: "🚨",
    label: "Break-Glass",
  },
  DOCUMENT: {
    icon: "▤",
    label: "Document",
  },
  AI_REVIEW: {
    icon: "✦",
    label: "AI Review",
  },
  INTEGRITY: {
    icon: "✓",
    label: "Integrity",
  },
  MODIFICATION: {
    icon: "✎",
    label: "Modification",
  },
  HISTORICAL_QUERY: {
    icon: "⌕",
    label: "Historical Query",
  },
}

function AuditType({ type }) {
  const config = typeConfig[type] || typeConfig.ACCESS

  return (
    <span className={`audit-type audit-type-${type.toLowerCase()}`}>
      <span>{config.icon}</span>
      {config.label}
    </span>
  )
}

function DoctorAudit() {
  const [filter, setFilter] = useState("ALL")
  const [search, setSearch] = useState("")
  const [selectedRecord, setSelectedRecord] = useState(null)

  const filteredRecords = auditRecords.filter((record) => {
    const matchesFilter =
      filter === "ALL" || record.type === filter

    const searchText = search.toLowerCase()

    const matchesSearch =
      record.patient.toLowerCase().includes(searchText) ||
      record.patientId.toLowerCase().includes(searchText) ||
      record.doctor.toLowerCase().includes(searchText) ||
      record.title.toLowerCase().includes(searchText)

    return matchesFilter && matchesSearch
  })

  return (
    <DashboardLayout
      role="doctor"
      userName="Dr. Priya Sharma"
    >
      <div className="doctor-page">

        {/* HEADER */}
        <div className="doctor-page-header">
          <div>
            <div className="doctor-eyebrow">
              TRANSPARENCY & ACCOUNTABILITY
            </div>

            <h1>Audit Trail</h1>

            <p>
              Review access, emergency actions, document activity,
              AI reviews, modifications and integrity verification.
            </p>
          </div>

          <div className="audit-live-status">
            <span></span>
            Audit Logging Active
          </div>
        </div>

        {/* TRANSPARENCY BANNER */}
        <div className="audit-info-banner">

          <div className="audit-info-icon">
            ◉
          </div>

          <div>
            <strong>
              Every sensitive action is recorded
            </strong>

            <p>
              Medi-Trace maintains an audit trail for patient
              access, break-glass authorization, medical document
              uploads, record modifications, historical queries
              and integrity verification.
            </p>
          </div>

        </div>

        {/* STATISTICS */}
        <div className="audit-stat-grid">

          <div className="audit-stat-card">
            <span className="audit-stat-icon">↗</span>
            <div>
              <small>Total Events</small>
              <strong>248</strong>
              <span>Recorded actions</span>
            </div>
          </div>

          <div className="audit-stat-card">
            <span className="audit-stat-icon emergency">🚨</span>
            <div>
              <small>Break-Glass Events</small>
              <strong>7</strong>
              <span>Emergency accesses</span>
            </div>
          </div>

          <div className="audit-stat-card">
            <span className="audit-stat-icon verification">✓</span>
            <div>
              <small>Verifications</small>
              <strong>42</strong>
              <span>Integrity checks</span>
            </div>
          </div>

          <div className="audit-stat-card">
            <span className="audit-stat-icon warning">!</span>
            <div>
              <small>Flagged Events</small>
              <strong>3</strong>
              <span>Require attention</span>
            </div>
          </div>

        </div>

        {/* FILTER TOOLBAR */}
        <div className="audit-toolbar">

          <div className="audit-search">
            <span>⌕</span>

            <input
              type="text"
              placeholder="Search patient, doctor or activity..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
            />
          </div>

          <div className="audit-filters">

            {[
              ["ALL", "All Activity"],
              ["ACCESS", "Access"],
              ["BREAK_GLASS", "Break-Glass"],
              ["DOCUMENT", "Documents"],
              ["AI_REVIEW", "AI Reviews"],
              ["INTEGRITY", "Integrity"],
              ["MODIFICATION", "Modifications"],
              ["HISTORICAL_QUERY", "Queries"],
            ].map(([value, label]) => (
              <button
                key={value}
                type="button"
                className={
                  filter === value
                    ? "audit-filter active"
                    : "audit-filter"
                }
                onClick={() => setFilter(value)}
              >
                {label}
              </button>
            ))}

          </div>

        </div>

        {/* AUDIT TABLE */}
        <div className="audit-table-card">

          <div className="audit-table-header">

            <div>
              <h2>Activity Log</h2>

              <span>
                Showing {filteredRecords.length} recent events
              </span>
            </div>

            <button
              type="button"
              className="audit-export-button"
              onClick={() =>
                alert("Demo: Audit export requested.")
              }
            >
              ↓ Export Audit Log
            </button>

          </div>

          <div className="audit-table-wrapper">

            <table className="audit-table">

              <thead>
                <tr>
                  <th>Activity</th>
                  <th>Patient</th>
                  <th>Performed By</th>
                  <th>Date & Time</th>
                  <th>Severity</th>
                  <th></th>
                </tr>
              </thead>

              <tbody>

                {filteredRecords.map((record) => (

                  <tr key={record.id}>

                    <td>
                      <div className="audit-activity">

                        <div className="audit-activity-icon">
                          {typeConfig[record.type]?.icon || "↗"}
                        </div>

                        <div>
                          <strong>{record.title}</strong>
                          <span>{record.id}</span>
                        </div>

                      </div>
                    </td>

                    <td>
                      <div className="audit-patient">

                        <strong>
                          {record.patient}
                        </strong>

                        <span>
                          {record.patientId}
                        </span>

                      </div>
                    </td>

                    <td>
                      <div className="audit-doctor">

                        <div className="audit-doctor-avatar">
                          {record.doctor
                            .replace("Dr. ", "")
                            .split(" ")
                            .map((word) => word[0])
                            .join("")
                            .slice(0, 2)}
                        </div>

                        <span>{record.doctor}</span>

                      </div>
                    </td>

                    <td>
                      <span className="audit-timestamp">
                        {record.timestamp}
                      </span>
                    </td>

                    <td>
                      <span
                        className={
                          record.severity === "HIGH"
                            ? "audit-severity high"
                            : "audit-severity normal"
                        }
                      >
                        {record.severity === "HIGH"
                          ? "Attention"
                          : "Normal"}
                      </span>
                    </td>

                    <td>

                      <button
                        type="button"
                        className="audit-view-button"
                        onClick={() =>
                          setSelectedRecord(record)
                        }
                      >
                        View →
                      </button>

                    </td>

                  </tr>

                ))}

              </tbody>

            </table>

            {filteredRecords.length === 0 && (
              <div className="audit-empty">
                No audit events match your search.
              </div>
            )}

          </div>

        </div>

        {/* AUDIT PRINCIPLES */}
        <div className="audit-principles">

          <div className="audit-principle-card">

            <div className="audit-principle-icon">
              🔐
            </div>

            <div>
              <h3>Access Transparency</h3>

              <p>
                Patient access and emergency access events are
                recorded so sensitive health information remains
                accountable.
              </p>
            </div>

          </div>

          <div className="audit-principle-card">

            <div className="audit-principle-icon">
              ✦
            </div>

            <div>
              <h3>AI Accountability</h3>

              <p>
                AI findings and historical queries can be traced
                back to the doctor workflow that initiated them.
              </p>
            </div>

          </div>

          <div className="audit-principle-card">

            <div className="audit-principle-icon">
              ⛓
            </div>

            <div>
              <h3>Integrity Traceability</h3>

              <p>
                Integrity verification activity records when
                provenance checks were performed and by whom.
              </p>
            </div>

          </div>

        </div>

      </div>

      {/* DETAILS MODAL */}
      {selectedRecord && (

        <div
          className="audit-modal-overlay"
          onClick={() => setSelectedRecord(null)}
        >

          <div
            className="audit-modal"
            onClick={(e) => e.stopPropagation()}
          >

            <div className="audit-modal-header">

              <div>
                <span>AUDIT EVENT</span>

                <h2>
                  {selectedRecord.title}
                </h2>
              </div>

              <button
                type="button"
                className="audit-close"
                onClick={() => setSelectedRecord(null)}
              >
                ×
              </button>

            </div>

            <div className="audit-modal-body">

              <AuditType type={selectedRecord.type} />

              <p className="audit-modal-description">
                {selectedRecord.description}
              </p>

              <div className="audit-detail-grid">

                <div>
                  <span>Audit ID</span>
                  <strong>{selectedRecord.id}</strong>
                </div>

                <div>
                  <span>Patient</span>
                  <strong>{selectedRecord.patient}</strong>
                </div>

                <div>
                  <span>Patient ID</span>
                  <strong>{selectedRecord.patientId}</strong>
                </div>

                <div>
                  <span>Performed By</span>
                  <strong>{selectedRecord.doctor}</strong>
                </div>

                <div>
                  <span>Date & Time</span>
                  <strong>{selectedRecord.timestamp}</strong>
                </div>

                <div>
                  <span>Severity</span>
                  <strong>
                    {selectedRecord.severity === "HIGH"
                      ? "Requires Attention"
                      : "Normal Activity"}
                  </strong>
                </div>

              </div>

              <div className="audit-reason-box">

                <span>RECORDED REASON / CONTEXT</span>

                <p>
                  {selectedRecord.reason}
                </p>

              </div>

              {selectedRecord.type === "BREAK_GLASS" && (
                <div className="audit-breakglass-note">

                  <strong>
                    🚨 Break-Glass Event
                  </strong>

                  <p>
                    This event represents emergency access.
                    The associated session provides read-only
                    emergency information and does not permit
                    modification of the patient's medical record.
                  </p>

                </div>
              )}

              {selectedRecord.type === "INTEGRITY" && (
                <div className="audit-integrity-note">

                  <strong>
                    ⛓ Integrity Activity
                  </strong>

                  <p>
                    This audit event records an integrity or
                    provenance verification action. Blockchain
                    verification provides provenance and does
                    not determine clinical truth.
                  </p>

                </div>
              )}

            </div>

            <div className="audit-modal-footer">

              <button
                type="button"
                className="audit-modal-close-button"
                onClick={() => setSelectedRecord(null)}
              >
                Close
              </button>

            </div>

          </div>

        </div>

      )}

    </DashboardLayout>
  )
}

export default DoctorAudit