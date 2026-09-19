import { useEffect, useState } from "react";
import {
  MapContainer,
  TileLayer,
  Marker,
  Popup,
  Circle,
  CircleMarker,
  Polygon,
  useMap,
} from "react-leaflet";
import L from "leaflet";
import "leaflet/dist/leaflet.css";

// Fix for default Leaflet marker icon asset paths
delete L.Icon.Default.prototype._getIconUrl;

L.Icon.Default.mergeOptions({
  iconRetinaUrl:
    "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png",
  iconUrl:
    "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png",
  shadowUrl:
    "https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png",
});


// ---------------------------------------------------------
// PILOT PARCEL GEOMETRY
// ---------------------------------------------------------
// These are temporary pilot map features.
// The GIS layer metadata itself now comes from the backend.
// Later we can replace these with actual GeoJSON/PostGIS data.

const sampleParcels = [
  {
    id: "P-101",
    name: "Deepor Beel Agrarian Catchment",
    coords: [26.12, 91.66],
    state: "Assam",
    ulpin: "18-06-202-004-912",
    surveyNo: "204/1A",
    area: "14.2 Hectares",
    classification: "Wetland Buffer / Agrarian",
    owner: "Customary Village Trust",
    dispute: "Active Alert (Encroachment Notice)",
    soilType: "Alluvial Silt / High Moisture",
  },
  {
    id: "P-102",
    name: "New Town Peri-Urban Corridor",
    coords: [22.58, 88.48],
    state: "West Bengal",
    ulpin: "19-14-101-008-334",
    surveyNo: "412/9B",
    area: "6.8 Hectares",
    classification: "Urban Transition / Mixed Commercial",
    owner: "State Housing Development Corp",
    dispute: "Clear / Verified",
    soilType: "Clay Loam / High Load Bearing",
  },
  {
    id: "P-103",
    name: "Mayurbhanj Community Forest Claim",
    coords: [21.93, 86.74],
    state: "Odisha",
    ulpin: "21-03-504-001-119",
    surveyNo: "FRA-CFR-08",
    area: "340.5 Hectares",
    classification: "Community Forest Resource (FRA Sec 3)",
    owner: "Gram Sabha Community Council",
    dispute: "Title Vested",
    soilType: "Red Sandy Loam / Forest Cover",
  },
  {
    id: "P-104",
    name: "Ranchi Sub-Plateau Agrarian Basin",
    coords: [23.34, 85.31],
    state: "Jharkhand",
    ulpin: "20-01-303-009-872",
    surveyNo: "118/3",
    area: "9.5 Hectares",
    classification: "Dryland Agriculture (Millets)",
    owner: "Private Smallholder Consortium",
    dispute: "Clear / Verified",
    soilType: "Laterite Red Soil",
  },
  {
    id: "P-105",
    name: "Hebbal Smart Infrastructure Zone",
    coords: [13.03, 77.59],
    state: "Karnataka",
    ulpin: "29-08-402-005-561",
    surveyNo: "88/2C",
    area: "4.1 Hectares",
    classification: "Commercial Special Tech Hub",
    owner: "Municipal Industrial Authority",
    dispute: "Clear / Verified",
    soilType: "Red Loam",
  },
];


// ---------------------------------------------------------
// MAP RECENTER
// ---------------------------------------------------------

function MapRecenter({ coords }) {
  const map = useMap();

  useEffect(() => {
    if (coords) {
      map.flyTo(coords, 10, {
        duration: 1.5,
      });
    }
  }, [coords, map]);

  return null;
}


// ---------------------------------------------------------
// GIS EXPLORER
// ---------------------------------------------------------

function GISExplorer() {
  const [baseMap, setBaseMap] = useState("streets");

  const [selectedParcel, setSelectedParcel] = useState(
    sampleParcels[0]
  );

  const [layers, setLayers] = useState({
    cadastral: true,
    floodRisk: true,
    forestCover: true,
  });

  const [searchQuery, setSearchQuery] = useState("");

  // Backend GIS layer state
  const [gisLayers, setGisLayers] = useState([]);

  const [loadingLayers, setLoadingLayers] = useState(true);

  const [layerError, setLayerError] = useState("");
  // -------------------------------------------------------
  // AI LAND RISK HOTSPOT STATE
  // -------------------------------------------------------

  const [hotspotCurrentFile, setHotspotCurrentFile] = useState(null);
  const [hotspotHistoricalFile, setHotspotHistoricalFile] = useState(null);
  const [hotspotData, setHotspotData] = useState(null);
  const [hotspotLoading, setHotspotLoading] = useState(false);
  const [hotspotError, setHotspotError] = useState("");
  const [selectedHotspot, setSelectedHotspot] = useState(null);
  const [showRiskHotspots, setShowRiskHotspots] = useState(true);



  // -------------------------------------------------------
  // FETCH GIS LAYERS FROM BACKEND
  // -------------------------------------------------------

  useEffect(() => {
    const fetchGisLayers = async () => {
      try {
        setLoadingLayers(true);
        setLayerError("");

        const response = await fetch(
          "http://127.0.0.1:8000/gis-layers/"
        );

        if (!response.ok) {
          throw new Error(
            `Failed to load GIS layers (${response.status})`
          );
        }

        const data = await response.json();

        setGisLayers(data);
      } catch (error) {
        console.error("GIS layer loading error:", error);

        setLayerError(
          error.message || "Unable to load GIS layers."
        );
      } finally {
        setLoadingLayers(false);
      }
    };

    fetchGisLayers();
  }, []);


  // -------------------------------------------------------
  // BASE MAPS
  // -------------------------------------------------------

  const tileUrls = {
    streets:
      "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",

    satellite:
      "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",

    topo:
      "https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png",
  };


  // -------------------------------------------------------
  // LAYER TOGGLE
  // -------------------------------------------------------

  const toggleLayer = (layerName) => {
    setLayers((prev) => ({
      ...prev,
      [layerName]: !prev[layerName],
    }));
  };


  // -------------------------------------------------------
  // FIND BACKEND LAYER
  // -------------------------------------------------------

  const getBackendLayer = (layerType) => {
    return gisLayers.find(
      (layer) =>
        layer.layer_type?.toLowerCase() ===
        layerType.toLowerCase()
    );
  };


  const cadastralLayer = getBackendLayer("Cadastral");

  const floodLayer = getBackendLayer("Flood Risk");

  const forestLayer = getBackendLayer("Forest Cover");


  // -------------------------------------------------------
  // SEARCH PARCELS
  // -------------------------------------------------------

  const filteredParcels = sampleParcels.filter(
    (parcel) =>
      parcel.name
        .toLowerCase()
        .includes(searchQuery.toLowerCase()) ||
      parcel.ulpin
        .toLowerCase()
        .includes(searchQuery.toLowerCase()) ||
      parcel.state
        .toLowerCase()
        .includes(searchQuery.toLowerCase())
  );


  // -------------------------------------------------------

  // -------------------------------------------------------
  // AI LAND RISK HOTSPOT HELPERS
  // -------------------------------------------------------

  const getRiskColor = (level) => {
    if (level === "Critical") return "#dc2626";
    if (level === "High") return "#f97316";
    if (level === "Moderate") return "#eab308";
    if (level === "Low") return "#16a34a";
    return "#64748b";
  };

  const getRiskBackground = (level) => {
    if (level === "Critical") return "#fef2f2";
    if (level === "High") return "#fff7ed";
    if (level === "Moderate") return "#fefce8";
    if (level === "Low") return "#f0fdf4";
    return "#f8fafc";
  };

  const analyzeAndMapRisks = async () => {
    if (!hotspotCurrentFile) {
      setHotspotError("Please select a current land dataset.");
      return;
    }

    try {
      setHotspotLoading(true);
      setHotspotError("");
      setSelectedHotspot(null);

      const formData = new FormData();
      formData.append("current_file", hotspotCurrentFile);

      if (hotspotHistoricalFile) {
        formData.append("historical_file", hotspotHistoricalFile);
      }

      const response = await fetch(
        "http://127.0.0.1:8000/land-analysis/hotspots",
        {
          method: "POST",
          body: formData,
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Unable to generate land-risk hotspots."
        );
      }

      setHotspotData(data);
      setShowRiskHotspots(true);

      if (data?.geojson?.features?.length) {
        setSelectedHotspot(data.geojson.features[0]);
      }
    } catch (error) {
      console.error("Land hotspot generation error:", error);
      setHotspotError(
        error.message || "Unable to generate land-risk hotspots."
      );
    } finally {
      setHotspotLoading(false);
    }
  };

  const hotspotFeatures = hotspotData?.geojson?.features || [];
  const riskDistribution =
    hotspotData?.risk_summary?.risk_distribution || {};

  // RENDER
  // -------------------------------------------------------

  return (
    <div className="gis-page">

      {/* PAGE HEADER */}

      <div
        className="page-header"
        style={{ marginBottom: "16px" }}
      >
        <div className="page-title-group">

          <h2>
            🗺️ National GIS Cadastral & Environmental Explorer
          </h2>

          <p>
            Interactive geospatial integration of cadastral
            parcels, remote sensing indices, and climate
            hazard zones.
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
              className={`btn btn-sm ${
                baseMap === "streets"
                  ? "btn-primary"
                  : "btn-secondary"
              }`}
              onClick={() => setBaseMap("streets")}
            >
              Street View
            </button>


            <button
              className={`btn btn-sm ${
                baseMap === "satellite"
                  ? "btn-primary"
                  : "btn-secondary"
              }`}
              onClick={() => setBaseMap("satellite")}
            >
              🛰️ Satellite
            </button>


            <button
              className={`btn btn-sm ${
                baseMap === "topo"
                  ? "btn-primary"
                  : "btn-secondary"
              }`}
              onClick={() => setBaseMap("topo")}
            >
              Topographic
            </button>

          </div>

        </div>

      </div>


      {/* MAIN GIS LAYOUT */}

      <div className="gis-container">


        {/* LEFT SIDEBAR */}

        <div className="gis-sidebar-panel">


          {/* LAYER CONTROLS */}

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
              Active Spatial Layers
            </div>


            {loadingLayers && (
              <div
                style={{
                  fontSize: "12px",
                  color: "var(--slate-500)",
                  marginBottom: "8px",
                }}
              >
                Loading GIS layers...
              </div>
            )}


            {layerError && (
              <div
                style={{
                  fontSize: "12px",
                  color: "#dc2626",
                  marginBottom: "8px",
                }}
              >
                {layerError}
              </div>
            )}


            <div
              style={{
                display: "flex",
                flexDirection: "column",
                gap: "6px",
              }}
            >


              {/* CADASTRAL */}

              <button
                className={`layer-toggle-btn ${
                  layers.cadastral ? "active" : ""
                }`}
                onClick={() =>
                  toggleLayer("cadastral")
                }
              >

                <span>
                  📍 Cadastral Boundaries (ULPIN)
                </span>

                <span>
                  {layers.cadastral ? "ON" : "OFF"}
                </span>

              </button>


              {/* FLOOD */}

              <button
                className={`layer-toggle-btn ${
                  layers.floodRisk ? "active" : ""
                }`}
                onClick={() =>
                  toggleLayer("floodRisk")
                }
              >

                <span>
                  🌊 Flood Inundation Hotspots
                </span>

                <span>
                  {layers.floodRisk ? "ON" : "OFF"}
                </span>

              </button>


              {/* FOREST */}

              <button
                className={`layer-toggle-btn ${
                  layers.forestCover ? "active" : ""
                }`}
                onClick={() =>
                  toggleLayer("forestCover")
                }
              >

                <span>
                  🌳 FRA Customary Forest Polygons
                </span>

                <span>
                  {layers.forestCover ? "ON" : "OFF"}
                </span>

              </button>

            </div>

              {/* AI LAND RISK HOTSPOTS */}

              <button
                className={`layer-toggle-btn ${
                  showRiskHotspots ? "active" : ""
                }`}
                onClick={() =>
                  setShowRiskHotspots((previous) => !previous)
                }
              >
                <span>🔥 AI Land Risk Hotspots</span>
                <span>{showRiskHotspots ? "ON" : "OFF"}</span>
              </button>


          </div>


          {/* BACKEND GIS STATUS */}

          <div
            style={{
              marginTop: "12px",
              padding: "10px",
              background: "#f8fafc",
              border: "1px solid #e2e8f0",
              borderRadius: "8px",
            }}
          >

            <div
              style={{
                fontSize: "11px",
                fontWeight: 700,
                color: "var(--slate-600)",
                marginBottom: "6px",
              }}
            >
              Backend GIS Registry
            </div>


            {loadingLayers ? (
              <div
                style={{
                  fontSize: "11px",
                  color: "var(--slate-500)",
                }}
              >
                Loading...
              </div>
            ) : (
              <div
                style={{
                  fontSize: "11px",
                  color: "var(--slate-600)",
                }}
              >
                {gisLayers.length} GIS layer
                {gisLayers.length !== 1 ? "s" : ""} registered
              </div>
            )}

          </div>


          {/* AI LAND RISK HOTSPOT UPLOAD */}

          <div
            style={{
              marginTop: "14px",
              padding: "12px",
              background: "#f8fafc",
              border: "1px solid #e2e8f0",
              borderRadius: "8px",
            }}
          >
            <div
              style={{
                fontSize: "12px",
                fontWeight: 800,
                color: "var(--slate-700)",
                marginBottom: "4px",
              }}
            >
              🔥 Land Risk Hotspots
            </div>

            <div
              style={{
                fontSize: "10px",
                color: "var(--slate-500)",
                lineHeight: 1.5,
                marginBottom: "10px",
              }}
            >
              Upload parcel data containing latitude and longitude
              to generate explainable GIS risk points.
            </div>

            <div
              style={{
                fontSize: "10px",
                fontWeight: 700,
                color: "var(--slate-600)",
                marginBottom: "4px",
              }}
            >
              Current Dataset *
            </div>

            <input
              type="file"
              accept=".csv,.xlsx,.xls"
              onChange={(event) =>
                setHotspotCurrentFile(event.target.files?.[0] || null)
              }
              style={{
                width: "100%",
                fontSize: "10px",
                marginBottom: "9px",
              }}
            />

            <div
              style={{
                fontSize: "10px",
                fontWeight: 700,
                color: "var(--slate-600)",
                marginBottom: "4px",
              }}
            >
              Historical Dataset
            </div>

            <input
              type="file"
              accept=".csv,.xlsx,.xls"
              onChange={(event) =>
                setHotspotHistoricalFile(event.target.files?.[0] || null)
              }
              style={{
                width: "100%",
                fontSize: "10px",
                marginBottom: "10px",
              }}
            />

            <button
              className="btn btn-primary btn-sm"
              onClick={analyzeAndMapRisks}
              disabled={hotspotLoading}
              style={{ width: "100%" }}
            >
              {hotspotLoading ? "Analyzing..." : "Analyze & Map Risks"}
            </button>

            {hotspotError && (
              <div
                style={{
                  marginTop: "8px",
                  padding: "7px",
                  background: "#fef2f2",
                  border: "1px solid #fecaca",
                  borderRadius: "6px",
                  color: "#dc2626",
                  fontSize: "10px",
                }}
              >
                {hotspotError}
              </div>
            )}

            {hotspotData && (
              <div
                style={{
                  marginTop: "10px",
                  padding: "8px",
                  background: "#ecfdf5",
                  border: "1px solid #a7f3d0",
                  borderRadius: "6px",
                }}
              >
                <div
                  style={{
                    color: "#047857",
                    fontSize: "10px",
                    fontWeight: 800,
                  }}
                >
                  ✓ {hotspotData.risk_summary?.mapped_records ?? 0} parcels mapped
                </div>

                <div
                  style={{
                    marginTop: "5px",
                    color: "#64748b",
                    fontSize: "9px",
                    lineHeight: 1.5,
                  }}
                >
                  Critical: {riskDistribution.Critical ?? 0}
                  {" • "}High: {riskDistribution.High ?? 0}
                  {" • "}Moderate: {riskDistribution.Moderate ?? 0}
                  {" • "}Low: {riskDistribution.Low ?? 0}
                </div>
              </div>
            )}
          </div>

          {/* PARCEL SEARCH */}

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
              Cadastral Parcel Locator
            </div>


            <div
              className="search-box"
              style={{ marginBottom: "10px" }}
            >

              <span>🔍</span>

              <input
                type="text"
                placeholder="Search parcel, ULPIN, or state..."
                value={searchQuery}
                onChange={(event) =>
                  setSearchQuery(event.target.value)
                }
              />

            </div>


            <div
              style={{
                display: "flex",
                flexDirection: "column",
                gap: "6px",
                maxHeight: "160px",
                overflowY: "auto",
              }}
            >

              {filteredParcels.map((parcel) => (

                <button
                  key={parcel.id}
                  style={{
                    padding: "8px 10px",
                    borderRadius: "6px",
                    border:
                      selectedParcel?.id === parcel.id
                        ? "1px solid #059669"
                        : "1px solid #e2e8f0",
                    background:
                      selectedParcel?.id === parcel.id
                        ? "#ecfdf5"
                        : "#ffffff",
                    textAlign: "left",
                    fontSize: "12px",
                    cursor: "pointer",
                  }}
                  onClick={() =>
                    setSelectedParcel(parcel)
                  }
                >

                  <div
                    style={{
                      fontWeight: 700,
                      color: "var(--slate-900)",
                    }}
                  >
                    {parcel.name}
                  </div>

                  <div
                    style={{
                      fontSize: "10px",
                      color: "var(--slate-500)",
                    }}
                  >
                    {parcel.state} • {parcel.ulpin}
                  </div>

                </button>

              ))}


              {filteredParcels.length === 0 && (
                <div
                  style={{
                    fontSize: "12px",
                    color: "var(--slate-500)",
                    padding: "8px",
                  }}
                >
                  No matching parcels found.
                </div>
              )}

            </div>

          </div>


          {/* SELECTED PARCEL */}

          {selectedParcel && (

            <div
              style={{
                background: "var(--slate-50)",
                border: "1px solid var(--slate-200)",
                borderRadius: "8px",
                padding: "14px",
              }}
            >

              <div
                style={{
                  display: "flex",
                  justifyContent: "space-between",
                  alignItems: "center",
                  marginBottom: "6px",
                }}
              >

                <span className="pill-tag">
                  {selectedParcel.state}
                </span>


                <span
                  className="badge"
                  style={{
                    fontSize: "10px",
                    background:
                      selectedParcel.dispute.includes(
                        "Alert"
                      )
                        ? "#fef2f2"
                        : "#ecfdf5",
                    color:
                      selectedParcel.dispute.includes(
                        "Alert"
                      )
                        ? "#e11d48"
                        : "#059669",
                  }}
                >
                  {selectedParcel.dispute}
                </span>

              </div>


              <div
                style={{
                  fontWeight: 800,
                  fontSize: "14px",
                  color: "var(--slate-900)",
                  marginBottom: "4px",
                }}
              >
                {selectedParcel.name}
              </div>


              <div
                style={{
                  fontSize: "11px",
                  color: "var(--primary-700)",
                  fontFamily: "var(--font-mono)",
                  marginBottom: "10px",
                }}
              >
                ULPIN: {selectedParcel.ulpin}
              </div>


              <div
                style={{
                  fontSize: "12px",
                  color: "var(--slate-600)",
                  display: "flex",
                  flexDirection: "column",
                  gap: "4px",
                }}
              >

                <div>
                  <strong>Survey No:</strong>{" "}
                  {selectedParcel.surveyNo}
                </div>

                <div>
                  <strong>Area:</strong>{" "}
                  {selectedParcel.area}
                </div>

                <div>
                  <strong>Classification:</strong>{" "}
                  {selectedParcel.classification}
                </div>

                <div>
                  <strong>Owner / Entity:</strong>{" "}
                  {selectedParcel.owner}
                </div>

                <div>
                  <strong>Soil & Terrain:</strong>{" "}
                  {selectedParcel.soilType}
                </div>

              </div>

            </div>

          )}


          {/* GIS LEGEND */}

          <div className="gis-legend">

            <div
              style={{
                fontSize: "11px",
                fontWeight: 700,
                color: "var(--slate-600)",
                marginBottom: "8px",
              }}
            >
              Map Legend
            </div>


            <div className="legend-row">
              <span
                className="legend-color-box"
                style={{ background: "#059669" }}
              ></span>
              <span>
                Cadastral Verified Boundary
              </span>
            </div>


            <div className="legend-row">
              <span
                className="legend-color-box"
                style={{ background: "#2563eb" }}
              ></span>
              <span>
                10-Yr Flood Vulnerability Buffer
              </span>
            </div>


            <div className="legend-row">
              <span
                className="legend-color-box"
                style={{ background: "#7c3aed" }}
              ></span>
              <span>
                FRA Customary Forest Zone
              </span>
            </div>


            <div className="legend-row">
              <span
                className="legend-color-box"
                style={{ background: "#e11d48" }}
              ></span>
              <span>
                Disputed / Encroachment Alert
              </span>
            </div>

            <div
              style={{
                marginTop: "9px",
                paddingTop: "8px",
                borderTop: "1px solid #e2e8f0",
              }}
            >
              <div
                style={{
                  fontSize: "10px",
                  fontWeight: 800,
                  color: "#475569",
                  marginBottom: "6px",
                }}
              >
                AI LAND RISK
              </div>

              {[
                ["#dc2626", "Critical Risk"],
                ["#f97316", "High Risk"],
                ["#eab308", "Moderate Risk"],
                ["#16a34a", "Low Risk"],
              ].map(([color, label]) => (
                <div className="legend-row" key={label}>
                  <span
                    style={{
                      width: "10px",
                      height: "10px",
                      borderRadius: "50%",
                      background: color,
                      display: "inline-block",
                    }}
                  ></span>
                  <span>{label}</span>
                </div>
              ))}
            </div>


          </div>

        </div>


        {/* RIGHT MAP */}

        <div className="gis-map-card">

          <MapContainer
            center={
              selectedParcel
                ? selectedParcel.coords
                : [22.5, 82.0]
            }
            zoom={5}
            scrollWheelZoom={true}
            style={{
              height: "100%",
              width: "100%",
            }}
          >

            <MapRecenter
              coords={selectedParcel?.coords}
            />


            <TileLayer
              attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
              url={tileUrls[baseMap]}
            />


            {/* CADASTRAL MARKERS */}

            {layers.cadastral &&
              sampleParcels.map((parcel) => (

                <Marker
                  key={parcel.id}
                  position={parcel.coords}
                  eventHandlers={{
                    click: () =>
                      setSelectedParcel(parcel),
                  }}
                >

                  <Popup>

                    <div
                      style={{
                        minWidth: "180px",
                        fontSize: "12px",
                      }}
                    >

                      <strong
                        style={{
                          fontSize: "13px",
                          color: "#065f46",
                        }}
                      >
                        {parcel.name}
                      </strong>


                      <div
                        style={{
                          color: "#64748b",
                          margin: "4px 0",
                        }}
                      >
                        ULPIN:{" "}
                        <code>{parcel.ulpin}</code>
                      </div>


                      <div>
                        <strong>Area:</strong>{" "}
                        {parcel.area}
                      </div>


                      <div>
                        <strong>Class:</strong>{" "}
                        {parcel.classification}
                      </div>


                      <div
                        style={{
                          marginTop: "6px",
                          color:
                            parcel.dispute.includes(
                              "Alert"
                            )
                              ? "#dc2626"
                              : "#059669",
                          fontWeight: 700,
                        }}
                      >
                        {parcel.dispute}
                      </div>

                    </div>

                  </Popup>

                </Marker>

              ))}


                          {/* REAL LAND RISK HOTSPOTS */}

              {showRiskHotspots &&
                hotspotFeatures.map((feature, index) => {
                  const properties = feature.properties || {};
                  const coordinates = feature.geometry?.coordinates || [];
                  const longitude = coordinates[0];
                  const latitude = coordinates[1];

                  if (
                    typeof latitude !== "number" ||
                    typeof longitude !== "number"
                  ) {
                    return null;
                  }

                  const riskColor = getRiskColor(properties.risk_level);

                  return (
                    <CircleMarker
                      key={`risk-${properties.parcel_id || index}`}
                      center={[latitude, longitude]}
                      radius={
                        properties.risk_level === "Critical"
                          ? 12
                          : properties.risk_level === "High"
                          ? 10
                          : 8
                      }
                      pathOptions={{
                        color: riskColor,
                        fillColor: riskColor,
                        fillOpacity: 0.72,
                        weight: 2,
                      }}
                      eventHandlers={{
                        click: () => setSelectedHotspot(feature),
                      }}
                    >
                      <Popup>
                        <div
                          style={{
                            minWidth: "220px",
                            fontSize: "12px",
                          }}
                        >
                          <div
                            style={{
                              fontSize: "13px",
                              fontWeight: 800,
                              color: "#0f172a",
                              marginBottom: "7px",
                            }}
                          >
                            Parcel {properties.parcel_id}
                          </div>

                          <div
                            style={{
                              display: "inline-block",
                              padding: "3px 7px",
                              borderRadius: "999px",
                              background: getRiskBackground(properties.risk_level),
                              color: riskColor,
                              fontSize: "10px",
                              fontWeight: 800,
                              marginBottom: "8px",
                            }}
                          >
                            {properties.risk_level} Risk
                          </div>

                          <div>
                            <strong>Risk Score:</strong>{" "}
                            {properties.risk_score}
                          </div>

                          <div>
                            <strong>Land Use:</strong>{" "}
                            {properties.current_land_use ||
                              properties.land_use ||
                              "N/A"}
                          </div>

                          {properties.land_use_changed && (
                            <div>
                              <strong>Transition:</strong>{" "}
                              {properties.land_use_transition || "Changed"}
                            </div>
                          )}

                          <div>
                            <strong>Anomaly:</strong>{" "}
                            {properties.anomaly_detected
                              ? "Detected"
                              : "Not detected"}
                          </div>

                          {properties.why?.length > 0 && (
                            <div
                              style={{
                                marginTop: "8px",
                                paddingTop: "7px",
                                borderTop: "1px solid #e2e8f0",
                              }}
                            >
                              <strong>Why is this parcel at risk?</strong>

                              <ul
                                style={{
                                  margin: "5px 0 0 16px",
                                  padding: 0,
                                }}
                              >
                                {properties.why.map((reason, reasonIndex) => (
                                  <li
                                    key={reasonIndex}
                                    style={{ marginBottom: "3px" }}
                                  >
                                    {reason}
                                  </li>
                                ))}
                              </ul>
                            </div>
                          )}
                        </div>
                      </Popup>
                    </CircleMarker>
                  );
                })}

{/* FLOOD PILOT GEOMETRY */}

            {layers.floodRisk && (
              <Circle
                center={[26.12, 91.66]}
                radius={25000}
                pathOptions={{
                  color: "#2563eb",
                  fillColor: "#3b82f6",
                  fillOpacity: 0.25,
                }}
              />
            )}


            {/* FOREST PILOT GEOMETRY */}

            {layers.forestCover && (
              <Polygon
                positions={[
                  [22.1, 86.5],
                  [22.3, 86.9],
                  [21.8, 86.8],
                ]}
                pathOptions={{
                  color: "#7c3aed",
                  fillColor: "#8b5cf6",
                  fillOpacity: 0.3,
                }}
              />
            )}

          </MapContainer>

        </div>

      </div>


      {/* SELECTED AI RISK HOTSPOT */}

      {selectedHotspot && (
        <div
          style={{
            marginTop: "16px",
            padding: "16px",
            background: "#ffffff",
            border: "1px solid #e2e8f0",
            borderRadius: "10px",
          }}
        >
          <div
            style={{
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
              gap: "12px",
              flexWrap: "wrap",
            }}
          >
            <div>
              <div
                style={{
                  fontSize: "10px",
                  fontWeight: 800,
                  color: "#64748b",
                  textTransform: "uppercase",
                  marginBottom: "4px",
                }}
              >
                AI Land Risk Hotspot
              </div>

              <div
                style={{
                  fontSize: "16px",
                  fontWeight: 800,
                  color: "#0f172a",
                }}
              >
                Parcel {selectedHotspot.properties?.parcel_id || "Unknown"}
              </div>
            </div>

            <div
              style={{
                padding: "6px 10px",
                borderRadius: "999px",
                background: getRiskBackground(
                  selectedHotspot.properties?.risk_level
                ),
                color: getRiskColor(
                  selectedHotspot.properties?.risk_level
                ),
                fontSize: "11px",
                fontWeight: 800,
              }}
            >
              {selectedHotspot.properties?.risk_level || "Unknown"} Risk
            </div>
          </div>

          <div
            style={{
              display: "grid",
              gridTemplateColumns:
                "repeat(auto-fit, minmax(150px, 1fr))",
              gap: "10px",
              marginTop: "14px",
            }}
          >
            {[
              ["RISK SCORE", selectedHotspot.properties?.risk_score ?? "—"],
              [
                "LAND USE",
                selectedHotspot.properties?.current_land_use ||
                  selectedHotspot.properties?.land_use ||
                  "—",
              ],
              [
                "TRANSITION",
                selectedHotspot.properties?.land_use_transition ||
                  "No detected change",
              ],
              [
                "ANOMALY",
                selectedHotspot.properties?.anomaly_detected
                  ? "Detected"
                  : "Not detected",
              ],
            ].map(([label, value]) => (
              <div
                key={label}
                style={{
                  padding: "10px",
                  background: "#f8fafc",
                  border: "1px solid #e2e8f0",
                  borderRadius: "7px",
                }}
              >
                <div
                  style={{
                    fontSize: "9px",
                    color: "#64748b",
                    fontWeight: 700,
                  }}
                >
                  {label}
                </div>
                <div
                  style={{
                    marginTop: "3px",
                    fontSize: "12px",
                    fontWeight: 700,
                  }}
                >
                  {value}
                </div>
              </div>
            ))}
          </div>

          {selectedHotspot.properties?.why?.length > 0 && (
            <div
              style={{
                marginTop: "12px",
                padding: "11px",
                background: "#f8fafc",
                border: "1px solid #e2e8f0",
                borderRadius: "8px",
              }}
            >
              <div
                style={{
                  fontSize: "11px",
                  fontWeight: 800,
                  color: "#334155",
                  marginBottom: "5px",
                }}
              >
                Why is this parcel at risk?
              </div>

              <ul
                style={{
                  margin: "0 0 0 17px",
                  padding: 0,
                  color: "#64748b",
                  fontSize: "11px",
                  lineHeight: 1.6,
                }}
              >
                {selectedHotspot.properties.why.map((reason, index) => (
                  <li key={index}>{reason}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}

      {/* BACKEND LAYER INFORMATION */}

      {!loadingLayers && gisLayers.length > 0 && (

        <div
          style={{
            marginTop: "16px",
            padding: "16px",
            background: "#ffffff",
            border: "1px solid #e2e8f0",
            borderRadius: "10px",
          }}
        >

          <div
            style={{
              fontSize: "13px",
              fontWeight: 800,
              color: "var(--slate-900)",
              marginBottom: "10px",
            }}
          >
            Registered GIS Layers
          </div>


          <div
            style={{
              display: "grid",
              gridTemplateColumns:
                "repeat(auto-fit, minmax(220px, 1fr))",
              gap: "10px",
            }}
          >

            {gisLayers.map((layer) => (

              <div
                key={layer.id}
                style={{
                  padding: "12px",
                  background: "#f8fafc",
                  border: "1px solid #e2e8f0",
                  borderRadius: "8px",
                }}
              >

                <div
                  style={{
                    fontWeight: 700,
                    fontSize: "12px",
                    color: "var(--slate-900)",
                    marginBottom: "4px",
                  }}
                >
                  {layer.name}
                </div>


                <div
                  style={{
                    fontSize: "11px",
                    color: "var(--slate-500)",
                    marginBottom: "4px",
                  }}
                >
                  Type: {layer.layer_type}
                </div>


                <div
                  style={{
                    fontSize: "11px",
                    color: "var(--slate-500)",
                  }}
                >
                  Geography: {layer.geography}
                </div>


                <div
                  style={{
                    marginTop: "6px",
                    fontSize: "10px",
                    color: "#059669",
                    fontWeight: 700,
                  }}
                >
                  Registered in backend
                </div>

              </div>

            ))}

          </div>

        </div>

      )}

    </div>
  );
}


export default GISExplorer;