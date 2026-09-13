import { useState } from "react";

function SDGScorecard() {
  const [form, setForm] = useState({
    housing_impact: 78,
    economic_impact: 72,
    food_security_impact: 45,
    climate_impact: 52,
    infrastructure_impact: 80,
  });

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleChange = (field, value) => {
    setForm((prev) => ({
      ...prev,
      [field]: Number(value),
    }));
  };

  const analyzePolicy = async () => {
    setLoading(true);

    try {
      const params = new URLSearchParams({
        housing_impact: form.housing_impact,
        economic_impact: form.economic_impact,
        food_security_impact:
          form.food_security_impact,
        climate_impact: form.climate_impact,
        infrastructure_impact:
          form.infrastructure_impact,
      });

      const response = await fetch(
        `http://127.0.0.1:8000/sdg-scorecard/?${params.toString()}`,
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
      console.error("SDG scorecard error:", error);

      alert(
        "Unable to generate SDG scorecard. Check the backend."
      );
    } finally {
      setLoading(false);
    }
  };

  const getLevelClass = (level) => {
    if (!level) return "";

    const value = level.toLowerCase();

    if (value === "strong") return "score-strong";
    if (value === "moderate") return "score-moderate";

    return "score-weak";
  };

  const formatName = (name) => {
    return name
      .replace(/_/g, " ")
      .replace(/\b\w/g, (char) =>
        char.toUpperCase()
      );
  };

  const scorecard = result?.scorecard || {};

  return (
    <div className="dashboard-page">

      {/* HEADER */}
      <div className="page-header">

        <div>

          <div className="hero-tag">
            SUSTAINABLE DEVELOPMENT ANALYSIS
          </div>

          <h1 className="page-title">
            SDG Policy Scorecard
          </h1>

          <p className="page-subtitle">
            Evaluate policy impacts across key sustainable
            development and land-governance dimensions.
          </p>

        </div>

        <div className="page-header-badge">
          🎯 SDG Intelligence
        </div>

      </div>

      {/* INPUT PANEL */}
      <div className="panel">

        <div className="panel-header">

          <div>

            <h3 className="panel-title">
              SDG Impact Indicators
            </h3>

            <p className="panel-subtitle">
              Provide impact scores from 0 to 100 for each
              development dimension.
            </p>

          </div>

          <span className="badge">
            INPUT
          </span>

        </div>

        <div className="form-grid">

          <div className="form-group">

            <label>
              Housing Impact
            </label>

            <input
              className="form-input"
              type="number"
              min="0"
              max="100"
              value={form.housing_impact}
              onChange={(e) =>
                handleChange(
                  "housing_impact",
                  e.target.value
                )
              }
            />

          </div>

          <div className="form-group">

            <label>
              Economic Impact
            </label>

            <input
              className="form-input"
              type="number"
              min="0"
              max="100"
              value={form.economic_impact}
              onChange={(e) =>
                handleChange(
                  "economic_impact",
                  e.target.value
                )
              }
            />

          </div>

          <div className="form-group">

            <label>
              Food Security Impact
            </label>

            <input
              className="form-input"
              type="number"
              min="0"
              max="100"
              value={form.food_security_impact}
              onChange={(e) =>
                handleChange(
                  "food_security_impact",
                  e.target.value
                )
              }
            />

          </div>

          <div className="form-group">

            <label>
              Climate Impact
            </label>

            <input
              className="form-input"
              type="number"
              min="0"
              max="100"
              value={form.climate_impact}
              onChange={(e) =>
                handleChange(
                  "climate_impact",
                  e.target.value
                )
              }
            />

          </div>

          <div className="form-group">

            <label>
              Infrastructure Impact
            </label>

            <input
              className="form-input"
              type="number"
              min="0"
              max="100"
              value={form.infrastructure_impact}
              onChange={(e) =>
                handleChange(
                  "infrastructure_impact",
                  e.target.value
                )
              }
            />

          </div>

        </div>

        <button
          className="btn btn-primary"
          onClick={analyzePolicy}
          disabled={loading}
          style={{ marginTop: "20px" }}
        >
          {loading
            ? "Generating Scorecard..."
            : "Generate SDG Scorecard"}
        </button>

      </div>

      {/* RESULTS */}
      {result ? (
        <>
          {/* SUMMARY METRICS */}
          <div className="metrics-grid">

            <div className="metric-card">

              <div className="metric-label">
                OVERALL SCORE
              </div>

              <div className="metric-value">
                {result.overall_score}
              </div>

              <div className="metric-subtext">
                Out of 100
              </div>

            </div>

            <div className="metric-card">

              <div className="metric-label">
                OVERALL LEVEL
              </div>

              <div
                className={`score-level ${getLevelClass(
                  result.overall_level
                )}`}
              >
                {result.overall_level}
              </div>

              <div className="metric-subtext">
                Overall SDG alignment
              </div>

            </div>

            <div className="metric-card">

              <div className="metric-label">
                STRENGTHS
              </div>

              <div className="metric-value">
                {(result.strengths || []).length}
              </div>

              <div className="metric-subtext">
                Strong dimensions
              </div>

            </div>

            <div className="metric-card">

              <div className="metric-label">
                AREAS TO IMPROVE
              </div>

              <div className="metric-value">
                {(result.weaknesses || []).length}
              </div>

              <div className="metric-subtext">
                Weaker dimensions
              </div>

            </div>

          </div>

          {/* SCORECARD */}
          <div className="panel">

            <div className="panel-header">

              <div>

                <h3 className="panel-title">
                  Development Dimensions
                </h3>

                <p className="panel-subtitle">
                  Impact scores returned by the SDG analysis engine.
                </p>

              </div>

              <span className="badge">
                SCORECARD
              </span>

            </div>

            <div className="scorecard-grid">

              {Object.entries(scorecard).map(
                ([key, value]) => (

                  <div
                    className="scorecard-item"
                    key={key}
                  >

                    <div className="scorecard-top">

                      <span className="scorecard-name">
                        {formatName(key)}
                      </span>

                      <span
                        className={`score-level ${getLevelClass(
                          value.level
                        )}`}
                      >
                        {value.level}
                      </span>

                    </div>

                    <div className="score-number">
                      {value.score}
                      <span>/100</span>
                    </div>

                    <div className="score-bar">

                      <div
                        className="score-bar-fill"
                        style={{
                          width: `${value.score}%`,
                        }}
                      />

                    </div>

                  </div>

                )
              )}

            </div>

          </div>

          {/* STRENGTHS / WEAKNESSES */}
          <div className="dashboard-grid">

            <div className="panel">

              <div className="panel-header">

                <h3 className="panel-title">
                  Policy Strengths
                </h3>

                <span className="badge">
                  POSITIVE
                </span>

              </div>

              {result.strengths?.length ? (

                <div className="tag-list">

                  {result.strengths.map(
                    (item, index) => (

                      <span
                        className="success-tag"
                        key={index}
                      >
                        ✓ {formatName(item)}
                      </span>

                    )
                  )}

                </div>

              ) : (

                <p className="muted-text">
                  No strong dimensions identified.
                </p>

              )}

            </div>

            <div className="panel">

              <div className="panel-header">

                <h3 className="panel-title">
                  Areas Requiring Attention
                </h3>

                <span className="badge">
                  REVIEW
                </span>

              </div>

              {result.weaknesses?.length ? (

                <div className="tag-list">

                  {result.weaknesses.map(
                    (item, index) => (

                      <span
                        className="warning-tag"
                        key={index}
                      >
                        ⚠ {formatName(item)}
                      </span>

                    )
                  )}

                </div>

              ) : (

                <p className="muted-text">
                  No major weaknesses identified.
                </p>

              )}

            </div>

          </div>

        </>
      ) : (

        <div className="panel">

          <div className="empty-state">

            <div className="empty-state-icon">
              🎯
            </div>

            <h3>
              No scorecard generated
            </h3>

            <p>
              Enter the impact indicators above and generate
              the SDG assessment to view the results.
            </p>

          </div>

        </div>

      )}

    </div>
  );
}

export default SDGScorecard;