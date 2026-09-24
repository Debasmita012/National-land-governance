import numpy as np

from satellite_features import (
    satellite_feature_service
)


print("=" * 80)
print("SATELLITE FEATURE ENGINE TEST")
print("=" * 80)


# ============================================================
# SYNTHETIC SENTINEL-2 COMPATIBLE REFLECTANCE
# ============================================================

green = np.array([
    [0.20, 0.25, 0.30],
    [0.18, 0.22, 0.28],
    [0.24, 0.27, 0.31]
])


red = np.array([
    [0.15, 0.18, 0.20],
    [0.12, 0.16, 0.19],
    [0.17, 0.20, 0.22]
])


nir = np.array([
    [0.55, 0.62, 0.70],
    [0.50, 0.58, 0.68],
    [0.60, 0.65, 0.72]
])


swir = np.array([
    [0.30, 0.34, 0.40],
    [0.28, 0.32, 0.38],
    [0.31, 0.36, 0.42]
])


# ============================================================
# CURRENT FEATURES
# ============================================================

result = satellite_feature_service.extract_features(
    green=green,
    red=red,
    nir=nir,
    swir=swir
)


print()
print("NDVI:")
print(result["ndvi"])


print()
print("NDWI:")
print(result["ndwi"])


print()
print("NDBI:")
print(result["ndbi"])


print()
print("Metadata:")
print(result["metadata"])


# ============================================================
# TEMPORAL NDVI CHANGE
# ============================================================

previous_ndvi = np.array([
    [0.70, 0.68, 0.65],
    [0.72, 0.69, 0.66],
    [0.71, 0.67, 0.64]
])


current_ndvi = np.array([
    [0.60, 0.65, 0.55],
    [0.70, 0.60, 0.52],
    [0.58, 0.63, 0.50]
])


change = satellite_feature_service.calculate_change(
    previous_values=previous_ndvi,
    current_values=current_ndvi
)


print()
print("TEMPORAL NDVI CHANGE:")
print(change)


# ============================================================
# COMPLETE
# ============================================================

print()
print("=" * 80)
print("SATELLITE FEATURE ENGINE TEST COMPLETE")
print("=" * 80)