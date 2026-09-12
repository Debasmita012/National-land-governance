from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db

from app.models.base_models import EvidenceCard

from ai.analysis.policy_red_team_service import (
    PolicyRedTeamService
)

from ai.analysis.sdg_scorecard_service import (
    SDGScorecardService
)

from ai.analysis.carbon_impact_service import (
    CarbonImpactService
)

from ai.analysis.dispute_warning_service import (
    DisputeWarningService
)

from ai.analysis.provenance_service import (
    ProvenanceService
)


router = APIRouter(
    prefix="/policy-analysis",
    tags=["Unified Policy Analysis"]
)


red_team_service = PolicyRedTeamService()

sdg_service = SDGScorecardService()

carbon_service = CarbonImpactService()

dispute_service = DisputeWarningService()

provenance_service = ProvenanceService()


@router.get("/{card_id}")
def get_complete_policy_analysis(
    card_id: int,
    db: Session = Depends(get_db)
):

    # --------------------------------------------------------
    # Find Evidence Card
    # --------------------------------------------------------

    card = (
        db.query(EvidenceCard)
        .filter(EvidenceCard.id == card_id)
        .first()
    )

    if not card:

        raise HTTPException(
            status_code=404,
            detail="Evidence card not found."
        )

    # --------------------------------------------------------
    # AI Policy Red-Team
    # --------------------------------------------------------

    red_team_result = red_team_service.analyze(

        recommendation=card.recommendation,

        confidence_score=(
            card.confidence_score or 0.0
        ),

        positive_impacts=(
            card.positive_impacts or []
        ),

        negative_impacts=(
            card.negative_impacts or []
        ),

        risks_limitations=(
            card.risks_limitations or []
        ),

        alternatives=(
            card.alternatives or []
        ),

        supporting_datasets=(
            card.supporting_datasets or []
        ),

        research_papers=(
            card.research_papers or []
        ),

        citations=(
            card.citations or []
        )
    )

    # --------------------------------------------------------
    # SDG Scorecard
    # --------------------------------------------------------
    #
    # These values are demonstration inputs for now.
    # Later they can come from real policy/GIS datasets.
    # --------------------------------------------------------

    sdg_result = sdg_service.calculate_score(

        housing_impact=78,

        economic_impact=72,

        food_security_impact=45,

        climate_impact=52,

        infrastructure_impact=80
    )

    # --------------------------------------------------------
    # Carbon Impact
    # --------------------------------------------------------
    #
    # Demonstration baseline/projected values.
    # Later these can be supplied by real datasets.
    # --------------------------------------------------------

    carbon_result = carbon_service.estimate(

        baseline_emissions=10000,

        projected_emissions=11500
    )

    # --------------------------------------------------------
    # Land-Dispute Warning
    # --------------------------------------------------------
    #
    # Demonstration indicators for the current prototype.
    # --------------------------------------------------------

    dispute_result = dispute_service.analyze(

        dispute_count=120,

        dispute_growth_percentage=55,

        land_use_change_percentage=35,

        population_growth_percentage=18,

        anomaly_detected=True
    )

    # --------------------------------------------------------
    # Provenance
    # --------------------------------------------------------

    provenance_records = (
        provenance_service.get_records(db)
    )

    card_provenance = [
        record
        for record in provenance_records
        if record["evidence_card_id"]
        == card_id
    ]

    provenance_verification = (
        provenance_service.verify_chain(db)
    )

    # --------------------------------------------------------
    # Final unified response
    # --------------------------------------------------------

    return {

        "evidence_card_id":
            card.id,

        "recommendation":
            card.recommendation,

        "affected_geography":
            card.affected_geography,

        "confidence": {

            "score":
                card.confidence_score,

            "level":
                card.confidence_level,

            "retrieval_confidence":
                card.retrieval_confidence,

            "evidence_coverage":
                card.evidence_coverage
        },

        "policy_red_team":
            red_team_result,

        "sdg_scorecard":
            sdg_result,

        "carbon_climate_impact":
            carbon_result,

        "land_dispute_early_warning":
            dispute_result,

        "provenance": {

            "records":
                card_provenance,

            "record_count":
                len(card_provenance),

            "chain_valid":
                provenance_verification["valid"],

            "records_checked":
                provenance_verification[
                    "records_checked"
                ]
        }
    }