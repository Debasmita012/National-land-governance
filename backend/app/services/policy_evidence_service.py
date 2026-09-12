from typing import Dict, List

from sqlalchemy.orm import Session

from app.services.rag_service import RAGService
from app.services.evidence_card_service import EvidenceCardService
from app.services.confidence_service import ConfidenceService
from app.services.evidence_quality_service import (
    EvidenceQualityService
)

from evidence_engine.evidence_engine import EvidenceEngine


class PolicyEvidenceService:

    def __init__(self):
        self.rag_service = RAGService()
        self.evidence_engine = EvidenceEngine()
        self.evidence_card_service = EvidenceCardService()
        self.confidence_service = ConfidenceService()
        self.evidence_quality_service = EvidenceQualityService()

    def generate_evidence_package(
        self,
        question: str,
        supporting_datasets: List[Dict],
        affected_geography: str = "Pilot District"
    ) -> Dict:

        if not question or not question.strip():
            raise ValueError(
                "Question cannot be empty."
            )

        if not supporting_datasets:
            raise ValueError(
                "At least one supporting dataset is required."
            )

        # Retrieve evidence using RAG
        rag_result = self.rag_service.answer(
            question=question,
            n_results=5
        )

        answer = rag_result.get(
            "answer",
            ""
        )

        citations = rag_result.get(
            "citations",
            []
        )

        if not answer or not answer.strip():
            raise ValueError(
                "RAG did not produce an evidence-based answer."
            )

        if not citations:
            raise ValueError(
                "RAG did not retrieve supporting citations."
            )

        # Build unique research-paper references
        research_papers = []

        seen_documents = set()

        for citation in citations:

            document_id = citation.get(
                "document_id"
            )

            if document_id is None:
                continue

            if document_id in seen_documents:
                continue

            seen_documents.add(
                document_id
            )

            research_papers.append(
                {
                    "document_id": document_id,
                    "title": citation.get(
                        "document_title",
                        "Retrieved Research Document"
                    ),
                    "source": "RAG Retrieved Evidence"
                }
            )

        if not research_papers:
            raise ValueError(
                "No valid research-paper references were found."
            )

        # Extract retrieval distances
        distances = [
            citation.get("distance")
            for citation in citations
            if citation.get("distance") is not None
        ]

        # Calculate retrieval confidence
        retrieval_confidence = (
            self.confidence_service
            .calculate_retrieval_confidence(
                distances
            )
        )

        # Calculate evidence coverage
        evidence_coverage = (
            self.evidence_quality_service
            .calculate_evidence_coverage(
                supporting_datasets=supporting_datasets,
                research_papers=research_papers,
                citations=citations
            )
        )

        # Calculate final confidence
        confidence_score = (
            self.confidence_service
            .calculate_final_confidence(
                retrieval_confidence=retrieval_confidence,
                evidence_coverage=evidence_coverage
            )
        )

        # Determine confidence level
        confidence_level = (
            self.confidence_service
            .get_confidence_level(
                confidence_score
            )
        )
        evidence_quality = {
    "retrieval_confidence": retrieval_confidence,
    "evidence_coverage": evidence_coverage
}

        # Generate structured evidence package
        evidence_package = (
            self.evidence_engine
            .generate_evidence_package(
                recommendation=answer,
                supporting_datasets=supporting_datasets,
                research_papers=research_papers,
                affected_geography=affected_geography,
                positive_impacts=[],
                negative_impacts=[],
                confidence_score=confidence_score,
                risks_limitations=[],
                alternatives=[],
                citations=citations
            )
        )

        # Add human-readable confidence level
        evidence_package["confidence_level"] = (
            confidence_level
        )
        evidence_package["evidence_quality"] = (
    evidence_quality
)

        return evidence_package

    def generate_and_save_evidence_card(
        self,
        db: Session,
        question: str,
        supporting_datasets: List[Dict],
        affected_geography: str = "Pilot District"
    ) -> Dict:

        evidence_package = (
            self.generate_evidence_package(
                question=question,
                supporting_datasets=supporting_datasets,
                affected_geography=affected_geography
            )
        )

        evidence_card = (
            self.evidence_card_service
            .create_evidence_card(
                db=db,
                evidence_package=evidence_package
            )
        )

        return evidence_card