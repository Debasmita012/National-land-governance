from app.services.policy_evidence_service import (
    PolicyEvidenceService
)


service = PolicyEvidenceService()


question = (
    "What are the major challenges of land governance "
    "in India?"
)


supporting_datasets = [
    {
        "dataset_id": 1,
        "name": "Agricultural Land Dataset",
        "source": "Government Dataset"
    }
]


try:

    evidence_package = (
        service.generate_evidence_package(
            question=question,
            supporting_datasets=supporting_datasets,
            affected_geography="Pilot District"
        )
    )

    print("\nRAG → EVIDENCE ENGINE")
    print("=" * 60)

    print("\nRecommendation:")
    print(
        evidence_package["recommendation"]
    )

    print("\nSupporting datasets:")
    print(
        evidence_package["supporting_datasets"]
    )

    print("\nResearch papers:")
    print(
        evidence_package["research_papers"]
    )

    print("\nAffected geography:")
    print(
        evidence_package["affected_geography"]
    )

    print("\nCitations:")
    print(
        evidence_package["citations"]
    )

    print("\nConfidence score:")
    print(
        evidence_package["confidence_score"]
    )

    print("\nConfidence level:")
    print(
        evidence_package["confidence_level"]
    )

    print("\nEvidence quality:")
    print(
        evidence_package["evidence_quality"]
    )

except Exception as error:

    print("\nERROR")
    print("=" * 60)
    print(error)