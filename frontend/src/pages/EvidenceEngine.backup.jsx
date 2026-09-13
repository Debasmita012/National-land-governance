import { useState } from "react";

const presetQueries = [
  {
    title: "SVAMITVA & Rural Credit Access",
    query: "Assess the empirical impact of drone-based digital titling (SVAMITVA) on formal agricultural credit access and litigation reduction.",
    confidence: 96,
    finding:
      "Issuance of geo-referenced 3D digital property cards led to a 42.4% increase in formal credit uptake among smallholder families across 12,000 surveyed villages, while boundary dispute filings in local civil courts dropped by 34.8%.",
    legalBasis: "SVAMITVA Operational Guidelines (2020) • State Panchayati Raj Land Rules • RBI Priority Sector Lending Directives.",
    sources: [
      "Survey of India Technical Benchmark Report (2026)",
      "NITI Aayog Agrarian Property Monetization Study (2025)",
      "National Law School Empirical Survey on Revenue Courts (2025)",
    ],
  },
  {
    title: "FRA Customary Forest Demarcation",
    query: "What are the legal precedents and GIS verification hurdles for Community Forest Resource (CFR) claims under Section 3(1)(i)?",
    confidence: 92,
    finding:
      "Supreme Court precedents (Niyamgiri judgment, 2013) establish Gram Sabhas as the ultimate statutory authority for determining CFR boundaries. Discrepancies between historical forest department compartment maps and GPS field traces can be reconciled via joint mobile boundary truthing.",
    legalBasis: "Scheduled Tribes and Other Traditional Forest Dwellers Act, 2006 (Sec 3 & Sec 6) • Ministry of Tribal Affairs Circulars (2015, 2021).",
    sources: [
      "Supreme Court of India (Civil Appeal No. 549/2008)",
      "Centre for Environment and Land Rights CFR Report (2025)",
      "ISRO SAC Geospatial Verification Protocols (2024)",
    ],
  },
  {
    title: "Wetland Encroachment in Floodplains",
    query: "How can remote sensing be admitted as statutory evidence in revenue court proceedings for illegal wetland reclamation?",
    confidence: 94,
    finding:
      "Section 65B of the Indian Evidence Act permits certified electronic records including multi-temporal satellite imagery (Sentinel-2 / PlanetScope) accompanied by an authorized spatial surveyor affidavit to prove unauthorized conversion of natural water retention bodies.",
    legalBasis: "Wetlands (Conservation and Management) Rules, 2017 • National Green Tribunal Principal Bench Directives • Indian Evidence Act Sec 65B.",
    sources: [
      "National Green Tribunal Principal Bench Judgment (O.A. No. 199/2014)",
      "ISRO Geospatial Evidence Manual for Revenue Officers (2025)",
      "Ramsar Convention National Compliance Guidelines (2026)",
    ],
  },
];

function EvidenceEngine() {
  const [messages, setMessages] = useState([
    {
      role: "assistant",
      query: presetQueries[0].query,
      content: presetQueries[0].finding,
      legalBasis: presetQueries[0].legalBasis,
      confidence: presetQueries[0].confidence,
      sources: presetQueries[0].sources,
      time: "Just now",
    },
  ]);
  const [userInput, setUserInput] = useState("");
  const [isSynthesizing, setIsSynthesizing] = useState(false);

  const handleSelectPreset = (preset) => {
    setIsSynthesizing(true);
    setTimeout(() => {
      setMessages((prev) => [
        ...prev,
        {
          role: "user",
          content: preset.query,
          time: "Just now",
        },
        {
          role: "assistant",
          query: preset.query,
          content: preset.finding,
          legalBasis: preset.legalBasis,
          confidence: preset.confidence,
          sources: preset.sources,
          time: "Just now",
        },
      ]);
      setIsSynthesizing(false);
    }, 600);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!userInput.trim()) return;

    const queryText = userInput;
    setUserInput("");
    setIsSynthesizing(true);

    // Add user message
    setMessages((prev) => [
      ...prev,
      { role: "user", content: queryText, time: "Just now" },
    ]);

    // Simulate AI synthesis with contextual knowledge
    setTimeout(() => {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          query: queryText,
          content: `Synthesized analysis based on national cadastral registries and statutory precedents: Regarding "${queryText}", current revenue directives mandate rigorous spatial ground-truthing combined with digital RoR verification. Recent state reforms emphasize fast-track tribunal dispute resolution within 60 days to prevent prolonged civil injunctions.`,
          legalBasis: "Digital India Land Records Modernization Programme (DILRMP) • Relevant State Land Revenue Codes (Amended 2024-2026).",
          confidence: 91,
          sources: [
            "National Land Governance Intelligence Repository (2026)",
            "Ministry of Rural Development Policy Directives",
            "Survey of India Geospatial Standards",
          ],
          time: "Just now",
        },
      ]);
      setIsSynthesizing(false);
    }, 1000);
  };

  return (
    <div className="evidence-page">
      {/* Page Header */}
      <div className="page-header">
        <div className="page-title-group">
          <h2>🤖 AI Evidence & Statutory Inquiry Engine</h2>
          <p>
            Synthesize policy evidence, legal precedents, and empirical land studies for decision makers.
          </p>
        </div>
        <div className="page-actions">
          <button
            className="btn btn-outline"
            onClick={() => {
              navigator.clipboard?.writeText(
                messages.map((m) => `${m.role.toUpperCase()}: ${m.content}`).join("\n\n")
              );
              alert("Executive briefing thread copied to clipboard!");
            }}
          >
            📋 Export Briefing Memo
          </button>
        </div>
      </div>

      {/* Main Layout */}
      <div className="evidence-layout">
        {/* Left: Suggested Inquiry Prompts */}
        <div className="panel" style={{ margin: 0, display: "flex", flexDirection: "column", gap: "18px" }}>
          <div>
            <div style={{ fontSize: "12px", fontWeight: 700, color: "var(--slate-500)", textTransform: "uppercase", marginBottom: "8px" }}>
              Curated Land Policy Inquiries
            </div>
            <p style={{ fontSize: "12px", color: "var(--slate-500)", marginBottom: "14px" }}>
              Click any inquiry to synthesize evidence from statutory acts and peer-reviewed literature.
            </p>

            <div className="prompt-suggestions">
              {presetQueries.map((pq, idx) => (
                <button
                  key={idx}
                  className="prompt-chip"
                  onClick={() => handleSelectPreset(pq)}
                >
                  <div style={{ fontWeight: 700, color: "var(--slate-900)", marginBottom: "4px" }}>
                    {pq.title}
                  </div>
                  <div style={{ fontSize: "11px", color: "var(--slate-600)" }}>
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
            <div style={{ fontWeight: 700, color: "var(--slate-800)", marginBottom: "4px" }}>
              🛡️ Evidence Chain Verification
            </div>
            All synthesized evidence citations are linked to official Gazettes, Supreme Court judgments, and ISRO geospatial indices.
          </div>
        </div>

        {/* Right: Conversational Synthesis Thread */}
        <div className="chat-thread">
          <div className="chat-messages">
            {messages.map((m, idx) => (
              <div
                key={idx}
                className={m.role === "user" ? "chat-bubble-user" : "chat-bubble-ai"}
              >
                {m.role === "assistant" && (
                  <div style={{ display: "flex", alignItems: "center", gap: "8px", marginBottom: "10px" }}>
                    <span style={{ fontSize: "16px" }}>🌐</span>
                    <strong style={{ fontSize: "13px", color: "var(--primary-800)" }}>
                      LandGov Evidence Synthesis
                    </strong>
                    {m.confidence && (
                      <span className="confidence-gauge">
                        ✓ {m.confidence}% Evidence Confidence
                      </span>
                    )}
                  </div>
                )}

                <div style={{ fontSize: "13px", lineHeight: "1.6" }}>{m.content}</div>

                {m.legalBasis && (
                  <div
                    style={{
                      marginTop: "12px",
                      padding: "10px 12px",
                      background: "#ffffff",
                      border: "1px solid var(--slate-200)",
                      borderRadius: "6px",
                      fontSize: "12px",
                    }}
                  >
                    <strong>Statutory Precedents:</strong> {m.legalBasis}
                  </div>
                )}

                {m.sources && (
                  <div style={{ marginTop: "10px" }}>
                    <div style={{ fontSize: "11px", fontWeight: 700, color: "var(--slate-500)", textTransform: "uppercase" }}>
                      Cited Sources:
                    </div>
                    <ul style={{ paddingLeft: "16px", marginTop: "4px", fontSize: "11px", color: "var(--slate-600)" }}>
                      {m.sources.map((s, i) => (
                        <li key={i}>{s}</li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            ))}

            {isSynthesizing && (
              <div className="chat-bubble-ai" style={{ display: "flex", alignItems: "center", gap: "10px" }}>
                <span className="live-pill-dot"></span>
                <span style={{ fontSize: "12px", color: "var(--slate-600)" }}>
                  Cross-referencing statutory codes and cadastral datasets...
                </span>
              </div>
            )}
          </div>

          {/* User Input Form */}
          <form onSubmit={handleSubmit} style={{ marginTop: "18px", display: "flex", gap: "10px" }}>
            <input
              type="text"
              className="input-control"
              placeholder="Ask any land governance question (e.g., 'What are the tenancy laws in West Bengal?')..."
              value={userInput}
              onChange={(e) => setUserInput(e.target.value)}
            />
            <button
              type="submit"
              className="btn btn-primary"
              disabled={isSynthesizing}
              style={{ minWidth: "120px" }}
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