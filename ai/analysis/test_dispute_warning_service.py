from ai.analysis.dispute_warning_service import (
    DisputeWarningService
)


service = DisputeWarningService()


result = service.analyze(

    dispute_count=120,

    dispute_growth_percentage=55,

    land_use_change_percentage=35,

    population_growth_percentage=18,

    anomaly_detected=True
)


print("\nLAND-DISPUTE EARLY-WARNING")
print("=" * 60)

print("\nRisk score:")
print(result["risk_score"])

print("\nRisk level:")
print(result["risk_level"])

print("\nWarning:")
print(result["warning"])

print("\nIndicators:")

for indicator in result["indicators"]:
    print(f"- {indicator}")

print("\nAnomaly detected:")
print(result["anomaly_detected"])