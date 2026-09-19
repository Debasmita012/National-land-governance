import React from "react";

function Sidebar({ activePage, setActivePage, onOpenHelp }) {
  const menuItems = [
    {
      id: "dashboard",
      icon: "🏠",
      label: "Dashboard",
    },
    {
      id: "research",
      icon: "📚",
      label: "Research Repository",
      badge: "1.2k",
    },
    {
      id: "policy",
      icon: "📜",
      label: "Policy Explorer",
    },
    {
      id: "datasets",
      icon: "📁",
      label: "Dataset Explorer",
      badge: "356",
    },
    {
      id: "gis",
      icon: "🗺️",
      label: "GIS Explorer",
      badge: "LIVE",
      badgePulse: true,
    },
    {
      id: "land-intelligence",
      icon: "🧠",
      label: "Land Intelligence",
      badge: "AI",
    },
    {
      id: "evidence",
      icon: "🤖",
      label: "Evidence Engine",
      badge: "AI",
    },
    {
      id: "sandbox",
      icon: "🧪",
      label: "Policy Sandbox",
    },
    {
      id: "analytics",
      icon: "📊",
      label: "Analytics",
    },

    // ---------------------------------------------------------
    // NEW INTELLIGENCE MODULES
    // ---------------------------------------------------------

    {
      id: "dispute-warning",
      icon: "⚠️",
      label: "Dispute Warning",
      badge: "RISK",
    },
    {
      id: "sdg-scorecard",
      icon: "🎯",
      label: "SDG Scorecard",
      badge: "SDG",
    },
    {
      id: "provenance",
      icon: "🔗",
      label: "Evidence Provenance",
      badge: "TRACE",
    },
  ];

  return (
    <aside className="sidebar">

      {/* =====================================================
          LOGO
      ====================================================== */}
      <div className="sidebar-logo">
        <div className="logo-brand">

          <div className="logo-emblem">
            🌐
          </div>

          <div className="logo-text-group">

            <div className="logo-mark">
              LAND<span>GOV</span>
            </div>

            <div className="logo-subtitle">
              National Land Governance
            </div>

          </div>

        </div>
      </div>

      {/* =====================================================
          NAVIGATION
      ====================================================== */}
      <nav className="sidebar-navigation">

        <div className="nav-title">
          Intelligence Core
        </div>

        {menuItems.map((item) => {

          const isActive = activePage === item.id;

          return (
            <button
              key={item.id}
              className={`sidebar-item ${
                isActive ? "active" : ""
              }`}
              onClick={() => setActivePage(item.id)}
            >

              <span className="sidebar-icon">
                {item.icon}
              </span>

              <span className="sidebar-label">
                {item.label}
              </span>

              {item.badge && (
                <span
                  className={`sidebar-badge ${
                    item.badgePulse ? "pulse" : ""
                  }`}
                >
                  {item.badge}
                </span>
              )}

            </button>
          );
        })}

      </nav>

      {/* =====================================================
          BOTTOM SECTION
      ====================================================== */}
      <div className="sidebar-bottom">

        {/* SYSTEM STATUS */}
        <div className="system-status">

          <span className="status-dot"></span>

          <div>
            <div className="status-title">
              System Online
            </div>

            <div className="status-text">
              Cadastral & GIS Sync Active
            </div>
          </div>

        </div>

        {/* HELP */}
        <button
          className="sidebar-help"
          onClick={onOpenHelp}
        >
          <span>💡</span>
          Quick User Guide
        </button>

      </div>

    </aside>
  );
}

export default Sidebar;