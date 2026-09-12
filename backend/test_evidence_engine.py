import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent

sys.path.append(str(PROJECT_ROOT))


from evidence_engine.evidence_engine import EvidenceEngine


engine = EvidenceEngine()


evidence = engine.generate_evidence_package(

    recommendation=(
        "Prioritize improved land-record digitization "
        "and transparent land-use monitoring in the "
        "pilot region."
    ),

    supporting_datasets=[
        {
            "dataset_id": 1,
            "name": "Agricultural Land Dataset",
            "source": "Government Dataset"
        }
    ],

    research_papers=[
        {
            "document_id": 1,
            "title": "Land Governance Test Document",
            "source": "Government Research Report"
        }
    ],

    affected_geography="Pilot District",

    positive_impacts=[
        "Improved land information accessibility",
        "Better evidence for land-use planning"
    ],

    negative_impacts=[
        "Implementation and digitization costs",
        "Potential data-quality issues"
    ],

    confidence_score=0.82,

    risks_limitations=[
        "Results depend on data quality",
        "Local implementation conditions may vary"
    ],

    alternatives=[
        "Continue existing land-record processes",
        "Implement phased digitization"
    ],

    citations=[
        {
            "document_id": 1,
            "document_title": "Land Governance Test Document",
            "chunk_index": 0
        }
    ]
)


print("\nEVIDENCE PACKAGE")
print("=" * 60)

for key, value in evidence.items():

    print(f"\n{key}:")
    print(value)