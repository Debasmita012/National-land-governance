from fastapi import APIRouter, HTTPException

from ai.analysis.carbon_impact_service import (
    CarbonImpactService
)


router = APIRouter(
    prefix="/carbon-impact",
    tags=["Carbon / Climate Impact"]
)


service = CarbonImpactService()


@router.post("/")
def estimate_carbon_impact(
    baseline_emissions: float,
    projected_emissions: float
):

    try:

        result = service.estimate(

            baseline_emissions=(
                baseline_emissions
            ),

            projected_emissions=(
                projected_emissions
            )
        )

        return result

    except ValueError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )