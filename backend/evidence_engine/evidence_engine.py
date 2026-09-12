from typing import Dict, List

from app.services.evidence_validation_service import (
    EvidenceValidationService
)


class EvidenceEngine:

    def __init__(self):
        self.validation_service = EvidenceValidationService()

    def generate_evidence_package(
        self,
        recommendation: str,
        supporting_datasets: List[Dict],
        research_papers: List[Dict],
        affected_geography: str,
        positive_impacts: List[str],
        negative_impacts: List[str],
        confidence_score: float,
        risks_limitations: List[str],
        alternatives: List[str],
        citations: List[Dict]
    ) -> Dict:

        if not recommendation.strip():
            raise ValueError(
                "Recommendation cannot be empty."
            )

        if not 0 <= confidence_score <= 1:
            raise ValueError(
                "Confidence score must be between 0 and 1."
            )

        if not supporting_datasets:
            raise ValueError(
                "At least one supporting dataset is required."
            )

        if not research_papers:
            raise ValueError(
                "At least one supporting research paper is required."
            )

        if not citations:
            raise ValueError(
                "At least one citation is required."
            )

        validation_result = (
            self.validation_service
            .validate_evidence_package(
                {
                    "recommendation": recommendation,
                    "supporting_datasets": supporting_datasets,
                    "research_papers": research_papers,
                    "citations": citations
                }
            )
        )

        if not validation_result["valid"]:
            raise ValueError(
                "Evidence validation failed: "
                + "; ".join(
                    validation_result["errors"]
                )
            )

        return {
            "recommendation": recommendation,
            "supporting_datasets": supporting_datasets,
            "research_papers": research_papers,
            "affected_geography": affected_geography,
            "expected_impacts": {
                "positive": positive_impacts,
                "negative": negative_impacts
            },
            "confidence_score": confidence_score,
            "risks_limitations": risks_limitations,
            "alternatives": alternatives,
            "citations": citations
        }