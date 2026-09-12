from typing import Dict, List


class EvidenceValidationService:

    def validate_evidence_package(
        self,
        evidence_package: Dict
    ) -> Dict:

        if not evidence_package:
            raise ValueError("Evidence package cannot be empty.")

        recommendation = evidence_package.get(
            "recommendation"
        )

        datasets = evidence_package.get(
            "supporting_datasets",
            []
        )

        research_papers = evidence_package.get(
            "research_papers",
            []
        )

        citations = evidence_package.get(
            "citations",
            []
        )

        errors: List[str] = []

        if not recommendation or not recommendation.strip():
            errors.append(
                "Recommendation is missing."
            )

        if not datasets:
            errors.append(
                "At least one supporting dataset is required."
            )

        if not research_papers:
            errors.append(
                "At least one supporting research paper is required."
            )

        if not citations:
            errors.append(
                "At least one citation is required."
            )

        for dataset in datasets:

            if dataset.get("dataset_id") is None:
                errors.append(
                    "Every supporting dataset must contain dataset_id."
                )

        for citation in citations:

            if citation.get("document_id") is None:
                errors.append(
                    "Every citation must contain document_id."
                )

        return {
            "valid": len(errors) == 0,
            "errors": errors
        }