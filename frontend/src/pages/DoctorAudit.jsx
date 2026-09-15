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
    reason:
      "Critical allergy information required during emergency presentation.",
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
    label: "Record Access",
    short: "Access",
    icon: "↗",
  },
  BREAK_GLASS: {
    label: "Break-Glass",
    short: "Emergency",
    icon: "!",
  },
  DOCUMENT: {
    label: "Document",
    short: "Document",
    icon: "▤",
  },
  AI_REVIEW: {
    label: "AI Review",
    short: "AI",
    icon: "✦",
  },
  INTEGRITY: {
    label: "Integrity",
    short: "Integrity",
    icon: "✓",
  },
  MODIFICATION: {
    label: "Modification",
    short: "Modified",
    icon: "✎",
  },
  HISTORICAL_QUERY: {
    label: "Historical Query",
    short: "Query",
    icon: "⌕",
  },
}

function Icon({ name, size = 18 }) {
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
    search: (
      <>
        <circle cx="11" cy="11" r="6.5" />
        <path d="m16 16 4 4" />
      </>
    ),

    download: (
      <>
        <path d="M12 3v12" />
        <path d="m7 10 5 5 5-5" />
        <path d="M4 20h16" />
      </>
    ),

    clock: (
      <>
        <circle cx="12" cy="12" r="8.5" />
        <path d="M12 7v5l3 2" />
      </>
    ),

    shield: (
      <>
        <path d="M12 3l8 3v5c0 5-3.3 8.4-8 10-4.7-1.6-8-5-8-10V6l8-3z" />
        <path d="m9 12 2 2 4-4" />
      </>
    ),

    lock: (
      <>
        <rect x="5" y="10" width="14" height="11" rx="2" />
        <path d="M8 10V7a4 4 0 0 1 8 0v3" />
      </>
    ),

    alert: (
      <>
        <path d="M10.3 3.8 2.2 18a2 2 0 0 0 1.7 3h16.2a2 2 0 0 0 1.7-3L13.7 3.8a2 2 0 0 0-3.4 0z" />
        <path d="M12 9v4M12 17h.01" />
      </>
    ),

    close: (
      <>
        <path d="m6 6 12 12M18 6 6 18" />
      </>
    ),

    file: (
      <>
        <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
        <path d="M14 2v6h6M8 13h8M8 17h5" />
      </>
    ),

    user: (
      <>
        <circle cx="12" cy="8" r="3.5" />
        <path d="M5 21a7 7 0 0 1 14 0" />
      </>
    ),
  }

  return <svg {...common}>{icons[name]}</svg>
}

function AuditType({ type }) {
  const config = typeConfig[type] || typeConfig.ACCESS

  return (
    <span className={`audit-type polished-audit-type audit-${type.toLowerCase()}`}>
      <span className="audit-type-symbol">{config.icon}</span>
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

    const searchText = search.toLowerCase().trim()

    const matchesSearch =
      !searchText ||
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
      <div className="doctor-page polished-audit-page">

        {/* HEADER */}
        <div className="doctor-page-header polished-audit-header">

          <div>
            <div className="doctor-eyebrow audit-eyebrow">
              <span>
                <Icon name="shield" size={13} />
              </span>
              TRANSPARENCY & ACCOUNTABILITY
            </div>

            <h1>Audit Trail</h1>

            <p>
              Review access, emergency actions, document activity,
              AI reviews, modifications and integrity verification.
            </p>
          </div>

          <div className="audit-live-status polished-live-status">
            <span></span>
            <div>
              <strong>Audit Logging Active</strong>
              <small>All sensitive actions are recorded</small>
            </div>
          </div>

        </div>

        {/* INFO BANNER */}
        <div className="audit-info-banner polished-audit-banner">

          <div className="audit-info-icon polished-audit-info-icon">
            <Icon name="shield" size={19} />
          </div>

          <div>
            <strong>Every sensitive action is recorded</strong>

            <p>
              Medi-Trace maintains an audit trail for patient access,
              break-glass authorization, document uploads, record
              modifications, historical queries and integrity verification.
            </p>
          </div>

          <div className="audit-banner-badge">
            <Icon name="lock" size={11} />
            ACCOUNTABLE
          </div>

        </div>

        {/* STATISTICS */}
        <div className="audit-stat-grid polished-audit-stat-grid">

          <div className="audit-stat-card polished-audit-stat-card">
            <span className="audit-stat-icon access">
              <Icon name="clock" size={17} />
            </span>

            <div>
              <small>Total Events</small>
              <strong>248</strong>
              <span>Recorded actions</span>
            </div>
          </div>

          <div className="audit-stat-card polished-audit-stat-card">
            <span className="audit-stat-icon emergency">
              <Icon name="alert" size={17} />
            </span>

            <div>
              <small>Break-Glass Events</small>
              <strong>7</strong>
              <span>Emergency accesses</span>
            </div>
          </div>

          <div className="audit-stat-card polished-audit-stat-card">
            <span className="audit-stat-icon verification">
              <Icon name="shield" size={17} />
            </span>

            <div>
              <small>Verifications</small>
              <strong>42</strong>
              <span>Integrity checks</span>
            </div>
          </div>

          <div className="audit-stat-card polished-audit-stat-card">
            <span className="audit-stat-icon warning">
              <Icon name="alert" size={17} />
            </span>

            <div>
              <small>Flagged Events</small>
              <strong>3</strong>
              <span>Require attention</span>
            </div>
          </div>

        </div>

        {/* TOOLBAR */}
        <div className="audit-toolbar polished-audit-toolbar">

          <div className="audit-search polished-audit-search">
            <Icon name="search" size={16} />

            <input
              type="text"
              placeholder="Search patient, doctor or activity..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
            />

            {search && (
              <button
                type="button"
                className="audit-clear-search"
                onClick={() => setSearch("")}
              >
                <Icon name="close" size={12} />
              </button>
            )}
          </div>

          <div className="audit-filters polished-audit-filters">
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
                    ? "audit-filter polished-audit-filter active"
                    : "audit-filter polished-audit-filter"
                }
                onClick={() => setFilter(value)}
              >
                {label}
              </button>
            ))}
          </div>

        </div>

        {/* TABLE */}
        <div className="audit-table-card polished-audit-table-card">

          <div className="audit-table-header polished-audit-table-header">

            <div>
              <span className="audit-table-eyebrow">
                SECURITY LOG
              </span>

              <h2>Activity Log</h2>

              <span>
                Showing {filteredRecords.length} recent events
              </span>
            </div>

            <button
              type="button"
              className="audit-export-button polished-export-button"
              onClick={() =>
                alert("Demo: Audit export requested.")
              }
            >
              <Icon name="download" size={14} />
              Export Audit Log
            </button>

          </div>

          <div className="audit-table-wrapper">

            <table className="audit-table polished-audit-table">

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
                      <div className="audit-activity polished-audit-activity">

                        <div
                          className={`audit-activity-icon audit-icon-${record.type.toLowerCase()}`}
                        >
                          {typeConfig[record.type]?.icon || "↗"}
                        </div>

                        <div>
                          <strong>{record.title}</strong>
                          <span>{record.id}</span>
                        </div>

                      </div>
                    </td>

                    <td>
                      <div className="audit-patient polished-audit-patient">

                        <strong>{record.patient}</strong>

                        <span>{record.patientId}</span>

                      </div>
                    </td>

                    <td>
                      <div className="audit-doctor polished-audit-doctor">

                        <div className="audit-doctor-avatar polished-doctor-avatar">
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
                      <span className="audit-timestamp polished-audit-timestamp">
                        {record.timestamp}
                      </span>
                    </td>

                    <td>
                      <span
                        className={
                          record.severity === "HIGH"
                            ? "audit-severity high polished-severity"
                            : "audit-severity normal polished-severity"
                        }
                      >
                        <span></span>
                        {record.severity === "HIGH"
                          ? "Attention"
                          : "Normal"}
                      </span>
                    </td>

                    <td>
                      <button
                        type="button"
                        className="audit-view-button polished-audit-view"
                        onClick={() => setSelectedRecord(record)}
                      >
                        View
                        <span>→</span>
                      </button>
                    </td>

                  </tr>

                ))}

              </tbody>

            </table>

            {filteredRecords.length === 0 && (
              <div className="audit-empty polished-audit-empty">
                <Icon name="search" size={25} />
                <strong>No audit events found</strong>
                <span>
                  Try changing the search text or activity filter.
                </span>
              </div>
            )}

          </div>
        </div>

        {/* PRINCIPLES */}
        <div className="audit-principles polished-audit-principles">

          <div className="audit-principle-card polished-principle-card">
            <div className="audit-principle-icon">
              <Icon name="lock" size={17} />
            </div>

            <div>
              <h3>Access Transparency</h3>
              <p>
                Patient access and emergency access events are
                recorded so sensitive health information remains accountable.
              </p>
            </div>
          </div>

          <div className="audit-principle-card polished-principle-card">
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

          <div className="audit-principle-card polished-principle-card">
            <div className="audit-principle-icon">
              <Icon name="shield" size={17} />
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
          className="audit-modal-overlay polished-audit-modal-overlay"
          onClick={() => setSelectedRecord(null)}
        >
          <div
            className="audit-modal polished-audit-modal"
            onClick={(e) => e.stopPropagation()}
          >

            <div className="audit-modal-header polished-modal-header">

              <div>
                <span className="modal-event-label">
                  AUDIT EVENT · {selectedRecord.id}
                </span>

                <h2>{selectedRecord.title}</h2>
              </div>

              <button
                type="button"
                className="audit-close polished-audit-close"
                onClick={() => setSelectedRecord(null)}
              >
                <Icon name="close" size={16} />
              </button>

            </div>

            <div className="audit-modal-body polished-modal-body">

              <AuditType type={selectedRecord.type} />

              <p className="audit-modal-description polished-modal-description">
                {selectedRecord.description}
              </p>

              <div className="audit-detail-grid polished-audit-detail-grid">

                <div>
                  <span>Audit ID</span>
                  <strong>{selectedRecord.id}</strong>
                </div>

                <div>
                  <span>Activity Type</span>
                  <strong>
                    {typeConfig[selectedRecord.type]?.label}
                  </strong>
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

              </div>

              <div className="audit-reason-box polished-reason-box">
                <span>RECORDED REASON / CONTEXT</span>

                <p>{selectedRecord.reason}</p>
              </div>

              {selectedRecord.type === "BREAK_GLASS" && (
                <div className="audit-breakglass-note polished-audit-note emergency-note">
                  <div>
                    <Icon name="alert" size={16} />
                  </div>

                  <section>
                    <strong>Break-Glass Event</strong>

                    <p>
                      This event represents emergency access. The
                      associated session provides read-only emergency
                      information and does not permit modification of
                      the patient's medical record.
                    </p>
                  </section>
                </div>
              )}

              {selectedRecord.type === "INTEGRITY" && (
                <div className="audit-integrity-note polished-audit-note integrity-note">
                  <div>
                    <Icon name="shield" size={16} />
                  </div>

                  <section>
                    <strong>Integrity Activity</strong>

                    <p>
                      This audit event records an integrity or
                      provenance verification action. Blockchain
                      verification provides provenance and does not
                      determine clinical truth.
                    </p>
                  </section>
                </div>
              )}

            </div>

            <div className="audit-modal-footer polished-modal-footer">

              <span>
                <Icon name="lock" size={12} />
                Audit record
              </span>

              <button
                type="button"
                className="audit-modal-close-button polished-modal-close-button"
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