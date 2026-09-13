import { useEffect, useState } from "react";

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";


function PolicySandbox() {

  const [conversionTax, setConversionTax] = useState(18);
  const [greenBuffer, setGreenBuffer] = useState(20);
  const [subsidy, setSubsidy] = useState(2500);
  const [tribunalDays, setTribunalDays] = useState(60);

  const [simulation, setSimulation] = useState(null);

  const [loading, setLoading] = useState(false);

  const [error, setError] = useState("");


  // -------------------------------------------------------
  // RUN BACKEND SIMULATION
  // -------------------------------------------------------

  const runSimulation = async () => {

    try {

      setLoading(true);
      setError("");

      const response = await fetch(
        "http://127.0.0.1:8000/sandbox/simulate",
        {
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
        }
      );


      if (!response.ok) {

        const errorData = await response.json();

        throw new Error(
          errorData.detail ||
          `Simulation failed (${response.status})`
        );
      }


      const data = await response.json();

      setSimulation(data);

    } catch (err) {

      console.error(
        "Policy simulation error:",
        err
      );

      setError(
        err.message ||
        "Unable to run policy simulation."
      );

    } finally {

      setLoading(false);

    }
  };


  // -------------------------------------------------------
  // RUN SIMULATION WHEN LEVERS CHANGE
  // -------------------------------------------------------

  useEffect(() => {

    const timer = setTimeout(() => {
      runSimulation();
    }, 250);

    return () => clearTimeout(timer);

  }, [
    conversionTax,
    greenBuffer,
    subsidy,
    tribunalDays,
  ]);


  // -------------------------------------------------------
  // PRESETS
  // -------------------------------------------------------

  const applyPreset = (preset) => {

    if (preset === "green") {

      setConversionTax(32);
      setGreenBuffer(30);
      setSubsidy(4000);
      setTribunalDays(45);

    } else if (preset === "balanced") {

      setConversionTax(18);
      setGreenBuffer(20);
      setSubsidy(2500);
      setTribunalDays(60);

    } else if (preset === "growth") {

      setConversionTax(8);
      setGreenBuffer(12);
      setSubsidy(1200);
      setTribunalDays(90);

    }

  };


  // -------------------------------------------------------
  // READ BACKEND RESULTS
  // -------------------------------------------------------

  const impacts = simulation?.impacts;

  const projectionData =
    simulation?.projection || [];


  return (

    <div className="sandbox-page">


      {/* PAGE HEADER */}

      <div className="page-header">

        <div className="page-title-group">

          <h2>
            🧪 National Land Policy Sandbox & Impact Simulator
          </h2>

          <p>
            Model "What-If" socio-economic and ecological
            outcomes by tuning statutory regulatory levers.
          </p>

        </div>


        <div className="page-actions">

          <div
            style={{
              display: "flex",
              gap: "6px",
            }}
          >

            <button
              className="btn btn-sm btn-secondary"
              onClick={() =>
                applyPreset("green")
              }
            >
              🌿 Eco-Conservation Preset
            </button>


            <button
              className="btn btn-sm btn-primary"
              onClick={() =>
                applyPreset("balanced")
              }
            >
              ⚖️ Balanced Agrarian Preset
            </button>


            <button
              className="btn btn-sm btn-secondary"
              onClick={() =>
                applyPreset("growth")
              }
            >
              🏗️ Accelerated Growth Preset
            </button>

          </div>

        </div>

      </div>



      {/* MAIN SANDBOX GRID */}

      <div className="sandbox-grid">


        {/* LEFT LEVERS PANEL */}

        <div
          className="panel"
          style={{ margin: 0 }}
        >

          <div className="panel-header">

            <div className="panel-title-group">

              <h3>
                Statutory Levers & Incentives
              </h3>

              <p>
                Adjust variables to simulate
                multi-year impacts
              </p>

            </div>

          </div>


          {/* CONVERSION TAX */}

          <div className="slider-group">

            <div className="slider-label-row">

              <span>
                Agrarian Land Conversion Tax
              </span>

              <span
                style={{
                  color: "var(--primary-700)",
                }}
              >
                {conversionTax}%
              </span>

            </div>


            <input
              type="range"
              min="5"
              max="40"
              value={conversionTax}
              onChange={(e) =>
                setConversionTax(
                  Number(e.target.value)
                )
              }
              className="range-slider"
            />


            <div
              style={{
                fontSize: "11px",
                color: "var(--slate-400)",
                marginTop: "4px",
              }}
            >
              Penalty fee imposed on shifting fertile
              agricultural plots to commercial zoning.
            </div>

          </div>



          {/* GREEN BUFFER */}

          <div className="slider-group">

            <div className="slider-label-row">

              <span>
                Mandatory Ecological Buffer Zone
              </span>

              <span
                style={{
                  color: "var(--primary-700)",
                }}
              >
                {greenBuffer}%
              </span>

            </div>


            <input
              type="range"
              min="10"
              max="35"
              value={greenBuffer}
              onChange={(e) =>
                setGreenBuffer(
                  Number(e.target.value)
                )
              }
              className="range-slider"
            />


            <div
              style={{
                fontSize: "11px",
                color: "var(--slate-400)",
                marginTop: "4px",
              }}
            >
              Percentage of peri-urban land legally
              reserved for wetlands and tree canopy.
            </div>

          </div>



          {/* SUBSIDY */}

          <div className="slider-group">

            <div className="slider-label-row">

              <span>
                Smallholder Drone Titling Subsidy
              </span>

              <span
                style={{
                  color: "var(--primary-700)",
                }}
              >
                ₹{subsidy.toLocaleString()} / acre
              </span>

            </div>


            <input
              type="range"
              min="500"
              max="5000"
              step="250"
              value={subsidy}
              onChange={(e) =>
                setSubsidy(
                  Number(e.target.value)
                )
              }
              className="range-slider"
            />


            <div
              style={{
                fontSize: "11px",
                color: "var(--slate-400)",
                marginTop: "4px",
              }}
            >
              Public fiscal incentive to cover
              cadastral GPS surveying costs for
              marginal farmers.
            </div>

          </div>



          {/* TRIBUNAL */}

          <div className="slider-group">

            <div className="slider-label-row">

              <span>
                Dispute Tribunal Resolution Mandate
              </span>

              <span
                style={{
                  color: "var(--primary-700)",
                }}
              >
                {tribunalDays} Days
              </span>

            </div>


            <input
              type="range"
              min="30"
              max="180"
              step="15"
              value={tribunalDays}
              onChange={(e) =>
                setTribunalDays(
                  Number(e.target.value)
                )
              }
              className="range-slider"
            />


            <div
              style={{
                fontSize: "11px",
                color: "var(--slate-400)",
                marginTop: "4px",
              }}
            >
              Statutory ceiling for disposal of
              land tenure cases before revenue courts.
            </div>

          </div>



          {/* MODEL STATUS */}

          <div
            style={{
              padding: "12px 14px",
              background: "var(--slate-50)",
              border: "1px solid var(--slate-200)",
              borderRadius: "8px",
              fontSize: "12px",
              color: "var(--slate-600)",
            }}
          >

            <strong>
              Simulation Model:
            </strong>{" "}

            {simulation?.model?.type ||
              "Loading backend simulation model..."}

            <div
              style={{
                marginTop: "5px",
                fontSize: "11px",
              }}
            >
              This is a transparent pilot
              rule-based simulation, not a
              statistical prediction.
            </div>

          </div>


        </div>



        {/* RIGHT SIDE */}

        <div
          style={{
            display: "flex",
            flexDirection: "column",
            gap: "20px",
          }}
        >


          {/* ERROR */}

          {error && (

            <div
              style={{
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


          {/* LOADING */}

          {loading && !simulation && (

            <div
              className="panel"
              style={{
                margin: 0,
                textAlign: "center",
                padding: "30px",
              }}
            >
              Running policy simulation...
            </div>

          )}



          {/* IMPACT TILES */}

          {impacts && (

            <div className="impact-matrix">


              <div className="impact-tile">

                <div
                  className="impact-tile-val"
                  style={{
                    color: "#059669",
                  }}
                >
                  -{impacts.sprawl_reduction}%
                </div>

                <div className="impact-tile-lbl">
                  Urban Sprawl Velocity Reduction
                </div>

              </div>



              <div className="impact-tile">

                <div
                  className="impact-tile-val"
                  style={{
                    color:
                      impacts.displacement_risk > 12
                        ? "#e11d48"
                        : "#059669",
                  }}
                >
                  {impacts.displacement_risk}%
                </div>

                <div className="impact-tile-lbl">
                  Smallholder Displacement Risk
                </div>

              </div>



              <div className="impact-tile">

                <div
                  className="impact-tile-val"
                  style={{
                    color: "#2563eb",
                  }}
                >
                  +₹
                  {impacts.municipal_revenue_cr}
                  {" "}Cr
                </div>

                <div className="impact-tile-lbl">
                  Projected Municipal Fiscal Inflow
                </div>

              </div>



              <div className="impact-tile">

                <div
                  className="impact-tile-val"
                  style={{
                    color: "#7c3aed",
                  }}
                >
                  +
                  {Number(
                    impacts.carbon_area_preserved_ha
                  ).toLocaleString()}
                  {" "}Ha
                </div>

                <div className="impact-tile-lbl">
                  Carbon Sink Land Protected
                </div>

              </div>

            </div>

          )}



          {/* PROJECTION CHART */}

          <div
            className="panel"
            style={{
              margin: 0,
              flex: 1,
            }}
          >

            <div className="panel-header">

              <div className="panel-title-group">

                <h3>
                  5-Year Trajectory:
                  Status Quo vs Simulated Levers
                </h3>

                <p>
                  Projected land dispute case volumes
                  across civil jurisdictions
                </p>

              </div>

            </div>


            <div
              style={{
                width: "100%",
                height: 300,
                marginTop: "10px",
              }}
            >

              <ResponsiveContainer
                width="100%"
                height="100%"
              >

                <LineChart
                  data={projectionData}
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
                    dataKey="year"
                    stroke="#64748b"
                    fontSize={12}
                    tickLine={false}
                  />

                  <YAxis
                    stroke="#64748b"
                    fontSize={12}
                    tickLine={false}
                    axisLine={false}
                  />

                  <Tooltip
                    contentStyle={{
                      backgroundColor: "#ffffff",
                      borderRadius: "8px",
                      border: "1px solid #e2e8f0",
                      fontSize: "12px",
                    }}
                  />

                  <Legend
                    wrapperStyle={{
                      paddingTop: "14px",
                      fontSize: "12px",
                    }}
                  />


                  <Line
                    type="monotone"
                    dataKey="baselineDisputes"
                    name="Status Quo (No Policy Intervention)"
                    stroke="#dc2626"
                    strokeWidth={2}
                    strokeDasharray="4 4"
                    dot={{ r: 4 }}
                  />


                  <Line
                    type="monotone"
                    dataKey="simulatedDisputes"
                    name="Simulated Policy Sandbox Outcome"
                    stroke="#059669"
                    strokeWidth={2.5}
                    dot={{ r: 5 }}
                  />

                </LineChart>

              </ResponsiveContainer>

            </div>

          </div>

        </div>

      </div>

    </div>

  );
}


export default PolicySandbox;