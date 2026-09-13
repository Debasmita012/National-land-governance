import { useEffect, useState } from "react";

import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";


function Dashboard({ onNavigate }) {

  const [documents, setDocuments] = useState([]);
  const [datasets, setDatasets] = useState([]);
  const [policies, setPolicies] = useState([]);
  const [gisLayers, setGisLayers] = useState([]);

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");


  // -------------------------------------------------------
  // LOAD REAL PLATFORM DATA
  // -------------------------------------------------------

  useEffect(() => {

    const loadDashboardData = async () => {

      try {

        setLoading(true);
        setError("");

        const [
          documentsResponse,
          datasetsResponse,
          policiesResponse,
          gisResponse,
        ] = await Promise.all([

          fetch(
            "http://127.0.0.1:8000/documents/"
          ),

          fetch(
            "http://127.0.0.1:8000/datasets/"
          ),

          fetch(
            "http://127.0.0.1:8000/policies/"
          ),

          fetch(
            "http://127.0.0.1:8000/gis-layers/"
          ),

        ]);


        if (
          !documentsResponse.ok ||
          !datasetsResponse.ok ||
          !policiesResponse.ok ||
          !gisResponse.ok
        ) {

          throw new Error(
            "Unable to load dashboard data from backend."
          );

        }


        const [
          documentsData,
          datasetsData,
          policiesData,
          gisData,
        ] = await Promise.all([

          documentsResponse.json(),
          datasetsResponse.json(),
          policiesResponse.json(),
          gisResponse.json(),

        ]);


        setDocuments(documentsData);
        setDatasets(datasetsData);
        setPolicies(policiesData);
        setGisLayers(gisData);

      } catch (err) {

        console.error(
          "Dashboard loading error:",
          err
        );

        setError(
          err.message ||
          "Unable to load dashboard data."
        );

      } finally {

        setLoading(false);

      }

    };


    loadDashboardData();

  }, []);


  // -------------------------------------------------------
  // REAL REGISTRY COUNTS
  // -------------------------------------------------------

  const researchCount = documents.length;
  const datasetCount = datasets.length;
  const policyCount = policies.length;
  const gisLayerCount = gisLayers.length;


  const registryChartData = [
    {
      category: "Research",
      count: researchCount,
    },
    {
      category: "Datasets",
      count: datasetCount,
    },
    {
      category: "Policies",
      count: policyCount,
    },
    {
      category: "GIS Layers",
      count: gisLayerCount,
    },
  ];


  return (

    <div className="dashboard-page">


      {/* HERO */}

      <div className="hero-banner">

        <div className="hero-content">

          <div className="hero-tag">
            <span>🛡️</span>
            Land Governance Intelligence Platform
          </div>


          <h2 className="hero-title">
            Land Governance & Geospatial Intelligence
          </h2>


          <p className="hero-description">
            Integrated research, datasets, policies,
            GIS layers, AI evidence analysis and
            policy simulation for evidence-based
            land governance.
          </p>


          {/* REAL PLATFORM COUNTS */}

          <div className="hero-stats-row">

            <div className="hero-mini-stat">

              <span className="hero-mini-val">
                {researchCount}
              </span>

              <span className="hero-mini-lbl">
                Registered Research Documents
              </span>

            </div>


            <div className="hero-mini-stat">

              <span className="hero-mini-val">
                {datasetCount}
              </span>

              <span className="hero-mini-lbl">
                Registered Datasets
              </span>

            </div>


            <div className="hero-mini-stat">

              <span className="hero-mini-val">
                {gisLayerCount}
              </span>

              <span className="hero-mini-lbl">
                Registered GIS Layers
              </span>

            </div>

          </div>

        </div>

      </div>



      {/* ERROR */}

      {error && (

        <div
          style={{
            marginTop: "16px",
            padding: "12px",
            borderRadius: "8px",
            background: "#fef2f2",
            border: "1px solid #fecaca",
            color: "#dc2626",
            fontSize: "12px",
          }}
        >
          {error}
        </div>

      )}



      {/* METRICS */}

      <div className="metrics-grid">


        <div className="metric-card">

          <div className="metric-top">

            <div className="metric-icon-wrap metric-icon-teal">
              📚
            </div>

            <span className="metric-trend">
              Backend
            </span>

          </div>

          <div className="metric-label">
            Research Documents
          </div>

          <div className="metric-value">
            {loading ? "..." : researchCount}
          </div>

          <div className="metric-subtitle">
            Records registered in the research repository
          </div>

        </div>



        <div className="metric-card">

          <div className="metric-top">

            <div className="metric-icon-wrap metric-icon-blue">
              📁
            </div>

            <span className="metric-trend">
              Backend
            </span>

          </div>

          <div className="metric-label">
            Datasets
          </div>

          <div className="metric-value">
            {loading ? "..." : datasetCount}
          </div>

          <div className="metric-subtitle">
            Dataset records registered in PostgreSQL
          </div>

        </div>



        <div className="metric-card">

          <div className="metric-top">

            <div className="metric-icon-wrap metric-icon-amber">
              📜
            </div>

            <span className="metric-trend">
              Backend
            </span>

          </div>

          <div className="metric-label">
            Policies
          </div>

          <div className="metric-value">
            {loading ? "..." : policyCount}
          </div>

          <div className="metric-subtitle">
            Policy records available for analysis
          </div>

        </div>



        <div className="metric-card">

          <div className="metric-top">

            <div className="metric-icon-wrap metric-icon-purple">
              🗺️
            </div>

            <span className="metric-trend">
              Backend
            </span>

          </div>

          <div className="metric-label">
            GIS Layers
          </div>

          <div className="metric-value">
            {loading ? "..." : gisLayerCount}
          </div>

          <div className="metric-subtitle">
            Spatial layers registered in the GIS registry
          </div>

        </div>

      </div>



      {/* MAIN DASHBOARD */}

      <div className="dashboard-grid">


        {/* REAL REGISTRY CHART */}

        <div className="panel">

          <div className="panel-header">

            <div className="panel-title-group">

              <h3>
                Platform Data Registry
              </h3>

              <p>
                Current records available across
                the core platform services
              </p>

            </div>

          </div>


          <div
            style={{
              width: "100%",
              height: 320,
              marginTop: "10px",
            }}
          >

            <ResponsiveContainer
              width="100%"
              height="100%"
            >

              <BarChart
                data={registryChartData}
                margin={{
                  top: 10,
                  right: 20,
                  left: -10,
                  bottom: 0,
                }}
              >

                <CartesianGrid
                  strokeDasharray="3 3"
                  stroke="#e2e8f0"
                  vertical={false}
                />

                <XAxis
                  dataKey="category"
                  stroke="#64748b"
                  fontSize={12}
                  tickLine={false}
                />

                <YAxis
                  stroke="#64748b"
                  fontSize={12}
                  tickLine={false}
                  axisLine={false}
                  allowDecimals={false}
                />

                <Tooltip
                  contentStyle={{
                    backgroundColor: "#ffffff",
                    borderRadius: "10px",
                    border: "1px solid #e2e8f0",
                    fontSize: "12px",
                  }}
                />

                <Bar
                  dataKey="count"
                  name="Registered Records"
                  fill="#059669"
                  radius={[
                    6,
                    6,
                    0,
                    0,
                  ]}
                />

              </BarChart>

            </ResponsiveContainer>

          </div>

        </div>



        {/* QUICK ACTIONS */}

        <div className="panel">

          <div className="panel-header">

            <div className="panel-title-group">

              <h3>
                Quick Actions
              </h3>

              <p>
                Navigate to core platform capabilities
              </p>

            </div>

          </div>


          <div className="quick-actions-grid">


            <button
              className="quick-action-btn"
              onClick={() =>
                onNavigate("research")
              }
            >

              <span className="qa-icon">
                🔍
              </span>

              <span className="qa-title">
                Search Research
              </span>

              <span className="qa-desc">
                Explore registered research documents
              </span>

            </button>



            <button
              className="quick-action-btn"
              onClick={() =>
                onNavigate("datasets")
              }
            >

              <span className="qa-icon">
                📁
              </span>

              <span className="qa-title">
                Explore Datasets
              </span>

              <span className="qa-desc">
                Browse registered governance datasets
              </span>

            </button>



            <button
              className="quick-action-btn"
              onClick={() =>
                onNavigate("gis")
              }
            >

              <span className="qa-icon">
                🗺️
              </span>

              <span className="qa-title">
                GIS Map Layers
              </span>

              <span className="qa-desc">
                Explore registered spatial layers
              </span>

            </button>



            <button
              className="quick-action-btn"
              onClick={() =>
                onNavigate("evidence")
              }
            >

              <span className="qa-icon">
                🤖
              </span>

              <span className="qa-title">
                Ask Evidence AI
              </span>

              <span className="qa-desc">
                Generate traceable evidence packages
              </span>

            </button>



            <button
              className="quick-action-btn"
              onClick={() =>
                onNavigate("sandbox")
              }
            >

              <span className="qa-icon">
                🧪
              </span>

              <span className="qa-title">
                Policy Sandbox
              </span>

              <span className="qa-desc">
                Simulate policy levers and impacts
              </span>

            </button>



            <button
              className="quick-action-btn"
              onClick={() =>
                onNavigate("policy")
              }
            >

              <span className="qa-icon">
                📜
              </span>

              <span className="qa-title">
                Policy Explorer
              </span>

              <span className="qa-desc">
                Explore registered policy records
              </span>

            </button>

          </div>


          {/* BACKEND STATUS */}

          <div style={{ marginTop: "18px" }}>

            <div
              style={{
                fontSize: "12px",
                fontWeight: 700,
                color: "var(--slate-500)",
                textTransform: "uppercase",
                letterSpacing: "0.5px",
                marginBottom: "8px",
              }}
            >
              Platform Backend Status
            </div>


            <div
              style={{
                display: "flex",
                alignItems: "center",
                justifyContent: "space-between",
                padding: "10px 14px",
                background: "var(--slate-50)",
                borderRadius: "8px",
                border: "1px solid var(--slate-200)",
                fontSize: "12px",
              }}
            >

              <span>
                PostgreSQL + FastAPI Services
              </span>

              <span
                className="badge"
                style={{
                  background: loading
                    ? "#fef3c7"
                    : "#ecfdf5",
                  color: loading
                    ? "#d97706"
                    : "#059669",
                  fontWeight: 700,
                }}
              >
                {loading
                  ? "Loading"
                  : "Connected"}
              </span>

            </div>

          </div>

        </div>

      </div>



      {/* REGISTERED POLICY SUMMARY */}

      <div className="panel">

        <div className="panel-header">

          <div className="panel-title-group">

            <h3>
              Registered Policy Records
            </h3>

            <p>
              Current policy records available
              from the backend
            </p>

          </div>


          <button
            className="btn btn-outline btn-sm"
            onClick={() =>
              onNavigate("policy")
            }
          >
            View Policies →
          </button>

        </div>


        {loading ? (

          <div
            style={{
              padding: "20px",
              textAlign: "center",
              color: "var(--slate-500)",
              fontSize: "13px",
            }}
          >
            Loading policy records...
          </div>

        ) : policies.length === 0 ? (

          <div
            style={{
              padding: "20px",
              textAlign: "center",
              color: "var(--slate-500)",
              fontSize: "13px",
            }}
          >
            No policy records are currently registered.
          </div>

        ) : (

          <div className="alerts-list">

            {policies.slice(0, 3).map((policy) => (

              <div
                key={policy.id}
                className="alert-item success"
              >

                <span className="alert-icon">
                  📜
                </span>


                <div className="alert-body">

                  <div className="alert-heading">
                    {policy.title}
                  </div>

                  <div className="alert-text">
                    {policy.overview ||
                      policy.description ||
                      "Policy record available for analysis."}
                  </div>

                  <div className="alert-time">
                    {policy.status ||
                      "Status not specified"}
                    {" • "}
                    {policy.geography ||
                      "Geography not specified"}
                  </div>

                </div>


                <button
                  className="btn btn-sm btn-secondary"
                  onClick={() =>
                    onNavigate("policy")
                  }
                >
                  View
                </button>

              </div>

            ))}

          </div>

        )}

      </div>


    </div>

  );
}


export default Dashboard;