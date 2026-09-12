from typing import Dict


class CarbonImpactService:

    def estimate(
        self,
        baseline_emissions: float,
        projected_emissions: float
    ) -> Dict:

        if baseline_emissions < 0:
            raise ValueError(
                "Baseline emissions cannot be negative."
            )

        if projected_emissions < 0:
            raise ValueError(
                "Projected emissions cannot be negative."
            )

        # --------------------------------------------------------
        # Calculate absolute change
        # --------------------------------------------------------

        emissions_change = (
            projected_emissions
            - baseline_emissions
        )

        # --------------------------------------------------------
        # Calculate percentage change
        # --------------------------------------------------------

        if baseline_emissions == 0:

            percentage_change = None

        else:

            percentage_change = (
                emissions_change
                / baseline_emissions
            ) * 100

            percentage_change = round(
                percentage_change,
                2
            )

        # --------------------------------------------------------
        # Determine climate impact
        # --------------------------------------------------------

        if emissions_change < 0:

            climate_impact = "Positive"

            interpretation = (
                "The policy scenario is estimated "
                "to reduce carbon emissions."
            )

        elif emissions_change > 0:

            climate_impact = "Negative"

            interpretation = (
                "The policy scenario is estimated "
                "to increase carbon emissions."
            )

        else:

            climate_impact = "Neutral"

            interpretation = (
                "The policy scenario is estimated "
                "to have no change in carbon emissions."
            )

        # --------------------------------------------------------
        # Determine impact level
        # --------------------------------------------------------

        if percentage_change is None:

            impact_level = "Unknown"

        elif abs(percentage_change) >= 20:

            impact_level = "High"

        elif abs(percentage_change) >= 10:

            impact_level = "Moderate"

        else:

            impact_level = "Low"

        # --------------------------------------------------------
        # Return result
        # --------------------------------------------------------

        return {

            "baseline_emissions":
                baseline_emissions,

            "projected_emissions":
                projected_emissions,

            "emissions_change":
                round(
                    emissions_change,
                    2
                ),

            "percentage_change":
                percentage_change,

            "climate_impact":
                climate_impact,

            "impact_level":
                impact_level,

            "interpretation":
                interpretation
        }