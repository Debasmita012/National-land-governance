import { useState } from "react";

const API_BASE_URL = "http://127.0.0.1:8000";

const presetQueries = [
  {
    title: "Land Governance Challenges",
    query:
      "What are the major land governance challenges in India and how can technology improve land administration?",
  },
  {
    title: "Land Records & Disputes",
    query:
      "How do weaknesses in land records contribute to land disputes in India?",
  },
  {
    title: "Urban Land Governance",
    query:
      "What are the major challenges in urban land governance in India?",
  },
];

function EvidenceEngine() {
  const [messages, setMessages] = useState([]);
  const [userInput, setUserInput] = useState("");
  const [isSynthesizing, setIsSynthesizing] = useState(false);

  const generateEvidence = async (queryText) => {
    const response = await fetch(
      `${API_BASE_URL}/evidence-cards/generate`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          question: queryText,
          supporting_datasets: [
  {
    dataset_id: 1,
    name: "Agricultural Land Dataset",
    source: "National Land Governance Platform",
  },
],
          affected_geography: "Pilot District",
        }),
      }
    );

    let data = null;

    try {
      data = await response.json();
    } catch {
      data = null;
    }

    if (!response.ok) {
      const errorDetail =
  typeof data?.detail === "string"
    ? data.detail
    : JSON.stringify(data?.detail);

throw new Error(
  errorDetail ||
    `Backend request failed with status ${response.status}.`
);
    }

    return data;
  };

  const convertBackendResponse = (data, queryText) => {
    const confidenceScore = Number(data?.confidence_score);

    const confidence = Number.isFinite(confidenceScore)
      ? Math.round(confidenceScore * 100)
      : null;

    const citations = Array.isArray(data?.citations)
      ? data.citations
      : [];

    const supportingDocuments = Array.isArray(data?.supporting_documents)
      ? data.supporting_documents
      : [];

    const sources = [
      ...supportingDocuments.map(
        (document) =>
          document?.title ||
          document?.source ||
          `Research document ${document?.document_id}`
      ),
      ...citations.map(
        (citation) =>
          citation?.document_title ||
          citation?.source ||
          `Research document ${citation?.document_id}`
      ),
    ].filter(Boolean);

    const uniqueSources = [...new Set(sources)];

    return {
      role: "assistant",
      query: queryText,

      content:
        data?.recommendation ||
        "The backend returned an evidence card without a recommendation.",

      legalBasis: data?.affected_geography
        ? `Affected geography: ${data.affected_geography}`
        : null,

      confidence,

      confidenceLevel: data?.confidence_level,

      retrievalConfidence: data?.retrieval_confidence,

      evidenceCoverage: data?.evidence_coverage,

      sources:
        uniqueSources.length > 0
          ? uniqueSources
          : null,

      supportingDocuments,

      citations,

      positiveImpacts:
        data?.expected_impacts?.positive || [],

      negativeImpacts:
        data?.expected_impacts?.negative || [],

      risks:
        data?.risks_limitations || [],

      alternatives:
        data?.alternatives || [],

      evidenceCardId: data?.id,

      time: "Just now",
    };
  };

  const runQuery = async (queryText) => {
    if (isSynthesizing || !queryText.trim()) {
      return;
    }

    setIsSynthesizing(true);

    setMessages((prev) => [
      ...prev,
      {
        role: "user",
        content: queryText,
        time: "Just now",
      },
    ]);

    try {
      const data = await generateEvidence(queryText);

      const assistantMessage = convertBackendResponse(
        data,
        queryText
      );

      setMessages((prev) => [
        ...prev,
        assistantMessage,
      ]);
    } catch (error) {
      console.error(
        "Evidence Engine error:",
        error
      );

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content:
            `Unable to generate evidence from the backend. ${error.message}`,
          legalBasis: null,
          confidence: null,
          sources: null,
          time: "Just now",
        },
      ]);
    } finally {
      setIsSynthesizing(false);
    }
  };

  const handleSelectPreset = (preset) => {
    runQuery(preset.query);
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    const queryText = userInput.trim();

    if (!queryText) {
      return;
    }

    setUserInput("");

    runQuery(queryText);
  };

  return (
    <div className="evidence-page">

      {/* Page Header */}
      <div className="page-header">
        <div className="page-title-group">
          <h2>
            🤖 AI Evidence & Statutory Inquiry Engine
          </h2>

          <p>
            Synthesize policy evidence, research, and
            land-governance data for decision makers.
          </p>
        </div>

        <div className="page-actions">
          <button
            className="btn btn-outline"
            onClick={() => {
              const text = messages
                .map(
                  (m) =>
                    `${m.role.toUpperCase()}: ${m.content}`
                )
                .join("\n\n");

              navigator.clipboard?.writeText(text);

              alert(
                "Executive briefing thread copied to clipboard!"
              );
            }}
          >
            📋 Export Briefing Memo
          </button>
        </div>
      </div>

      {/* Main Layout */}
      <div className="evidence-layout">

        {/* Left Panel */}
        <div
          className="panel"
          style={{
            margin: 0,
            display: "flex",
            flexDirection: "column",
            gap: "18px",
          }}
        >
          <div>

            <div
              style={{
                fontSize: "12px",
                fontWeight: 700,
                color: "var(--slate-500)",
                textTransform: "uppercase",
                marginBottom: "8px",
              }}
            >
              Curated Land Policy Inquiries
            </div>

            <p
              style={{
                fontSize: "12px",
                color: "var(--slate-500)",
                marginBottom: "14px",
              }}
            >
              Ask questions and retrieve evidence from
              the connected land-governance knowledge base.
            </p>

            <div className="prompt-suggestions">

              {presetQueries.map((pq, idx) => (
                <button
                  key={idx}
                  className="prompt-chip"
                  onClick={() =>
                    handleSelectPreset(pq)
                  }
                  disabled={isSynthesizing}
                >
                  <div
                    style={{
                      fontWeight: 700,
                      color: "var(--slate-900)",
                      marginBottom: "4px",
                    }}
                  >
                    {pq.title}
                  </div>

                  <div
                    style={{
                      fontSize: "11px",
                      color: "var(--slate-600)",
                    }}
                  >
                    {pq.query}
                  </div>
                </button>
              ))}

            </div>
          </div>

          <div
            style={{
              marginTop: "auto",
              padding: "14px",
              background: "var(--slate-50)",
              borderRadius: "8px",
              border: "1px solid var(--slate-200)",
              fontSize: "12px",
              color: "var(--slate-600)",
            }}
          >
            <div
              style={{
                fontWeight: 700,
                color: "var(--slate-800)",
                marginBottom: "4px",
              }}
            >
              🛡️ Evidence Chain Verification
            </div>

            Evidence is retrieved from the connected
            research and land-governance knowledge base.
          </div>
        </div>

        {/* Right Panel */}
        <div className="chat-thread">

          <div className="chat-messages">

            {messages.map((m, idx) => (

              <div
                key={idx}
                className={
                  m.role === "user"
                    ? "chat-bubble-user"
                    : "chat-bubble-ai"
                }
              >

                {m.role === "assistant" && (
                  <div
                    style={{
                      display: "flex",
                      alignItems: "center",
                      gap: "8px",
                      marginBottom: "10px",
                      flexWrap: "wrap",
                    }}
                  >

                    <span
                      style={{
                        fontSize: "16px",
                      }}
                    >
                      🌐
                    </span>

                    <strong
                      style={{
                        fontSize: "13px",
                        color: "var(--primary-800)",
                      }}
                    >
                      LandGov Evidence Synthesis
                    </strong>

                    {m.confidence !== null &&
                      m.confidence !== undefined && (
                        <span className="confidence-gauge">
                          ✓ {m.confidence}% Evidence Confidence
                        </span>
                      )}

                  </div>
                )}

                <div
                  style={{
                    fontSize: "13px",
                    lineHeight: "1.6",
                  }}
                >
                  {m.content}
                </div>

                {m.confidenceLevel && (
                  <div
                    style={{
                      marginTop: "8px",
                      fontSize: "12px",
                      fontWeight: 600,
                    }}
                  >
                    Confidence level:{" "}
                    {m.confidenceLevel}
                  </div>
                )}

                {m.evidenceCardId && (
                  <div
                    style={{
                      marginTop: "8px",
                      fontSize: "11px",
                      color: "var(--slate-500)",
                    }}
                  >
                    Evidence Card ID:{" "}
                    {m.evidenceCardId}
                  </div>
                )}

                {m.legalBasis && (
                  <div
                    style={{
                      marginTop: "12px",
                      padding: "10px 12px",
                      background: "#ffffff",
                      border:
                        "1px solid var(--slate-200)",
                      borderRadius: "6px",
                      fontSize: "12px",
                    }}
                  >
                    <strong>
                      Affected Geography:
                    </strong>{" "}
                    {m.legalBasis}
                  </div>
                )}

                {m.sources &&
                  m.sources.length > 0 && (
                    <div
                      style={{
                        marginTop: "10px",
                      }}
                    >
                      <div
                        style={{
                          fontSize: "11px",
                          fontWeight: 700,
                          color: "var(--slate-500)",
                          textTransform: "uppercase",
                        }}
                      >
                        Supporting Sources
                      </div>

                      <ul
                        style={{
                          paddingLeft: "16px",
                          marginTop: "4px",
                          fontSize: "11px",
                          color: "var(--slate-600)",
                        }}
                      >
                        {m.sources.map((s, i) => (
                          <li key={i}>{s}</li>
                        ))}
                      </ul>
                    </div>
                  )}

                {m.positiveImpacts?.length > 0 && (
                  <div
                    style={{
                      marginTop: "12px",
                      fontSize: "12px",
                    }}
                  >
                    <strong>
                      Positive Impacts:
                    </strong>

                    <ul>
                      {m.positiveImpacts.map(
                        (impact, i) => (
                          <li key={i}>{impact}</li>
                        )
                      )}
                    </ul>
                  </div>
                )}

                {m.negativeImpacts?.length > 0 && (
                  <div
                    style={{
                      marginTop: "12px",
                      fontSize: "12px",
                    }}
                  >
                    <strong>
                      Negative Impacts:
                    </strong>

                    <ul>
                      {m.negativeImpacts.map(
                        (impact, i) => (
                          <li key={i}>{impact}</li>
                        )
                      )}
                    </ul>
                  </div>
                )}

                {m.risks?.length > 0 && (
                  <div
                    style={{
                      marginTop: "12px",
                      fontSize: "12px",
                    }}
                  >
                    <strong>
                      Risks & Limitations:
                    </strong>

                    <ul>
                      {m.risks.map(
                        (risk, i) => (
                          <li key={i}>{risk}</li>
                        )
                      )}
                    </ul>
                  </div>
                )}

                {m.alternatives?.length > 0 && (
                  <div
                    style={{
                      marginTop: "12px",
                      fontSize: "12px",
                    }}
                  >
                    <strong>
                      Alternatives:
                    </strong>

                    <ul>
                      {m.alternatives.map(
                        (alternative, i) => (
                          <li key={i}>
                            {alternative}
                          </li>
                        )
                      )}
                    </ul>
                  </div>
                )}

              </div>
            ))}

            {isSynthesizing && (
              <div
                className="chat-bubble-ai"
                style={{
                  display: "flex",
                  alignItems: "center",
                  gap: "10px",
                }}
              >
                <span className="live-pill-dot"></span>

                <span
                  style={{
                    fontSize: "12px",
                    color: "var(--slate-600)",
                  }}
                >
                  Retrieving evidence from the
                  knowledge base...
                </span>
              </div>
            )}

          </div>

          {/* User Input */}
          <form
            onSubmit={handleSubmit}
            style={{
              marginTop: "18px",
              display: "flex",
              gap: "10px",
            }}
          >

            <input
              type="text"
              className="input-control"
              placeholder="Ask a land governance question..."
              value={userInput}
              onChange={(e) =>
                setUserInput(e.target.value)
              }
              disabled={isSynthesizing}
            />

            <button
              type="submit"
              className="btn btn-primary"
              disabled={isSynthesizing}
              style={{
                minWidth: "120px",
              }}
            >
              Ask AI
            </button>

          </form>

        </div>
      </div>
    </div>
  );
}

export default EvidenceEngine;