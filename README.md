# National Land Governance Platform

AI + GIS + Research Intelligence + Policy Simulation + Evidence Traceability

The National Land Governance Platform is an AI-powered decision-support platform for land governance, research intelligence, geospatial analysis, evidence generation, and policy simulation.

The platform connects land data, research documents, datasets, GIS information, policy information, AI analytics, and simulation into a unified workflow:

DATA → EVIDENCE → INSIGHT → SIMULATION → POLICY → OUTCOME → FEEDBACK

Instead of treating research papers, datasets, land records, GIS layers, and policies as isolated resources, the platform connects them to support explainable and evidence-based land-governance decisions.

1. AI LAND INTELLIGENCE

Users can upload land-governance datasets and automatically analyze them.

Supported formats include:

- CSV
- Excel
- GeoJSON
- JSON
- PDF for profiling/document workflows

The system automatically detects relevant fields such as:

- Parcel ID
- Land use
- Dispute count
- Population
- Latitude
- Longitude
- Area
- Survey-related fields

The system generates:

- Data-quality indicators
- Parcel statistics
- Dispute statistics
- Population indicators
- Land-use distributions
- Geographic indicators
- Risk indicators

2. EXPLAINABLE LAND RISK ENGINE

The platform contains an explainable pilot land-risk engine that calculates a composite risk index for individual parcels.

The current model combines:

- Dispute pressure
- Population pressure
- Land-use pressure
- Anomaly pressure

Pilot weights:

Dispute Pressure     35%
Population Pressure  20%
Land-Use Pressure    20%
Anomaly Pressure     25%

Each parcel receives:

- Risk score from 0–100
- Risk level
- Risk components
- Anomaly information
- Human-readable explanation

Risk levels:

- Low
- Moderate
- High
- Critical

The current score is a pilot composite risk index for demonstration and decision-support purposes. It is not a statistically validated probability of a land dispute.

3. HISTORICAL LAND-USE CHANGE DETECTION

The platform can compare historical and current land-use datasets.

It automatically detects:

- Matching parcels
- Changed parcels
- Unchanged parcels
- Conversion rate
- Land-use transitions
- Historical land-use distribution
- Current land-use distribution

Example transitions:

Agricultural → Residential
Agricultural → Industrial
Forest → Residential
Residential → Agricultural

Historical land-use changes can also be incorporated into integrated parcel-level risk analysis.

4. AI GIS RISK HOTSPOTS

The platform converts parcel-level AI risk analysis into GeoJSON and displays the results on an interactive GIS map.

Each risk hotspot contains:

- Parcel ID
- Risk score
- Risk level
- Land use
- Previous land use
- Current land use
- Land-use transition
- Risk components
- Anomaly information
- Explanation
- Latitude
- Longitude

Example:

Parcel P004
Risk Score: 94.77
Risk Level: Critical

Agricultural → Industrial

Contributing indicators:

- High observed dispute pressure
- High population pressure
- High development pressure
- Unusual data pattern

GIS workflow:

LAND DATA
↓
AI RISK ANALYSIS
↓
PARCEL RISK RECORDS
↓
GEOJSON
↓
GIS RISK HOTSPOTS

5. RESEARCH REPOSITORY

The platform provides a centralized repository for research and policy-related information.

It supports:

- Research documents
- Policy documents
- Government reports
- Dataset metadata
- Document text extraction
- Semantic search
- Research retrieval

Documents can be processed into chunks and indexed for semantic retrieval.

6. AI RESEARCH AND RAG

The platform uses Retrieval-Augmented Generation concepts to connect research documents with evidence.

Pipeline:

PDF
↓
Text Extraction
↓
Text Cleaning
↓
Chunking
↓
Embeddings
↓
Vector Database
↓
Semantic Retrieval
↓
Evidence

Technologies include:

- Sentence Transformers
- ChromaDB
- Vector embeddings
- Retrieval services
- Citation-aware evidence retrieval

Retrieved evidence can be connected to Evidence Cards and policy analysis.

7. EVIDENCE-TO-POLICY ENGINE

The Evidence Engine converts supporting evidence into structured evidence packages.

An Evidence Card can contain:

- Recommendation
- Supporting datasets
- Research papers
- Affected geography
- Positive impacts
- Negative impacts
- Confidence score
- Risks and limitations
- Alternatives
- Citations

The system validates evidence sources before creating an evidence package.

The resulting relationship is:

Dataset
↓
Research Evidence
↓
Analysis
↓
Recommendation
↓
Policy

8. EVIDENCE PROVENANCE

The platform provides evidence provenance and traceability.

It supports:

- Evidence links
- Source traceability
- Verification
- Provenance records
- Hash-chain style provenance tracking
- Evidence-source validation

This helps answer:

"Where did this recommendation come from?"

The platform is designed so that recommendations can be connected back to their supporting datasets and research evidence.

9. POLICY SANDBOX

The Policy Sandbox allows users to modify policy parameters and observe simulated impacts.

Example policy parameters include:

- Conversion tax
- Green buffer
- Agricultural subsidy
- Tribunal resolution time

The sandbox can produce indicators such as:

- Sprawl reduction
- Displacement risk
- Municipal revenue
- Carbon area preserved
- Projected dispute trends

The current implementation uses a rule-based pilot simulation for demonstration and decision-support purposes.

It is not presented as a statistically validated prediction model.

10. AI ANALYTICS

The platform provides analytical services for numeric datasets.

TREND ANALYSIS

The trend engine can identify:

- Increasing trends
- Decreasing trends
- Stable trends
- Average
- Minimum
- Maximum
- Absolute change
- Percentage change
- Pattern strength

ANOMALY DETECTION

The platform uses Isolation Forest to identify unusual observations.

It provides:

- Anomaly count
- Anomaly values
- Anomaly scores
- Explainable findings

11. POLICY EXPLORER

The Policy Explorer provides structured policy information including:

- Policy title
- Policy type
- Geography
- Status
- Year
- Policy code
- Lead ministry
- Overview
- Key clauses
- Impact

Policy records are retrieved from the backend database.

12. GIS EXPLORER

The GIS Explorer provides interactive geospatial visualization.

Current capabilities include:

- Street basemap
- Satellite basemap
- Topographic basemap
- Cadastral pilot layers
- Flood pilot layer
- Forest pilot layer
- AI land-risk hotspots
- Parcel search
- Risk legend
- Risk hotspot details
- Backend GIS registry

AI risk hotspots use latitude and longitude supplied by uploaded datasets.

13. LAND-DISPUTE EARLY WARNING

The platform contains a land-dispute early-warning component.

It can combine indicators such as:

- Current disputes
- Previous disputes
- Land-use change
- Population growth
- Anomaly detection

The system produces:

- Risk score
- Risk level
- Warning message
- Contributing indicators
- Anomaly status

This is intended as a decision-support early-warning indicator.

14. SDG SCORECARD

The platform provides an SDG-oriented impact scorecard.

It evaluates policy impact dimensions including:

- Housing
- Economic impact
- Food security
- Climate impact
- Infrastructure

The system generates:

- Overall score
- Overall level
- Strengths
- Weaknesses

15. DASHBOARD

The main dashboard provides a centralized overview of the platform.

It retrieves backend registry information for:

- Research documents
- Datasets
- Policies
- GIS layers

It also provides quick access to major platform modules.

SYSTEM ARCHITECTURE

DATA SOURCES
CSV / Excel / PDF / GIS
        ↓
DATA INGESTION
Profiling / Validation
        ↓
STORAGE
PostgreSQL + PostGIS + Vector DB
        ↓
AI / RAG + GIS + ANALYTICS
        ↓
EVIDENCE-TO-POLICY ENGINE
        ↓
EVIDENCE CARD
        ↓
POLICY SANDBOX
        ↓
POLICY DECISION
        ↓
OUTCOME / FEEDBACK

TECHNOLOGY STACK

Frontend:
- React
- JavaScript
- Leaflet
- React Leaflet
- CSS

Backend:
- Python
- FastAPI
- Uvicorn
- SQLAlchemy
- Pydantic

Database:
- PostgreSQL
- PostGIS

AI / Machine Learning:
- Python
- Pandas
- NumPy
- Scikit-learn
- Sentence Transformers
- Isolation Forest
- Retrieval-Augmented Generation

Vector Search:
- ChromaDB
- Sentence embeddings

Geospatial:
- Leaflet
- React Leaflet
- GeoJSON
- PostGIS
- Uploaded latitude/longitude data

Infrastructure:
- Docker
- Docker Compose

PROJECT STRUCTURE

national-land-governance/
│
├── ai/
│   ├── analysis/
│   ├── embeddings/
│   ├── ingestion/
│   ├── models/
│   └── rag/
│
├── backend/
│   ├── app/
│   │   ├── models/
│   │   ├── routes/
│   │   ├── schemas/
│   │   └── services/
│   │
│   └── database.py
│
├── sandbox/
│
├── gis/
│
├── frontend/
│
├── data/
│   ├── documents/
│   ├── csv/
│   ├── geojson/
│   ├── raster/
│   ├── processed/
│   └── vector_db/
│
├── scripts/
│
├── security/
│
├── docker-compose.yml
├── requirements.txt
└── README.md

DATABASE CONFIGURATION

The platform uses PostgreSQL with PostGIS.

Database:
land_governance

User:
land_admin

Host:
localhost

Host Port:
5433

Container Port:
5432

The host port is 5433 because port 5432 may already be used by another PostgreSQL service.

INSTALLATION AND LOCAL SETUP

1. Clone the repository:

git clone https://github.com/Debasmita012/national-land-governance.git
cd national-land-governance

2. Start PostgreSQL/PostGIS:

Make sure Docker Desktop is running.

docker compose up -d postgres

Verify:

docker ps

The PostgreSQL container should expose:

5433 → 5432

3. Configure Backend Environment:

Create:

backend/.env

Add:

DATABASE_URL=postgresql://land_admin:land_password@localhost:5433/land_governance
OPENAI_API_KEY=your_api_key_here

Do not commit .env files or API keys to GitHub.

4. Start the Backend:

cd backend
python -m uvicorn app.main:app --reload --port 8000

Backend:

http://127.0.0.1:8000

Swagger:

http://127.0.0.1:8000/docs

5. Start the Frontend:

Open another terminal:

cd frontend
npm install
npm run dev

Frontend:

http://localhost:5173

API ENDPOINTS

Land Intelligence:

POST /land-analysis/upload
POST /land-analysis/profile
POST /land-analysis/analyze
POST /land-analysis/complete
POST /land-analysis/land-use-change
POST /land-analysis/hotspots

Analytics:

POST /analytics/trend
POST /analytics/anomaly
POST /analytics/summary

Evidence:

POST /evidence-cards/
POST /evidence-cards/generate
GET /evidence-cards/{card_id}
GET /evidence-cards/{card_id}/red-team
GET /evidence-cards/{card_id}/traceability

GIS:

GET /gis-layers/
GET /gis-layers/{layer_id}

Policies:

GET /policies/
GET /policies/{policy_id}

Policy Sandbox:

POST /sandbox/simulate

Dispute Warning:

POST /dispute-warning/

SDG Scorecard:

POST /sdg-scorecard/

Provenance:

POST /provenance/
GET /provenance/
GET /provenance/verify
GET /provenance/{evidence_card_id}

EXAMPLE AI LAND RISK WORKFLOW

A current dataset can contain:

parcel_id
land_use
dispute_count
population
latitude
longitude
area

An optional historical dataset can contain previous land-use information.

Complete workflow:

Current Dataset
+
Historical Dataset
↓
Automatic Field Detection
↓
Land-Use Change Detection
↓
Dispute Pressure
+
Population Pressure
+
Land-Use Pressure
+
Anomaly Detection
↓
Integrated Land Risk
↓
Risk Score + Explanation
↓
GeoJSON
↓
GIS Risk Hotspots

EXAMPLE RISK OUTPUT

For a pilot dataset containing 10 parcels, the platform can generate:

Critical Risk: 2
High Risk: 2
Moderate Risk: 2
Low Risk: 4
Unknown: 0

Example parcel:

P004
Risk Score: 94.77
Risk Level: Critical

Agricultural → Industrial

Contributing indicators:

- High observed dispute pressure
- High population pressure
- High development pressure
- Unusual data pattern

EVIDENCE TRACEABILITY

The platform is designed around source traceability.

A recommendation can be connected through:

Dataset
↓
Research Evidence
↓
Analysis
↓
Evidence Card
↓
Policy Recommendation
↓
Simulation

This allows users to inspect the supporting evidence behind an analysis or recommendation.

CURRENT IMPLEMENTATION STATUS

PostgreSQL + PostGIS              Implemented
FastAPI Backend                   Implemented
React Frontend                    Implemented
Data Profiling                    Implemented
Land Intelligence                 Implemented
Explainable Land Risk             Implemented
Land-Use Change Detection         Implemented
GIS Risk Hotspots                 Implemented
Research Repository               Implemented
Semantic Retrieval                Implemented
Evidence Engine                   Implemented
Evidence Provenance               Implemented
Policy Explorer                   Implemented
Policy Sandbox                    Implemented - Pilot
Analytics                         Implemented
Dispute Early Warning             Implemented - Pilot
SDG Scorecard                     Implemented
Authentication / RBAC             Partial
Advanced Remote Sensing           Roadmap
Collaborative Workspace           Roadmap
Innovation Marketplace            Roadmap

LIMITATIONS

Risk Model:

The current land-risk score is a composite pilot index and should not be interpreted as a statistically validated probability of a land dispute.

Policy Simulation:

The Policy Sandbox currently uses a rule-based pilot simulation.

GIS Data:

AI risk hotspots currently use latitude and longitude supplied by uploaded datasets.

Remote Sensing:

Full production integration with satellite imagery and remote-sensing pipelines remains part of the roadmap.

Authentication:

Production-grade authentication and full RBAC enforcement remain under development.

FUTURE ROADMAP

Phase 1 — Foundation:

- Data ingestion
- PostgreSQL/PostGIS
- Document repository
- Dataset registry
- GIS registry

Phase 2 — Intelligence:

- Semantic search
- RAG
- AI summarization
- Trend analysis
- Anomaly detection

Phase 3 — Evidence Engine:

- Evidence Cards
- Source traceability
- Evidence validation
- Policy recommendations

Phase 4 — GIS Intelligence:

- Remote sensing integration
- Satellite-derived indicators
- Temporal land-use monitoring
- Advanced spatial analytics

Phase 5 — Policy Sandbox:

- Advanced scenario models
- Multi-variable simulation
- Policy comparison
- Impact forecasting

Phase 6 — Platform Expansion:

- Secure RBAC
- Collaborative workspaces
- Citizen ground-truth verification
- Multilingual RAG
- SDG-linked analytics
- Carbon impact estimation
- External API marketplace

CORE INNOVATION

The central idea of the platform is not simply storing land documents.

It connects:

LAND DATA
↓
AI ANALYSIS
↓
GIS INTELLIGENCE
↓
EVIDENCE
↓
POLICY
↓
SIMULATION
↓
DECISION
↓
OUTCOME
↓
FEEDBACK

This creates a decision-support ecosystem where land-governance decisions can be supported by connected data, explainable AI analysis, traceable evidence, geospatial intelligence, and policy simulation.

LICENSE

This project is developed as an academic and innovation project for demonstrating AI-enabled land-governance and decision-support capabilities.
