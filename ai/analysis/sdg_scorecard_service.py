from typing import Dict


class SDGScorecardService:

    def calculate_score(
        self,
        housing_impact: float,
        economic_impact: float,
        food_security_impact: float,
        climate_impact: float,
        infrastructure_impact: float
    ) -> Dict:

        scores = {
            "housing": housing_impact,
            "economic_development": economic_impact,
            "food_security": food_security_impact,
            "climate_action": climate_impact,
            "infrastructure": infrastructure_impact
        }

        # --------------------------------------------------------
        # Validate scores
        # --------------------------------------------------------

        for name, score in scores.items():

            if not 0 <= score <= 100:

                raise ValueError(
                    f"{name} score must be between 0 and 100."
                )

        # --------------------------------------------------------
        # Overall score
        # --------------------------------------------------------

        overall_score = (
            housing_impact
            + economic_impact
            + food_security_impact
            + climate_impact
            + infrastructure_impact
        ) / 5

        overall_score = round(
            overall_score,
            2
        )

        # --------------------------------------------------------
        # Performance levels
        # --------------------------------------------------------

        def get_level(score: float) -> str:

            if score >= 75:
                return "Strong"

            elif score >= 50:
                return "Moderate"

            else:
                return "Weak"

        # --------------------------------------------------------
        # Identify strengths and weaknesses
        # --------------------------------------------------------

        strengths = [
            name
            for name, score in scores.items()
            if score >= 75
        ]

        weaknesses = [
            name
            for name, score in scores.items()
            if score < 50
        ]

        # --------------------------------------------------------
        # Overall level
        # --------------------------------------------------------

        overall_level = get_level(
            overall_score
        )

        # --------------------------------------------------------
        # Return scorecard
        # --------------------------------------------------------

        return {

            "scorecard": {

                "housing": {
                    "score": housing_impact,
                    "level": get_level(
                        housing_impact
                    )
                },

                "economic_development": {
                    "score": economic_impact,
                    "level": get_level(
                        economic_impact
                    )
                },

                "food_security": {
                    "score": food_security_impact,
                    "level": get_level(
                        food_security_impact
                    )
                },

                "climate_action": {
                    "score": climate_impact,
                    "level": get_level(
                        climate_impact
                    )
                },

                "infrastructure": {
                    "score": infrastructure_impact,
                    "level": get_level(
                        infrastructure_impact
                    )
                }
            },

            "overall_score":
                overall_score,

            "overall_level":
                overall_level,

            "strengths":
                strengths,

            "weaknesses":
                weaknesses
        }