from typing import List


class ConfidenceService:

    def calculate_retrieval_confidence(
        self,
        distances: List[float]
    ) -> float:

        if not distances:
            return 0.0

        average_distance = (
            sum(distances) / len(distances)
        )

        confidence = 1.0 - average_distance

        confidence = max(
            0.0,
            min(1.0, confidence)
        )

        return round(
            confidence,
            2
        )

    def calculate_final_confidence(
        self,
        retrieval_confidence: float,
        evidence_coverage: float
    ) -> float:

        final_confidence = (
            0.70 * retrieval_confidence
            + 0.30 * evidence_coverage
        )

        final_confidence = max(
            0.0,
            min(1.0, final_confidence)
        )

        return round(
            final_confidence,
            2
        )

    def get_confidence_level(
        self,
        confidence_score: float
    ) -> str:

        if not 0 <= confidence_score <= 1:
            raise ValueError(
                "Confidence score must be between 0 and 1."
            )

        if confidence_score < 0.40:
            return "Low"

        if confidence_score < 0.70:
            return "Moderate"

        return "High"