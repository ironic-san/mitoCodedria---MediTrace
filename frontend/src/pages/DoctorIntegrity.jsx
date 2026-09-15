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

function StatusBadge({ status }) {
  const config = {
    MATCH: {
      className: "integrity-status-match",
      icon: "✓",
      label: "MATCH",
    },
    MISMATCH: {
      className: "integrity-status-mismatch",
      icon: "!",
      label: "MISMATCH",
    },
    "HISTORICAL RECORD MISSING": {
      className: "integrity-status-missing",
      icon: "⌁",
      label: "HISTORICAL RECORD MISSING",
    },
    "NO PROVENANCE": {
      className: "integrity-status-none",
      icon: "○",
      label: "NO PROVENANCE",
    },
    "PENDING / UNANCHORED": {
      className: "integrity-status-pending",
      icon: "◷",
      label: "PENDING / UNANCHORED",
    },
  }

  const item = config[status] || config["NO PROVENANCE"]

  return (
    <span className={`integrity-status ${item.className}`}>
      <span>{item.icon}</span>
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
      <div className="doctor-page">

        {/* HEADER */}
        <div className="doctor-page-header">
          <div>
            <div className="doctor-eyebrow">
              PROVENANCE & INTEGRITY
            </div>

            <h1>Integrity Verification</h1>

            <p>
              Verify that critical medical records remain consistent
              with their cryptographically anchored provenance.
            </p>
          </div>
        </div>

        {/* INFO BANNER */}
        <div className="integrity-info-banner">
          <div className="integrity-info-icon">⛓</div>

          <div>
            <strong>Blockchain provides provenance, not medical truth</strong>
            <p>
              Medi-Trace uses cryptographic hashes and Hyperledger
              Fabric to verify whether a record matches its anchored
              historical proof. Verification does not determine
              clinical correctness.
            </p>
          </div>
        </div>

        {/* SUMMARY CARDS */}
        <div className="integrity-summary-grid">

          <div className="integrity-summary-card">
            <div className="integrity-summary-icon match">✓</div>
            <div>
              <span>Verified Matches</span>
              <strong>{matchCount}</strong>
            </div>
          </div>

          <div className="integrity-summary-card">
            <div className="integrity-summary-icon mismatch">!</div>
            <div>
              <span>Mismatches</span>
              <strong>{mismatchCount}</strong>
            </div>
          </div>

          <div className="integrity-summary-card">
            <div className="integrity-summary-icon missing">⌁</div>
            <div>
              <span>Missing Records</span>
              <strong>{missingCount}</strong>
            </div>
          </div>

          <div className="integrity-summary-card">
            <div className="integrity-summary-icon none">○</div>
            <div>
              <span>No Provenance</span>
              <strong>{noProvenanceCount}</strong>
            </div>
          </div>

        </div>

        {/* TOOLBAR */}
        <div className="integrity-toolbar">

          <div className="integrity-search">
            <span>⌕</span>

            <input
              type="text"
              placeholder="Search patient or medical event..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
            />
          </div>

          <div className="integrity-filters">

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

        {/* RECORD TABLE */}
        <div className="integrity-table-card">

          <div className="integrity-table-header">
            <div>
              <h2>Integrity Records</h2>
              <span>
                {filteredRecords.length} records displayed
              </span>
            </div>

            <div className="blockchain-network">
              <span className="network-dot"></span>
              Hyperledger Fabric
            </div>
          </div>

          <div className="integrity-table-wrapper">

            <table className="integrity-table">

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
                      <div className="integrity-patient">
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
                      <div className="integrity-event">
                        <strong>{record.event}</strong>
                        <span>{record.eventType}</span>
                      </div>
                    </td>

                    <td>{record.eventDate}</td>

                    <td>
                      <span className="version-badge">
                        {record.version}
                      </span>
                    </td>

                    <td>
                      <StatusBadge status={record.status} />
                    </td>

                    <td>
                      <button
                        type="button"
                        className="integrity-view-button"
                        onClick={() => setSelectedRecord(record)}
                      >
                        View Details →
                      </button>
                    </td>

                  </tr>

                ))}

              </tbody>

            </table>

            {filteredRecords.length === 0 && (
              <div className="integrity-empty">
                No integrity records match your search.
              </div>
            )}

          </div>

        </div>

        {/* EXPLANATION */}
        <div className="integrity-explanation-grid">

          <div className="integrity-explanation-card">

            <div className="explanation-icon">#</div>

            <div>
              <h3>How verification works</h3>

              <p>
                An approved critical medical event is converted
                into a canonical representation. Medi-Trace
                generates a SHA-256 hash and anchors that hash
                through the blockchain service.
              </p>

              <div className="verification-flow">
                <span>Medical Event</span>
                <b>→</b>
                <span>Canonical Data</span>
                <b>→</b>
                <span>SHA-256</span>
                <b>→</b>
                <span>Fabric Proof</span>
              </div>
            </div>

          </div>

          <div className="integrity-explanation-card">

            <div className="explanation-icon">!</div>

            <div>
              <h3>Important clinical note</h3>

              <p>
                A MATCH only means that the current record
                corresponds to the anchored proof. A MISMATCH
                or missing record should be reviewed by the
                doctor and does not automatically mean the
                medical information is false.
              </p>
            </div>

          </div>

        </div>

      </div>

      {/* DETAILS MODAL */}
      {selectedRecord && (

        <div
          className="integrity-modal-overlay"
          onClick={() => setSelectedRecord(null)}
        >

          <div
            className="integrity-modal"
            onClick={(e) => e.stopPropagation()}
          >

            <div className="integrity-modal-header">

              <div>
                <span>INTEGRITY RECORD</span>
                <h2>{selectedRecord.event}</h2>
              </div>

              <button
                type="button"
                className="integrity-close"
                onClick={() => setSelectedRecord(null)}
              >
                ×
              </button>

            </div>

            <div className="integrity-modal-status">
              <StatusBadge status={selectedRecord.status} />

              <p>{selectedRecord.description}</p>
            </div>

            <div className="integrity-detail-grid">

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

            </div>

            <div className="integrity-hash-box">

              <span>SHA-256 EVENT HASH</span>

              <code>
                {selectedRecord.hash || "No hash available"}
              </code>

            </div>

            {selectedRecord.status === "MISMATCH" && (

              <div className="integrity-warning-box">

                <strong>Doctor review required</strong>

                <p>
                  The current structured record differs from
                  historical evidence. Review the underlying
                  medical document and update the record only
                  after clinical verification.
                </p>

              </div>

            )}

            {selectedRecord.status ===
              "HISTORICAL RECORD MISSING" && (

              <div className="integrity-warning-box">

                <strong>Historical record unavailable</strong>

                <p>
                  Blockchain provenance confirms that a proof
                  was previously anchored, but the corresponding
                  current database record is unavailable.
                  The blockchain does not recover deleted
                  medical data.
                </p>

              </div>

            )}

            <div className="integrity-modal-footer">

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
              </button>

            </div>

          </div>

        </div>

      )}

    </DashboardLayout>
  )
}

export default DoctorIntegrity