from pathlib import Path
from typing import Any, Dict, List

import pandas as pd


class LandHotspotService:
    """
    Converts parcel-level land-risk information into
    GeoJSON features suitable for Leaflet / GIS display.

    This is a visualization layer over the existing
    land-risk analysis. It does not claim that the
    risk score is a statistically validated probability.
    """

    # ========================================================
    # LOAD DATA
    # ========================================================

    def _load_dataframe(
        self,
        file_path: str,
    ) -> pd.DataFrame:

        extension = Path(
            file_path
        ).suffix.lower()

        if extension == ".csv":
            return pd.read_csv(file_path)

        if extension in {
            ".xlsx",
            ".xls",
        }:
            return pd.read_excel(file_path)

        raise ValueError(
            "Hotspot analysis supports CSV and Excel files."
        )

    # ========================================================
    # NORMALIZE VALUE
    # ========================================================

    def _normalize(
        self,
        value: Any,
    ) -> str:

        if pd.isna(value):
            return ""

        return str(value).strip().lower()

    # ========================================================
    # SAFE FLOAT
    # ========================================================

    def _safe_float(
        self,
        value: Any,
        default: float = 0.0,
    ) -> float:

        try:

            if pd.isna(value):
                return default

            return float(value)

        except (
            TypeError,
            ValueError,
        ):

            return default

    # ========================================================
    # FIND RISK RECORD
    # ========================================================

    def _build_risk_lookup(
        self,
        parcel_risks: List[Dict[str, Any]],
    ) -> Dict[str, Dict[str, Any]]:

        lookup = {}

        for risk in parcel_risks:

            if not isinstance(
                risk,
                dict,
            ):
                continue

            parcel_id = (
                risk.get("parcel_id")
                or risk.get("parcel")
                or risk.get("id")
                or risk.get("ulpin")
            )

            key = self._normalize(
                parcel_id
            )

            if not key:
                continue

            lookup[key] = risk

        return lookup

    # ========================================================
    # BUILD GEOJSON
    # ========================================================

    def create_geojson(
        self,
        file_path: str,
        detected_fields: Dict[str, Any],
        parcel_risks: List[Dict[str, Any]],
    ) -> Dict[str, Any]:

        dataframe = self._load_dataframe(
            file_path
        )

        # ----------------------------------------------------
        # Detect coordinate fields
        # ----------------------------------------------------

        latitude_column = (
            detected_fields.get(
                "latitude"
            )
        )

        longitude_column = (
            detected_fields.get(
                "longitude"
            )
        )

        parcel_column = (
            detected_fields.get(
                "parcel_id"
            )
        )

        land_use_column = (
            detected_fields.get(
                "land_use"
            )
        )

        if not latitude_column:

            raise ValueError(
                "Latitude column could not be detected."
            )

        if not longitude_column:

            raise ValueError(
                "Longitude column could not be detected."
            )

        if not parcel_column:

            raise ValueError(
                "Parcel ID column could not be detected."
            )

        # ----------------------------------------------------
        # Risk lookup
        # ----------------------------------------------------

        risk_lookup = (
            self._build_risk_lookup(
                parcel_risks
            )
        )

        features = []

        skipped_records = 0

        # ====================================================
        # CREATE FEATURES
        # ====================================================

        for _, row in dataframe.iterrows():

            latitude = self._safe_float(
                row.get(
                    latitude_column
                ),
                default=None,
            )

            longitude = self._safe_float(
                row.get(
                    longitude_column
                ),
                default=None,
            )

            # -----------------------------------------------
            # Validate coordinates
            # -----------------------------------------------

            if (
                latitude is None
                or longitude is None
            ):

                skipped_records += 1

                continue

            if not (
                -90 <= latitude <= 90
            ):

                skipped_records += 1

                continue

            if not (
                -180 <= longitude <= 180
            ):

                skipped_records += 1

                continue

            # -----------------------------------------------
            # Parcel ID
            # -----------------------------------------------

            parcel_id = row.get(
                parcel_column
            )

            parcel_key = self._normalize(
                parcel_id
            )

            # -----------------------------------------------
            # Get risk record
            # -----------------------------------------------

            risk = risk_lookup.get(
                parcel_key,
                {},
            )

            risk_score = self._safe_float(
                risk.get(
                    "integrated_risk_score",
                    risk.get(
                        "risk_score",
                        0,
                    ),
                )
            )

            risk_level = (
                risk.get(
                    "integrated_risk_level"
                )
                or risk.get(
                    "risk_level"
                )
                or "Unknown"
            )

            # -----------------------------------------------
            # Land use
            # -----------------------------------------------

            land_use = None

            if land_use_column:

                value = row.get(
                    land_use_column
                )

                if not pd.isna(value):

                    land_use = str(
                        value
                    )

            # -----------------------------------------------
            # Risk explanation
            # -----------------------------------------------

            why = risk.get(
                "why",
                [],
            )

            if not isinstance(
                why,
                list,
            ):

                why = [str(why)]

            # -----------------------------------------------
            # Land-use change
            # -----------------------------------------------

            previous_land_use = (
                risk.get(
                    "previous_land_use"
                )
            )

            current_land_use = (
                risk.get(
                    "current_land_use"
                )
                or land_use
            )

            land_use_changed = bool(
                risk.get(
                    "land_use_changed",
                    False,
                )
            )

            transition = (
                risk.get(
                    "land_use_transition"
                )
            )

            # -----------------------------------------------
            # Create GeoJSON feature
            # -----------------------------------------------

            feature = {
                "type": "Feature",

                "geometry": {
                    "type": "Point",

                    "coordinates": [
                        longitude,
                        latitude,
                    ],
                },

                "properties": {
                    "parcel_id": (
                        str(parcel_id)
                        if parcel_id is not None
                        else None
                    ),

                    "risk_score": round(
                        risk_score,
                        2,
                    ),

                    "risk_level": (
                        risk_level
                    ),

                    "land_use": (
                        land_use
                    ),

                    "previous_land_use": (
                        previous_land_use
                    ),

                    "current_land_use": (
                        current_land_use
                    ),

                    "land_use_changed": (
                        land_use_changed
                    ),

                    "land_use_transition": (
                        transition
                    ),

                    "why": why,

                    "risk_components": (
                        risk.get(
                            "components",
                            {},
                        )
                    ),

                    "anomaly_detected": bool(
                        risk.get(
                            "anomaly_detected",
                            False,
                        )
                    ),

                    "latitude": (
                        latitude
                    ),

                    "longitude": (
                        longitude
                    ),
                },
            }

            features.append(
                feature
            )

        # ====================================================
        # SUMMARY
        # ====================================================

        risk_distribution = {
            "Critical": 0,
            "High": 0,
            "Moderate": 0,
            "Low": 0,
            "Unknown": 0,
        }

        for feature in features:

            level = feature[
                "properties"
            ].get(
                "risk_level",
                "Unknown",
            )

            if level not in risk_distribution:

                level = "Unknown"

            risk_distribution[
                level
            ] += 1

        # ====================================================
        # RETURN GEOJSON
        # ====================================================

        return {
            "type": "FeatureCollection",

            "features": features,

            "metadata": {
                "total_records": len(
                    dataframe
                ),

                "mapped_records": len(
                    features
                ),

                "skipped_records": (
                    skipped_records
                ),

                "risk_distribution": (
                    risk_distribution
                ),

                "geometry_type": "Point",

                "coordinate_source": (
                    "Uploaded dataset latitude "
                    "and longitude fields."
                ),

                "model_status": (
                    "Visualization of the "
                    "existing pilot land-risk "
                    "analysis."
                ),

                "statistical_probability": False,
            },
        }