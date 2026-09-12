from typing import Optional, List, Dict, Any

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import get_db

from ai.analysis.provenance_service import (
    ProvenanceService
)


router = APIRouter(
    prefix="/provenance",
    tags=["Evidence Provenance"]
)


service = ProvenanceService()


# ============================================================
# REQUEST MODEL
# ============================================================

class ProvenanceRecordCreate(BaseModel):

    evidence_card_id: int

    action: str

    source_documents: List[Any]

    source_datasets: List[Any]

    details: Optional[Dict[str, Any]] = None


# ============================================================
# CREATE PROVENANCE RECORD
# ============================================================

@router.post("/")
def create_provenance_record(
    provenance_data: ProvenanceRecordCreate,
    db: Session = Depends(get_db)
):

    try:

        result = service.create_record(

            db=db,

            evidence_card_id=(
                provenance_data.evidence_card_id
            ),

            action=(
                provenance_data.action
            ),

            source_documents=(
                provenance_data.source_documents
            ),

            source_datasets=(
                provenance_data.source_datasets
            ),

            details=(
                provenance_data.details
            )
        )

        return result

    except ValueError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )


# ============================================================
# GET ALL PROVENANCE RECORDS
# ============================================================

@router.get("/")
def get_provenance_records(
    db: Session = Depends(get_db)
):

    records = service.get_records(db)

    return {
        "records": records,
        "record_count": len(records)
    }


# ============================================================
# VERIFY PROVENANCE HASH CHAIN
# ============================================================

@router.get("/verify")
def verify_provenance_chain(
    db: Session = Depends(get_db)
):

    result = service.verify_chain(db)

    return result


# ============================================================
# GET PROVENANCE FOR AN EVIDENCE CARD
# ============================================================

@router.get("/{evidence_card_id}")
def get_evidence_card_provenance(
    evidence_card_id: int,
    db: Session = Depends(get_db)
):

    records = service.get_records(db)

    card_records = [
        record
        for record in records
        if record["evidence_card_id"]
        == evidence_card_id
    ]

    if not card_records:

        raise HTTPException(
            status_code=404,
            detail=(
                "No provenance records found "
                "for this evidence card."
            )
        )

    return {
        "evidence_card_id":
            evidence_card_id,

        "records":
            card_records,

        "record_count":
            len(card_records)
    }