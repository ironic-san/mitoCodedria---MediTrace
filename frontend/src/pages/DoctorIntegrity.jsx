import { useState } from "react"
import DashboardLayout from "../layouts/DashboardLayout"

const integrityRecords = [
  {
    id: "INT-001",
    patient: "Kabir Malhotra",
    patientId: "PT-KABIR-005",
    event: "Severe Penicillin Allergy",
    eventType: "ALLERGY",
    eventDate: "12 Mar 2019",
    version: "v1",
    status: "MATCH",
    description:
      "The current medical record matches the cryptographically anchored blockchain proof.",
    hash: "8c4f91d7a2b6...e93c",
    transactionId: "TX-7F29A81C",
    proofId: "PROOF-KABIR-001",
    network: "Hyperledger Fabric",
  },
  {
    id: "INT-002",
    patient: "Kabir Malhotra",
    patientId: "PT-KABIR-005",
    event: "Historical Emergency Event",
    eventType: "MEDICAL EVENT",
    eventDate: "18 Jan 2024",
    version: "v1",
    status: "HISTORICAL RECORD MISSING",
    description:
      "A blockchain proof exists for this event, but the corresponding current database record could not be found.",
    hash: "4d8e72c91f03...a71b",
    transactionId: "TX-91BC72DE",
    proofId: "PROOF-KABIR-002",
    network: "Hyperledger Fabric",
  },
  {
    id: "INT-003",
    patient: "Tanya Bose",
    patientId: "PT-TANYA-006",
    event: "Brain Surgery",
    eventType: "PROCEDURE",
    eventDate: "10 Sep 2025",
    version: "v2",
    status: "MISMATCH",
    description:
      "The current database record differs from the historical evidence associated with the anchored event.",
    hash: "2fa7d8b14c65...9a20",
    transactionId: "TX-44AE19BC",
    proofId: "PROOF-TANYA-001",
    network: "Hyperledger Fabric",
  },
  {
    id: "INT-004",
    patient: "Aarav Mehta",
    patientId: "PT-AARAV-001",
    event: "Femur Fracture Fixation",
    eventType: "PROCEDURE",
    eventDate: "22 Aug 2023",
    version: "v1",
    status: "MATCH",
    description:
      "The current procedure record matches the anchored integrity proof.",
    hash: "91ab43e7c812...c920",
    transactionId: "TX-83D4F12A",
    proofId: "PROOF-AARAV-001",
    network: "Hyperledger Fabric",
  },
  {
    id: "INT-005",
    patient: "Ishita Kapoor",
    patientId: "PT-ISHITA-002",
    event: "Diabetes Diagnosis",
    eventType: "CONDITION",
    eventDate: "06 Jun 2021",
    version: "v1",
    status: "NO PROVENANCE",
    description:
      "A current medical record exists, but no blockchain provenance record is available.",
    hash: null,
    transactionId: null,
    proofId: null,
    network: null,
  },
]

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
    shield: (
      <>
        <path d="M12 3l8 3v5c0 5.2-3.4 8.5-8 10-4.6-1.5-8-4.8-8-10V6l8-3z" />
        <path d="m9 12 2 2 4-4" />
      </>
    ),

    link: (
      <>
        <path d="M10 13a5 5 0 0 0 7.1.1l2-2a5 5 0 0 0-7.1-7.1l-1.1 1.1" />
        <path d="M14 11a5 5 0 0 0-7.1-.1l-2 2A5 5 0 0 0 12 20l1.1-1.1" />
      </>
    ),

    search: (
      <>
        <circle cx="11" cy="11" r="7" />
        <path d="m20 20-4-4" />
      </>
    ),

    check: <path d="m5 12 4 4L19 6" />,

    alert: (
      <>
        <path d="M10.3 3.8 2.2 18a2 2 0 0 0 1.7 3h16.2a2 2 0 0 0 1.7-3L13.7 3.8a2 2 0 0 0-3.4 0z" />
        <path d="M12 9v4M12 17h.01" />
      </>
    ),

    database: (
      <>
        <ellipse cx="12" cy="5" rx="8" ry="3" />
        <path d="M4 5v7c0 1.7 3.6 3 8 3s8-1.3 8-3V5" />
        <path d="M4 12v7c0 1.7 3.6 3 8 3s8-1.3 8-3v-7" />
      </>
    ),

    hash: (
      <>
        <path d="M10 3 8 21M16 3l-2 18M4 9h17M3 15h17" />
      </>
    ),

    file: (
      <>
        <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
        <path d="M14 2v6h6" />
        <path d="M8 13h8M8 17h5" />
      </>
    ),

    close: (
      <>
        <path d="m6 6 12 12M18 6 6 18" />
      </>
    ),

    arrow: (
      <>
        <path d="M5 12h14" />
        <path d="m13 6 6 6-6 6" />
      </>
    ),
  }

  return <svg {...common}>{icons[name]}</svg>
}

function StatusBadge({ status }) {
  const config = {
    MATCH: {
      className: "integrity-status-match",
      icon: <Icon name="check" size={12} />,
      label: "MATCH",
    },

    MISMATCH: {
      className: "integrity-status-mismatch",
      icon: <Icon name="alert" size={12} />,
      label: "MISMATCH",
    },

    "HISTORICAL RECORD MISSING": {
      className: "integrity-status-missing",
      icon: <Icon name="database" size={12} />,
      label: "HISTORICAL RECORD MISSING",
    },

    "NO PROVENANCE": {
      className: "integrity-status-none",
      icon: <Icon name="link" size={12} />,
      label: "NO PROVENANCE",
    },

    "PENDING / UNANCHORED": {
      className: "integrity-status-pending",
      icon: <Icon name="database" size={12} />,
      label: "PENDING / UNANCHORED",
    },
  }

  const item = config[status] || config["NO PROVENANCE"]

  return (
    <span className={`integrity-status ${item.className}`}>
      <span className="integrity-status-icon">{item.icon}</span>
      {item.label}
    </span>
  )
}

function DoctorIntegrity() {
  const [selectedRecord, setSelectedRecord] = useState(null)
  const [filter, setFilter] = useState("ALL")
  const [search, setSearch] = useState("")

  const filteredRecords = integrityRecords.filter((record) => {
    const matchesFilter =
      filter === "ALL" || record.status === filter

    const searchText = search.toLowerCase()

    const matchesSearch =
      record.patient.toLowerCase().includes(searchText) ||
      record.patientId.toLowerCase().includes(searchText) ||
      record.event.toLowerCase().includes(searchText)

    return matchesFilter && matchesSearch
  })

  const matchCount = integrityRecords.filter(
    (item) => item.status === "MATCH"
  ).length

  const mismatchCount = integrityRecords.filter(
    (item) => item.status === "MISMATCH"
  ).length

  const missingCount = integrityRecords.filter(
    (item) => item.status === "HISTORICAL RECORD MISSING"
  ).length

  const noProvenanceCount = integrityRecords.filter(
    (item) => item.status === "NO PROVENANCE"
  ).length

  return (
    <DashboardLayout
      role="doctor"
      userName="Dr. Priya Sharma"
    >
      <div className="doctor-page polished-integrity-page">

        {/* HEADER */}
        <div className="doctor-page-header integrity-polished-header">
          <div>
            <div className="doctor-eyebrow integrity-eyebrow">
              <span>
                <Icon name="shield" size={14} />
              </span>
              PROVENANCE & INTEGRITY
            </div>

            <h1>Integrity Verification</h1>

            <p>
              Verify that critical medical records remain consistent with
              their cryptographically anchored provenance.
            </p>
          </div>

          <div className="integrity-network-status">
            <span className="network-status-dot"></span>

            <div>
              <strong>Fabric Network Active</strong>
              <small>Provenance verification available</small>
            </div>
          </div>
        </div>

        {/* INFO BANNER */}
        <div className="integrity-info-banner polished-integrity-info">
          <div className="integrity-info-icon polished-info-icon">
            <Icon name="link" size={21} />
          </div>

          <div className="integrity-info-content">
            <div className="info-title-row">
              <strong>Blockchain provides provenance, not medical truth</strong>
              <span>VERIFICATION LAYER</span>
            </div>

            <p>
              Medi-Trace uses cryptographic hashes and Hyperledger Fabric to
              verify whether a record matches its anchored historical proof.
              Verification does not determine clinical correctness.
            </p>
          </div>
        </div>

        {/* SUMMARY */}
        <div className="integrity-summary-grid polished-integrity-summary">

          <div className="integrity-summary-card polished-integrity-card match-card">
            <div className="integrity-summary-icon match">
              <Icon name="check" size={19} />
            </div>

            <div>
              <span>Verified Matches</span>
              <strong>{matchCount}</strong>
              <small>Cryptographic match</small>
            </div>
          </div>

          <div className="integrity-summary-card polished-integrity-card mismatch-card">
            <div className="integrity-summary-icon mismatch">
              <Icon name="alert" size={18} />
            </div>

            <div>
              <span>Mismatches</span>
              <strong>{mismatchCount}</strong>
              <small>Requires review</small>
            </div>
          </div>

          <div className="integrity-summary-card polished-integrity-card missing-card">
            <div className="integrity-summary-icon missing">
              <Icon name="database" size={18} />
            </div>

            <div>
              <span>Missing Records</span>
              <strong>{missingCount}</strong>
              <small>Proof exists, record missing</small>
            </div>
          </div>

          <div className="integrity-summary-card polished-integrity-card none-card">
            <div className="integrity-summary-icon none">
              <Icon name="link" size={18} />
            </div>

            <div>
              <span>No Provenance</span>
              <strong>{noProvenanceCount}</strong>
              <small>No blockchain proof</small>
            </div>
          </div>

        </div>

        {/* TOOLBAR */}
        <div className="integrity-toolbar polished-integrity-toolbar">

          <div className="integrity-search polished-integrity-search">
            <Icon name="search" size={17} />

            <input
              type="text"
              placeholder="Search patient, ID or medical event..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
            />

            {search && (
              <button
                type="button"
                className="clear-integrity-search"
                onClick={() => setSearch("")}
              >
                <Icon name="close" size={13} />
              </button>
            )}
          </div>

          <div className="integrity-filters polished-integrity-filters">
            {[
              "ALL",
              "MATCH",
              "MISMATCH",
              "HISTORICAL RECORD MISSING",
              "NO PROVENANCE",
            ].map((item) => (
              <button
                key={item}
                type="button"
                className={
                  filter === item
                    ? "integrity-filter active"
                    : "integrity-filter"
                }
                onClick={() => setFilter(item)}
              >
                {item === "ALL"
                  ? "All Records"
                  : item === "HISTORICAL RECORD MISSING"
                    ? "Missing"
                    : item === "NO PROVENANCE"
                      ? "No Provenance"
                      : item}
              </button>
            ))}
          </div>
        </div>

        {/* TABLE */}
        <div className="integrity-table-card polished-integrity-table-card">

          <div className="integrity-table-header polished-table-header">
            <div>
              <div className="table-title-row">
                <div className="table-title-icon">
                  <Icon name="database" size={18} />
                </div>

                <div>
                  <h2>Integrity Records</h2>
                  <span>
                    {filteredRecords.length} of {integrityRecords.length} records
                  </span>
                </div>
              </div>
            </div>

            <div className="blockchain-network polished-blockchain-network">
              <span className="network-dot"></span>
              <div>
                <strong>Hyperledger Fabric</strong>
                <small>Blockchain provenance</small>
              </div>
            </div>
          </div>

          <div className="integrity-table-wrapper">
            <table className="integrity-table polished-integrity-table">

              <thead>
                <tr>
                  <th>Patient</th>
                  <th>Medical Event</th>
                  <th>Event Date</th>
                  <th>Version</th>
                  <th>Verification</th>
                  <th>Action</th>
                </tr>
              </thead>

              <tbody>
                {filteredRecords.map((record) => (
                  <tr key={record.id}>

                    <td>
                      <div className="integrity-patient polished-integrity-patient">
                        <div className="integrity-avatar">
                          {record.patient
                            .split(" ")
                            .map((word) => word[0])
                            .join("")
                            .slice(0, 2)}
                        </div>

                        <div>
                          <strong>{record.patient}</strong>
                          <span>{record.patientId}</span>
                        </div>
                      </div>
                    </td>

                    <td>
                      <div className="integrity-event polished-integrity-event">
                        <strong>{record.event}</strong>
                        <span>{record.eventType}</span>
                      </div>
                    </td>

                    <td>
                      <span className="integrity-date">
                        {record.eventDate}
                      </span>
                    </td>

                    <td>
                      <span className="version-badge polished-version-badge">
                        {record.version}
                      </span>
                    </td>

                    <td>
                      <StatusBadge status={record.status} />
                    </td>

                    <td>
                      <button
                        type="button"
                        className="integrity-view-button polished-integrity-view"
                        onClick={() => setSelectedRecord(record)}
                      >
                        View
                        <Icon name="arrow" size={14} />
                      </button>
                    </td>

                  </tr>
                ))}
              </tbody>

            </table>

            {filteredRecords.length === 0 && (
              <div className="integrity-empty polished-integrity-empty">
                <Icon name="search" size={25} />
                <strong>No matching records</strong>
                <span>
                  Try changing the search text or verification filter.
                </span>
              </div>
            )}
          </div>
        </div>

        {/* VERIFICATION ARCHITECTURE */}
        <div className="integrity-explanation-grid polished-explanation-grid">

          <div className="integrity-explanation-card polished-explanation-card">
            <div className="explanation-icon polished-explanation-icon">
              <Icon name="hash" size={20} />
            </div>

            <div className="explanation-content">
              <div className="explanation-heading">
                <span className="explanation-label">
                  VERIFICATION PIPELINE
                </span>
                <h3>How verification works</h3>
              </div>

              <p>
                An approved critical medical event is converted into a
                canonical representation. Medi-Trace generates a SHA-256 hash
                and anchors that hash through the blockchain service.
              </p>

              <div className="verification-flow polished-verification-flow">
                <div>
                  <span>01</span>
                  <strong>Medical Event</strong>
                </div>

                <b>→</b>

                <div>
                  <span>02</span>
                  <strong>Canonical Data</strong>
                </div>

                <b>→</b>

                <div>
                  <span>03</span>
                  <strong>SHA-256</strong>
                </div>

                <b>→</b>

                <div>
                  <span>04</span>
                  <strong>Fabric Proof</strong>
                </div>
              </div>
            </div>
          </div>

          <div className="integrity-explanation-card polished-explanation-card clinical-note-card">
            <div className="explanation-icon clinical-note-icon">
              <Icon name="shield" size={20} />
            </div>

            <div className="explanation-content">
              <div className="explanation-heading">
                <span className="explanation-label">
                  CLINICAL INTERPRETATION
                </span>
                <h3>Important clinical note</h3>
              </div>

              <p>
                A <strong>MATCH</strong> only means that the current record
                corresponds to the anchored proof. A <strong>MISMATCH</strong>{" "}
                or missing record should be reviewed by the doctor and does not
                automatically mean the medical information is false.
              </p>

              <div className="clinical-note-footer">
                <Icon name="alert" size={14} />
                <span>Doctor review remains the final authority.</span>
              </div>
            </div>
          </div>

        </div>

      </div>

      {/* DETAILS MODAL */}
      {selectedRecord && (
        <div
          className="integrity-modal-overlay polished-integrity-overlay"
          onClick={() => setSelectedRecord(null)}
        >
          <div
            className="integrity-modal polished-integrity-modal"
            onClick={(e) => e.stopPropagation()}
          >

            <div className="integrity-modal-header polished-modal-header">
              <div>
                <span>INTEGRITY RECORD</span>
                <h2>{selectedRecord.event}</h2>
                <small>
                  {selectedRecord.id} · {selectedRecord.eventType}
                </small>
              </div>

              <button
                type="button"
                className="integrity-close polished-integrity-close"
                onClick={() => setSelectedRecord(null)}
              >
                <Icon name="close" size={17} />
              </button>
            </div>

            <div className="integrity-modal-status polished-modal-status">
              <StatusBadge status={selectedRecord.status} />

              <p>{selectedRecord.description}</p>
            </div>

            <div className="integrity-detail-grid polished-detail-grid">

              <div>
                <span>Patient</span>
                <strong>{selectedRecord.patient}</strong>
              </div>

              <div>
                <span>Patient ID</span>
                <strong>{selectedRecord.patientId}</strong>
              </div>

              <div>
                <span>Event Date</span>
                <strong>{selectedRecord.eventDate}</strong>
              </div>

              <div>
                <span>Version</span>
                <strong>{selectedRecord.version}</strong>
              </div>

              <div>
                <span>Proof ID</span>
                <strong>
                  {selectedRecord.proofId || "Not available"}
                </strong>
              </div>

              <div>
                <span>Transaction ID</span>
                <strong>
                  {selectedRecord.transactionId || "Not available"}
                </strong>
              </div>

              <div>
                <span>Network</span>
                <strong>
                  {selectedRecord.network || "Not available"}
                </strong>
              </div>

              <div>
                <span>Event Type</span>
                <strong>{selectedRecord.eventType}</strong>
              </div>

            </div>

            <div className="integrity-hash-box polished-hash-box">
              <div className="hash-heading">
                <Icon name="hash" size={15} />
                <span>SHA-256 EVENT HASH</span>
              </div>

              <code>
                {selectedRecord.hash || "No hash available"}
              </code>
            </div>

            {selectedRecord.status === "MATCH" && (
              <div className="integrity-result-box result-match">
                <div>
                  <Icon name="check" size={17} />
                </div>

                <section>
                  <strong>Cryptographic verification passed</strong>
                  <p>
                    The current record corresponds to the anchored provenance
                    proof for this event.
                  </p>
                </section>
              </div>
            )}

            {selectedRecord.status === "MISMATCH" && (
              <div className="integrity-warning-box polished-warning-box">
                <div>
                  <Icon name="alert" size={17} />
                </div>

                <section>
                  <strong>Doctor review required</strong>
                  <p>
                    The current structured record differs from historical
                    evidence. Review the underlying medical document and update
                    the record only after clinical verification.
                  </p>
                </section>
              </div>
            )}

            {selectedRecord.status ===
              "HISTORICAL RECORD MISSING" && (
                <div className="integrity-warning-box polished-warning-box">
                  <div>
                    <Icon name="database" size={17} />
                  </div>

                  <section>
                    <strong>Historical record unavailable</strong>
                    <p>
                      Blockchain provenance confirms that a proof was
                      previously anchored, but the corresponding current
                      database record is unavailable. The blockchain does not
                      recover deleted medical data.
                    </p>
                  </section>
                </div>
              )}

            {selectedRecord.status === "NO PROVENANCE" && (
              <div className="integrity-neutral-box">
                <div>
                  <Icon name="link" size={17} />
                </div>

                <section>
                  <strong>No blockchain provenance available</strong>
                  <p>
                    A current medical record exists, but no corresponding
                    blockchain proof is available for verification.
                  </p>
                </section>
              </div>
            )}

            <div className="integrity-modal-footer polished-modal-footer">
              <button
                type="button"
                className="integrity-secondary-button"
                onClick={() => setSelectedRecord(null)}
              >
                Close
              </button>

              <button
                type="button"
                className="integrity-primary-button"
                onClick={() => setSelectedRecord(null)}
              >
                Open Patient Record
                <Icon name="arrow" size={14} />
              </button>
            </div>

          </div>
        </div>
      )}
    </DashboardLayout>
  )
}

export default DoctorIntegrity