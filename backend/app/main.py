from fastapi import FastAPI

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
app = FastAPI(
    title="National Land Governance Platform",
    version="1.0.0"
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