from fastapi import APIRouter, HTTPException

from ai.analysis.sdg_scorecard_service import (
    SDGScorecardService
)


router = APIRouter(
    prefix="/sdg-scorecard",
    tags=["SDG Policy Scorecard"]
)


service = SDGScorecardService()


@router.post("/")
def calculate_sdg_scorecard(
    housing_impact: float,
    economic_impact: float,
    food_security_impact: float,
    climate_impact: float,
    infrastructure_impact: float
):

    try:

        result = service.calculate_score(

            housing_impact=housing_impact,

            economic_impact=economic_impact,

            food_security_impact=food_security_impact,

            climate_impact=climate_impact,

            infrastructure_impact=infrastructure_impact
        )

        return result

    except ValueError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )