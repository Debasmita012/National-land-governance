from ai.analysis.trend_analysis_service import (
    TrendAnalysisService
)

from ai.analysis.anomaly_detection_service import (
    AnomalyDetectionService
)

from ai.analysis.explainability_service import (
    ExplainabilityService
)


# -----------------------------------------
# Create services
# -----------------------------------------

trend_service = TrendAnalysisService()

anomaly_service = AnomalyDetectionService(
    contamination=0.1
)

explainability_service = (
    ExplainabilityService()
)


# -----------------------------------------
# Test data
# -----------------------------------------

values = [
    100,
    102,
    101,
    105,
    103,
    104,
    102,
    106,
    101,
    250
]


# -----------------------------------------
# Run analysis
# -----------------------------------------

trend_result = (
    trend_service.analyze(
        values
    )
)

anomaly_result = (
    anomaly_service.detect(
        values
    )
)


# -----------------------------------------
# Generate explanations
# -----------------------------------------

summary = (
    explainability_service
    .build_analysis_summary(
        trend_result=trend_result,
        anomaly_result=anomaly_result
    )
)


# -----------------------------------------
# Print results
# -----------------------------------------

print("\nEXPLAINABLE AI ANALYSIS")
print("=" * 60)

print("\nTREND FINDING")
print("-" * 60)

print(
    summary["trend"]["finding"]
)

print("\nReason:")
print(
    summary["trend"]["reason"]
)

print("\nRisk signal:")
print(
    summary["trend"]["risk_signal"]
)

print("\nPattern strength:")
print(
    summary["trend"]["pattern_strength"]
)

print("\nANOMALY FINDING")
print("-" * 60)

print(
    summary["anomalies"]["finding"]
)

print("\nReason:")
print(
    summary["anomalies"]["reason"]
)

print("\nRisk signal:")
print(
    summary["anomalies"]["risk_signal"]
)

print("\nAnomaly values:")
print(
    summary["anomalies"]["anomaly_values"]
)

print("\nOVERALL FINDING")
print("-" * 60)

print(
    summary["overall_finding"]
)