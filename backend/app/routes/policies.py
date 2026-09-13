from typing import Any, Dict

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db

from app.models.base_models import Policy


router = APIRouter(
    prefix="/policies",
    tags=["Policies"]
)


def policy_to_dict(policy: Policy) -> Dict[str, Any]:
    metadata = policy.extra_metadata or {}

    return {
        "id": policy.id,
        "title": policy.title,
        "description": policy.description,
        "policy_type": policy.policy_type,
        "geography": policy.geography,
        "status": policy.status,
        "created_at": policy.created_at,

        # Additional Policy Explorer fields
        "code": metadata.get("code"),
        "year": metadata.get("year"),
        "implementationRate": metadata.get(
            "implementationRate"
        ),
        "leadMinistry": metadata.get(
            "leadMinistry"
        ),
        "overview": metadata.get(
            "overview",
            policy.description
        ),
        "keyClauses": metadata.get(
            "keyClauses",
            []
        ),
        "impact": metadata.get(
            "impact"
        ),
    }


@router.get("/")
def get_policies(
    db: Session = Depends(get_db)
):
    policies = (
        db.query(Policy)
        .order_by(Policy.id)
        .all()
    )

    return [
        policy_to_dict(policy)
        for policy in policies
    ]


@router.get("/{policy_id}")
def get_policy(
    policy_id: int,
    db: Session = Depends(get_db)
):
    policy = (
        db.query(Policy)
        .filter(Policy.id == policy_id)
        .first()
    )

    if not policy:
        raise HTTPException(
            status_code=404,
            detail="Policy not found."
        )

    return policy_to_dict(policy)