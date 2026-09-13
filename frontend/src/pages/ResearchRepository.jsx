import { useEffect, useState } from "react";

const API_BASE_URL = "http://127.0.0.1:8000";

function ResearchRepository({ savedCount, onToggleSave }) {
  const [documents, setDocuments] = useState([]);
  const [search, setSearch] = useState("");
  const [selectedType, setSelectedType] = useState("All Types");
  const [savedIds, setSavedIds] = useState([]);
  const [activeDocument, setActiveDocument] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    fetchDocuments();
  }, []);

  const fetchDocuments = async () => {
    try {
      setLoading(true);
      setError("");

      const response = await fetch(
        `${API_BASE_URL}/documents/`
      );

      let data = null;

      try {
        data = await response.json();
      } catch {
        data = null;
      }

      if (!response.ok) {
        const detail =
          typeof data?.detail === "string"
            ? data.detail
            : JSON.stringify(data?.detail);

        throw new Error(
          detail ||
            `Failed to load documents (${response.status}).`
        );
      }

      setDocuments(Array.isArray(data) ? data : []);
    } catch (err) {
      console.error("Document API error:", err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const documentTypes = [
    "All Types",
    ...new Set(
      documents
        .map((document) => document.document_type)
        .filter(Boolean)
    ),
  ];

  const toggleSave = (id) => {
    setSavedIds((previous) => {
      const next = previous.includes(id)
        ? previous.filter((item) => item !== id)
        : [...previous, id];

      if (onToggleSave) {
        onToggleSave(next.length);
      }

      return next;
    });
  };

  const filteredDocuments = documents.filter(
    (document) => {
      const searchText = search.toLowerCase();

      const matchesSearch =
        document.title
          ?.toLowerCase()
          .includes(searchText) ||
        document.source
          ?.toLowerCase()
          .includes(searchText) ||
        document.document_type
          ?.toLowerCase()
          .includes(searchText);

      const matchesType =
        selectedType === "All Types" ||
        document.document_type === selectedType;

      return matchesSearch && matchesType;
    }
  );

  return (
    <div className="repository-page">

      {/* Header */}
      <div className="page-header">

        <div className="page-title-group">
          <h2>
            📚 National Land Research Repository
          </h2>

          <p>
            Research documents registered in the
            Land Governance knowledge base.
          </p>
        </div>

        <div className="page-actions">
          <button
            className="btn btn-outline"
            onClick={fetchDocuments}
            disabled={loading}
          >
            🔄 Refresh
          </button>
        </div>

      </div>

      {/* Loading */}
      {loading && (
        <div
          className="panel"
          style={{
            marginBottom: "16px",
            textAlign: "center",
          }}
        >
          Loading research documents from backend...
        </div>
      )}

      {/* Error */}
      {error && (
        <div
          className="panel"
          style={{
            marginBottom: "16px",
            color: "#b91c1c",
            background: "#fef2f2",
            border: "1px solid #fecaca",
          }}
        >
          <strong>
            Unable to load research documents.
          </strong>

          <div style={{ marginTop: "6px" }}>
            {error}
          </div>
        </div>
      )}

      {/* Filter Bar */}
      <div className="filter-bar">

        <div className="search-box filter-bar-input">
          <span>🔍</span>

          <input
            type="text"
            placeholder="Search by title, source, or document type..."
            value={search}
            onChange={(e) =>
              setSearch(e.target.value)
            }
          />
        </div>

        <select
          className="select-control"
          style={{ width: "180px" }}
          value={selectedType}
          onChange={(e) =>
            setSelectedType(e.target.value)
          }
        >
          {documentTypes.map((type) => (
            <option key={type} value={type}>
              {type}
            </option>
          ))}
        </select>

        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: "8px",
            marginLeft: "auto",
          }}
        >
          <span
            style={{
              fontSize: "12px",
              color: "var(--slate-500)",
            }}
          >
            Showing{" "}
            <strong>
              {filteredDocuments.length}
            </strong>{" "}
            documents
          </span>

          <span
            className="badge"
            style={{
              background: "#fffbeb",
              color: "#b45309",
            }}
          >
            ★ {savedIds.length} Bookmarked
          </span>
        </div>

      </div>

      {/* Repository Grid */}
      <div className="research-grid">

        {!loading &&
          !error &&
          filteredDocuments.map((document) => {

            const isSaved = savedIds.includes(
              document.id
            );

            return (
              <div
                key={document.id}
                className="research-card"
              >

                <div className="card-tag-row">

                  <span className="pill-tag">
                    {document.document_type ||
                      "Document"}
                  </span>

                  <button
                    className={`bookmark-btn ${
                      isSaved ? "saved" : ""
                    }`}
                    onClick={() =>
                      toggleSave(document.id)
                    }
                    title={
                      isSaved
                        ? "Remove bookmark"
                        : "Bookmark document"
                    }
                  >
                    {isSaved ? "★" : "☆"}
                  </button>

                </div>

                <h4>
                  {document.title}
                </h4>

                <p
                  className="research-abstract"
                >
                  Registered research document
                  available in the Land Governance
                  backend.
                </p>

                <div className="research-meta">

                  <div>
                    <strong>
                      Document ID:
                    </strong>{" "}
                    {document.id}
                  </div>

                  <div>
                    <strong>
                      Source:
                    </strong>{" "}
                    {document.source ||
                      "Not specified"}
                  </div>

                  <div>
                    <strong>
                      Type:
                    </strong>{" "}
                    {document.document_type ||
                      "Not specified"}
                  </div>

                </div>

                <div
                  style={{
                    display: "flex",
                    gap: "8px",
                    marginTop: "auto",
                  }}
                >

                  <button
                    className="btn btn-sm btn-primary"
                    style={{ flex: 1 }}
                    onClick={() =>
                      setActiveDocument(document)
                    }
                  >
                    View Document
                  </button>

                </div>

              </div>
            );
          })}

        {!loading &&
          !error &&
          filteredDocuments.length === 0 && (
            <div
              className="panel"
              style={{
                gridColumn: "1 / -1",
                textAlign: "center",
                padding: "40px",
              }}
            >
              No research documents found.
            </div>
          )}

      </div>

      {/* Document Details Modal */}
      {activeDocument && (
        <div
          className="modal-overlay"
          onClick={() =>
            setActiveDocument(null)
          }
        >
          <div
            className="modal-content"
            onClick={(e) =>
              e.stopPropagation()
            }
          >

            <div className="modal-header">

              <div>

                <span className="pill-tag">
                  {activeDocument.document_type ||
                    "Document"}
                </span>

                <h3
                  style={{
                    fontSize: "18px",
                    color:
                      "var(--slate-900)",
                    marginTop: "6px",
                  }}
                >
                  {activeDocument.title}
                </h3>

              </div>

              <button
                className="modal-close-btn"
                onClick={() =>
                  setActiveDocument(null)
                }
              >
                ✕
              </button>

            </div>

            <div
              style={{
                display: "flex",
                flexDirection: "column",
                gap: "16px",
              }}
            >

              <div>

                <div
                  style={{
                    fontSize: "11px",
                    textTransform:
                      "uppercase",
                    fontWeight: 700,
                    color:
                      "var(--slate-500)",
                  }}
                >
                  Document Information
                </div>

                <div
                  style={{
                    marginTop: "8px",
                    fontSize: "13px",
                    lineHeight: "1.7",
                    color:
                      "var(--slate-700)",
                  }}
                >

                  <div>
                    <strong>
                      Document ID:
                    </strong>{" "}
                    {activeDocument.id}
                  </div>

                  <div>
                    <strong>
                      Title:
                    </strong>{" "}
                    {activeDocument.title}
                  </div>

                  <div>
                    <strong>
                      Source:
                    </strong>{" "}
                    {activeDocument.source ||
                      "Not specified"}
                  </div>

                  <div>
                    <strong>
                      Document Type:
                    </strong>{" "}
                    {activeDocument.document_type ||
                      "Not specified"}
                  </div>

                  <div>
                    <strong>
                      File Path:
                    </strong>{" "}
                    {activeDocument.file_path ||
                      "Not available"}
                  </div>

                </div>

              </div>

              <div
                style={{
                  padding: "14px",
                  background:
                    "var(--slate-50)",
                  borderRadius: "8px",
                  fontSize: "12px",
                  color:
                    "var(--slate-600)",
                }}
              >
                This document is registered in
                the backend and can be used by the
                AI Evidence Engine for evidence
                retrieval.
              </div>

              <div
                style={{
                  display: "flex",
                  justifyContent:
                    "flex-end",
                  gap: "10px",
                  borderTop:
                    "1px solid var(--border-subtle)",
                  paddingTop: "14px",
                }}
              >

                <button
                  className="btn btn-secondary"
                  onClick={() =>
                    setActiveDocument(null)
                  }
                >
                  Close
                </button>

              </div>

            </div>

          </div>
        </div>
      )}

    </div>
  );
}

export default ResearchRepository;