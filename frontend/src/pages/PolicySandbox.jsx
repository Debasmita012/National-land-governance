import React, { useEffect, useState } from "react";

const API_BASE_URL = "http://127.0.0.1:8000";

export default function PolicySandbox() {
  const [conversionTax, setConversionTax] = useState(18);
  const [greenBuffer, setGreenBuffer] = useState(20);
  const [subsidy, setSubsidy] = useState(2500);
  const [tribunalDays, setTribunalDays] = useState(60);

  const [simulation, setSimulation] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const [baselineEmissions, setBaselineEmissions] = useState(100);
  const [projectedEmissions, setProjectedEmissions] = useState(80);

  const [carbonImpact, setCarbonImpact] = useState(null);
  const [carbonLoading, setCarbonLoading] = useState(false);
  const [carbonError, setCarbonError] = useState("");

  // ---------------------------------------------------------
  // POLICY SIMULATION
  // ---------------------------------------------------------
  const runSimulation = async () => {
    setLoading(true);
    setError("");

    try {
      const response = await fetch(`${API_BASE_URL}/sandbox/simulate`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          conversion_tax: conversionTax,
          green_buffer: greenBuffer,
          subsidy: subsidy,
          tribunal_days: tribunalDays,
        }),
      });

      if (!response.ok) {
        throw new Error("Failed to run policy simulation.");
      }

      const data = await response.json();
      setSimulation(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    runSimulation();
  }, [conversionTax, greenBuffer, subsidy, tribunalDays]);

  // ---------------------------------------------------------
  // CARBON IMPACT
  // ---------------------------------------------------------
  const calculateCarbonImpact = async () => {
    setCarbonLoading(true);
    setCarbonError("");

    try {
      const params = new URLSearchParams({
        baseline_emissions: baselineEmissions,
        projected_emissions: projectedEmissions,
      });

      const response = await fetch(
        `${API_BASE_URL}/carbon-impact/?${params.toString()}`,
        {
          method: "POST",
        }
      );

      if (!response.ok) {
        throw new Error("Failed to calculate carbon impact.");
      }

      const data = await response.json();
      setCarbonImpact(data);
    } catch (err) {
      setCarbonError(err.message);
    } finally {
      setCarbonLoading(false);
    }
  };

  useEffect(() => {
    calculateCarbonImpact();
  }, [baselineEmissions, projectedEmissions]);

  return (
    <div className="sandbox-page">
      <style>{`
        .sandbox-page {
          min-height: 100vh;
          background: #f5f7fb;
          padding: 32px;
          color: #172033;
        }

        .sandbox-container {
          max-width: 1200px;
          margin: 0 auto;
        }

        .sandbox-header {
          margin-bottom: 28px;
        }

        .sandbox-title {
          margin: 0;
          font-size: 32px;
          font-weight: 700;
          color: #102a43;
          letter-spacing: -0.5px;
        }

        .sandbox-subtitle {
          margin: 8px 0 0;
          color: #64748b;
          font-size: 15px;
          line-height: 1.6;
        }

        .card {
          background: #ffffff;
          border: 1px solid #e5eaf0;
          border-radius: 16px;
          box-shadow: 0 4px 14px rgba(15, 23, 42, 0.06);
          padding: 24px;
          margin-bottom: 24px;
        }

        .card-header {
          display: flex;
          align-items: flex-start;
          justify-content: space-between;
          gap: 16px;
          margin-bottom: 22px;
        }

        .card-title {
          margin: 0;
          font-size: 20px;
          font-weight: 700;
          color: #102a43;
        }

        .card-description {
          margin: 6px 0 0;
          color: #64748b;
          font-size: 14px;
        }

        .simulation-status {
          font-size: 13px;
          color: #2563eb;
          background: #eff6ff;
          padding: 7px 12px;
          border-radius: 999px;
          white-space: nowrap;
        }

        .controls-grid {
          display: grid;
          grid-template-columns: repeat(2, minmax(0, 1fr));
          gap: 22px;
        }

        .control-box {
          background: #f8fafc;
          border: 1px solid #e2e8f0;
          border-radius: 12px;
          padding: 18px;
        }

        .control-header {
          display: flex;
          align-items: center;
          justify-content: space-between;
          margin-bottom: 14px;
        }

        .control-label {
          font-size: 14px;
          font-weight: 600;
          color: #334155;
        }

        .control-value {
          font-size: 14px;
          font-weight: 700;
          color: #2563eb;
        }

        .range-input {
          width: 100%;
          accent-color: #2563eb;
          cursor: pointer;
        }

        .carbon-input {
          width: 100%;
          box-sizing: border-box;
          border: 1px solid #cbd5e1;
          border-radius: 10px;
          padding: 12px 14px;
          font-size: 15px;
          color: #172033;
          background: #ffffff;
          outline: none;
        }

        .carbon-input:focus {
          border-color: #2563eb;
          box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.12);
        }

        .input-help {
          margin: 7px 0 0;
          color: #94a3b8;
          font-size: 12px;
        }

        .metrics-grid {
          display: grid;
          grid-template-columns: repeat(4, minmax(0, 1fr));
          gap: 16px;
        }

        .metric-card {
          border-radius: 14px;
          padding: 20px;
          border: 1px solid transparent;
        }

        .metric-blue {
          background: #eff6ff;
          border-color: #dbeafe;
        }

        .metric-orange {
          background: #fff7ed;
          border-color: #fed7aa;
        }

        .metric-green {
          background: #f0fdf4;
          border-color: #bbf7d0;
        }

        .metric-emerald {
          background: #ecfdf5;
          border-color: #a7f3d0;
        }

        .metric-label {
          font-size: 13px;
          color: #64748b;
          margin-bottom: 8px;
        }

        .metric-value {
          font-size: 25px;
          font-weight: 700;
          line-height: 1.2;
        }

        .blue-text {
          color: #2563eb;
        }

        .orange-text {
          color: #ea580c;
        }

        .green-text {
          color: #16a34a;
        }

        .emerald-text {
          color: #059669;
        }

        .dark-text {
          color: #172033;
        }

        .table-wrapper {
          overflow-x: auto;
          border: 1px solid #e2e8f0;
          border-radius: 12px;
        }

        .projection-table {
          width: 100%;
          border-collapse: collapse;
          font-size: 14px;
        }

        .projection-table th {
          background: #f8fafc;
          color: #64748b;
          font-weight: 600;
          text-align: left;
          padding: 14px 16px;
          border-bottom: 1px solid #e2e8f0;
        }

        .projection-table td {
          padding: 14px 16px;
          border-bottom: 1px solid #eef2f7;
          color: #334155;
        }

        .projection-table tr:last-child td {
          border-bottom: none;
        }

        .projection-table .highlight {
          color: #2563eb;
          font-weight: 700;
        }

        .model-info {
          background: #f8fafc;
          border: 1px solid #e2e8f0;
          border-radius: 12px;
          padding: 14px 16px;
          color: #64748b;
          font-size: 13px;
          margin-top: 18px;
        }

        .model-info strong {
          color: #334155;
        }

        .error-box {
          background: #fef2f2;
          border: 1px solid #fecaca;
          color: #b91c1c;
          border-radius: 10px;
          padding: 14px 16px;
          margin-bottom: 24px;
          font-size: 14px;
        }

        .carbon-section {
          border-top: 4px solid #16a34a;
        }

        .carbon-badge {
          background: #f0fdf4;
          color: #15803d;
          border: 1px solid #bbf7d0;
          border-radius: 999px;
          padding: 7px 12px;
          font-size: 12px;
          font-weight: 600;
        }

        .carbon-input-grid {
          display: grid;
          grid-template-columns: repeat(2, minmax(0, 1fr));
          gap: 20px;
        }

        .input-group label {
          display: block;
          margin-bottom: 8px;
          font-size: 14px;
          font-weight: 600;
          color: #334155;
        }

        .carbon-results {
          margin-top: 26px;
          padding-top: 24px;
          border-top: 1px solid #e2e8f0;
        }

        .results-title {
          margin: 0 0 16px;
          font-size: 17px;
          font-weight: 700;
          color: #102a43;
        }

        .interpretation {
          margin-top: 18px;
          background: #f0fdf4;
          border: 1px solid #bbf7d0;
          border-radius: 12px;
          padding: 18px;
        }

        .interpretation-title {
          margin: 0 0 7px;
          font-size: 13px;
          font-weight: 700;
          color: #166534;
        }

        .interpretation-text {
          margin: 0;
          font-size: 14px;
          color: #166534;
          line-height: 1.6;
        }

        @media (max-width: 900px) {
          .metrics-grid {
            grid-template-columns: repeat(2, minmax(0, 1fr));
          }

          .controls-grid,
          .carbon-input-grid {
            grid-template-columns: 1fr;
          }
        }

        @media (max-width: 600px) {
          .sandbox-page {
            padding: 18px;
          }

          .sandbox-title {
            font-size: 26px;
          }

          .metrics-grid {
            grid-template-columns: 1fr;
          }

          .card {
            padding: 18px;
          }
        }
      `}</style>

      <div className="sandbox-container">

        {/* HEADER */}
        <div className="sandbox-header">
          <h1 className="sandbox-title">Policy Sandbox</h1>
          <p className="sandbox-subtitle">
            Test policy scenarios and estimate their land, economic and
            environmental impacts before implementation.
          </p>
        </div>

        {/* POLICY SCENARIO */}
        <div className="card">
          <div className="card-header">
            <div>
              <h2 className="card-title">Policy Scenario</h2>
              <p className="card-description">
                Adjust the policy levers to see how the simulated outcomes
                change.
              </p>
            </div>

            {loading && (
              <span className="simulation-status">
                Updating...
              </span>
            )}
          </div>

          <div className="controls-grid">

            <div className="control-box">
              <div className="control-header">
                <span className="control-label">
                  Conversion Tax
                </span>
                <span className="control-value">
                  {conversionTax}%
                </span>
              </div>

              <input
                className="range-input"
                type="range"
                min="0"
                max="50"
                value={conversionTax}
                onChange={(e) =>
                  setConversionTax(Number(e.target.value))
                }
              />
            </div>

            <div className="control-box">
              <div className="control-header">
                <span className="control-label">
                  Green Buffer
                </span>
                <span className="control-value">
                  {greenBuffer}%
                </span>
              </div>

              <input
                className="range-input"
                type="range"
                min="0"
                max="50"
                value={greenBuffer}
                onChange={(e) =>
                  setGreenBuffer(Number(e.target.value))
                }
              />
            </div>

            <div className="control-box">
              <div className="control-header">
                <span className="control-label">
                  Green Subsidy
                </span>
                <span className="control-value">
                  ₹{subsidy}
                </span>
              </div>

              <input
                className="range-input"
                type="range"
                min="0"
                max="5000"
                step="100"
                value={subsidy}
                onChange={(e) =>
                  setSubsidy(Number(e.target.value))
                }
              />
            </div>

            <div className="control-box">
              <div className="control-header">
                <span className="control-label">
                  Tribunal Resolution Time
                </span>
                <span className="control-value">
                  {tribunalDays} days
                </span>
              </div>

              <input
                className="range-input"
                type="range"
                min="15"
                max="180"
                step="5"
                value={tribunalDays}
                onChange={(e) =>
                  setTribunalDays(Number(e.target.value))
                }
              />
            </div>

          </div>
        </div>

        {error && (
          <div className="error-box">
            {error}
          </div>
        )}

        {/* SIMULATED POLICY IMPACT */}
        {simulation && (
          <div className="card">

            <div className="card-header">
              <div>
                <h2 className="card-title">
                  Simulated Policy Impact
                </h2>

                <p className="card-description">
                  Results returned by the backend policy simulation engine.
                </p>
              </div>
            </div>

            <div className="metrics-grid">

              <div className="metric-card metric-blue">
                <div className="metric-label">
                  Sprawl Reduction
                </div>

                <div className="metric-value blue-text">
                  {simulation.impacts.sprawl_reduction}%
                </div>
              </div>

              <div className="metric-card metric-orange">
                <div className="metric-label">
                  Displacement Risk
                </div>

                <div className="metric-value orange-text">
                  {simulation.impacts.displacement_risk}%
                </div>
              </div>

              <div className="metric-card metric-green">
                <div className="metric-label">
                  Municipal Revenue
                </div>

                <div className="metric-value green-text">
                  ₹{simulation.impacts.municipal_revenue_cr} Cr
                </div>
              </div>

              <div className="metric-card metric-emerald">
                <div className="metric-label">
                  Carbon Area Preserved
                </div>

                <div className="metric-value emerald-text">
                  {simulation.impacts.carbon_area_preserved_ha} ha
                </div>
              </div>

            </div>
          </div>
        )}

        {/* 5 YEAR PROJECTION */}
        {simulation && (
          <div className="card">

            <div className="card-header">
              <div>
                <h2 className="card-title">
                  5-Year Projection
                </h2>

                <p className="card-description">
                  Projected policy outcomes generated by the simulation model.
                </p>
              </div>
            </div>

            <div className="table-wrapper">
              <table className="projection-table">

                <thead>
                  <tr>
                    <th>Year</th>
                    <th>Baseline Disputes</th>
                    <th>Simulated Disputes</th>
                    <th>Revenue (Cr)</th>
                  </tr>
                </thead>

                <tbody>
                  {simulation.projection.map((row) => (
                    <tr key={row.year}>
                      <td>
                        <strong>{row.year}</strong>
                      </td>

                      <td>
                        {row.baselineDisputes}
                      </td>

                      <td className="highlight">
                        {row.simulatedDisputes}
                      </td>

                      <td>
                        ₹{row.revenueCr}
                      </td>
                    </tr>
                  ))}
                </tbody>

              </table>
            </div>

            <div className="model-info">
              <strong>Simulation model:</strong>{" "}
              {simulation.model.type}. This is a demonstration model and
              does not represent a statistical prediction.
            </div>

          </div>
        )}

        {/* CARBON IMPACT */}
        <div className="card carbon-section">

          <div className="card-header">
            <div>
              <h2 className="card-title">
                Carbon Impact Estimator
              </h2>

              <p className="card-description">
                Compare baseline and projected emissions for the policy
                scenario.
              </p>
            </div>

            <span className="carbon-badge">
              Climate Analysis
            </span>
          </div>

          <div className="carbon-input-grid">

            <div className="input-group">
              <label>
                Baseline Emissions
              </label>

              <input
                className="carbon-input"
                type="number"
                min="0"
                value={baselineEmissions}
                onChange={(e) =>
                  setBaselineEmissions(Number(e.target.value))
                }
              />

              <p className="input-help">
                Emissions before the policy scenario.
              </p>
            </div>

            <div className="input-group">
              <label>
                Projected Emissions
              </label>

              <input
                className="carbon-input"
                type="number"
                min="0"
                value={projectedEmissions}
                onChange={(e) =>
                  setProjectedEmissions(Number(e.target.value))
                }
              />

              <p className="input-help">
                Estimated emissions after the policy scenario.
              </p>
            </div>

          </div>

          {carbonError && (
            <div className="error-box" style={{ marginTop: "20px" }}>
              {carbonError}
            </div>
          )}

          {carbonImpact && (
            <div className="carbon-results">

              <div
                style={{
                  display: "flex",
                  justifyContent: "space-between",
                  alignItems: "center",
                  marginBottom: "16px",
                }}
              >
                <h3 className="results-title">
                  Climate Impact Results
                </h3>

                {carbonLoading && (
                  <span className="simulation-status">
                    Calculating...
                  </span>
                )}
              </div>

              <div className="metrics-grid">

                <div className="metric-card metric-blue">
                  <div className="metric-label">
                    Emissions Change
                  </div>

                  <div className="metric-value blue-text">
                    {carbonImpact.emissions_change}
                  </div>
                </div>

                <div className="metric-card metric-blue">
                  <div className="metric-label">
                    Percentage Change
                  </div>

                  <div className="metric-value blue-text">
                    {carbonImpact.percentage_change}%
                  </div>
                </div>

                <div className="metric-card metric-green">
                  <div className="metric-label">
                    Climate Impact
                  </div>

                  <div className="metric-value green-text">
                    {carbonImpact.climate_impact}
                  </div>
                </div>

                <div className="metric-card metric-emerald">
                  <div className="metric-label">
                    Impact Level
                  </div>

                  <div className="metric-value emerald-text">
                    {carbonImpact.impact_level}
                  </div>
                </div>

              </div>

              <div className="interpretation">
                <p className="interpretation-title">
                  Interpretation
                </p>

                <p className="interpretation-text">
                  {carbonImpact.interpretation}
                </p>
              </div>

            </div>
          )}

        </div>

      </div>
    </div>
  );
}