import { useEffect, useState } from "react";

function Provenance() {
  const [records, setRecords] = useState([]);
  const [verification, setVerification] = useState(null);
  const [selectedCard, setSelectedCard] = useState("");
  const [cardTraceability, setCardTraceability] =
    useState(null);

  const [loading, setLoading] = useState(true);
  const [verifyLoading, setVerifyLoading] =
    useState(false);
  const [traceLoading, setTraceLoading] =
    useState(false);
  const [error, setError] = useState(null);

  const API = "http://127.0.0.1:8000";

  // =====================================================
  // LOAD PROVENANCE RECORDS
  // =====================================================

  const loadRecords = async () => {
    try {
      setLoading(true);
      setError(null);

      const response = await fetch(
        `${API}/provenance/`
      );

      if (!response.ok) {
        throw new Error(
          `Failed to load provenance records (${response.status})`
        );
      }

      const data = await response.json();

      setRecords(
        Array.isArray(data)
          ? data
          : data.records || []
      );

    } catch (err) {
      console.error(
        "Provenance records error:",
        err
      );

      setError(
        "Unable to load provenance records from the backend."
      );
    } finally {
      setLoading(false);
    }
  };

  // =====================================================
  // VERIFY CHAIN
  // =====================================================

  const verifyChain = async () => {
    try {
      setVerifyLoading(true);

      const response = await fetch(
        `${API}/provenance/verify`
      );

      if (!response.ok) {
        throw new Error(
          `Verification failed (${response.status})`
        );
      }

      const data = await response.json();

      setVerification(data);

    } catch (err) {
      console.error(
        "Provenance verification error:",
        err
      );

      alert(
        "Unable to verify provenance chain. Check the backend."
      );
    } finally {
      setVerifyLoading(false);
    }
  };

  // =====================================================
  // TRACE EVIDENCE CARD
  // =====================================================

  const traceCard = async () => {
    if (!selectedCard) {
      alert(
        "Please enter an Evidence Card ID."
      );
      return;
    }

    try {
      setTraceLoading(true);

      const response = await fetch(
        `${API}/provenance/${selectedCard}`
      );

      if (!response.ok) {
        const errorText =
          await response.text();

        console.error(
          "Traceability backend error:",
          errorText
        );

        throw new Error(
          `Traceability request failed (${response.status})`
        );
      }

      const data = await response.json();

      setCardTraceability(data);

    } catch (err) {
      console.error(
        "Traceability error:",
        err
      );

      alert(
        "Unable to retrieve evidence traceability. Check the Evidence Card ID."
      );
    } finally {
      setTraceLoading(false);
    }
  };

  useEffect(() => {
    loadRecords();
  }, []);

  // =====================================================
  // HELPERS
  // =====================================================

  const getVerificationStatus = () => {
    if (!verification) {
      return null;
    }

    if (
      verification.valid === true ||
      verification.chain_valid === true ||
      verification.is_valid === true
    ) {
      return "VALID";
    }

    return "CHECK";
  };

  const getRecordId = (record) => {
    return (
      record.id ??
      record.provenance_id ??
      record.record_id ??
      "—"
    );
  };

  const getCardId = (record) => {
    return (
      record.evidence_card_id ??
      record.card_id ??
      "—"
    );
  };

  const getHash = (record) => {
    return (
      record.record_hash ??
      record.hash ??
      record.current_hash ??
      "—"
    );
  };

  const getPreviousHash = (record) => {
    return (
      record.previous_hash ??
      record.prev_hash ??
      "—"
    );
  };

  return (
    <div className="dashboard-page">

      {/* =====================================================
          HEADER
      ====================================================== */}

      <div className="page-header">

        <div>

          <div className="hero-tag">
            EVIDENCE TRACEABILITY
          </div>

          <h1 className="page-title">
            Evidence Provenance
          </h1>

          <p className="page-subtitle">
            Verify the origin, integrity and traceability
            of evidence used by the platform.
          </p>

        </div>

        <div className="page-header-badge">
          🔗 Provenance Ledger
        </div>

      </div>

      {/* =====================================================
          METRICS
      ====================================================== */}

      <div className="metrics-grid">

        <div className="metric-card">

          <div className="metric-label">
            PROVENANCE RECORDS
          </div>

          <div className="metric-value">
            {records.length}
          </div>

          <div className="metric-subtext">
            Registered evidence records
          </div>

        </div>

        <div className="metric-card">

          <div className="metric-label">
            CHAIN STATUS
          </div>

          <div className="metric-value">
            {verification
              ? getVerificationStatus()
              : "—"}
          </div>

          <div className="metric-subtext">
            Cryptographic verification
          </div>

        </div>

        <div className="metric-card">

          <div className="metric-label">
            EVIDENCE LINKS
          </div>

          <div className="metric-value">
            {records.filter(
              (record) =>
                record.evidence_card_id ||
                record.card_id
            ).length}
          </div>

          <div className="metric-subtext">
            Linked Evidence Cards
          </div>

        </div>

        <div className="metric-card">

          <div className="metric-label">
            TRACEABILITY
          </div>

          <div className="metric-value">
            ACTIVE
          </div>

          <div className="metric-subtext">
            Source-level tracking
          </div>

        </div>

      </div>

      {/* =====================================================
          VERIFICATION PANEL
      ====================================================== */}

      <div className="panel">

        <div className="panel-header">

          <div>

            <h3 className="panel-title">
              Provenance Verification
            </h3>

            <p className="panel-subtitle">
              Check whether the provenance chain remains
              internally consistent.
            </p>

          </div>

          <span className="badge">
            HASH CHAIN
          </span>

        </div>

        <button
          className="btn btn-primary"
          onClick={verifyChain}
          disabled={verifyLoading}
        >
          {verifyLoading
            ? "Verifying..."
            : "Verify Provenance Chain"}
        </button>

        {verification && (

          <div
            style={{
              marginTop: "20px",
              padding: "20px",
              borderRadius: "14px",
              background:
                "var(--slate-50, #f8fafc)",
              border:
                "1px solid var(--slate-200, #e2e8f0)",
            }}
          >

            <div
              style={{
                display: "flex",
                justifyContent:
                  "space-between",
                alignItems: "center",
                gap: "20px",
                flexWrap: "wrap",
              }}
            >

              <div>

                <div className="metric-label">
                  VERIFICATION RESULT
                </div>

                <div
                  style={{
                    fontSize: "28px",
                    fontWeight: 800,
                    marginTop: "6px",
                  }}
                >
                  {getVerificationStatus()}
                </div>

              </div>

              <div
                style={{
                  fontSize: "14px",
                  color:
                    "var(--slate-600, #475569)",
                }}
              >
                {verification.message ||
                  verification.detail ||
                  "Provenance verification completed."}
              </div>

            </div>

          </div>

        )}

      </div>

      {/* =====================================================
          TRACE SPECIFIC EVIDENCE CARD
      ====================================================== */}

      <div className="panel">

        <div className="panel-header">

          <div>

            <h3 className="panel-title">
              Trace Evidence Card
            </h3>

            <p className="panel-subtitle">
              Retrieve provenance information for a
              specific Evidence Card.
            </p>

          </div>

          <span className="badge">
            TRACE
          </span>

        </div>

        <div
          style={{
            display: "flex",
            gap: "12px",
            alignItems: "end",
            flexWrap: "wrap",
          }}
        >

          <div
            className="form-group"
            style={{
              margin: 0,
              minWidth: "240px",
            }}
          >

            <label>
              Evidence Card ID
            </label>

            <input
              className="form-input"
              type="number"
              min="1"
              placeholder="Example: 1"
              value={selectedCard}
              onChange={(e) =>
                setSelectedCard(
                  e.target.value
                )
              }
            />

          </div>

          <button
            className="btn btn-primary"
            onClick={traceCard}
            disabled={traceLoading}
          >
            {traceLoading
              ? "Tracing..."
              : "Trace Evidence"}
          </button>

        </div>

        {cardTraceability && (

          <div
            style={{
              marginTop: "24px",
            }}
          >

            <h4>
              Traceability Result
            </h4>

            <pre
              style={{
                marginTop: "12px",
                padding: "18px",
                borderRadius: "12px",
                background: "#0f172a",
                color: "#e2e8f0",
                overflowX: "auto",
                fontSize: "13px",
                lineHeight: 1.6,
              }}
            >
              {JSON.stringify(
                cardTraceability,
                null,
                2
              )}
            </pre>

          </div>

        )}

      </div>

      {/* =====================================================
          RECORDS
      ====================================================== */}

      <div className="panel">

        <div className="panel-header">

          <div>

            <h3 className="panel-title">
              Provenance Records
            </h3>

            <p className="panel-subtitle">
              Evidence records currently registered
              in the provenance system.
            </p>

          </div>

          <span className="badge">
            {records.length} RECORDS
          </span>

        </div>

        {loading ? (

          <div className="empty-state">

            <div className="empty-state-icon">
              🔄
            </div>

            <h3>
              Loading provenance records
            </h3>

            <p>
              Connecting to the provenance service...
            </p>

          </div>

        ) : error ? (

          <div className="empty-state">

            <div className="empty-state-icon">
              ⚠️
            </div>

            <h3>
              Unable to load records
            </h3>

            <p>
              {error}
            </p>

            <button
              className="btn btn-primary"
              onClick={loadRecords}
              style={{
                marginTop: "15px",
              }}
            >
              Retry
            </button>

          </div>

        ) : records.length === 0 ? (

          <div className="empty-state">

            <div className="empty-state-icon">
              🔗
            </div>

            <h3>
              No provenance records
            </h3>

            <p>
              No provenance records are currently
              registered in the backend.
            </p>

          </div>

        ) : (

          <div
            style={{
              display: "flex",
              flexDirection: "column",
              gap: "12px",
            }}
          >

            {records.map(
              (record, index) => (

                <div
                  key={
                    getRecordId(record) !== "—"
                      ? getRecordId(record)
                      : index
                  }
                  style={{
                    padding: "18px",
                    border:
                      "1px solid var(--slate-200, #e2e8f0)",
                    borderRadius: "12px",
                    background:
                      "var(--white, #ffffff)",
                  }}
                >

                  <div
                    style={{
                      display: "grid",
                      gridTemplateColumns:
                        "repeat(auto-fit, minmax(180px, 1fr))",
                      gap: "16px",
                    }}
                  >

                    <div>

                      <div className="metric-label">
                        RECORD ID
                      </div>

                      <strong>
                        #{getRecordId(record)}
                      </strong>

                    </div>

                    <div>

                      <div className="metric-label">
                        EVIDENCE CARD
                      </div>

                      <strong>
                        {getCardId(record)}
                      </strong>

                    </div>

                    <div>

                      <div className="metric-label">
                        RECORD HASH
                      </div>

                      <div
                        style={{
                          fontFamily:
                            "monospace",
                          fontSize: "12px",
                          wordBreak:
                            "break-all",
                        }}
                      >
                        {getHash(record)}
                      </div>

                    </div>

                    <div>

                      <div className="metric-label">
                        PREVIOUS HASH
                      </div>

                      <div
                        style={{
                          fontFamily:
                            "monospace",
                          fontSize: "12px",
                          wordBreak:
                            "break-all",
                        }}
                      >
                        {getPreviousHash(
                          record
                        )}
                      </div>

                    </div>

                  </div>

                </div>

              )
            )}

          </div>

        )}

      </div>

    </div>
  );
}

export default Provenance;