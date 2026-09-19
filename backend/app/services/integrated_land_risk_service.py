from pathlib import Path
from typing import Any, Dict

import pandas as pd

from app.services.land_risk_service import LandRiskService
from app.services.land_use_change_service import (
    LandUseChangeService,
)


class IntegratedLandRiskService:
    """
    Combines:

        1. Current land-risk analysis
        2. Historical/current land-use change

    into one explainable land-risk result.

    This is a pilot decision-support model.
    It is NOT a statistically validated probability model.
    """

    def __init__(self):
        self.risk_service = LandRiskService()
        self.change_service = LandUseChangeService()

    # ========================================================
    # LOAD TABULAR DATA
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

        if extension in {".xlsx", ".xls"}:
            return pd.read_excel(file_path)

        raise ValueError(
            "Only CSV and Excel files are supported "
            "for integrated land-risk analysis."
        )

    # ========================================================
    # NORMALIZE VALUES
    # ========================================================

    def _normalize_value(
        self,
        value: Any,
    ) -> str:

        if pd.isna(value):
            return ""

        return str(value).strip().lower()

    # ========================================================
    # BUILD LAND-USE CHANGE LOOKUP
    # ========================================================

    def _build_change_lookup(
        self,
        historical_file: str,
        current_file: str,
        historical_parcel_column: str,
        historical_land_use_column: str,
        current_parcel_column: str,
        current_land_use_column: str,
    ) -> Dict[str, Dict[str, Any]]:

        historical_df = self._load_dataframe(
            historical_file
        )

        current_df = self._load_dataframe(
            current_file
        )

        historical_df = historical_df[
            [
                historical_parcel_column,
                historical_land_use_column,
            ]
        ].copy()

        current_df = current_df[
            [
                current_parcel_column,
                current_land_use_column,
            ]
        ].copy()

        historical_df["_parcel_key"] = (
            historical_df[
                historical_parcel_column
            ]
            .apply(self._normalize_value)
        )

        current_df["_parcel_key"] = (
            current_df[
                current_parcel_column
            ]
            .apply(self._normalize_value)
        )

        historical_lookup = {}

        for _, row in historical_df.iterrows():

            parcel_key = row["_parcel_key"]

            if not parcel_key:
                continue

            historical_lookup[
                parcel_key
            ] = self._normalize_value(
                row[
                    historical_land_use_column
                ]
            )

        change_lookup = {}

        for _, row in current_df.iterrows():

            parcel_key = row["_parcel_key"]

            if not parcel_key:
                continue

            current_land_use = (
                self._normalize_value(
                    row[
                        current_land_use_column
                    ]
                )
            )

            previous_land_use = (
                historical_lookup.get(
                    parcel_key
                )
            )

            changed = (
                previous_land_use is not None
                and previous_land_use
                != current_land_use
            )

            change_lookup[
                parcel_key
            ] = {
                "previous_land_use": (
                    previous_land_use
                ),
                "current_land_use": (
                    current_land_use
                ),
                "land_use_changed": changed,
                "transition": (
                    f"{previous_land_use} → "
                    f"{current_land_use}"
                    if changed
                    else None
                ),
            }

        return change_lookup

    # ========================================================
    # LAND-USE CHANGE PRESSURE
    # ========================================================

    def _change_pressure(
        self,
        previous_land_use: str | None,
        current_land_use: str | None,
    ) -> float:

        if (
            not previous_land_use
            or not current_land_use
        ):
            return 0.0

        if (
            previous_land_use
            == current_land_use
        ):
            return 0.0

        # Higher pressure for transitions
        # associated with development/conversion.
        development_types = {
            "residential",
            "industrial",
            "commercial",
            "urban",
            "infrastructure",
        }

        protected_types = {
            "forest",
            "agricultural",
            "wetland",
            "protected",
        }

        if (
            previous_land_use in protected_types
            and current_land_use
            in development_types
        ):
            return 100.0

        if (
            previous_land_use
            in development_types
            and current_land_use
            in development_types
        ):
            return 65.0

        return 40.0

    # ========================================================
    # INTEGRATED ANALYSIS
    # ========================================================

    def analyze(
        self,
        current_file: str,
        current_detected_fields: Dict[str, Any],
        historical_file: str | None = None,
        historical_detected_fields: Dict[str, Any]
        | None = None,
    ) -> Dict[str, Any]:

        # ----------------------------------------------------
        # Base risk analysis
        # ----------------------------------------------------

        base_result = (
            self.risk_service.analyze_file(
                file_path=current_file,
                detected_fields=(
                    current_detected_fields
                ),
            )
        )

        # ----------------------------------------------------
        # No historical data
        # ----------------------------------------------------

        if not historical_file:

            return {
                **base_result,

                "land_use_change_integration": {
                    "available": False,
                    "message": (
                        "Historical land-use data was "
                        "not provided. Land-use change "
                        "pressure was not included."
                    ),
                },

                "model": {
                    "type": (
                        "Explainable composite "
                        "land-risk index"
                    ),
                    "status": "pilot",
                    "statistical_probability": False,
                },
            }

        # ----------------------------------------------------
        # Validate detected fields
        # ----------------------------------------------------

        historical_detected_fields = (
            historical_detected_fields
            or {}
        )

        historical_parcel_column = (
            historical_detected_fields.get(
                "parcel_id"
            )
        )

        historical_land_use_column = (
            historical_detected_fields.get(
                "land_use"
            )
        )

        current_parcel_column = (
            current_detected_fields.get(
                "parcel_id"
            )
        )

        current_land_use_column = (
            current_detected_fields.get(
                "land_use"
            )
        )

        if not historical_parcel_column:

            raise ValueError(
                "Historical dataset is missing "
                "a detectable parcel ID field."
            )

        if not historical_land_use_column:

            raise ValueError(
                "Historical dataset is missing "
                "a detectable land-use field."
            )

        if not current_parcel_column:

            raise ValueError(
                "Current dataset is missing "
                "a detectable parcel ID field."
            )

        if not current_land_use_column:

            raise ValueError(
                "Current dataset is missing "
                "a detectable land-use field."
            )

        # ----------------------------------------------------
        # Build change lookup
        # ----------------------------------------------------

        change_lookup = (
            self._build_change_lookup(
                historical_file=historical_file,
                current_file=current_file,
                historical_parcel_column=(
                    historical_parcel_column
                ),
                historical_land_use_column=(
                    historical_land_use_column
                ),
                current_parcel_column=(
                    current_parcel_column
                ),
                current_land_use_column=(
                    current_land_use_column
                ),
            )
        )

        # ----------------------------------------------------
        # Calculate overall change pressure
        # ----------------------------------------------------

        changed_count = sum(
            1
            for item in change_lookup.values()
            if item["land_use_changed"]
        )

        matched_count = len(
            change_lookup
        )

        conversion_rate = (
            (
                changed_count
                / matched_count
            )
            * 100
            if matched_count
            else 0
        )

        # ----------------------------------------------------
        # Try to identify parcel-level risk list
        # ----------------------------------------------------

        parcel_risks = []

        if isinstance(
            base_result,
            dict,
        ):

            possible_keys = [
                "parcel_risks",
                "risks",
                "risk_by_parcel",
                "parcel_analysis",
            ]

            for key in possible_keys:

                value = base_result.get(
                    key
                )

                if isinstance(
                    value,
                    list,
                ):

                    parcel_risks = value
                    break

        # ----------------------------------------------------
        # Enrich parcel risks
        # ----------------------------------------------------

        enriched_risks = []

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

            parcel_key = (
                self._normalize_value(
                    parcel_id
                )
            )

            change = change_lookup.get(
                parcel_key,
                {},
            )

            previous_land_use = (
                change.get(
                    "previous_land_use"
                )
            )

            current_land_use = (
                change.get(
                    "current_land_use"
                )
            )

            changed = change.get(
                "land_use_changed",
                False,
            )

            pressure = (
                self._change_pressure(
                    previous_land_use,
                    current_land_use,
                )
            )

            existing_score = float(
                risk.get(
                    "risk_score",
                    0,
                )
                or 0
            )

            # ------------------------------------------------
            # Integrate change pressure.
            #
            # Land-use change contributes up to
            # 20% of the final pilot score.
            # ------------------------------------------------

            if changed:

                integrated_score = (
                    existing_score * 0.80
                    + pressure * 0.20
                )

            else:

                integrated_score = (
                    existing_score * 0.90
                    + pressure * 0.10
                )

            integrated_score = round(
                max(
                    0,
                    min(
                        100,
                        integrated_score,
                    ),
                ),
                2,
            )

            # ------------------------------------------------
            # Risk level
            # ------------------------------------------------

            if integrated_score >= 80:

                risk_level = "Critical"

            elif integrated_score >= 60:

                risk_level = "High"

            elif integrated_score >= 30:

                risk_level = "Moderate"

            else:

                risk_level = "Low"

            # ------------------------------------------------
            # Explainability
            # ------------------------------------------------

            why = list(
                risk.get(
                    "why",
                    [],
                )
                or []
            )

            if changed:

                why.insert(
                    0,
                    (
                        "Land-use conversion detected: "
                        f"{previous_land_use} → "
                        f"{current_land_use}."
                    ),
                )

            enriched_risk = {
                **risk,

                "base_risk_score": (
                    existing_score
                ),

                "land_use_change_pressure": (
                    pressure
                ),

                "integrated_risk_score": (
                    integrated_score
                ),

                "integrated_risk_level": (
                    risk_level
                ),

                "previous_land_use": (
                    previous_land_use
                ),

                "current_land_use": (
                    current_land_use
                ),

                "land_use_changed": (
                    changed
                ),

                "land_use_transition": (
                    change.get(
                        "transition"
                    )
                ),

                "why": why,
            }

            enriched_risks.append(
                enriched_risk
            )

        # ----------------------------------------------------
        # Return integrated result
        # ----------------------------------------------------

        result = {
            **base_result,

            "land_use_change_integration": {
                "available": True,

                "matched_parcels": (
                    matched_count
                ),

                "changed_parcels": (
                    changed_count
                ),

                "unchanged_parcels": (
                    matched_count
                    - changed_count
                ),

                "conversion_rate": round(
                    conversion_rate,
                    2,
                ),
            },

            "model": {
                "type": (
                    "Integrated explainable "
                    "land-risk index"
                ),
                "status": "pilot",
                "statistical_probability": False,
                "land_use_change_weight": 0.20,
            },
        }

        if enriched_risks:

            result[
                "parcel_risks"
            ] = enriched_risks

        return result