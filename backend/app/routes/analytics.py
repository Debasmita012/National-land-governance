from typing import List

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from ai.analysis.trend_analysis_service import TrendAnalysisService
from ai.analysis.anomaly_detection_service import AnomalyDetectionService
from ai.analysis.explainability_service import ExplainabilityService


router = APIRouter(
    prefix="/analytics",
    tags=["AI Analytics"]
)


trend_service = TrendAnalysisService()
anomaly_service = AnomalyDetectionService()
explainability_service = ExplainabilityService()


class AnalyticsRequest(BaseModel):
    values: List[float]


@router.post("/trend")
def analyze_trend(data: AnalyticsRequest):
    try:
        result = trend_service.analyze(
            values=data.values
        )

        explanation = (
            explainability_service.explain_trend(
                result
            )
        )

        return {
            "trend": result,
            "explanation": explanation
        }

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )


@router.post("/anomaly")
def analyze_anomalies(data: AnalyticsRequest):
    try:
        result = anomaly_service.detect(
            values=data.values
        )

        explanation = (
            explainability_service.explain_anomalies(
                result
            )
        )

        return {
            "anomalies": result,
            "explanation": explanation
        }

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )


@router.post("/summary")
def analyze_summary(data: AnalyticsRequest):
    try:
        trend_result = trend_service.analyze(
            values=data.values
        )

        anomaly_result = anomaly_service.detect(
            values=data.values
        )

        summary = (
            explainability_service.build_analysis_summary(
                trend_result,
                anomaly_result
            )
        )

        return summary

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )