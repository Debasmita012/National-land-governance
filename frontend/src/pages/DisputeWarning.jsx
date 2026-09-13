import { useState } from "react";

function DisputeWarning() {
  const [form, setForm] = useState({
    dispute_count: 120,
    dispute_growth_percentage: 50,
    land_use_change_percentage: 35,
    population_growth_percentage: 12,
    anomaly_detected: true,
  });

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleChange = (field, value) => {
    setForm((prev) => ({
      ...prev,
      [field]:
        field === "anomaly_detected"
          ? value
          : Number(value),
    }));
  };

  const analyzeRisk = async () => {
    setLoading(true);

    try {
      const params = new URLSearchParams({
        dispute_count: form.dispute_count,
        dispute_growth_percentage:
          form.dispute_growth_percentage,
        land_use_change_percentage:
          form.land_use_change_percentage,
        population_growth_percentage:
          form.population_growth_percentage,
        anomaly_detected: form.anomaly_detected,
      });

      const response = await fetch(
        `http://127.0.0.1:8000/dispute-warning/?${params.toString()}`,
        {
          method: "POST",
        }
      );

      if (!response.ok) {
        const errorText = await response.text();
        console.error("Backend error:", errorText);
        throw new Error(errorText);
      }

      const data = await response.json();

      setResult(data);
    } catch (error) {
      console.error("Dispute warning error:", error);
      alert(
        "Unable to analyze dispute risk. Check the backend."
      );
    } finally {
      setLoading(false);
    }
  };

  const getRiskClass = (level) => {
    if (!level) return "";

    const value = level.toLowerCase();

    if (value === "high") return "risk-high";
    if (value === "moderate") return "risk-moderate";

    return "risk-low";
  };

  return (
    <div className="dashboard-page">

      {/* HEADER */}
      <div className="page-header">
        <div>
          <div className="hero-tag">
            EARLY WARNING SYSTEM
          </div>

          <h1 className="page-title">
            Land Dispute Early Warning
          </h1>

          <p className="page-subtitle">
            Analyze land-governance indicators and identify
            areas showing potential dispute pressure.
          </p>
        </div>

        <div className="page-header-badge">
          ⚠️ Risk Intelligence
        </div>
      </div>

      {/* METRICS */}
      <div className="metrics-grid">

        <div className="metric-card">
          <div className="metric-label">
            CURRENT DISPUTES
          </div>

          <div className="metric-value">
            {form.dispute_count}
          </div>

          <div className="metric-subtext">
            Recorded cases
          </div>
        </div>

        <div className="metric-card">
          <div className="metric-label">
            DISPUTE GROWTH
          </div>

          <div className="metric-value">
            {form.dispute_growth_percentage}%
          </div>

          <div className="metric-subtext">
            Change from previous period
          </div>
        </div>

        <div className="metric-card">
          <div className="metric-label">
            LAND-USE CHANGE
          </div>

          <div className="metric-value">
            {form.land_use_change_percentage}%
          </div>

          <div className="metric-subtext">
            Detected change
          </div>
        </div>

        <div className="metric-card">
          <div className="metric-label">
            POPULATION GROWTH
          </div>

          <div className="metric-value">
            {form.population_growth_percentage}%
          </div>

          <div className="metric-subtext">
            Growth indicator
          </div>
        </div>

      </div>

      {/* INPUT + RESULT */}
      <div className="dashboard-grid">

        {/* INPUT */}
        <div className="panel">

          <div className="panel-header">
            <div>
              <h3 className="panel-title">
                Risk Indicators
              </h3>

              <p className="panel-subtitle">
                Provide current indicators for the area being assessed.
              </p>
            </div>

            <span className="badge">
              INPUT
            </span>
          </div>

          <div className="form-grid">

            <div className="form-group">
              <label>
                Current Disputes
              </label>

              <input
                className="form-input"
                type="number"
                value={form.dispute_count}
                onChange={(e) =>
                  handleChange(
                    "dispute_count",
                    e.target.value
                  )
                }
              />
            </div>

            <div className="form-group">
              <label>
                Dispute Growth (%)
              </label>

              <input
                className="form-input"
                type="number"
                value={
                  form.dispute_growth_percentage
                }
                onChange={(e) =>
                  handleChange(
                    "dispute_growth_percentage",
                    e.target.value
                  )
                }
              />
            </div>

            <div className="form-group">
              <label>
                Land-Use Change (%)
              </label>

              <input
                className="form-input"
                type="number"
                value={
                  form.land_use_change_percentage
                }
                onChange={(e) =>
                  handleChange(
                    "land_use_change_percentage",
                    e.target.value
                  )
                }
              />
            </div>

            <div className="form-group">
              <label>
                Population Growth (%)
              </label>

              <input
                className="form-input"
                type="number"
                value={
                  form.population_growth_percentage
                }
                onChange={(e) =>
                  handleChange(
                    "population_growth_percentage",
                    e.target.value
                  )
                }
              />
            </div>

          </div>

          <label className="checkbox-row">
            <input
              type="checkbox"
              checked={form.anomaly_detected}
              onChange={(e) =>
                handleChange(
                  "anomaly_detected",
                  e.target.checked
                )
              }
            />

            <span>
              Anomaly detected in underlying data
            </span>
          </label>

          <button
            className="btn btn-primary"
            onClick={analyzeRisk}
            disabled={loading}
            style={{ marginTop: "20px" }}
          >
            {loading
              ? "Analyzing..."
              : "Analyze Dispute Risk"}
          </button>

        </div>

        {/* RESULT */}
        <div className="panel">

          <div className="panel-header">
            <div>
              <h3 className="panel-title">
                Risk Assessment
              </h3>

              <p className="panel-subtitle">
                Backend-generated early-warning assessment.
              </p>
            </div>

            <span className="badge">
              AI ANALYSIS
            </span>
          </div>

          {!result ? (
            <div className="empty-state">

              <div className="empty-state-icon">
                ⚠️
              </div>

              <h3>
                No assessment generated
              </h3>

              <p>
                Enter the indicators and run the analysis
                to generate a dispute-risk assessment.
              </p>

            </div>
          ) : (
            <div>

              <div className="risk-result">

                <div className="risk-score">

                  <span className="metric-label">
                    RISK SCORE
                  </span>

                  <strong>
                    {result.risk_score}
                  </strong>

                </div>

                <div
                  className={`risk-level ${getRiskClass(
                    result.risk_level
                  )}`}
                >
                  {result.risk_level}
                </div>

              </div>

              <div className="warning-box">

                <strong>
                  Early Warning
                </strong>

                <p>
                  {result.warning}
                </p>

              </div>

              <div className="panel-section">

                <h4>
                  Triggering Indicators
                </h4>

                <div className="indicator-list">

                  {(result.indicators || []).map(
                    (indicator, index) => (
                      <div
                        className="indicator-item"
                        key={index}
                      >
                        <span>⚠</span>
                        {indicator}
                      </div>
                    )
                  )}

                </div>

              </div>

              <div className="analysis-footer">

                <span>
                  Anomaly Signal
                </span>

                <strong>
                  {result.anomaly_detected
                    ? "Detected"
                    : "Not detected"}
                </strong>

              </div>

            </div>
          )}

        </div>

      </div>

    </div>
  );
}

export default DisputeWarning;