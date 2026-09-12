from ai.analysis.anomaly_detection_service import (
    AnomalyDetectionService
)


service = AnomalyDetectionService(
    contamination=0.1
)


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


result = service.detect(
    values
)


print("\nANOMALY DETECTION")
print("=" * 60)

print("\nInput values:")
print(values)

print("\nTotal values:")
print(
    result["total_values"]
)

print("\nAnomalies detected:")
print(
    result["anomaly_count"]
)

print("\nNormal values:")
print(
    result["normal_count"]
)

print("\nAnomaly percentage:")
print(
    result["anomaly_percentage"]
)

print("\nDetailed results:")
print("-" * 60)

for item in result["results"]:

    print(
        f"Index: {item['index']} | "
        f"Value: {item['value']} | "
        f"Anomaly: {item['is_anomaly']} | "
        f"Score: {item['anomaly_score']}"
    )