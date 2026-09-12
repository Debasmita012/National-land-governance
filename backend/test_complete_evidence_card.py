from database import SessionLocal

from app.services.policy_evidence_service import (
    PolicyEvidenceService
)


db = SessionLocal()

try:

    service = PolicyEvidenceService()

    evidence_card = (
        service.generate_and_save_evidence_card(
            db=db,
            question=(
                "What are the major challenges of "
                "land governance in India?"
            ),
            supporting_datasets=[
                {
                    "dataset_id": 1,
                    "name": "Agricultural Land Dataset",
                    "source": "Government Dataset"
                }
            ],
            affected_geography="Pilot District"
        )
    )

    print("\nEVIDENCE CARD CREATED")
    print("=" * 60)

    print("\nID:")
    print(evidence_card.id)

    print("\nRecommendation:")
    print(evidence_card.recommendation)

    print("\nConfidence score:")
    print(evidence_card.confidence_score)

    print("\nConfidence level:")
    print(evidence_card.confidence_level)

finally:

    db.close()