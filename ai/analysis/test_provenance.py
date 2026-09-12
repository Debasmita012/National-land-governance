from ai.analysis.provenance_service import (
    ProvenanceService
)


service = ProvenanceService()


# -----------------------------------------
# Create first provenance record
# -----------------------------------------

record_1 = service.create_record(
    evidence_card_id=11,
    action="Evidence Card Created",
    source_documents=[
        {
            "document_id": 2,
            "chunk_index": 0
        }
    ],
    source_datasets=[
        {
            "dataset_id": 1
        }
    ],
    details={
        "confidence_score": 0.55
    }
)


# -----------------------------------------
# Create second provenance record
# -----------------------------------------

record_2 = service.create_record(
    evidence_card_id=11,
    action="Evidence Card Validated",
    source_documents=[
        {
            "document_id": 2,
            "chunk_index": 0
        }
    ],
    source_datasets=[
        {
            "dataset_id": 1
        }
    ],
    details={
        "validation_status": "valid"
    }
)


print("\nPROVENANCE LEDGER")
print("=" * 60)


print("\nRecord 1:")
print(record_1)


print("\nRecord 2:")
print(record_2)


# -----------------------------------------
# Verify chain
# -----------------------------------------

verification = (
    service.verify_chain()
)


print("\nCHAIN VERIFICATION")
print("=" * 60)

print("\nValid:")
print(
    verification["valid"]
)

print("\nRecords checked:")
print(
    verification["records_checked"]
)

print("\nErrors:")
print(
    verification["errors"]
)