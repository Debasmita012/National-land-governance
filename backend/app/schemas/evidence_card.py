from typing import List, Dict, Optional

from pydantic import BaseModel, Field


class EvidenceCardCreate(BaseModel):
    recommendation: str

    supporting_datasets: List[Dict]

    research_papers: List[Dict]

    affected_geography: Optional[str] = None

    expected_impacts: Dict[str, List[str]] = Field(
        default_factory=lambda: {
            "positive": [],
            "negative": []
        }
    )

    confidence_score: float = Field(
        ge=0,
        le=1
    )

    risks_limitations: List[str] = Field(
        default_factory=list
    )

    alternatives: List[str] = Field(
        default_factory=list
    )

    citations: List[Dict]


class EvidenceCardGenerate(BaseModel):
    question: str

    supporting_datasets: List[Dict]

    affected_geography: str = "Pilot District"