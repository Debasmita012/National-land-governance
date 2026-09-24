# National Digital Platform for Research, Policy Innovation & Evidence-Based Land Governance

AI + GIS + Research Intelligence + Policy Simulation + Evidence Traceability

An AI-powered Land Intelligence and Governance platform that combines land datasets, research evidence, GIS, satellite-derived features, risk analysis, and policy simulation into a unified decision-support system.

The platform follows the workflow:

DATA → EVIDENCE → INSIGHT → SIMULATION → POLICY → OUTCOME


## 🚀 What the Platform Does

• AI-powered land-risk analysis
• Explainable parcel-level risk scoring
• GIS-based land-risk hotspot visualization
• Historical and current land-use change detection
• Land-dispute early warning
• Anomaly detection using Isolation Forest
• Research document search using RAG
• Evidence Card generation
• Evidence provenance and traceability
• Policy exploration
• Policy impact simulation
• SDG impact scoring
• Sentinel-2 compatible satellite feature analysis
• Authentication and role-based access control


## 🧠 Our Land-Risk Model

The core intelligence of the platform is an Explainable Integrated Land-Risk Model.

The model does not simply produce a risk number. It breaks the score into interpretable components so users can understand why a parcel receives a particular risk level.

### Risk Components

Dispute Pressure       → 35%
Population Pressure    → 20%
Land-Use Pressure      → 20%
Anomaly Pressure       → 25%

### 1. Dispute Pressure

Measures the relative level of observed disputes for a parcel compared with other records in the uploaded dataset.

### 2. Population Pressure

Measures population pressure relative to the uploaded dataset.

### 3. Land-Use Pressure

Different land-use categories are assigned pilot pressure values.

Example:

Forest          → 15
Agricultural    → 35
Mixed           → 70
Residential     → 75
Urban           → 85
Commercial      → 90
Industrial      → 100

These values are pilot model values and are not universal land-governance rules.

### 4. Anomaly Pressure

The model uses Isolation Forest to identify unusual combinations of dispute and population values.

### Risk Levels

0–29    → Low
30–59   → Moderate
60–79   → High
80–100  → Critical

The current risk engine is an explainable pilot decision-support model and is not a statistically validated probability of future land conflict.


## 🔄 Historical Land-Use Change

The platform compares historical and current land datasets at parcel level.

It identifies:

• Changed parcels
• Unchanged parcels
• Conversion rate
• Previous land use
• Current land use
• Land-use transitions

Example transitions:

Agricultural → Residential
Agricultural → Industrial
Residential  → Commercial

Historical land-use change is integrated into the parcel-level risk analysis.


## 🤖 Machine Learning Integration

The architecture supports an optional supervised Random Forest conflict-risk model.

The model can be loaded from:

ai/training/models/

When a properly trained and validated model is available, the architecture supports:

70% Composite Risk
+
30% ML Probability Score

The supervised model is not currently the primary operational model because sufficient real, properly labelled conflict observations are required before responsible supervised training and validation.

Therefore, the current operational intelligence pipeline is:

Dispute Data
+
Population Data
+
Land-Use Data
+
Isolation Forest Anomaly Detection
+
Historical Land-Use Change
↓
Integrated Explainable Land-Risk Score
↓
Low / Moderate / High / Critical

The system automatically continues using the composite risk model when a supervised ML model is unavailable.

No fabricated conflict labels are used for supervised model training.


## 🚨 Anomaly Detection

The platform uses Isolation Forest to identify unusual observations based on available dispute and population information.

Example:

Normal:
100 disputes
1200 population

Potential anomaly:
250 disputes
2700 population

Detected anomalies become an additional component of the explainable risk analysis.


## 🗺️ GIS Land-Risk Hotspots

The GIS Explorer converts parcel-level risk results into GeoJSON and displays them on an interactive Leaflet map.

Each hotspot can contain:

• Parcel ID
• Risk Score
• Risk Level
• Land Use
• Previous Land Use
• Current Land Use
• Land-Use Change
• Risk Components
• Anomaly Status
• Latitude
• Longitude

Users can select individual parcels and inspect the underlying risk information and explanation.


## 📚 Research Intelligence & RAG

Research documents are processed through the following pipeline:

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
ChromaDB
↓
Semantic Retrieval
↓
Evidence

The platform uses:

• Sentence Transformers
• ChromaDB
• Retrieval-Augmented Generation

Retrieved evidence can include:

• Document ID
• Document Title
• Chunk Index
• Similarity Distance
• Evidence Text

This keeps research-based insights connected to their underlying evidence.


## 🧾 Evidence Engine

The Evidence Engine converts supporting research and datasets into structured Evidence Cards.

An Evidence Card can contain:

• Recommendation
• Supporting Datasets
• Research Papers
• Affected Geography
• Positive Impacts
• Negative Impacts
• Confidence
• Risks and Limitations
• Alternatives
• Citations

The system validates that supporting evidence exists before generating an Evidence Card.


## 🔗 Evidence Provenance

The platform maintains traceability between evidence and its sources.

Evidence Card
↓
Dataset / Document
↓
Source
↓
Provenance Record
↓
Verification

This makes it possible to verify where an insight originated.


## ⚠️ Land-Dispute Early Warning

The Dispute Warning module combines indicators such as:

• Current disputes
• Previous disputes
• Land-use change
• Population growth
• Anomaly detection

It produces:

• Risk Score
• Risk Level
• Warning
• Supporting Indicators
• Anomaly Status

This is a decision-support early-warning mechanism rather than a guaranteed prediction of future conflict.


## 🛰️ Satellite Intelligence

The platform includes Sentinel-2 compatible remote-sensing feature extraction.

### NDVI

NDVI = (NIR - Red) / (NIR + Red)

Used for vegetation and land-cover analysis.

### NDWI

NDWI = (Green - NIR) / (Green + NIR)

Used for water-related surface analysis.

### NDBI

NDBI = (SWIR - NIR) / (SWIR + NIR)

Used as a built-up and urbanization indicator.

The satellite module also supports temporal comparison between previous and current observations.


## 🧪 Policy Sandbox

The Policy Sandbox provides a rule-based environment for testing policy scenarios.

Example inputs include:

• Conversion Tax
• Green Buffer
• Subsidy
• Tribunal Resolution Time

The simulation produces indicators such as:

• Sprawl Reduction
• Displacement Risk
• Municipal Revenue
• Carbon Area Preserved

The current sandbox is a rule-based pilot simulation and is not a statistically validated forecasting model.


## 🏛️ Policy Explorer

The Policy Explorer provides structured policy information including:

• Policy Title
• Policy Code
• Year
• Policy Type
• Geography
• Status
• Lead Ministry
• Overview
• Key Clauses
• Impact

Policy information is retrieved from the backend database.


## 🌱 SDG Scorecard

The SDG Scorecard evaluates policy impacts across:

• Housing
• Economic Impact
• Food Security
• Climate
• Infrastructure

It produces:

• Overall Score
• Overall Level
• Strengths
• Weaknesses


## 📈 Analytics

The Analytics module provides:

### Trend Analysis

Identifies whether a time series is:

• Increasing
• Decreasing
• Stable

and calculates trend strength and change.

### Anomaly Detection

Uses Isolation Forest to identify unusual observations.

### Summary Analysis

Provides statistical summaries of uploaded datasets.


## 🏗️ System Architecture & Data Flow

The platform works as an end-to-end pipeline where raw data is transformed into evidence, intelligence, risk insights, and policy decisions.

USER / DATA SOURCES
        │
        ▼
┌──────────────────────────────┐
│  1. DATA INGESTION           │
│                              │
│  • Land datasets             │
│  • Research documents        │
│  • GIS / GeoJSON data        │
│  • Satellite imagery        │
│  • Policy data               │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│  2. DATA PROCESSING          │
│                              │
│  • Validation                │
│  • Cleaning                  │
│  • Field detection           │
│  • PDF text extraction       │
│  • Data profiling            │
│  • Spatial processing        │
└──────────────┬───────────────┘
               │
       ┌───────┴────────┐
       │                │
       ▼                ▼
┌──────────────┐  ┌──────────────────┐
│ STRUCTURED   │  │ RESEARCH         │
│ DATA         │  │ KNOWLEDGE        │
│              │  │                  │
│ PostgreSQL   │  │ Embeddings       │
│ + PostGIS    │  │ + ChromaDB       │
└──────┬───────┘  └────────┬─────────┘
       │                   │
       └─────────┬─────────┘
                 │
                 ▼
┌──────────────────────────────────┐
│  3. AI & INTELLIGENCE ENGINE     │
│                                  │
│  • Land-risk analysis            │
│  • Isolation Forest anomalies    │
│  • Land-use change detection     │
│  • RAG / semantic retrieval      │
│  • Satellite feature extraction  │
│  • Optional ML conflict model    │
└────────────────┬─────────────────┘
                 │
                 ▼
┌──────────────────────────────────┐
│  4. EVIDENCE & RISK ENGINE       │
│                                  │
│  • Explainable risk score        │
│  • Risk components               │
│  • Evidence Cards                │
│  • Confidence                    │
│  • Supporting datasets           │
│  • Research citations            │
│  • Provenance                    │
└────────────────┬─────────────────┘
                 │
        ┌────────┴─────────┐
        │                  │
        ▼                  ▼
┌────────────────┐  ┌──────────────────┐
│ 5. GIS          │  │ 6. ANALYTICS     │
│ INTELLIGENCE    │  │                  │
│                 │  │ • Trends         │
│ • Risk hotspots │  │ • Anomalies      │
│ • GeoJSON       │  │ • Statistics     │
│ • Spatial view  │  │ • Summaries      │
└────────┬────────┘  └────────┬─────────┘
         │                    │
         └──────────┬─────────┘
                    │
                    ▼
┌──────────────────────────────────┐
│  7. POLICY INTELLIGENCE          │
│                                  │
│  • Policy Explorer               │
│  • Evidence-based insights       │
│  • Policy recommendations        │
│  • SDG Scorecard                 │
└────────────────┬─────────────────┘
                 │
                 ▼
┌──────────────────────────────────┐
│  8. POLICY SANDBOX               │
│                                  │
│  User changes policy parameters  │
│              ↓                   │
│  Scenario simulation             │
│              ↓                   │
│  Impact projection               │
│                                  │
│  • Sprawl reduction              │
│  • Displacement risk             │
│  • Revenue impact                │
│  • Carbon area preserved         │
└────────────────┬─────────────────┘
                 │
                 ▼
┌──────────────────────────────────┐
│  9. DECISION SUPPORT             │
│                                  │
│  • Risk visualization            │
│  • Evidence Cards                │
│  • Policy scenarios              │
│  • Impact indicators             │
│  • SDG outcomes                  │
└────────────────┬─────────────────┘
                 │
                 ▼
              OUTCOME
                 │
                 ▼
        New observations /
        updated datasets /
        feedback
                 │
                 └───────────────↺
                    FEEDBACK LOOP


## 📁 Project Structure

national-land-governance/
│
├── ai/
│   ├── analysis/
│   ├── embeddings/
│   ├── ingestion/
│   ├── models/
│   ├── rag/
│   └── training/
│       ├── data/
│       ├── processed/
│       ├── scripts/
│       └── models/
│
├── backend/
│   ├── app/
│   │   ├── models/
│   │   ├── routes/
│   │   ├── schemas/
│   │   └── services/
│   ├── database.py
│   └── .env
│
├── data/
│   ├── documents/
│   ├── csv/
│   ├── geojson/
│   ├── raster/
│   ├── processed/
│   └── vector_db/
│
├── frontend/
├── gis/
├── sandbox/
├── scripts/
├── security/
│
├── docker-compose.yml
├── requirements.txt
└── README.md


## 🔐 Authentication & RBAC

The platform includes authentication and role-based access control.

Supported roles include:

• ADMIN
• RESEARCH
• POLICY

Protected endpoints verify:

Authentication
+
User Identity
+
User Role


## 🔌 Main API Modules

/datasets/
/documents/
/evidence-cards/
/provenance/
/policies/
/gis-layers/
/analytics/
/dispute-warning/
/sdg-scorecard/
/carbon-impact/
/sandbox/
/land-analysis/
/policy-analysis/
/auth-test/


## ⚙️ Local Setup

### 1. Clone the Repository

git clone <your-github-repository-url>
cd national-land-governance

### 2. Create Python Virtual Environment

python -m venv venv

Windows:

.\venv\Scripts\Activate.ps1

### 3. Install Dependencies

pip install -r requirements.txt

### 4. Start PostgreSQL/PostGIS

docker compose up -d

Current database configuration:

Host: localhost
Port: 5433
Database: land_governance
Username: land_admin

### 5. Configure Environment Variables

Create:

backend/.env

Example:

DATABASE_URL=postgresql://land_admin:land_password@localhost:5433/land_governance
OPENAI_API_KEY=your_api_key_here

Never commit .env files to GitHub.

### 6. Start Backend

cd backend
uvicorn app.main:app --reload --port 8000

### 7. Start Frontend

Open another terminal:

cd frontend
npm install
npm run dev


## ⚠️ Model Status

The currently operational land-risk system is an explainable pilot model.

The primary operational pipeline is:

Dispute Pressure
+
Population Pressure
+
Land-Use Pressure
+
Isolation Forest Anomaly Detection
+
Historical Land-Use Change
↓
Integrated Explainable Land-Risk Score
↓
Risk Level

The supervised Random Forest component is an optional extension and is only used when a properly trained and validated model is available.

The project does not fabricate conflict labels and does not claim that the current pilot model provides a statistically validated probability of future land conflict.


## 💡 Core Innovation

The platform goes beyond being a land-data repository.

It connects:

Land Data
+
Research Evidence
+
AI / ML
+
GIS
+
Satellite Intelligence
+
Policy Simulation
+
Evidence Provenance
↓
Evidence-Based Land Governance

The core idea is to connect data to evidence, evidence to insight, insight to policy, and policy back to measurable outcomes.

## 🎯 Vision

To provide an integrated Land Intelligence and Evidence-to-Policy platform where land risks can be detected, explained, visualized, supported by evidence, and evaluated against policy scenarios.
