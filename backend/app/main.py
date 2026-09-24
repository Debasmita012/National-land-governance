from app.routes.auth_test import router as auth_test_router
from app.routes.auth import router as auth_router
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.analytics import (
    router as analytics_router
)
from app.routes.datasets import router as datasets_router
from app.routes.documents import router as documents_router
from app.routes.evidence_cards import router as evidence_cards_router
from app.routes.dispute_warning import (
    router as dispute_warning_router
)
from app.routes.provenance import (
    router as provenance_router
)
from app.routes.sdg_scorecard import (
    router as sdg_scorecard_router
)
from app.routes.carbon_impact import (
    router as carbon_impact_router
)

from app.routes.policy_analysis import (
    router as policy_analysis_router
)

from app.routes.policies import (
    router as policies_router
)
from app.routes.gis_layers import (
    router as gis_layers_router
)
from app.routes.sandbox import router as sandbox_router
from app.routes import datasets
from app.routes import documents
from app.routes import evidence_cards
from app.routes import land_analysis

app = FastAPI(
    title="National Land Governance Platform",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(datasets_router)
app.include_router(documents_router)
app.include_router(evidence_cards_router)
app.include_router(dispute_warning_router)
app.include_router(provenance_router)
app.include_router(
    sdg_scorecard_router
)
app.include_router(
    carbon_impact_router
)
app.include_router(
    policy_analysis_router
)
app.include_router(
    analytics_router
)
app.include_router(
    policies_router
)
app.include_router(
    gis_layers_router
)
app.include_router(sandbox_router)
app.include_router(land_analysis.router)
app.include_router(
    auth_router
)
app.include_router(
    auth_test_router
)


@app.get("/")
def root():
    return {
        "message": "National Land Governance API is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }