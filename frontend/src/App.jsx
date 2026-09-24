import LandIntelligence from "./pages/LandIntelligence";

import { useEffect, useState } from "react";
import Login from "./pages/Login";
import Sidebar from "./components/Sidebar";

import Dashboard from "./pages/Dashboard";
import ResearchRepository from "./pages/ResearchRepository";
import PolicyExplorer from "./pages/PolicyExplorer";
import DatasetExplorer from "./pages/DatasetExplorer";
import GISExplorer from "./pages/GISExplorer";
import EvidenceEngine from "./pages/EvidenceEngine";
import PolicySandbox from "./pages/PolicySandbox";
import Analytics from "./pages/Analytics";
import DisputeWarning from "./pages/DisputeWarning";
import SDGScorecard from "./pages/SDGScorecard";
import Provenance from "./pages/Provenance";

import "./App.css";

const API_BASE_URL = "http://127.0.0.1:8000";

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(() =>
    Boolean(localStorage.getItem("land_governance_token"))
  );

  const [currentUser, setCurrentUser] = useState(() => {
    const storedUser = localStorage.getItem("land_governance_user");
    if (!storedUser) return null;

    try {
      return JSON.parse(storedUser);
    } catch {
      return null;
    }
  });

  const [authChecking, setAuthChecking] = useState(true);

  const [activePage, setActivePage] = useState("dashboard");
  const [notificationsOpen, setNotificationsOpen] = useState(false);
  const [helpOpen, setHelpOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");
  const [savedItemsCount, setSavedItemsCount] = useState(3);

  useEffect(() => {
    const token = localStorage.getItem("land_governance_token");
    const storedUser = localStorage.getItem("land_governance_user");

    if (!token || !storedUser) {
      setIsAuthenticated(false);
      setCurrentUser(null);
      setAuthChecking(false);
      return;
    }

    try {
      const user = JSON.parse(storedUser);

      if (!user?.username || !user?.role) {
        throw new Error("Invalid stored user");
      }

      setCurrentUser(user);
      setIsAuthenticated(true);
    } catch {
      localStorage.removeItem("land_governance_token");
      localStorage.removeItem("land_governance_user");
      setCurrentUser(null);
      setIsAuthenticated(false);
    } finally {
      setAuthChecking(false);
    }
  }, []);

  const handleLogin = (user, token) => {
    localStorage.setItem("land_governance_token", token);
    localStorage.setItem("land_governance_user", JSON.stringify(user));
    setCurrentUser(user);
    setIsAuthenticated(true);
    setActivePage("dashboard");
    setNotificationsOpen(false);
  };

  const handleLogout = () => {
    localStorage.removeItem("land_governance_token");
    localStorage.removeItem("land_governance_user");
    setCurrentUser(null);
    setIsAuthenticated(false);
    setActivePage("dashboard");
    setNotificationsOpen(false);
    setHelpOpen(false);
  };

  const getRoleLabel = (role) => {
    switch (role) {
      case "ADMIN":
        return "System Administrator";
      case "RESEARCHER":
        return "Research & Evidence";
      case "POLICY_MAKER":
        return "Policy Maker";
      default:
        return "Authenticated User";
    }
  };

  const getUserInitials = (username) => {
    if (!username) return "U";

    const parts = username.trim().split(/\s+/).filter(Boolean);

    if (parts.length >= 2) {
      return (parts[0][0] + parts[1][0]).toUpperCase();
    }

    return username.substring(0, 2).toUpperCase();
  };

  const notifications = [
    {
      id: 1,
      title: "Urgent Cadastral Boundary Conflict",
      desc: "Zone B-14 in Guwahati flagged for wetland overlay conflict.",
      time: "10 mins ago",
      urgent: true,
    },
    {
      id: 2,
      title: "New Remote Sensing Ingestion",
      desc: "Sentinel-2 NDVI layer updated for Northeast agrarian belt.",
      time: "1 hour ago",
      urgent: false,
    },
    {
      id: 3,
      title: "Policy Draft Uploaded",
      desc: "Model Tenancy Act (State Adaptation 2026) submitted for review.",
      time: "3 hours ago",
      urgent: false,
    },
  ];

  // =========================================================
  // PAGE NAVIGATION
  // =========================================================

  const navigateTo = (page) => {
    setActivePage(page);
    setNotificationsOpen(false);
  };

  // =========================================================
  // GLOBAL SEARCH
  // =========================================================

  const handleGlobalSearch = (e) => {
    e.preventDefault();

    if (!searchQuery.trim()) return;

    const q = searchQuery.toLowerCase().trim();

    if (
      q.includes("provenance") ||
      q.includes("hash") ||
      q.includes("traceability") ||
      q.includes("ledger")
    ) {
      navigateTo("provenance");
    } else if (
      q.includes("sdg") ||
      q.includes("sustainable") ||
      q.includes("development goal")
    ) {
      navigateTo("sdg-scorecard");
    } else if (
      q.includes("dispute") ||
      q.includes("warning") ||
      q.includes("risk")
    ) {
      navigateTo("dispute-warning");
    } else if (
      q.includes("gis") ||
      q.includes("map") ||
      q.includes("layer") ||
      q.includes("spatial")
    ) {
      navigateTo("gis");
    } else if (
      q.includes("policy") ||
      q.includes("act") ||
      q.includes("law")
    ) {
      navigateTo("policy");
    } else if (
      q.includes("data") ||
      q.includes("dataset") ||
      q.includes("csv") ||
      q.includes("geojson")
    ) {
      navigateTo("datasets");
    } else if (
      q.includes("ai") ||
      q.includes("evidence") ||
      q.includes("query")
    ) {
      navigateTo("evidence");
    } else if (
      q.includes("sandbox") ||
      q.includes("simulat") ||
      q.includes("scenario")
    ) {
      navigateTo("sandbox");
    } else if (
      q.includes("analytic") ||
      q.includes("trend") ||
      q.includes("anomaly") ||
      q.includes("chart")
    ) {
      navigateTo("analytics");
    } else if (
      q.includes("research") ||
      q.includes("paper") ||
      q.includes("document")
    ) {
      navigateTo("research");
    } else {
      navigateTo("research");
    }

    setSearchQuery("");
  };

  // =========================================================
  // PAGE RENDERING
  // =========================================================

  const renderPage = () => {
    switch (activePage) {
      case "dashboard":
        return <Dashboard onNavigate={navigateTo} />;

      case "research":
        return (
          <ResearchRepository
            savedCount={savedItemsCount}
            onToggleSave={(count) => setSavedItemsCount(count)}
          />
        );

      case "policy":
        return <PolicyExplorer onNavigate={navigateTo} />;

      case "datasets":
        return <DatasetExplorer onNavigate={navigateTo} />;

      case "gis":
        return <GISExplorer />;

      case "evidence":
        return <EvidenceEngine />;

      case "sandbox":
        return <PolicySandbox />;

      case "analytics":
        return <Analytics onNavigate={navigateTo} />;

      case "dispute-warning":
        return <DisputeWarning key="dispute-warning" />;

      case "sdg-scorecard":
        return <SDGScorecard key="sdg-scorecard" />;

      case "provenance":
        return <Provenance key="provenance" />;
      case "land-intelligence":
         return <LandIntelligence />;
      default:
        return <Dashboard onNavigate={navigateTo} />;
    }
  };

  if (authChecking) {
    return (
      <div
        style={{
          minHeight: "100vh",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          background: "linear-gradient(135deg, #07111f, #172554)",
          color: "#ffffff",
          fontFamily: "Inter, system-ui, sans-serif",
        }}
      >
        <div style={{ textAlign: "center" }}>
          <div
            style={{
              width: "42px",
              height: "42px",
              margin: "0 auto 14px",
              borderRadius: "50%",
              border: "4px solid rgba(255,255,255,0.22)",
              borderTopColor: "#38bdf8",
              animation: "landGovernanceSpin 0.8s linear infinite",
            }}
          />
          <div style={{ fontSize: "14px", fontWeight: 700 }}>
            Restoring secure session...
          </div>
        </div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return <Login onLogin={handleLogin} />;
  }

  return (
    <div className="app">
      <style>{`
        @keyframes landGovernanceSpin {
          to { transform: rotate(360deg); }
        }
      `}</style>

      {/* =====================================================
          SIDEBAR
      ====================================================== */}

      <Sidebar
        activePage={activePage}
        setActivePage={navigateTo}
        onOpenHelp={() => setHelpOpen(true)}
      />

      {/* =====================================================
          MAIN AREA
      ====================================================== */}

      <div className="main-area">

        {/* ===================================================
            TOP HEADER
        ==================================================== */}

        <header className="topbar">

          <div className="topbar-left">

            <h1 className="topbar-title">
              National Land Governance Platform
            </h1>

            <span className="topbar-subtitle">
              Unified Cadastral Intelligence, Policy Analytics &
              Evidence Framework
            </span>

          </div>

          {/* =================================================
              SEARCH
          ================================================== */}

          <form
            className="topbar-center"
            onSubmit={handleGlobalSearch}
          >

            <div className="search-box">

              <span>🔍</span>

              <input
                type="text"
                placeholder="Search research papers, policies, cadastral maps, or ask AI..."
                value={searchQuery}
                onChange={(e) =>
                  setSearchQuery(e.target.value)
                }
              />

              <span className="search-kbd">
                ↵ Enter
              </span>

            </div>

          </form>

          {/* =================================================
              HEADER ACTIONS
          ================================================== */}

          <div className="topbar-actions">

            {/* LIVE STATUS */}

            <div
              className="live-pill"
              title="National GIS nodes connected"
            >

              <span className="live-pill-dot"></span>

              <span>
                All 28 States Synced
              </span>

            </div>

            <div
              title="Current access role"
              style={{
                display: "inline-flex",
                alignItems: "center",
                gap: "6px",
                padding: "7px 10px",
                borderRadius: "999px",
                background: "#eff6ff",
                border: "1px solid #bfdbfe",
                color: "#1d4ed8",
                fontSize: "11px",
                fontWeight: 800,
                whiteSpace: "nowrap",
              }}
            >
              🔐 {currentUser?.role || "USER"}
            </div>

            {/* =================================================
                NOTIFICATIONS
            ================================================== */}

            <div className="notification-wrapper">

              <button
                className="notification-btn"
                onClick={() =>
                  setNotificationsOpen(
                    !notificationsOpen
                  )
                }
                title="Notifications"
              >

                🔔

                <span className="notification-count">
                  {notifications.length}
                </span>

              </button>

              {notificationsOpen && (
                <div className="notification-panel">

                  <div className="notif-header">

                    <h4>
                      Operational Alerts & Logs
                    </h4>

                    <span
                      className="badge"
                      style={{
                        fontSize: "10px",
                      }}
                    >
                      3 New
                    </span>

                  </div>

                  {notifications.map((n) => (
                    <div
                      key={n.id}
                      className={`notif-item ${
                        n.urgent ? "urgent" : ""
                      }`}
                    >

                      <div
                        style={{
                          fontWeight: 700,
                        }}
                      >
                        {n.title}
                      </div>

                      <div className="alert-text">
                        {n.desc}
                      </div>

                      <div className="notif-time">
                        {n.time}
                      </div>

                    </div>
                  ))}

                  <button
                    className="btn btn-secondary btn-sm"
                    style={{
                      width: "100%",
                      marginTop: "6px",
                    }}
                    onClick={() =>
                      setNotificationsOpen(false)
                    }
                  >
                    Dismiss Panel
                  </button>

                </div>
              )}

            </div>

            {/* =================================================
                ADMIN
            ================================================== */}

            <div
              className="admin-area"
              style={{
                display: "flex",
                alignItems: "center",
                gap: "10px",
              }}
            >
              <div
                className="admin-info"
                style={{ textAlign: "right" }}
              >
                <strong>
                  {currentUser?.username || "User"}
                </strong>
                <span>
                  {getRoleLabel(currentUser?.role)}
                </span>
              </div>

              <div
                className="admin-avatar"
                title={currentUser?.role || "Authenticated User"}
              >
                {getUserInitials(currentUser?.username)}
              </div>

              <button
                type="button"
                onClick={handleLogout}
                title="Sign out"
                style={{
                  border: "1px solid #cbd5e1",
                  background: "#ffffff",
                  color: "#334155",
                  borderRadius: "9px",
                  padding: "8px 11px",
                  fontSize: "12px",
                  fontWeight: 700,
                  cursor: "pointer",
                }}
              >
                Logout
              </button>
            </div>

          </div>

        </header>

        {/* ===================================================
            PAGE CONTENT
        ==================================================== */}

        <main className="content">
          {renderPage()}
        </main>

      </div>

      {/* =====================================================
          HELP MODAL
      ====================================================== */}

      {helpOpen && (

        <div
          className="modal-overlay"
          onClick={() => setHelpOpen(false)}
        >

          <div
            className="modal-content"
            onClick={(e) =>
              e.stopPropagation()
            }
          >

            <div className="modal-header">

              <h3
                style={{
                  margin: 0,
                  fontSize: "18px",
                  color: "var(--slate-900)",
                }}
              >
                📖 National Land Governance Guide
              </h3>

              <button
                className="modal-close-btn"
                onClick={() =>
                  setHelpOpen(false)
                }
              >
                ✕
              </button>

            </div>

            <div
              style={{
                fontSize: "14px",
                lineHeight: "1.6",
                color: "var(--slate-700)",
              }}
            >

              <p>
                Welcome to the{" "}
                <strong>
                  National Land Governance Platform
                </strong>
                . Here is how to use the modules:
              </p>

              <ul
                style={{
                  paddingLeft: "20px",
                  marginTop: "10px",
                  display: "flex",
                  flexDirection: "column",
                  gap: "8px",
                }}
              >

                <li>
                  <strong>🏠 Dashboard:</strong>{" "}
                  High-level platform KPIs and system status.
                </li>

                <li>
                  <strong>📚 Research Repository:</strong>{" "}
                  Research documents and evidence resources.
                </li>

                <li>
                  <strong>📜 Policy Explorer:</strong>{" "}
                  Registered land-governance policies.
                </li>

                <li>
                  <strong>📁 Dataset Explorer:</strong>{" "}
                  Registered datasets.
                </li>

                <li>
                  <strong>🗺️ GIS Explorer:</strong>{" "}
                  GIS layers and spatial information.
                </li>

                <li>
                  <strong>🤖 Evidence Engine:</strong>{" "}
                  AI-assisted evidence synthesis.
                </li>

                <li>
                  <strong>🧪 Policy Sandbox:</strong>{" "}
                  Policy scenario simulation.
                </li>

                <li>
                  <strong>📊 Analytics:</strong>{" "}
                  Trend and anomaly analysis.
                </li>

                <li>
                  <strong>⚠️ Dispute Warning:</strong>{" "}
                  Land-dispute early-warning analysis.
                </li>

                <li>
                  <strong>🎯 SDG Scorecard:</strong>{" "}
                  Sustainable-development impact scoring.
                </li>

                <li>
                  <strong>🔗 Evidence Provenance:</strong>{" "}
                  Evidence traceability and provenance verification.
                </li>

              </ul>

              <div
                style={{
                  marginTop: "20px",
                  textAlign: "right",
                }}
              >

                <button
                  className="btn btn-primary"
                  onClick={() =>
                    setHelpOpen(false)
                  }
                >
                  Got it!
                </button>

              </div>

            </div>

          </div>

        </div>

      )}

    </div>
  );
}

export default App;