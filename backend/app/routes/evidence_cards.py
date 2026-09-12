import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db

from ai.analysis.policy_red_team_service import (
    PolicyRedTeamService
)

from app.models.base_models import (
    EvidenceCard,
    EvidenceCardDataset,
    EvidenceCardDocument,
    Dataset,
    Document
)

from app.schemas.evidence_card import (
    EvidenceCardCreate,
    EvidenceCardGenerate
)

from app.services.evidence_card_service import (
    EvidenceCardService
)

from app.services.policy_evidence_service import (
    PolicyEvidenceService
)


router = APIRouter(
    prefix="/evidence-cards",
    tags=["Evidence Cards"]
)


evidence_card_service = EvidenceCardService()

policy_evidence_service = PolicyEvidenceService()


# ============================================================
# CREATE EVIDENCE CARD
# ============================================================

@router.post("/")
def create_evidence_card(
    evidence_data: EvidenceCardCreate,
    db: Session = Depends(get_db)
):
    try:

        evidence_card = (
            evidence_card_service.create_evidence_card(
                db=db,
                evidence_package=evidence_data.model_dump()
            )
        )

        return evidence_card

    except ValueError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )


# ============================================================
# GENERATE EVIDENCE CARD
# ============================================================

@router.post("/generate")
def generate_evidence_card(
    evidence_data: EvidenceCardGenerate,
    db: Session = Depends(get_db)
):
    try:

        evidence_card = (
            policy_evidence_service
            .generate_and_save_evidence_card(
                db=db,
                question=evidence_data.question,
                supporting_datasets=(
                    evidence_data.supporting_datasets
                ),
                affected_geography=(
                    evidence_data.affected_geography
                )
            )
        )

        return evidence_card

    except ValueError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )


# ============================================================
# AI POLICY RED-TEAM
# ============================================================

@router.get("/{card_id}/red-team")
def red_team_evidence_card(
    card_id: int,
    db: Session = Depends(get_db)
):

    card = (
        db.query(EvidenceCard)
        .filter(EvidenceCard.id == card_id)
        .first()
    )

    if not card:

        raise HTTPException(
            status_code=404,
            detail="Evidence card not found."
        )

    service = PolicyRedTeamService()

    result = service.analyze(

        recommendation=card.recommendation,

        confidence_score=(
            card.confidence_score or 0.0
        ),

        positive_impacts=(
            card.positive_impacts or []
        ),

        negative_impacts=(
            card.negative_impacts or []
        ),

        risks_limitations=(
            card.risks_limitations or []
        ),

        alternatives=(
            card.alternatives or []
        ),

        supporting_datasets=(
            card.supporting_datasets or []
        ),

        research_papers=(
            card.research_papers or []
        ),

        citations=(
            card.citations or []
        )
    )

    return {
        "evidence_card_id": card.id,
        "red_team": result
    }


# ============================================================
# EVIDENCE CARD TRACEABILITY
# ============================================================

@router.get("/{card_id}/traceability")
def get_evidence_card_traceability(
    card_id: int,
    db: Session = Depends(get_db)
):

    card = (
        db.query(EvidenceCard)
        .filter(EvidenceCard.id == card_id)
        .first()
    )

    if not card:

        raise HTTPException(
            status_code=404,
            detail="Evidence card not found"
        )

    dataset_links = (
        db.query(
            EvidenceCardDataset,
            Dataset
        )
        .join(
            Dataset,
            EvidenceCardDataset.dataset_id == Dataset.id
        )
        .filter(
            EvidenceCardDataset.evidence_card_id == card_id
        )
        .all()
    )

    document_links = (
        db.query(
            EvidenceCardDocument,
            Document
        )
        .join(
            Document,
            EvidenceCardDocument.document_id == Document.id
        )
        .filter(
            EvidenceCardDocument.evidence_card_id == card_id
        )
        .all()
    )

    datasets = []

    for link, dataset in dataset_links:

        datasets.append(
            {
                "dataset_id": dataset.id,
                "name": dataset.name,
                "source": dataset.source
            }
        )

    documents = []

    for link, document in document_links:

        evidence_text = None

        distance = None

        for citation in card.citations or []:

            if (
                citation.get("document_id")
                == document.id
                and citation.get("chunk_index")
                == link.chunk_index
            ):

                evidence_text = citation.get(
                    "evidence_text"
                )

                distance = citation.get(
                    "distance"
                )

                break

        documents.append(
            {
                "document_id": document.id,
                "title": document.title,
                "source": document.source,
                "chunk_index": link.chunk_index,
                "distance": distance,
                "evidence_text": evidence_text
            }
        )

    return {
        "evidence_card_id": card_id,

        "datasets": datasets,

        "documents": documents,

        "dataset_count": len(datasets),

        "document_count": len(documents)
    }


# ============================================================
# GET COMPLETE EVIDENCE CARD
# ============================================================

@router.get("/{card_id}")
def get_evidence_card(
    card_id: int,
    db: Session = Depends(get_db)
):

    card = (
        db.query(EvidenceCard)
        .filter(EvidenceCard.id == card_id)
        .first()
    )

    if not card:

        raise HTTPException(
            status_code=404,
            detail="Evidence card not found"
        )

    # --------------------------------------------------------
    # Supporting datasets
    # --------------------------------------------------------

    dataset_links = (
        db.query(
            EvidenceCardDataset,
            Dataset
        )
        .join(
            Dataset,
            EvidenceCardDataset.dataset_id == Dataset.id
        )
        .filter(
            EvidenceCardDataset.evidence_card_id == card_id
        )
        .all()
    )

    # --------------------------------------------------------
    # Supporting documents
    # --------------------------------------------------------

    document_links = (
        db.query(
            EvidenceCardDocument,
            Document
        )
        .join(
            Document,
            EvidenceCardDocument.document_id == Document.id
        )
        .filter(
            EvidenceCardDocument.evidence_card_id == card_id
        )
        .all()
    )

    # --------------------------------------------------------
    # Build supporting dataset information
    # --------------------------------------------------------

    supporting_datasets = []

    for link, dataset in dataset_links:

        supporting_datasets.append(
            {
                "dataset_id": dataset.id,
                "name": dataset.name,
                "source": dataset.source
            }
        )

    # --------------------------------------------------------
    # Build supporting document information
    # --------------------------------------------------------

    supporting_documents = []

    for link, document in document_links:

        supporting_documents.append(
            {
                "document_id": document.id,
                "title": document.title,
                "source": document.source,
                "chunk_index": link.chunk_index
            }
        )

    # --------------------------------------------------------
    # AI Policy Red-Team
    # --------------------------------------------------------

    red_team_service = PolicyRedTeamService()

    red_team_result = red_team_service.analyze(

        recommendation=card.recommendation,

        confidence_score=(
            card.confidence_score or 0.0
        ),

        positive_impacts=(
            card.positive_impacts or []
        ),

        negative_impacts=(
            card.negative_impacts or []
        ),

        risks_limitations=(
            card.risks_limitations or []
        ),

        alternatives=(
            card.alternatives or []
        ),

        supporting_datasets=(
            card.supporting_datasets or []
        ),

        research_papers=(
            card.research_papers or []
        ),

        citations=(
            card.citations or []
        )
    )

    # --------------------------------------------------------
    # Final complete response
    # --------------------------------------------------------

    return {

        "id": card.id,

        "title": card.title,

        "recommendation":
            card.recommendation,

        "affected_geography":
            card.affected_geography,

        "confidence_score":
            card.confidence_score,

        "confidence_level":
            card.confidence_level,

        "retrieval_confidence":
            card.retrieval_confidence,

        "evidence_coverage":
            card.evidence_coverage,

        "expected_impacts": {

            "positive":
                card.positive_impacts,

            "negative":
                card.negative_impacts
        },

        "risks_limitations":
            card.risks_limitations,

        "alternatives":
            card.alternatives,

        "supporting_datasets":
            supporting_datasets,

        "supporting_documents":
            supporting_documents,

        "citations":
            card.citations,

        "traceability": {

            "evidence_card_id":
                card.id,

            "dataset_count":
                len(supporting_datasets),

            "document_count":
                len(supporting_documents),

            "citation_count":
                len(card.citations or [])
        },

        # ----------------------------------------------------
        # AI POLICY RED-TEAM RESULT
        # ----------------------------------------------------

        "red_team":
            red_team_result
    }