from fastapi import APIRouter, HTTPException

from ai.analysis.dispute_warning_service import (
    DisputeWarningService
)


router = APIRouter(
    prefix="/dispute-warning",
    tags=["Land-Dispute Early Warning"]
)


service = DisputeWarningService()


@router.post("/")
def analyze_dispute_warning(
    dispute_count: int,
    dispute_growth_percentage: float,
    land_use_change_percentage: float,
    population_growth_percentage: float,
    anomaly_detected: bool
):

    try:

        result = service.analyze(

            dispute_count=dispute_count,

            dispute_growth_percentage=(
                dispute_growth_percentage
            ),

            land_use_change_percentage=(
                land_use_change_percentage
            ),

            population_growth_percentage=(
                population_growth_percentage
            ),

            anomaly_detected=anomaly_detected
        )

        return result

    except ValueError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )