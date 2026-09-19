# 🌍 National Land Governance Platform

AI-Powered Land Intelligence • GIS Risk Detection • Evidence-Based Policy Support

The National Land Governance Platform is an AI-powered decision-support system that transforms land data into explainable risk insights, GIS hotspots, research evidence, and policy simulations.

The platform connects land records, datasets, research papers, GIS information, and policy analysis into one workflow:

DATA → ANALYSIS → RISK → MAP → EVIDENCE → POLICY → SIMULATION

---

## 🎯 What the Platform Does

A user can upload land-related data containing information such as:

- Parcel ID
- Land use
- Dispute count
- Population
- Area
- Latitude
- Longitude

The platform then:

1. Understands and profiles the uploaded data
2. Detects important fields and data-quality issues
3. Compares current and historical land use
4. Detects land-use changes
5. Analyzes dispute and population pressure
6. Detects unusual patterns
7. Calculates an explainable parcel-level risk score
8. Displays risky parcels as GIS hotspots
9. Explains why a parcel received its risk level
10. Connects findings with research evidence
11. Allows policy scenarios to be explored through the Policy Sandbox

In simple terms:

UPLOAD → ANALYZE → DETECT RISK → EXPLAIN → MAP → FIND EVIDENCE → SIMULATE POLICY

---

## 🧠 How It Works

                         ┌──────────────────────┐
                         │     LAND DATA        │
                         │ CSV / Excel / GIS    │
                         │ Research / Policies  │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │    DATA PROFILING    │
                         │                      │
                         │ Field Detection      │
                         │ Validation            │
                         │ Data Quality         │
                         └──────────┬───────────┘
                                    │
                                    ▼
                    ┌──────────────────────────────┐
                    │   LAND INTELLIGENCE ENGINE  │
                    │                              │
                    │ Land-Use Change             │
                    │ Dispute Pressure            │
                    │ Population Pressure         │
                    │ Anomaly Detection            │
                    └──────────────┬───────────────┘
                                   │
                                   ▼
                         ┌──────────────────────┐
                         │  EXPLAINABLE RISK    │
                         │                      │
                         │ Risk Score           │
                         │ Risk Level           │
                         │ Risk Factors         │
                         │ Explanation           │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │     GIS HOTSPOTS     │
                         │                      │
                         │ GeoJSON + Map        │
                         └──────────┬───────────┘
                                    │
                                    ▼
                    ┌──────────────────────────────┐
                    │      EVIDENCE ENGINE        │
                    │                              │
                    │ Research + Datasets +       │
                    │ Sources + Citations         │
                    └──────────────┬───────────────┘
                                   │
                                   ▼
                         ┌──────────────────────┐
                         │    POLICY SANDBOX    │
                         │                      │
                         │ What-if Scenarios    │
                         │ Impact Simulation     │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │   DECISION SUPPORT   │
                         └──────────────────────┘

---

## 🔥 Core Features

### 1. AI Land Intelligence

The platform automatically profiles uploaded land datasets.

It can identify fields such as:

parcel_id
land_use
dispute_count
population
latitude
longitude
area

It also provides:

- Number of records
- Detected columns
- Data types
- Missing-value information
- Duplicate information
- Geographic availability
- Basic land statistics

---

### 2. Historical Land-Use Change Detection

The platform can compare historical and current land-use datasets.

For example:

P002
Agricultural → Residential

P004
Agricultural → Industrial

P007
Forest → Residential

The system identifies:

- Changed parcels
- Unchanged parcels
- Conversion rate
- Land-use transitions
- Historical distribution
- Current distribution

This allows the platform to identify where land-use patterns are changing.

---

### 3. Explainable AI Risk Engine

The platform calculates a composite pilot risk score for each parcel.

The current risk model uses:

Dispute Pressure     → 35%
Population Pressure  → 20%
Land-Use Pressure    → 20%
Anomaly Pressure     → 25%

Risk levels:

0–29     → Low
30–59    → Moderate
60–79    → High
80–100   → Critical

Example:

Parcel: P004

Risk Score: 94.77
Risk Level: Critical

Land-use transition:

Agricultural → Industrial

Contributing indicators:

- High observed dispute pressure
- High population pressure
- High development pressure
- Unusual data pattern

The important part is that the platform does not only provide a risk score.

It also explains the factors contributing to that score.

The current score is a pilot composite risk index for decision support. It is not a statistically validated probability of a future land dispute.

---

### 4. GIS Risk Hotspots

After calculating parcel-level risk, the platform converts the results into GeoJSON and displays them on an interactive GIS map.

Each hotspot contains:

- Parcel ID
- Risk score
- Risk level
- Current land use
- Previous land use
- Land-use transition
- Risk components
- Anomaly information
- Explanation
- Latitude
- Longitude

Risk levels are displayed as:

🔴 Critical
🟠 High
🟡 Moderate
🟢 Low

The workflow is:

LAND DATA
↓
AI RISK ANALYSIS
↓
PARCEL RISK RECORDS
↓
GEOJSON
↓
GIS RISK HOTSPOTS

This connects the numerical analysis directly to the physical location of the parcel.

---

### 5. Research Repository

The platform provides a centralized repository for land and policy-related research.

It can work with:

- Research papers
- Government reports
- Policy documents
- Land studies
- Dataset metadata

Documents can be processed and indexed for semantic retrieval.

---

### 6. AI Research and RAG

Research documents follow this pipeline:

DOCUMENT
↓
TEXT EXTRACTION
↓
TEXT CLEANING
↓
CHUNKING
↓
EMBEDDINGS
↓
VECTOR DATABASE
↓
SEMANTIC SEARCH
↓
RELEVANT EVIDENCE

The platform uses:

- Sentence Transformers
- ChromaDB
- Vector embeddings
- Semantic retrieval
- Retrieval-Augmented Generation concepts
- Citation-aware evidence retrieval

This allows the system to find relevant research based on meaning rather than only exact keywords.

---

### 7. Evidence-to-Policy Engine

The Evidence Engine connects analysis with supporting sources.

An Evidence Card can contain:

- Recommendation
- Supporting datasets
- Research papers
- Affected geography
- Positive impacts
- Negative impacts
- Confidence information
- Risks and limitations
- Alternatives
- Citations

The evidence flow is:

DATASET
↓
RESEARCH EVIDENCE
↓
AI ANALYSIS
↓
RECOMMENDATION
↓
EVIDENCE CARD
↓
POLICY OPTION

This makes the reasoning behind recommendations easier to trace.

---

### 8. Evidence Provenance

The platform tracks relationships between evidence and its sources.

The provenance flow is:

DATASET
↓
RESEARCH
↓
ANALYSIS
↓
EVIDENCE CARD
↓
POLICY RECOMMENDATION

This helps answer:

"Where did this recommendation come from?"

---

### 9. Policy Sandbox

The Policy Sandbox allows users to explore "what-if" scenarios.

Users can change parameters such as:

- Conversion tax
- Green buffer
- Agricultural subsidy
- Tribunal resolution time

The system then produces pilot scenario indicators such as:

- Sprawl reduction
- Displacement risk
- Municipal revenue
- Carbon area preserved
- Projected dispute trends

The current simulator is rule-based and intended for demonstration and decision-support purposes.

---

### 10. Analytics and Early Warning

The platform includes analytical tools for identifying patterns in land-related data.

Trend Analysis can identify:

- Increasing trends
- Decreasing trends
- Stable trends
- Average
- Minimum
- Maximum
- Percentage change
- Pattern strength

Anomaly Detection uses Isolation Forest to identify unusual observations.

The platform also contains a land-dispute early-warning component that combines indicators such as:

- Current disputes
- Previous disputes
- Land-use change
- Population growth
- Anomalies

The result is an early-warning indicator for further investigation.

---

# 🏗️ System Architecture

                         ┌─────────────────────────────┐
                         │         DATA SOURCES        │
                         │                             │
                         │ Land Data                   │
                         │ Research Papers             │
                         │ Policy Documents            │
                         │ GIS / Geospatial Data       │
                         └──────────────┬──────────────┘
                                        │
                                        ▼
                         ┌─────────────────────────────┐
                         │         INGESTION           │
                         │                             │
                         │ Upload                      │
                         │ Profiling                   │
                         │ Validation                  │
                         │ Field Detection             │
                         └──────────────┬──────────────┘
                                        │
                                        ▼
              ┌────────────────────────────────────────────────┐
              │                    STORAGE                     │
              │                                                │
              │ PostgreSQL + PostGIS + ChromaDB                │
              └──────────────────────┬─────────────────────────┘
                                     │
                  ┌──────────────────┼──────────────────┐
                  │                  │                  │
                  ▼                  ▼                  ▼
        ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
        │   AI / RAG      │ │  GIS ENGINE     │ │   ANALYTICS     │
        │                 │ │                 │ │                 │
        │ Embeddings      │ │ GeoJSON         │ │ Trend Analysis  │
        │ Semantic Search │ │ Risk Hotspots   │ │ Anomalies       │
        │ Evidence        │ │ Mapping         │ │ Early Warning   │
        └────────┬────────┘ └────────┬────────┘ └────────┬────────┘
                 │                   │                   │
                 └───────────────────┼───────────────────┘
                                     │
                                     ▼
                         ┌─────────────────────────────┐
                         │    EVIDENCE-TO-POLICY       │
                         │           ENGINE            │
                         └──────────────┬──────────────┘
                                        │
                                        ▼
                         ┌─────────────────────────────┐
                         │        EVIDENCE CARD        │
                         │                             │
                         │ Sources                     │
                         │ Recommendation              │
                         │ Risks                       │
                         │ Alternatives                │
                         │ Citations                   │
                         └──────────────┬──────────────┘
                                        │
                                        ▼
                         ┌─────────────────────────────┐
                         │       POLICY SANDBOX        │
                         │                             │
                         │ What-if Scenarios           │
                         │ Impact Simulation           │
                         └──────────────┬──────────────┘
                                        │
                                        ▼
                         ┌─────────────────────────────┐
                         │       DECISION SUPPORT      │
                         └─────────────────────────────┘

---

# 🛠️ Technology Stack

Frontend:
React • JavaScript • Leaflet • React Leaflet • CSS

Backend:
Python • FastAPI • SQLAlchemy • Uvicorn • Pydantic

AI / ML:
Pandas • NumPy • Scikit-learn • Isolation Forest • Sentence Transformers • RAG

Database:
PostgreSQL • PostGIS

Vector Database:
ChromaDB

Infrastructure:
Docker • Docker Compose

---

# 📁 Project Structure

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
│   └── database.py
│
├── frontend/
├── gis/
├── sandbox/
├── data/
├── scripts/
├── security/
│
├── docker-compose.yml
├── requirements.txt
└── README.md

---

# 🚀 Running the Project

## 1. Clone the repository

git clone https://github.com/Debasmita012/national-land-governance.git

cd national-land-governance

## 2. Start PostgreSQL/PostGIS

Make sure Docker Desktop is running.

docker compose up -d postgres

## 3. Configure the backend

Create:

backend/.env

Add:

DATABASE_URL=postgresql://land_admin:land_password@localhost:5433/land_governance
OPENAI_API_KEY=your_api_key_here

Do not commit .env files or API keys.

## 4. Start the backend

cd backend

python -m uvicorn app.main:app --reload --port 8000

API documentation:

http://127.0.0.1:8000/docs

## 5. Start the frontend

Open another terminal:

cd frontend

npm install

npm run dev

Open:

http://localhost:5173

---

# 📌 Current Status

Implemented:

✓ PostgreSQL + PostGIS
✓ FastAPI Backend
✓ React Frontend
✓ Automatic Data Profiling
✓ AI Land Intelligence
✓ Historical Land-Use Change Detection
✓ Explainable Land Risk Engine
✓ GIS Risk Hotspots
✓ Research Repository
✓ Semantic Retrieval / RAG
✓ Evidence-to-Policy Engine
✓ Evidence Provenance
✓ Policy Explorer
✓ Policy Sandbox
✓ Trend Analysis
✓ Anomaly Detection
✓ Land-Dispute Early Warning
✓ SDG Scorecard
✓ Interactive Dashboard

Roadmap:

→ Advanced satellite and remote-sensing integration
→ Production authentication and RBAC
→ Collaborative workspaces
→ Citizen ground-truth verification
→ Multilingual RAG
→ Advanced policy simulation
→ Carbon impact estimation
→ External API marketplace

---

# 🌍 Core Innovation

The platform is designed around one continuous decision-support loop:

DATA
↓
EVIDENCE
↓
INSIGHT
↓
SIMULATION
↓
POLICY
↓
OUTCOME
↓
FEEDBACK

The goal is not simply to store land data.

The goal is to answer:

WHERE IS THE PROBLEM?
        ↓
WHAT CHANGED?
        ↓
WHY IS IT HAPPENING?
        ↓
WHERE IS THE RISK?
        ↓
WHY IS THE AREA FLAGGED?
        ↓
WHAT EVIDENCE SUPPORTS THE FINDING?
        ↓
WHAT POLICY OPTIONS CAN BE EXPLORED?
        ↓
WHAT COULD HAPPEN?

This creates a unified platform for turning complex land data into explainable geospatial intelligence and evidence-based policy support.
