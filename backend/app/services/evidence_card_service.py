from sqlalchemy.orm import Session

from app.models.base_models import (
    EvidenceCard,
    EvidenceCardDataset,
    EvidenceCardDocument,
)


class EvidenceCardService:

    def create_evidence_card(
        self,
        db: Session,
        evidence_package: dict
    ) -> EvidenceCard:

        if not evidence_package:
            raise ValueError("Evidence package cannot be empty.")

        if not evidence_package.get("recommendation"):
            raise ValueError(
                "Evidence package must contain a recommendation."
            )

        supporting_datasets = evidence_package.get(
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

        if not supporting_datasets:
            raise ValueError(
                "Evidence package must contain supporting datasets."
            )

        if not research_papers:
            raise ValueError(
                "Evidence package must contain research papers."
            )

        if not citations:
            raise ValueError(
                "Evidence package must contain citations."
            )

        expected_impacts = evidence_package.get(
            "expected_impacts",
            {
                "positive": [],
                "negative": []
            }
        )

        # --------------------------------------------------
        # 1. Create the main Evidence Card
        # --------------------------------------------------

        evidence_card = EvidenceCard(
            title="Evidence-Based Policy Recommendation",

            recommendation=evidence_package[
                "recommendation"
            ],

            # Keep JSONB fields for API compatibility
            supporting_datasets=supporting_datasets,

            research_papers=research_papers,

            affected_geography=evidence_package.get(
                "affected_geography"
            ),

            positive_impacts=expected_impacts.get(
                "positive",
                []
            ),

            negative_impacts=expected_impacts.get(
                "negative",
                []
            ),

            confidence_score=evidence_package.get(
                "confidence_score"
            ),
            confidence_level=evidence_package.get(
    "confidence_level"
),
            retrieval_confidence=evidence_package.get(
    "evidence_quality",
    {}
).get(
    "retrieval_confidence"
),

evidence_coverage=evidence_package.get(
    "evidence_quality",
    {}
).get(
    "evidence_coverage"
),

            risks_limitations=evidence_package.get(
                "risks_limitations",
                []
            ),

            alternatives=evidence_package.get(
                "alternatives",
                []
            ),

            citations=citations
        )

        db.add(evidence_card)

        # Flush so PostgreSQL generates the Evidence Card ID
        # before creating the relationship records.
        db.flush()

        # --------------------------------------------------
        # 2. Link Evidence Card → Datasets
        # --------------------------------------------------

        for dataset in supporting_datasets:

            dataset_id = dataset.get("dataset_id")

            if dataset_id is None:
                raise ValueError(
                    "Every supporting dataset must contain dataset_id."
                )

            dataset_exists = (
                db.query(EvidenceCardDataset)
                .filter(
                    EvidenceCardDataset.evidence_card_id
                    == evidence_card.id,
                    EvidenceCardDataset.dataset_id
                    == dataset_id
                )
                .first()
            )

            if not dataset_exists:

                relationship = EvidenceCardDataset(
                    evidence_card_id=evidence_card.id,
                    dataset_id=dataset_id
                )

                db.add(relationship)

        # --------------------------------------------------
        # 3. Link Evidence Card → Documents + chunks
        # --------------------------------------------------

        for citation in citations:

            document_id = citation.get("document_id")

            if document_id is None:
                raise ValueError(
                    "Every citation must contain document_id."
                )

            chunk_index = citation.get(
                "chunk_index"
            )

            relationship = EvidenceCardDocument(
                evidence_card_id=evidence_card.id,
                document_id=document_id,
                chunk_index=chunk_index
            )

            db.add(relationship)

        # --------------------------------------------------
        # 4. Commit everything together
        # --------------------------------------------------

        try:

            db.commit()

        except Exception:

            db.rollback()

            raise

        db.refresh(evidence_card)

        return evidence_card