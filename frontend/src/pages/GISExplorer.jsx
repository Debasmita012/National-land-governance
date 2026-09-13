import { useEffect, useState } from "react";
import {
  MapContainer,
  TileLayer,
  Marker,
  Popup,
  Circle,
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