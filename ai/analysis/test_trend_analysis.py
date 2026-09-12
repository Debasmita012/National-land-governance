from ai.analysis.trend_analysis_service import (
    TrendAnalysisService
)


service = TrendAnalysisService()


values = [
    100,
    110,
    125,
    130,
    150
]


result = service.analyze(
    values
)


print("\nTREND ANALYSIS")
print("=" * 60)

print("\nInput values:")
print(values)

print("\nTrend direction:")
print(
    result["trend_direction"]
)

print("\nTrend strength:")
print(
    result["trend_strength"]
)

print("\nFirst value:")
print(
    result["first_value"]
)

print("\nLast value:")
print(
    result["last_value"]
)

print("\nAbsolute change:")
print(
    result["absolute_change"]
)

print("\nPercentage change:")
print(
    result["percentage_change"]
)

print("\nAverage:")
print(
    result["average_value"]
)

print("\nHighest:")
print(
    result["highest_value"]
)

print("\nLowest:")
print(
    result["lowest_value"]
)

print("\nData points:")
print(
    result["data_points"]
)