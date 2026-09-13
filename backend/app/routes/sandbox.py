from typing import Dict, List

from fastapi import APIRouter
from pydantic import BaseModel, Field


router = APIRouter(
    prefix="/sandbox",
    tags=["Policy Sandbox"]
)


class SandboxRequest(BaseModel):
    conversion_tax: float = Field(
        default=18,
        ge=5,
        le=40
    )

    green_buffer: float = Field(
        default=20,
        ge=10,
        le=35
    )

    subsidy: float = Field(
        default=2500,
        ge=500,
        le=5000
    )

    tribunal_days: float = Field(
        default=60,
        ge=30,
        le=180
    )


def calculate_simulation(
    data: SandboxRequest
) -> Dict:

    conversion_tax = data.conversion_tax
    green_buffer = data.green_buffer
    subsidy = data.subsidy
    tribunal_days = data.tribunal_days

    # -----------------------------------------------------
    # Pilot rule-based simulation
    # -----------------------------------------------------
    #
    # These are transparent demonstration formulas.
    # They are NOT statistical predictions.
    #

    sprawl_reduction = min(
        45,
        round(
            (conversion_tax * 1.2 + green_buffer * 0.8),
            1
        )
    )

    displacement_risk = max(
        2.1,
        round(
            (
                25
                - subsidy / 200
                - (180 - tribunal_days) / 20
            ),
            1
        )
    )

    municipal_revenue = round(
        180
        + conversion_tax * 18.5
        - subsidy * 0.03
    )

    carbon_area_preserved = round(
        green_buffer * 6500
        + conversion_tax * 1200
    )


    # -----------------------------------------------------
    # 5-year pilot trajectory
    # -----------------------------------------------------

    projection_data: List[Dict] = [
        {
            "year": "2026",
            "baselineDisputes": 120,
            "simulatedDisputes": 120,
            "revenueCr": round(
                municipal_revenue * 0.8,
                2
            )
        },
        {
            "year": "2027",
            "baselineDisputes": 135,
            "simulatedDisputes": round(
                120 * (tribunal_days / 80)
            ),
            "revenueCr": round(
                municipal_revenue * 0.9,
                2
            )
        },
        {
            "year": "2028",
            "baselineDisputes": 148,
            "simulatedDisputes": round(
                110 * (tribunal_days / 90)
            ),
            "revenueCr": round(
                municipal_revenue * 1.05,
                2
            )
        },
        {
            "year": "2029",
            "baselineDisputes": 162,
            "simulatedDisputes": round(
                95 * (tribunal_days / 100)
            ),
            "revenueCr": round(
                municipal_revenue * 1.15,
                2
            )
        },
        {
            "year": "2030",
            "baselineDisputes": 180,
            "simulatedDisputes": round(
                80 * (tribunal_days / 110)
            ),
            "revenueCr": round(
                municipal_revenue * 1.25,
                2
            )
        }
    ]


    return {
        "inputs": {
            "conversion_tax": conversion_tax,
            "green_buffer": green_buffer,
            "subsidy": subsidy,
            "tribunal_days": tribunal_days
        },

        "impacts": {
            "sprawl_reduction": sprawl_reduction,
            "displacement_risk": displacement_risk,
            "municipal_revenue_cr": municipal_revenue,
            "carbon_area_preserved_ha": carbon_area_preserved
        },

        "projection": projection_data,

        "model": {
            "type": "Rule-based pilot simulation",
            "status": "demonstration",
            "statistical_prediction": False
        }
    }


@router.post("/simulate")
def simulate_policy(
    data: SandboxRequest
):
    return calculate_simulation(data)