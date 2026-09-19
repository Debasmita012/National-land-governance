import React, { useMemo, useState } from "react";

const API_BASE = "http://127.0.0.1:8000";

const styles = {
  page: {
    minHeight: "100vh",
    background: "#f3f6fa",
    color: "#142033",
    padding: "24px 38px 40px",
    boxSizing: "border-box",
  },

  header: {
    marginBottom: "24px",
  },

  eyebrow: {
    color: "#2f80ed",
    fontSize: "13px",
    fontWeight: 800,
    letterSpacing: "0.8px",
    textTransform: "uppercase",
    marginBottom: "7px",
  },

  title: {
    margin: 0,
    fontSize: "30px",
    fontWeight: 800,
    color: "#162033",
    letterSpacing: "-0.5px",
  },

  subtitle: {
    margin: "8px 0 0",
    color: "#66758a",
    fontSize: "14px",
    lineHeight: 1.6,
    maxWidth: "900px",
  },

  card: {
    background: "#ffffff",
    border: "1px solid #dce4ee",
    borderRadius: "14px",
    boxShadow: "0 3px 12px rgba(20, 32, 51, 0.05)",
  },

  sectionTitle: {
    margin: 0,
    fontSize: "18px",
    fontWeight: 800,
    color: "#182438",
  },

  sectionDescription: {
    margin: "6px 0 0",
    fontSize: "13px",
    color: "#718096",
    lineHeight: 1.5,
  },
};

function StatCard({
  icon,
  label,
  value,
  accent = "#2f80ed",
}) {
  return (
    <div
      style={{
        ...styles.card,
        padding: "18px",
        minHeight: "112px",
        position: "relative",
        overflow: "hidden",
      }}
    >
      <div
        style={{
          position: "absolute",
          left: 0,
          top: 0,
          bottom: 0,
          width: "4px",
          background: accent,
        }}
      />

      <div
        style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          marginBottom: "14px",
        }}
      >
        <span
          style={{
            color: "#718096",
            fontSize: "12px",
            fontWeight: 700,
            textTransform: "uppercase",
            letterSpacing: "0.4px",
          }}
        >
          {label}
        </span>

        <span
          style={{
            width: "32px",
            height: "32px",
            borderRadius: "9px",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            background: `${accent}15`,
            fontSize: "16px",
          }}
        >
          {icon}
        </span>
      </div>

      <div
        style={{
          fontSize: "26px",
          fontWeight: 800,
          color: "#162033",
        }}
      >
        {value}
      </div>
    </div>
  );
}

function RiskBadge({ level }) {
  const config = {
    Critical: {
      background: "#fee2e2",
      color: "#b91c1c",
      border: "#fecaca",
    },
    High: {
      background: "#fff1e6",
      color: "#c2410c",
      border: "#fed7aa",
    },
    Moderate: {
      background: "#fff7d6",
      color: "#a16207",
      border: "#fde68a",
    },
    Low: {
      background: "#e9f9f1",
      color: "#047857",
      border: "#a7f3d0",
    },
  };

  const style =
    config[level] || {
      background: "#f1f5f9",
      color: "#475569",
      border: "#cbd5e1",
    };

  return (
    <span
      style={{
        display: "inline-flex",
        alignItems: "center",
        padding: "5px 10px",
        borderRadius: "999px",
        background: style.background,
        color: style.color,
        border: `1px solid ${style.border}`,
        fontSize: "11px",
        fontWeight: 800,
      }}
    >
      {level || "Unknown"}
    </span>
  );
}

function FileUploadBox({
  title,
  required,
  file,
  onChange,
}) {
  return (
    <div
      style={{
        border: "1px solid #dce4ee",
        borderRadius: "12px",
        padding: "16px",
        background: "#fbfcfe",
      }}
    >
      <div
        style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          marginBottom: "10px",
        }}
      >
        <label
          style={{
            fontSize: "13px",
            fontWeight: 800,
            color: "#27364d",
          }}
        >
          {title}
          {required && (
            <span style={{ color: "#ef4444" }}>
              {" "}
              *
            </span>
          )}
        </label>

        <span
          style={{
            fontSize: "10px",
            color: "#8290a5",
            fontWeight: 700,
          }}
        >
          CSV / XLSX / XLS
        </span>
      </div>

      <label
        style={{
          display: "flex",
          alignItems: "center",
          gap: "12px",
          minHeight: "48px",
          padding: "8px 12px",
          border: "1px dashed #cbd5e1",
          borderRadius: "9px",
          background: "#ffffff",
          cursor: "pointer",
          boxSizing: "border-box",
        }}
      >
        <span
          style={{
            background: "#eef4ff",
            color: "#2f80ed",
            padding: "7px 11px",
            borderRadius: "7px",
            fontSize: "12px",
            fontWeight: 800,
            whiteSpace: "nowrap",
          }}
        >
          Choose File
        </span>

        <span
          style={{
            color: file
              ? "#24344d"
              : "#94a3b8",
            fontSize: "12px",
            overflow: "hidden",
            textOverflow: "ellipsis",
            whiteSpace: "nowrap",
          }}
        >
          {file
            ? file.name
            : "No file selected"}
        </span>

        <input
          type="file"
          accept=".csv,.xlsx,.xls"
          onChange={onChange}
          style={{ display: "none" }}
        />
      </label>

      {file && (
        <div
          style={{
            marginTop: "8px",
            color: "#059669",
            fontSize: "11px",
            fontWeight: 700,
          }}
        >
          ✓ Dataset ready for analysis
        </div>
      )}
    </div>
  );
}

export default function LandIntelligence() {
  const [currentFile, setCurrentFile] =
    useState(null);

  const [historicalFile, setHistoricalFile] =
    useState(null);

  const [loading, setLoading] =
    useState(false);

  const [error, setError] =
    useState("");

  const [result, setResult] =
    useState(null);

  const analyzeLand = async () => {
    if (!currentFile) {
      setError(
        "Please select the current land dataset."
      );
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    try {
      const formData = new FormData();

      formData.append(
        "current_file",
        currentFile
      );

      if (historicalFile) {
        formData.append(
          "historical_file",
          historicalFile
        );
      }

      const response = await fetch(
        `${API_BASE}/land-analysis/complete`,
        {
          method: "POST",
          body: formData,
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail ||
            "Land analysis failed."
        );
      }

      setResult(data);
    } catch (err) {
      setError(
        err.message ||
          "Unable to analyze land data."
      );
    } finally {
      setLoading(false);
    }
  };

  const analysis =
    result?.current?.analysis || {};

  const indicators =
    analysis?.indicators || {};

  const landUse =
    analysis?.land_use || {};

  const riskAnalysis =
    result?.risk_analysis || {};

  const changeAnalysis =
    riskAnalysis?.land_use_change_integration;

  const parcelRisks =
    riskAnalysis?.parcel_risks || [];

  const topRisks = useMemo(() => {
    return [...parcelRisks]
      .sort(
        (a, b) =>
          (b.integrated_risk_score ??
            b.risk_score ??
            0) -
          (a.integrated_risk_score ??
            a.risk_score ??
            0)
      )
      .slice(0, 10);
  }, [parcelRisks]);

  return (
    <div style={styles.page}>
      {/* ================================================= */}
      {/* PAGE HEADER */}
      {/* ================================================= */}

      <div style={styles.header}>
        <div style={styles.eyebrow}>
          AI + GIS + LAND INTELLIGENCE
        </div>

        <h1 style={styles.title}>
          Land Intelligence Engine
        </h1>

        <p style={styles.subtitle}>
          Upload land-governance datasets to
          automatically profile land records,
          identify land-use patterns, analyze
          dispute pressure, detect anomalies and
          explain potential land-risk hotspots.
        </p>
      </div>

      {/* ================================================= */}
      {/* UPLOAD CARD */}
      {/* ================================================= */}

      <div
        style={{
          ...styles.card,
          padding: "22px",
          marginBottom: "22px",
        }}
      >
        <div
          style={{
            display: "flex",
            justifyContent: "space-between",
            alignItems: "flex-start",
            gap: "20px",
            flexWrap: "wrap",
          }}
        >
          <div>
            <h2 style={styles.sectionTitle}>
              Upload Land Data
            </h2>

            <p
              style={
                styles.sectionDescription
              }
            >
              Current data is required.
              Historical data enables
              land-use change analysis and
              integrated risk assessment.
            </p>
          </div>

          <div
            style={{
              display: "flex",
              alignItems: "center",
              gap: "7px",
              padding: "7px 11px",
              background: "#eaf8f1",
              border: "1px solid #b8ecd1",
              borderRadius: "999px",
              color: "#087f5b",
              fontSize: "11px",
              fontWeight: 800,
            }}
          >
            <span>●</span>
            ANALYSIS READY
          </div>
        </div>

        <div
          style={{
            display: "grid",
            gridTemplateColumns:
              "repeat(auto-fit, minmax(320px, 1fr))",
            gap: "16px",
            marginTop: "20px",
          }}
        >
          <FileUploadBox
            title="Current Land Dataset"
            required
            file={currentFile}
            onChange={(event) =>
              setCurrentFile(
                event.target.files?.[0] ||
                  null
              )
            }
          />

          <FileUploadBox
            title="Historical Land Dataset"
            file={historicalFile}
            onChange={(event) =>
              setHistoricalFile(
                event.target.files?.[0] ||
                  null
              )
            }
          />
        </div>

        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: "14px",
            marginTop: "18px",
            flexWrap: "wrap",
          }}
        >
          <button
            onClick={analyzeLand}
            disabled={loading}
            style={{
              border: "none",
              borderRadius: "8px",
              padding: "11px 20px",
              background: loading
                ? "#94a3b8"
                : "#2f80ed",
              color: "#ffffff",
              fontWeight: 800,
              fontSize: "12px",
              cursor: loading
                ? "not-allowed"
                : "pointer",
              boxShadow:
                "0 3px 8px rgba(47,128,237,0.22)",
            }}
          >
            {loading
              ? "Analyzing..."
              : "Analyze Land Landscape →"}
          </button>

          {historicalFile && (
            <span
              style={{
                color: "#64748b",
                fontSize: "12px",
              }}
            >
              Historical comparison enabled
            </span>
          )}
        </div>

        {error && (
          <div
            style={{
              marginTop: "15px",
              padding: "11px 13px",
              borderRadius: "8px",
              background: "#fff1f2",
              border:
                "1px solid #fecdd3",
              color: "#be123c",
              fontSize: "12px",
              fontWeight: 600,
            }}
          >
            {error}
          </div>
        )}
      </div>

      {/* ================================================= */}
      {/* RESULTS */}
      {/* ================================================= */}

      {result && (
        <>
          {/* ============================================= */}
          {/* REPORT HEADER */}
          {/* ============================================= */}

          <div
            style={{
              ...styles.card,
              padding: "18px 20px",
              marginBottom: "18px",
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
              gap: "20px",
              flexWrap: "wrap",
            }}
          >
            <div>
              <div
                style={{
                  fontSize: "11px",
                  color: "#2f80ed",
                  fontWeight: 800,
                  letterSpacing: "0.5px",
                  marginBottom: "4px",
                }}
              >
                AUTOMATED ANALYSIS
              </div>

              <h2
                style={{
                  margin: 0,
                  fontSize: "20px",
                  color: "#172238",
                }}
              >
                Land Intelligence Report
              </h2>

              <div
                style={{
                  marginTop: "5px",
                  color: "#718096",
                  fontSize: "12px",
                }}
              >
                {result.current?.filename}
              </div>
            </div>

            <div
              style={{
                padding: "8px 12px",
                borderRadius: "8px",
                background: "#f0fdf4",
                border:
                  "1px solid #bbf7d0",
                color: "#15803d",
                fontSize: "11px",
                fontWeight: 800,
              }}
            >
              ✓ ANALYSIS COMPLETE
            </div>
          </div>

          {/* ============================================= */}
          {/* STATISTICS */}
          {/* ============================================= */}

          <div
            style={{
              display: "grid",
              gridTemplateColumns:
                "repeat(auto-fit, minmax(175px, 1fr))",
              gap: "14px",
              marginBottom: "20px",
            }}
          >
            <StatCard
              icon="▦"
              label="Parcels Analyzed"
              value={
                indicators.parcels_analyzed ??
                0
              }
            />

            <StatCard
              icon="⚠"
              label="Total Disputes"
              value={
                indicators.total_disputes ??
                0
              }
              accent="#ef4444"
            />

            <StatCard
              icon="◉"
              label="Disputed Parcels"
              value={
                indicators.parcels_with_disputes ??
                0
              }
              accent="#f97316"
            />

            <StatCard
              icon="♙"
              label="Population"
              value={
                indicators.population_total ??
                0
              }
              accent="#8b5cf6"
            />

            <StatCard
              icon="⌗"
              label="Total Area"
              value={
                indicators.total_area ?? 0
              }
              accent="#059669"
            />

            <StatCard
              icon="!"
              label="Dispute Pressure"
              value={`${indicators.dispute_pressure ?? 0}%`}
              accent="#e11d48"
            />
          </div>

          {/* ============================================= */}
          {/* TWO-COLUMN ANALYSIS */}
          {/* ============================================= */}

          <div
            style={{
              display: "grid",
              gridTemplateColumns:
                "minmax(0, 1fr) minmax(0, 1fr)",
              gap: "18px",
              marginBottom: "20px",
            }}
          >
            {/* LAND USE */}

            <div
              style={{
                ...styles.card,
                padding: "20px",
              }}
            >
              <h2 style={styles.sectionTitle}>
                Land-Use Distribution
              </h2>

              <p
                style={
                  styles.sectionDescription
                }
              >
                Distribution detected from the
                uploaded current dataset.
              </p>

              <div
                style={{
                  marginTop: "20px",
                }}
              >
                {Object.entries(
                  landUse.percentages || {}
                ).map(
                  ([
                    category,
                    percentage,
                  ]) => (
                    <div
                      key={category}
                      style={{
                        marginBottom:
                          "15px",
                      }}
                    >
                      <div
                        style={{
                          display: "flex",
                          justifyContent:
                            "space-between",
                          marginBottom:
                            "6px",
                        }}
                      >
                        <span
                          style={{
                            fontSize: "12px",
                            color:
                              "#334155",
                            fontWeight:
                              700,
                          }}
                        >
                          {category}
                        </span>

                        <span
                          style={{
                            fontSize: "12px",
                            color:
                              "#2f80ed",
                            fontWeight:
                              800,
                          }}
                        >
                          {percentage}%
                        </span>
                      </div>

                      <div
                        style={{
                          height: "7px",
                          borderRadius:
                            "999px",
                          background:
                            "#e8eef5",
                          overflow:
                            "hidden",
                        }}
                      >
                        <div
                          style={{
                            width: `${percentage}%`,
                            height: "100%",
                            background:
                              "#2f80ed",
                            borderRadius:
                              "999px",
                          }}
                        />
                      </div>
                    </div>
                  )
                )}
              </div>
            </div>

            {/* LAND USE CHANGE */}

            <div
              style={{
                ...styles.card,
                padding: "20px",
              }}
            >
              <h2 style={styles.sectionTitle}>
                Land-Use Change
              </h2>

              <p
                style={
                  styles.sectionDescription
                }
              >
                Historical/current comparison
                identifies observed parcel
                conversions.
              </p>

              {changeAnalysis?.available ? (
                <div
                  style={{
                    display: "grid",
                    gridTemplateColumns:
                      "1fr 1fr",
                    gap: "12px",
                    marginTop: "20px",
                  }}
                >
                  <div
                    style={{
                      background:
                        "#f8fafc",
                      border:
                        "1px solid #e2e8f0",
                      borderRadius:
                        "10px",
                      padding: "14px",
                    }}
                  >
                    <div
                      style={{
                        fontSize: "11px",
                        color:
                          "#718096",
                        fontWeight:
                          700,
                      }}
                    >
                      MATCHED
                    </div>

                    <div
                      style={{
                        marginTop: "5px",
                        fontSize:
                          "23px",
                        fontWeight:
                          800,
                      }}
                    >
                      {
                        changeAnalysis.matched_parcels
                      }
                    </div>
                  </div>

                  <div
                    style={{
                      background:
                        "#fff7ed",
                      border:
                        "1px solid #fed7aa",
                      borderRadius:
                        "10px",
                      padding: "14px",
                    }}
                  >
                    <div
                      style={{
                        fontSize: "11px",
                        color:
                          "#9a3412",
                        fontWeight:
                          700,
                      }}
                    >
                      CHANGED
                    </div>

                    <div
                      style={{
                        marginTop: "5px",
                        fontSize:
                          "23px",
                        fontWeight:
                          800,
                        color:
                          "#c2410c",
                      }}
                    >
                      {
                        changeAnalysis.changed_parcels
                      }
                    </div>
                  </div>

                  <div
                    style={{
                      background:
                        "#f0fdf4",
                      border:
                        "1px solid #bbf7d0",
                      borderRadius:
                        "10px",
                      padding: "14px",
                    }}
                  >
                    <div
                      style={{
                        fontSize: "11px",
                        color:
                          "#166534",
                        fontWeight:
                          700,
                      }}
                    >
                      UNCHANGED
                    </div>

                    <div
                      style={{
                        marginTop: "5px",
                        fontSize:
                          "23px",
                        fontWeight:
                          800,
                        color:
                          "#15803d",
                      }}
                    >
                      {
                        changeAnalysis.unchanged_parcels
                      }
                    </div>
                  </div>

                  <div
                    style={{
                      background:
                        "#eff6ff",
                      border:
                        "1px solid #bfdbfe",
                      borderRadius:
                        "10px",
                      padding: "14px",
                    }}
                  >
                    <div
                      style={{
                        fontSize: "11px",
                        color:
                          "#1d4ed8",
                        fontWeight:
                          700,
                      }}
                    >
                      CONVERSION RATE
                    </div>

                    <div
                      style={{
                        marginTop: "5px",
                        fontSize:
                          "23px",
                        fontWeight:
                          800,
                        color:
                          "#2563eb",
                      }}
                    >
                      {
                        changeAnalysis.conversion_rate
                      }
                      %
                    </div>
                  </div>
                </div>
              ) : (
                <div
                  style={{
                    marginTop: "20px",
                    padding: "16px",
                    background:
                      "#f8fafc",
                    border:
                      "1px solid #e2e8f0",
                    borderRadius:
                      "10px",
                    color:
                      "#64748b",
                    fontSize: "12px",
                  }}
                >
                  Historical data was not
                  provided. Upload a historical
                  dataset to enable land-use
                  change analysis.
                </div>
              )}
            </div>
          </div>

          {/* ============================================= */}
          {/* RISK TABLE */}
          {/* ============================================= */}

          <div
            style={{
              ...styles.card,
              padding: "20px",
              marginBottom: "20px",
            }}
          >
            <div
              style={{
                display: "flex",
                justifyContent:
                  "space-between",
                alignItems: "center",
                gap: "15px",
                flexWrap: "wrap",
              }}
            >
              <div>
                <h2
                  style={styles.sectionTitle}
                >
                  Land Risk Assessment
                </h2>

                <p
                  style={
                    styles.sectionDescription
                  }
                >
                  Highest-risk parcels ranked
                  using the integrated pilot
                  land-risk index.
                </p>
              </div>

              <div
                style={{
                  padding: "7px 11px",
                  background: "#f8fafc",
                  border:
                    "1px solid #e2e8f0",
                  borderRadius: "7px",
                  color: "#64748b",
                  fontSize: "10px",
                  fontWeight: 800,
                }}
              >
                PILOT DECISION-SUPPORT MODEL
              </div>
            </div>

            {topRisks.length === 0 ? (
              <div
                style={{
                  marginTop: "18px",
                  padding: "20px",
                  background:
                    "#f8fafc",
                  borderRadius: "10px",
                  color: "#64748b",
                  fontSize: "12px",
                }}
              >
                No parcel-level risk records
                were returned for this dataset.
              </div>
            ) : (
              <div
                style={{
                  overflowX: "auto",
                  marginTop: "18px",
                }}
              >
                <table
                  style={{
                    width: "100%",
                    borderCollapse:
                      "collapse",
                    minWidth: "850px",
                  }}
                >
                  <thead>
                    <tr
                      style={{
                        background:
                          "#f8fafc",
                      }}
                    >
                      {[
                        "Parcel",
                        "Risk",
                        "Score",
                        "Land-Use Change",
                        "Risk Drivers",
                      ].map(
                        (heading) => (
                          <th
                            key={heading}
                            style={{
                              textAlign:
                                "left",
                              padding:
                                "11px 12px",
                              borderBottom:
                                "1px solid #e2e8f0",
                              color:
                                "#64748b",
                              fontSize:
                                "10px",
                              fontWeight:
                                800,
                              textTransform:
                                "uppercase",
                            }}
                          >
                            {heading}
                          </th>
                        )
                      )}
                    </tr>
                  </thead>

                  <tbody>
                    {topRisks.map(
                      (
                        parcel,
                        index
                      ) => {
                        const score =
                          parcel.integrated_risk_score ??
                          parcel.risk_score ??
                          0;

                        const level =
                          parcel.integrated_risk_level ??
                          parcel.risk_level ??
                          "Unknown";

                        const parcelId =
                          parcel.parcel_id ??
                          parcel.id ??
                          parcel.ulpin ??
                          `Parcel ${
                            index + 1
                          }`;

                        return (
                          <tr
                            key={`${parcelId}-${index}`}
                          >
                            <td
                              style={{
                                padding:
                                  "13px 12px",
                                borderBottom:
                                  "1px solid #edf1f5",
                                color:
                                  "#1e293b",
                                fontSize:
                                  "12px",
                                fontWeight:
                                  800,
                              }}
                            >
                              {parcelId}
                            </td>

                            <td
                              style={{
                                padding:
                                  "13px 12px",
                                borderBottom:
                                  "1px solid #edf1f5",
                              }}
                            >
                              <RiskBadge
                                level={level}
                              />
                            </td>

                            <td
                              style={{
                                padding:
                                  "13px 12px",
                                borderBottom:
                                  "1px solid #edf1f5",
                                fontSize:
                                  "13px",
                                fontWeight:
                                  800,
                                color:
                                  "#1e293b",
                              }}
                            >
                              {score}
                            </td>

                            <td
                              style={{
                                padding:
                                  "13px 12px",
                                borderBottom:
                                  "1px solid #edf1f5",
                                fontSize:
                                  "12px",
                              }}
                            >
                              {parcel.land_use_changed ? (
                                <span
                                  style={{
                                    color:
                                      "#c2410c",
                                    fontWeight:
                                      700,
                                  }}
                                >
                                  {
                                    parcel.land_use_transition
                                  }
                                </span>
                              ) : (
                                <span
                                  style={{
                                    color:
                                      "#64748b",
                                  }}
                                >
                                  No change
                                </span>
                              )}
                            </td>

                            <td
                              style={{
                                padding:
                                  "13px 12px",
                                borderBottom:
                                  "1px solid #edf1f5",
                                color:
                                  "#526174",
                                fontSize:
                                  "12px",
                                lineHeight:
                                  1.5,
                                maxWidth:
                                  "420px",
                              }}
                            >
                              {Array.isArray(
                                parcel.why
                              )
                                ? parcel.why.join(
                                    " "
                                  )
                                : "Risk indicators detected."}
                            </td>
                          </tr>
                        );
                      }
                    )}
                  </tbody>
                </table>
              </div>
            )}
          </div>

          {/* ============================================= */}
          {/* DATA QUALITY / MODEL INFORMATION */}
          {/* ============================================= */}

          <div
            style={{
              display: "grid",
              gridTemplateColumns:
                "repeat(auto-fit, minmax(280px, 1fr))",
              gap: "18px",
            }}
          >
            <div
              style={{
                ...styles.card,
                padding: "18px",
              }}
            >
              <h3
                style={{
                  margin: 0,
                  fontSize: "14px",
                  color: "#1e293b",
                }}
              >
                Data Quality
              </h3>

              <div
                style={{
                  marginTop: "13px",
                  display: "grid",
                  gridTemplateColumns:
                    "1fr 1fr",
                  gap: "10px",
                }}
              >
                <div>
                  <div
                    style={{
                      color:
                        "#718096",
                      fontSize:
                        "10px",
                      fontWeight:
                        700,
                    }}
                  >
                    MISSING VALUES
                  </div>

                  <div
                    style={{
                      marginTop:
                        "4px",
                      fontSize:
                        "17px",
                      fontWeight:
                        800,
                    }}
                  >
                    {analysis
                      ?.data_quality
                      ?.missing_values ??
                      0}
                  </div>
                </div>

                <div>
                  <div
                    style={{
                      color:
                        "#718096",
                      fontSize:
                        "10px",
                      fontWeight:
                        700,
                    }}
                  >
                    DUPLICATES
                  </div>

                  <div
                    style={{
                      marginTop:
                        "4px",
                      fontSize:
                        "17px",
                      fontWeight:
                        800,
                    }}
                  >
                    {analysis
                      ?.data_quality
                      ?.duplicate_rows ??
                      0}
                  </div>
                </div>
              </div>
            </div>

            <div
              style={{
                ...styles.card,
                padding: "18px",
              }}
            >
              <h3
                style={{
                  margin: 0,
                  fontSize: "14px",
                  color: "#1e293b",
                }}
              >
                Model Transparency
              </h3>

              <p
                style={{
                  margin:
                    "10px 0 0",
                  color:
                    "#64748b",
                  fontSize:
                    "11px",
                  lineHeight:
                    1.6,
                }}
              >
                The risk score is an
                explainable pilot composite
                index. It is not a statistically
                validated probability of a future
                land dispute.
              </p>
            </div>
          </div>
        </>
      )}
    </div>
  );
}