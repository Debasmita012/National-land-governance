from app.services.evidence_validation_service import (
    EvidenceValidationService
)


service = EvidenceValidationService()


valid_package = {
    "recommendation": "Improve land-use monitoring.",
    "supporting_datasets": [
        {
            "dataset_id": 1,
            "name": "Agricultural Land Dataset"
        }
    ],
    "research_papers": [
        {
            "document_id": 1,
            "title": "Land Governance Test Document"
        }
    ],
    "citations": [
        {
            "document_id": 1,
            "chunk_index": 0
        }
    ]
}


result = service.validate_evidence_package(
    valid_package
)

print("VALID PACKAGE")
print(result)


invalid_package = {
    "recommendation": "Improve land-use monitoring.",
    "supporting_datasets": [],
    "research_papers": [],
    "citations": []
}


result = service.validate_evidence_package(
    invalid_package
)

print("\nINVALID PACKAGE")
print(result)