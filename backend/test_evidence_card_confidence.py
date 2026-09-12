from database import SessionLocal

from app.models.base_models import EvidenceCard


db = SessionLocal()

try:

    card = (
        db.query(EvidenceCard)
        .order_by(EvidenceCard.id.desc())
        .first()
    )

    if not card:

        print("NO EVIDENCE CARD FOUND")

    else:

        print("\nLATEST EVIDENCE CARD")
        print("=" * 60)

        print("\nID:")
        print(card.id)

        print("\nRecommendation:")
        print(card.recommendation)

        print("\nConfidence score:")
        print(card.confidence_score)

        print("\nConfidence level:")
        print(card.confidence_level)

finally:

    db.close()