from ai.analysis.sdg_scorecard_service import (
    SDGScorecardService
)


service = SDGScorecardService()


result = service.calculate_score(

    housing_impact=78,

    economic_impact=72,

    food_security_impact=45,

    climate_impact=52,

    infrastructure_impact=80
)


print("\nSDG-LINKED POLICY SCORECARD")
print("=" * 60)

print("\nScores:")

for name, data in result["scorecard"].items():

    print(
        f"{name}: "
        f"{data['score']}/100 "
        f"({data['level']})"
    )


print("\nOverall score:")
print(
    result["overall_score"]
)


print("\nOverall level:")
print(
    result["overall_level"]
)


print("\nStrengths:")

for item in result["strengths"]:
    print(
        f"- {item}"
    )


print("\nWeaknesses:")

for item in result["weaknesses"]:
    print(
        f"- {item}"
    )