import rasterio
from pathlib import Path
from typing import Dict, Optional

import numpy as np


class SatelliteFeatureService:
    """
    Remote-sensing feature extraction for land intelligence.

    Supported indicators:

        NDVI  - vegetation condition
        NDWI  - water/moisture signal
        NDBI  - built-up area signal

    The service works with NumPy arrays representing
    satellite bands.

    Sentinel-2 band mapping:

        B3  = Green
        B4  = Red
        B8  = Near Infrared
        B11 = Short Wave Infrared
    """

    EPS = 1e-10

    # ========================================================
    # SAFE NORMALIZED DIFFERENCE
    # ========================================================

    @staticmethod
    def _normalized_difference(
        numerator,
        denominator
    ):

        numerator = np.asarray(
            numerator,
            dtype=float
        )

        denominator = np.asarray(
            denominator,
            dtype=float
        )

        result = (
            (numerator - denominator)
            /
            (
                numerator
                + denominator
                + SatelliteFeatureService.EPS
            )
        )

        return np.clip(
            result,
            -1.0,
            1.0
        )

    # ========================================================
    # NDVI
    # ========================================================

    def calculate_ndvi(
        self,
        red,
        nir
    ):

        """
        NDVI = (NIR - Red) / (NIR + Red)
        """

        return self._normalized_difference(
            nir,
            red
        )

    # ========================================================
    # NDWI
    # ========================================================

    def calculate_ndwi(
        self,
        green,
        nir
    ):

        """
        NDWI = (Green - NIR) / (Green + NIR)
        """

        return self._normalized_difference(
            green,
            nir
        )

    # ========================================================
    # NDBI
    # ========================================================

    def calculate_ndbi(
        self,
        nir,
        swir
    ):

        """
        NDBI = (SWIR - NIR) / (SWIR + NIR)

        Higher values generally indicate stronger
        built-up signals.
        """

        return self._normalized_difference(
            swir,
            nir
        )

    # ========================================================
    # STATISTICS
    # ========================================================

    @staticmethod
    def _statistics(
        values
    ):

        values = np.asarray(
            values,
            dtype=float
        )

        valid = values[
            np.isfinite(values)
        ]

        if len(valid) == 0:

            return {
                "mean": None,
                "median": None,
                "minimum": None,
                "maximum": None,
                "std": None
            }

        return {
            "mean": round(
                float(
                    np.mean(valid)
                ),
                4
            ),

            "median": round(
                float(
                    np.median(valid)
                ),
                4
            ),

            "minimum": round(
                float(
                    np.min(valid)
                ),
                4
            ),

            "maximum": round(
                float(
                    np.max(valid)
                ),
                4
            ),

            "std": round(
                float(
                    np.std(valid)
                ),
                4
            )
        }

    # ========================================================
    # COMPLETE FEATURE EXTRACTION
    # ========================================================
        # ========================================================
    # TEMPORAL CHANGE
    # ========================================================

    def calculate_change(
        self,
        previous_values,
        current_values
    ):
        """
        Calculate temporal change between two satellite
        observations of the same area.

        Useful for detecting:

            vegetation loss
            water-signal change
            built-up expansion
        """

        previous_values = np.asarray(
            previous_values,
            dtype=float
        )

        current_values = np.asarray(
            current_values,
            dtype=float
        )

        if previous_values.shape != current_values.shape:
            raise ValueError(
                "Previous and current satellite arrays "
                "must have the same shape."
            )

        difference = (
            current_values
            - previous_values
        )

        valid = (
            np.isfinite(previous_values)
            &
            np.isfinite(current_values)
        )

        if not np.any(valid):

            return {
                "mean_change": None,
                "absolute_mean_change": None,
                "increase_pixels": 0,
                "decrease_pixels": 0,
                "changed_pixels": 0
            }

        valid_difference = difference[
            valid
        ]

        return {
            "mean_change": round(
                float(
                    np.mean(
                        valid_difference
                    )
                ),
                4
            ),

            "absolute_mean_change": round(
                float(
                    np.mean(
                        np.abs(
                            valid_difference
                        )
                    )
                ),
                4
            ),

            "increase_pixels": int(
                np.sum(
                    valid_difference > 0.05
                )
            ),

            "decrease_pixels": int(
                np.sum(
                    valid_difference < -0.05
                )
            ),

            "changed_pixels": int(
                np.sum(
                    np.abs(
                        valid_difference
                    ) > 0.05
                )
            )
        }
    def extract_features(
        self,
        green,
        red,
        nir,
        swir
    ):

        ndvi = self.calculate_ndvi(
            red,
            nir
        )

        ndwi = self.calculate_ndwi(
            green,
            nir
        )

        ndbi = self.calculate_ndbi(
            nir,
            swir
        )

        return {
            "ndvi": self._statistics(
                ndvi
            ),

            "ndwi": self._statistics(
                ndwi
            ),

            "ndbi": self._statistics(
                ndbi
            ),

            "metadata": {
                "source": "Sentinel-2 compatible",
                "indices": [
                    "NDVI",
                    "NDWI",
                    "NDBI"
                ],
                "status": "computed"
            }
        }
        # ========================================================
    # GEOTIFF BAND READER
    # ========================================================

    def extract_from_geotiffs(
        self,
        green_path,
        red_path,
        nir_path,
        swir_path
    ):
        """
        Read Sentinel-2-compatible GeoTIFF bands and calculate
        NDVI, NDWI and NDBI.

        Expected bands:

            green -> Sentinel-2 B3
            red   -> Sentinel-2 B4
            nir   -> Sentinel-2 B8
            swir  -> Sentinel-2 B11
        """

        paths = {
            "green": Path(green_path),
            "red": Path(red_path),
            "nir": Path(nir_path),
            "swir": Path(swir_path)
        }

        for name, path in paths.items():

            if not path.exists():

                raise FileNotFoundError(
                    f"{name.upper()} GeoTIFF not found:\n{path}"
                )


        with rasterio.open(
            paths["green"]
        ) as src_green:

            green = src_green.read(1)

            green_profile = src_green.profile

            green_crs = src_green.crs

            green_transform = src_green.transform


        with rasterio.open(
            paths["red"]
        ) as src_red:

            red = src_red.read(1)


        with rasterio.open(
            paths["nir"]
        ) as src_nir:

            nir = src_nir.read(1)


        with rasterio.open(
            paths["swir"]
        ) as src_swir:

            swir = src_swir.read(1)


        # ----------------------------------------------------
        # Shape validation
        # ----------------------------------------------------

        shapes = {
            "green": green.shape,
            "red": red.shape,
            "nir": nir.shape,
            "swir": swir.shape
        }


        if len(
            set(
                shapes.values()
            )
        ) != 1:

            raise ValueError(
                "GeoTIFF bands do not have matching "
                f"dimensions: {shapes}"
            )


        # ----------------------------------------------------
        # Calculate indices
        # ----------------------------------------------------

        ndvi = self.calculate_ndvi(
            red,
            nir
        )

        ndwi = self.calculate_ndwi(
            green,
            nir
        )

        ndbi = self.calculate_ndbi(
            nir,
            swir
        )


        # ----------------------------------------------------
        # Result
        # ----------------------------------------------------

        return {

            "ndvi":
                self._statistics(
                    ndvi
                ),

            "ndwi":
                self._statistics(
                    ndwi
                ),

            "ndbi":
                self._statistics(
                    ndbi
                ),

            "raster": {

                "width":
                    green_profile.get(
                        "width"
                    ),

                "height":
                    green_profile.get(
                        "height"
                    ),

                "crs":
                    str(
                        green_crs
                    )
                    if green_crs
                    else None,

                "transform":
                    str(
                        green_transform
                    )
            },

            "metadata": {

                "source":
                    "Sentinel-2 compatible GeoTIFF",

                "indices": [
                    "NDVI",
                    "NDWI",
                    "NDBI"
                ],

                "status":
                    "computed_from_geotiff"
            }
        }

# ============================================================
# SERVICE INSTANCE
# ============================================================

satellite_feature_service = (
    SatelliteFeatureService()
)