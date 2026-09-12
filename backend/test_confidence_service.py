from app.services.confidence_service import (
    ConfidenceService
)


service = ConfidenceService()


distances = [
    0.4917895495891571,
    0.5335665345191956,
    0.565862774848938,
    0.5728985071182251,
    0.5934445261955261
]


confidence = service.calculate_confidence(
    distances
)


print("RETRIEVAL DISTANCES")
print(distances)

print("\nCONFIDENCE SCORE")
print(confidence)