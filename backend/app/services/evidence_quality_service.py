from typing import Dict, List


class EvidenceQualityService:

    def calculate_evidence_coverage(
        self,
        supporting_datasets: List[Dict],
        research_papers: List[Dict],
        citations: List[Dict]
    ) -> float:

        score = 0.0

        # Supporting dataset
        if supporting_datasets:
            score += 0.33

        # Supporting research
        if research_papers:
            score += 0.33

        # Traceable citations
        if citations:
            valid_citations = [
                citation
                for citation in citations
                if citation.get("document_id") is not None
            ]

            if valid_citations:
                score += 0.34

        return round(
            min(score, 1.0),
            2
        )