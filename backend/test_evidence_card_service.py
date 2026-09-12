from database import SessionLocal

from app.services.evidence_card_service import EvidenceCardService


service = EvidenceCardService()

db = SessionLocal()

try:

    evidence_package = {
        "recommendation": (
            "Prioritize improved land-record digitization "
            "and transparent land-use monitoring in the "
            "pilot region."
        ),

        "supporting_datasets": [
            {
                "dataset_id": 1,
                "name": "Agricultural Land Dataset",
                "source": "Government Dataset"
            }
        ],

        "research_papers": [
            {
                "document_id": 1,
                "title": "Land Governance Test Document",
                "source": "Government Research Report"
            }
        ],

        "affected_geography": "Pilot District",

        "expected_impacts": {
            "positive": [
                "Improved land information accessibility",
                "Better evidence for land-use planning"
            ],
            "negative": [
                "Implementation and digitization costs",
                "Potential data-quality issues"
            ]
        },

        "confidence_score": 0.82,

        "risks_limitations": [
            "Results depend on data quality",
            "Local implementation conditions may vary"
        ],

        "alternatives": [
            "Continue existing land-record processes",
            "Implement phased digitization"
        ],

        "citations": [
            {
                "document_id": 1,
                "document_title": "Land Governance Test Document",
                "chunk_index": 0
            }
        ]
    }

    evidence_card = service.create_evidence_card(
        db=db,
        evidence_package=evidence_package
    )

    print("\nEVIDENCE CARD CREATED")
    print("=" * 60)

    print(f"ID: {evidence_card.id}")
    print(f"Title: {evidence_card.title}")
    print(f"Recommendation: {evidence_card.recommendation}")
    print(f"Geography: {evidence_card.affected_geography}")
    print(f"Confidence: {evidence_card.confidence_score}")

    print("\nSupporting datasets:")
    print(evidence_card.supporting_datasets)

    print("\nResearch papers:")
    print(evidence_card.research_papers)

    print("\nCitations:")
    print(evidence_card.citations)

finally:
    db.close()