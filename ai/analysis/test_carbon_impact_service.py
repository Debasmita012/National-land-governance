from ai.analysis.carbon_impact_service import (
    CarbonImpactService
)


service = CarbonImpactService()


result = service.estimate(

    baseline_emissions=10000,

    projected_emissions=11500
)


print("\nCARBON / CLIMATE IMPACT ESTIMATOR")
print("=" * 60)

print("\nBaseline emissions:")
print(
    result["baseline_emissions"],
    "tCO2e"
)

print("\nProjected emissions:")
print(
    result["projected_emissions"],
    "tCO2e"
)

print("\nEmissions change:")
print(
    result["emissions_change"],
    "tCO2e"
)

print("\nPercentage change:")
print(
    result["percentage_change"],
    "%"
)

print("\nClimate impact:")
print(
    result["climate_impact"]
)

print("\nImpact level:")
print(
    result["impact_level"]
)

print("\nInterpretation:")
print(
    result["interpretation"]
)