import { useState } from "react";

const API_BASE_URL = "http://127.0.0.1:8000";

function Analytics({ onNavigate }) {
  const [valuesInput, setValuesInput] = useState(
    "100, 110, 125, 130, 150"
  );

  const [trendResult, setTrendResult] = useState(null);
  const [anomalyResult, setAnomalyResult] = useState(null);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  // --------------------------------------------------
  // Convert input string into numeric values
  // --------------------------------------------------
  const parseValues = () => {
    const values = valuesInput
      .split(",")
      .map((value) => value.trim())
      .filter(Boolean)
      .map(Number);

    if (
      values.length === 0 ||
      values.some((value) => !Number.isFinite(value))
    ) {
      throw new Error(
        "Please enter valid comma-separated numbers."
      );
    }

    return values;
  };

  // --------------------------------------------------
  // Run Trend + Anomaly Analysis
  // --------------------------------------------------
  const runAnalytics = async () => {
    try {
      setLoading(true);
      setError("");

      const values = parseValues();

      if (values.length < 5) {
        throw new Error(
          "Please provide at least 5 values for anomaly analysis."
        );
      }

      // Call both real backend endpoints
      const [trendResponse, anomalyResponse] =
        await Promise.all([
          fetch(`${API_BASE_URL}/analytics/trend`, {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              values,
            }),
          }),

          fetch(`${API_BASE_URL}/analytics/anomaly`, {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              values,
            }),
          }),
        ]);

      let trendData = null;
      let anomalyData = null;

      try {
        trendData = await trendResponse.json();
      } catch {
        trendData = null;
      }

      try {
        anomalyData = await anomalyResponse.json();
      } catch {
        anomalyData = null;
      }

      // --------------------------------------------------
      // Check Trend API
      // --------------------------------------------------
      if (!trendResponse.ok) {
        const detail =
          typeof trendData?.detail === "string"
            ? trendData.detail
            : JSON.stringify(trendData?.detail);

        throw new Error(
          detail ||
            `Trend analysis failed (${trendResponse.status}).`
        );
      }

      // --------------------------------------------------
      // Check Anomaly API
      // --------------------------------------------------
      if (!anomalyResponse.ok) {
        const detail =
          typeof anomalyData?.detail === "string"
            ? anomalyData.detail
            : JSON.stringify(anomalyData?.detail);

        throw new Error(
          detail ||
            `Anomaly analysis failed (${anomalyResponse.status}).`
        );
      }

      // --------------------------------------------------
      // Combine raw analysis + explainability
      // --------------------------------------------------
      setTrendResult({
        ...trendData.trend,
        ...trendData.explanation,
      });

      setAnomalyResult({
        ...anomalyData.anomalies,
        ...anomalyData.explanation,
      });

    } catch (err) {
      console.error("Analytics error:", err);

      setError(
        err.message || "Unable to run analytics."
      );

      setTrendResult(null);
      setAnomalyResult(null);
    } finally {
      setLoading(false);
    }
  };

  // --------------------------------------------------
  // Export CSV
  // --------------------------------------------------
  const handleExportCSV = () => {
    if (!trendResult || !anomalyResult) {
      alert("Run the analytics first.");
      return;
    }

    const rows = [
      ["Metric", "Value"],

      [
        "Trend Direction",
        trendResult.trend_direction,
      ],

      [
        "Trend Strength",
        trendResult.trend_strength,
      ],

      [
        "Pattern Strength",
        trendResult.pattern_strength,
      ],

      [
        "First Value",
        trendResult.first_value,
      ],

      [
        "Last Value",
        trendResult.last_value,
      ],

      [
        "Absolute Change",
        trendResult.absolute_change,
      ],

      [
        "Percentage Change",
        trendResult.percentage_change,
      ],

      [
        "Average Value",
        trendResult.average_value,
      ],

      [
        "Highest Value",
        trendResult.highest_value,
      ],

      [
        "Lowest Value",
        trendResult.lowest_value,
      ],

      [
        "Data Points",
        trendResult.data_points,
      ],

      [
        "Anomaly Count",
        anomalyResult.anomaly_count,
      ],

      [
        "Normal Count",
        anomalyResult.normal_count,
      ],

      [
        "Anomaly Percentage",
        anomalyResult.anomaly_percentage,
      ],
    ];

    const csv = rows
      .map((row) =>
        row
          .map((value) => {
            const text = String(
              value ?? ""
            );

            return `"${text.replace(
              /"/g,
              '""'
            )}"`;
          })
          .join(",")
      )
      .join("\n");

    const blob = new Blob([csv], {
      type: "text/csv;charset=utf-8;",
    });

    const url = URL.createObjectURL(blob);

    const link = document.createElement("a");

    link.href = url;
    link.download =
      "land_governance_ai_analytics.csv";

    document.body.appendChild(link);

    link.click();

    document.body.removeChild(link);

    URL.revokeObjectURL(url);
  };

  // --------------------------------------------------
  // Get detected anomalies
  // --------------------------------------------------
  const anomalyValues =
    anomalyResult?.results?.filter(
      (item) => item.is_anomaly
    ) || [];

  return (
    <div className="analytics-page">

      {/* =================================================
          PAGE HEADER
      ================================================= */}

      <div className="page-header">

        <div className="page-title-group">

          <h2>
            📊 AI Land Governance Analytics
          </h2>

          <p>
            Trend analysis, anomaly detection,
            and explainable AI insights from the
            backend.
          </p>

        </div>

        <div className="page-actions">

          <button
            className="btn btn-primary"
            onClick={handleExportCSV}
            disabled={
              !trendResult ||
              !anomalyResult
            }
          >
            📥 Export CSV Report
          </button>

        </div>

      </div>

      {/* =================================================
          INPUT PANEL
      ================================================= */}

      <div
        className="panel"
        style={{
          marginBottom: "22px",
        }}
      >

        <div className="panel-header">

          <div className="panel-title-group">

            <h3>
              Run AI Analysis
            </h3>

            <p>
              Enter a time-series or indicator
              sequence. At least 5 values are
              required.
            </p>

          </div>

        </div>

        <div
          style={{
            display: "flex",
            gap: "12px",
            alignItems: "center",
            marginTop: "12px",
          }}
        >

          <input
            className="input-control"
            style={{
              flex: 1,
            }}
            value={valuesInput}
            onChange={(e) =>
              setValuesInput(
                e.target.value
              )
            }
            placeholder="Example: 100, 110, 125, 130, 150"
          />

          <button
            className="btn btn-primary"
            onClick={runAnalytics}
            disabled={loading}
          >
            {loading
              ? "Analyzing..."
              : "Run Analysis"}
          </button>

        </div>

      </div>

      {/* =================================================
          ERROR
      ================================================= */}

      {error && (
        <div
          className="panel"
          style={{
            marginBottom: "22px",
            background: "#fef2f2",
            border: "1px solid #fecaca",
            color: "#b91c1c",
          }}
        >

          <strong>
            Analytics Error
          </strong>

          <div
            style={{
              marginTop: "6px",
            }}
          >
            {error}
          </div>

        </div>
      )}

      {/* =================================================
          KPI CARDS
      ================================================= */}

      {trendResult &&
        anomalyResult && (
          <div className="metrics-grid">

            {/* Trend Direction */}
            <div className="metric-card">

              <div className="metric-top">

                <div className="metric-icon-wrap metric-icon-teal">
                  📈
                </div>

                <span className="metric-trend up">
                  {trendResult.trend_direction}
                </span>

              </div>

              <div className="metric-label">
                Trend Direction
              </div>

              <div className="metric-value">
                {trendResult.trend_direction}
              </div>

              <div className="metric-subtitle">
                Pattern strength:{" "}
                {trendResult.pattern_strength ||
                  trendResult.trend_strength}
              </div>

            </div>

            {/* Percentage Change */}
            <div className="metric-card">

              <div className="metric-top">

                <div className="metric-icon-wrap metric-icon-blue">
                  📊
                </div>

              </div>

              <div className="metric-label">
                Percentage Change
              </div>

              <div className="metric-value">
                {trendResult.percentage_change}%
              </div>

              <div className="metric-subtitle">
                From{" "}
                {trendResult.first_value}{" "}
                to{" "}
                {trendResult.last_value}
              </div>

            </div>

            {/* Anomalies */}
            <div className="metric-card">

              <div className="metric-top">

                <div className="metric-icon-wrap metric-icon-amber">
                  ⚠️
                </div>

                <span className="metric-trend">
                  {anomalyResult.anomaly_count}{" "}
                  detected
                </span>

              </div>

              <div className="metric-label">
                Anomalies
              </div>

              <div className="metric-value">
                {anomalyResult.anomaly_count}
              </div>

              <div className="metric-subtitle">
                {anomalyResult.anomaly_percentage}%
                {" "}
                of observations
              </div>

            </div>

            {/* Observations */}
            <div className="metric-card">

              <div className="metric-top">

                <div className="metric-icon-wrap metric-icon-purple">
                  🧠
                </div>

              </div>

              <div className="metric-label">
                Observations
              </div>

              <div className="metric-value">
                {trendResult.data_points}
              </div>

              <div className="metric-subtitle">
                Analyzed by the AI backend
              </div>

            </div>

          </div>
        )}

      {/* =================================================
          TREND + ANOMALY
      ================================================= */}

      {trendResult &&
        anomalyResult && (
          <div
            className="dashboard-grid"
            style={{
              marginTop: "22px",
            }}
          >

            {/* =================================================
                TREND ANALYSIS
            ================================================= */}

            <div
              className="panel"
              style={{
                margin: 0,
              }}
            >

              <div className="panel-header">

                <div className="panel-title-group">

                  <h3>
                    📈 Trend Analysis
                  </h3>

                  <p>
                    Statistical trend analysis
                    generated by the backend.
                  </p>

                </div>

              </div>

              <div
                style={{
                  display: "grid",
                  gridTemplateColumns:
                    "1fr 1fr",
                  gap: "18px",
                  marginTop: "18px",
                }}
              >

                <div>
                  <strong>
                    Direction
                  </strong>

                  <div
                    style={{
                      marginTop: "5px",
                    }}
                  >
                    {trendResult.trend_direction}
                  </div>
                </div>

                <div>
                  <strong>
                    Pattern Strength
                  </strong>

                  <div
                    style={{
                      marginTop: "5px",
                    }}
                  >
                    {trendResult.pattern_strength ||
                      trendResult.trend_strength}
                  </div>
                </div>

                <div>
                  <strong>
                    Average
                  </strong>

                  <div
                    style={{
                      marginTop: "5px",
                    }}
                  >
                    {trendResult.average_value}
                  </div>
                </div>

                <div>
                  <strong>
                    Absolute Change
                  </strong>

                  <div
                    style={{
                      marginTop: "5px",
                    }}
                  >
                    {trendResult.absolute_change}
                  </div>
                </div>

                <div>
                  <strong>
                    Highest
                  </strong>

                  <div
                    style={{
                      marginTop: "5px",
                    }}
                  >
                    {trendResult.highest_value}
                  </div>
                </div>

                <div>
                  <strong>
                    Lowest
                  </strong>

                  <div
                    style={{
                      marginTop: "5px",
                    }}
                  >
                    {trendResult.lowest_value}
                  </div>
                </div>

                <div>
                  <strong>
                    First Value
                  </strong>

                  <div
                    style={{
                      marginTop: "5px",
                    }}
                  >
                    {trendResult.first_value}
                  </div>
                </div>

                <div>
                  <strong>
                    Last Value
                  </strong>

                  <div
                    style={{
                      marginTop: "5px",
                    }}
                  >
                    {trendResult.last_value}
                  </div>
                </div>

              </div>

            </div>

            {/* =================================================
                ANOMALY DETECTION
            ================================================= */}

            <div
              className="panel"
              style={{
                margin: 0,
              }}
            >

              <div className="panel-header">

                <div className="panel-title-group">

                  <h3>
                    ⚠️ Anomaly Detection
                  </h3>

                  <p>
                    Isolation Forest results from
                    the backend.
                  </p>

                </div>

              </div>

              <div
                style={{
                  marginTop: "18px",
                }}
              >

                <div
                  style={{
                    fontSize: "13px",
                    marginBottom: "14px",
                  }}
                >

                  <strong>
                    {anomalyResult.anomaly_count}
                  </strong>{" "}
                  anomalies detected out of{" "}
                  <strong>
                    {anomalyResult.total_values}
                  </strong>{" "}
                  observations.

                </div>

                {/* Actual anomalies */}
                {anomalyValues.length > 0 ? (

                  anomalyValues.map(
                    (item) => (
                      <div
                        key={item.index}
                        style={{
                          padding: "14px",
                          marginBottom: "8px",
                          background:
                            "#fff7ed",
                          border:
                            "1px solid #fed7aa",
                          borderRadius: "8px",
                          fontSize: "12px",
                        }}
                      >

                        <strong>
                          ⚠️ Anomaly at index{" "}
                          {item.index}
                        </strong>

                        <div
                          style={{
                            marginTop: "5px",
                          }}
                        >
                          Value:{" "}
                          {item.value}
                        </div>

                        <div
                          style={{
                            marginTop: "3px",
                          }}
                        >
                          Anomaly score:{" "}
                          {item.anomaly_score}
                        </div>

                      </div>
                    )
                  )

                ) : (

                  <div
                    style={{
                      padding: "16px",
                      background:
                        "var(--slate-50)",
                      borderRadius: "8px",
                      fontSize: "12px",
                    }}
                  >
                    No unusual values were
                    detected.
                  </div>

                )}

              </div>

            </div>

          </div>
        )}

      {/* =================================================
          EXPLAINABILITY
      ================================================= */}

      {trendResult &&
        anomalyResult && (
          <div
            className="panel"
            style={{
              marginTop: "22px",
            }}
          >

            <div className="panel-header">

              <div className="panel-title-group">

                <h3>
                  🧠 Explainable AI Findings
                </h3>

                <p>
                  Human-readable interpretation
                  generated by the Explainability
                  Service.
                </p>

              </div>

            </div>

            <div
              style={{
                display: "grid",
                gap: "14px",
                marginTop: "16px",
              }}
            >

              {/* Trend explanation */}
              <div
                style={{
                  padding: "16px",
                  background:
                    "var(--slate-50)",
                  borderRadius: "8px",
                }}
              >

                <strong>
                  Trend Finding
                </strong>

                <p
                  style={{
                    marginTop: "7px",
                    marginBottom: "7px",
                  }}
                >
                  {trendResult.finding}
                </p>

                <p
                  style={{
                    fontSize: "12px",
                    color:
                      "var(--slate-600)",
                    marginBottom: "6px",
                  }}
                >
                  <strong>
                    Reason:
                  </strong>{" "}
                  {trendResult.reason}
                </p>

                <p
                  style={{
                    fontSize: "12px",
                    color:
                      "var(--slate-600)",
                    margin: 0,
                  }}
                >
                  <strong>
                    Risk signal:
                  </strong>{" "}
                  {trendResult.risk_signal}
                </p>

              </div>

              {/* Anomaly explanation */}
              <div
                style={{
                  padding: "16px",
                  background:
                    "var(--slate-50)",
                  borderRadius: "8px",
                }}
              >

                <strong>
                  Anomaly Finding
                </strong>

                <p
                  style={{
                    marginTop: "7px",
                    marginBottom: "7px",
                  }}
                >
                  {anomalyResult.finding}
                </p>

                <p
                  style={{
                    fontSize: "12px",
                    color:
                      "var(--slate-600)",
                    marginBottom: "6px",
                  }}
                >
                  <strong>
                    Reason:
                  </strong>{" "}
                  {anomalyResult.reason}
                </p>

                <p
                  style={{
                    fontSize: "12px",
                    color:
                      "var(--slate-600)",
                    margin: 0,
                  }}
                >
                  <strong>
                    Risk signal:
                  </strong>{" "}
                  {anomalyResult.risk_signal}
                </p>

              </div>

            </div>

          </div>
        )}

      {/* =================================================
          EMPTY STATE
      ================================================= */}

      {!trendResult &&
        !anomalyResult &&
        !loading && (

          <div
            className="panel"
            style={{
              textAlign: "center",
              padding: "50px",
            }}
          >

            <div
              style={{
                fontSize: "34px",
                marginBottom: "12px",
              }}
            >
              📊
            </div>

            <h3>
              No analysis run yet
            </h3>

            <p
              style={{
                color:
                  "var(--slate-500)",
                marginTop: "7px",
              }}
            >
              Enter indicator values above and
              click Run Analysis.
            </p>

          </div>

        )}

    </div>
  );
}

export default Analytics;