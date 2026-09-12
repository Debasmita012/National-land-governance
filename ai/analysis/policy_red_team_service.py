from typing import Dict, List


class PolicyRedTeamService:

    def analyze(
        self,
        recommendation: str,
        confidence_score: float,
        positive_impacts: List[str],
        negative_impacts: List[str],
        risks_limitations: List[str],
        alternatives: List[str],
        supporting_datasets: List[Dict],
        research_papers: List[Dict],
        citations: List[Dict]
    ) -> Dict:

        if not recommendation or not recommendation.strip():
            raise ValueError(
                "Policy recommendation cannot be empty."
            )

        if not 0 <= confidence_score <= 1:
            raise ValueError(
                "Confidence score must be between 0 and 1."
            )

        challenges = []
        evidence_gaps = []
        risk_level = "Low"

        # -----------------------------------------
        # Check confidence
        # -----------------------------------------

        if confidence_score < 0.40:

            challenges.append(
                "The recommendation has low evidence confidence."
            )

            evidence_gaps.append(
                "Additional supporting evidence should be collected."
            )

            risk_level = "High"

        elif confidence_score < 0.70:

            challenges.append(
                "The recommendation has moderate evidence confidence."
            )

            evidence_gaps.append(
                "Additional evidence could improve confidence."
            )

            risk_level = "Moderate"

        # -----------------------------------------
        # Check negative impacts
        # -----------------------------------------

        if negative_impacts:

            challenges.append(
                "Potential negative impacts have been identified."
            )

            if risk_level == "Low":
                risk_level = "Moderate"

        else:

            evidence_gaps.append(
                "No negative impacts were explicitly documented."
            )

        # -----------------------------------------
        # Check risks and limitations
        # -----------------------------------------

        if risks_limitations:

            challenges.append(
                "Known risks or limitations should be considered "
                "before implementation."
            )

            risk_level = "Moderate"

        else:

            evidence_gaps.append(
                "No explicit risks or limitations were provided."
            )

        # -----------------------------------------
        # Check alternatives
        # -----------------------------------------

        if alternatives:

            challenges.append(
                "Alternative policy options are available "
                "and should be compared."
            )

        else:

            evidence_gaps.append(
                "No alternative policy options were provided."
            )

        # -----------------------------------------
        # Check supporting evidence
        # -----------------------------------------

        if not supporting_datasets:

            evidence_gaps.append(
                "No supporting datasets were provided."
            )

            risk_level = "High"

        if not research_papers:

            evidence_gaps.append(
                "No supporting research papers were provided."
            )

            risk_level = "High"

        if not citations:

            evidence_gaps.append(
                "No source citations were provided."
            )

            risk_level = "High"

        # -----------------------------------------
        # Add general policy challenge
        # -----------------------------------------

        challenges.append(
            "The recommendation should be evaluated "
            "against affected geography, implementation "
            "constraints, and unintended consequences."
        )

        # -----------------------------------------
        # Determine final assessment
        # -----------------------------------------

        if risk_level == "High":

            final_assessment = (
                "Policy recommendation requires "
                "additional evidence and risk review "
                "before implementation."
            )

        elif risk_level == "Moderate":

            final_assessment = (
                "Policy recommendation is potentially "
                "viable but requires further risk review."
            )

        else:

            final_assessment = (
                "No major red-team concerns were identified "
                "from the supplied evidence."
            )

        # -----------------------------------------
        # Return result
        # -----------------------------------------

        return {

            "recommendation":
                recommendation,

            "risk_level":
                risk_level,

            "challenges":
                challenges,

            "evidence_gaps":
                evidence_gaps,

            "final_assessment":
                final_assessment,

            "review_required":
                risk_level in [
                    "Moderate",
                    "High"
                ]
        }