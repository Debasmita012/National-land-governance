import { useEffect, useState } from "react";

const API_BASE_URL = "http://127.0.0.1:8000";

function DatasetExplorer() {
  const [datasets, setDatasets] = useState([]);
  const [formatFilter, setFormatFilter] = useState("All");
  const [search, setSearch] = useState("");
  const [selectedDataset, setSelectedDataset] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    fetchDatasets();
  }, []);

  const fetchDatasets = async () => {
    try {
      setLoading(true);
      setError("");

      const response = await fetch(
        `${API_BASE_URL}/datasets/`
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
            `Failed to load datasets (${response.status}).`
        );
      }

      setDatasets(Array.isArray(data) ? data : []);
    } catch (err) {
      console.error("Dataset API error:", err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const formats = [
    "All",
    ...new Set(
      datasets
        .map((dataset) => dataset.data_type)
        .filter(Boolean)
    ),
  ];

  const filteredDatasets = datasets.filter((dataset) => {
    const searchText = search.toLowerCase();

    const matchesSearch =
      dataset.name?.toLowerCase().includes(searchText) ||
      dataset.description
        ?.toLowerCase()
        .includes(searchText) ||
      dataset.source?.toLowerCase().includes(searchText) ||
      dataset.geography
        ?.toLowerCase()
        .includes(searchText);

    const matchesFormat =
      formatFilter === "All" ||
      dataset.data_type === formatFilter;

    return matchesSearch && matchesFormat;
  });

  return (
    <div className="datasets-page">

      {/* Page Header */}
      <div className="page-header">
        <div className="page-title-group">
          <h2>
            📁 National Land Governance Datasets
          </h2>

          <p>
            Browse datasets registered in the Land
            Governance backend.
          </p>
        </div>

        <div className="page-actions">
          <button
            className="btn btn-outline"
            onClick={fetchDatasets}
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
          Loading datasets from backend...
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
            Unable to load datasets.
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
            placeholder="Search dataset name, geography, source..."
            value={search}
            onChange={(e) =>
              setSearch(e.target.value)
            }
          />
        </div>

        <div
          style={{
            display: "flex",
            gap: "6px",
            alignItems: "center",
          }}
        >
          <span
            style={{
              fontSize: "12px",
              fontWeight: 700,
              color: "var(--slate-500)",
            }}
          >
            Format:
          </span>

          {formats.map((format) => (
            <button
              key={format}
              className={`btn btn-sm ${
                formatFilter === format
                  ? "btn-primary"
                  : "btn-secondary"
              }`}
              onClick={() =>
                setFormatFilter(format)
              }
            >
              {format}
            </button>
          ))}
        </div>
      </div>

      {/* Dataset Count */}
      {!loading && !error && (
        <div
          style={{
            marginBottom: "12px",
            fontSize: "12px",
            color: "var(--slate-500)",
          }}
        >
          Showing{" "}
          <strong>{filteredDatasets.length}</strong>{" "}
          dataset
          {filteredDatasets.length !== 1
            ? "s"
            : ""}
        </div>
      )}

      {/* Dataset Table */}
      <div className="table-wrapper">
        <table className="table">

          <thead>
            <tr>
              <th>Dataset</th>
              <th>Format</th>
              <th>Geography</th>
              <th>Source</th>
              <th>ID</th>
              <th
                style={{
                  textAlign: "right",
                }}
              >
                Actions
              </th>
            </tr>
          </thead>

          <tbody>

            {!loading &&
              filteredDatasets.map((dataset) => (
                <tr key={dataset.id}>

                  <td
                    style={{
                      maxWidth: "360px",
                    }}
                  >
                    <div
                      style={{
                        fontWeight: 700,
                        color:
                          "var(--slate-900)",
                        marginBottom: "4px",
                      }}
                    >
                      {dataset.name}
                    </div>

                    <div
                      style={{
                        fontSize: "11px",
                        color:
                          "var(--slate-500)",
                      }}
                    >
                      {dataset.description}
                    </div>
                  </td>

                  <td>
                    <span className="badge">
                      {dataset.data_type ||
                        "Unknown"}
                    </span>
                  </td>

                  <td>
                    {dataset.geography ||
                      "Not specified"}
                  </td>

                  <td>
                    {dataset.source ||
                      "Not specified"}
                  </td>

                  <td
                    style={{
                      fontFamily:
                        "var(--font-mono)",
                      fontSize: "12px",
                    }}
                  >
                    {dataset.id}
                  </td>

                  <td
                    style={{
                      textAlign: "right",
                    }}
                  >
                    <button
                      className="btn btn-sm btn-outline"
                      onClick={() =>
                        setSelectedDataset(
                          dataset
                        )
                      }
                    >
                      View Details
                    </button>
                  </td>

                </tr>
              ))}

            {!loading &&
              !error &&
              filteredDatasets.length === 0 && (
                <tr>
                  <td
                    colSpan="6"
                    style={{
                      textAlign: "center",
                      padding: "40px",
                      color:
                        "var(--slate-500)",
                    }}
                  >
                    No datasets found.
                  </td>
                </tr>
              )}

          </tbody>
        </table>
      </div>

      {/* Dataset Details Modal */}
      {selectedDataset && (
        <div
          className="modal-overlay"
          onClick={() =>
            setSelectedDataset(null)
          }
        >
          <div
            className="modal-content"
            style={{
              maxWidth: "700px",
            }}
            onClick={(e) =>
              e.stopPropagation()
            }
          >

            <div className="modal-header">

              <div>
                <span className="pill-tag">
                  {selectedDataset.data_type}
                </span>

                <h3
                  style={{
                    fontSize: "18px",
                    color:
                      "var(--slate-900)",
                    marginTop: "6px",
                  }}
                >
                  {selectedDataset.name}
                </h3>
              </div>

              <button
                className="modal-close-btn"
                onClick={() =>
                  setSelectedDataset(null)
                }
              >
                ✕
              </button>

            </div>

            <div
              style={{
                fontSize: "13px",
                lineHeight: "1.6",
                color:
                  "var(--slate-600)",
              }}
            >

              <p>
                <strong>Description:</strong>{" "}
                {selectedDataset.description ||
                  "No description available."}
              </p>

              <p>
                <strong>Source:</strong>{" "}
                {selectedDataset.source ||
                  "Not specified"}
              </p>

              <p>
                <strong>Geography:</strong>{" "}
                {selectedDataset.geography ||
                  "Not specified"}
              </p>

              <p>
                <strong>Data Type:</strong>{" "}
                {selectedDataset.data_type ||
                  "Not specified"}
              </p>

              <p>
                <strong>Dataset ID:</strong>{" "}
                {selectedDataset.id}
              </p>

              {selectedDataset.file_path && (
                <p>
                  <strong>File Path:</strong>{" "}
                  {selectedDataset.file_path}
                </p>
              )}

            </div>

            <div
              style={{
                display: "flex",
                justifyContent: "flex-end",
                marginTop: "20px",
              }}
            >
              <button
                className="btn btn-secondary"
                onClick={() =>
                  setSelectedDataset(null)
                }
              >
                Close
              </button>
            </div>

          </div>
        </div>
      )}

    </div>
  );
}

export default DatasetExplorer;