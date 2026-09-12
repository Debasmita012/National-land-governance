from ai.analysis.policy_red_team_service import (
    PolicyRedTeamService
)


service = PolicyRedTeamService()


recommendation = (
    "Expand urban development by 10% "
    "in the pilot district."
)


result = service.analyze(

    recommendation=recommendation,

    confidence_score=0.55,

    positive_impacts=[
        "Increased housing capacity",
        "Improved infrastructure availability"
    ],

    negative_impacts=[
        "Potential agricultural land loss"
    ],

    risks_limitations=[
        "Infrastructure demand may increase",
        "Climate vulnerability may increase"
    ],

    alternatives=[
        "Densification of existing urban areas",
        "Development around existing infrastructure"
    ],

    supporting_datasets=[
        {
            "dataset_id": 1,
            "name": "Agricultural Land Dataset"
        }
    ],

    research_papers=[
        {
            "document_id": 2,
            "title": "Land Governance Test Document"
        }
    ],

    citations=[
        {
            "document_id": 2,
            "chunk_index": 0
        }
    ]
)


print("\nAI POLICY RED-TEAM")
print("=" * 60)

print("\nRecommendation:")
print(
    result["recommendation"]
)

print("\nRisk level:")
print(
    result["risk_level"]
)

print("\nChallenges:")
for challenge in result["challenges"]:
    print(
        f"- {challenge}"
    )

print("\nEvidence gaps:")
for gap in result["evidence_gaps"]:
    print(
        f"- {gap}"
    )

print("\nFinal assessment:")
print(
    result["final_assessment"]
)

print("\nReview required:")
print(
    result["review_required"]
)