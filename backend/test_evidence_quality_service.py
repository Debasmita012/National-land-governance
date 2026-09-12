from app.services.evidence_quality_service import (
    EvidenceQualityService
)


service = EvidenceQualityService()


supporting_datasets = [
    {
        "dataset_id": 1,
        "name": "Agricultural Land Dataset"
    }
]

research_papers = [
    {
        "document_id": 1,
        "title": "Land Governance Test Document"
    }
]

citations = [
    {
        "document_id": 1,
        "chunk_index": 49
    },
    {
        "document_id": 1,
        "chunk_index": 4
    }
]


coverage = service.calculate_evidence_coverage(
    supporting_datasets=supporting_datasets,
    research_papers=research_papers,
    citations=citations
)


print("EVIDENCE COVERAGE")
print(coverage)