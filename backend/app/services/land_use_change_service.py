from pathlib import Path
from typing import Any, Dict

import pandas as pd


class LandUseChangeService:
    """
    Detect land-use changes between a historical dataset
    and a current dataset.

    The datasets must contain:
        - parcel identifier
        - land-use category
    """

    def analyze_change(
        self,
        historical_file: str,
        current_file: str,
        historical_parcel_column: str,
        historical_land_use_column: str,
        current_parcel_column: str,
        current_land_use_column: str,
    ) -> Dict[str, Any]:

        historical_path = Path(
            historical_file
        )

        current_path = Path(
            current_file
        )

        if not historical_path.exists():

            raise ValueError(
                "Historical dataset does not exist."
            )

        if not current_path.exists():

            raise ValueError(
                "Current dataset does not exist."
            )

        historical_df = self._load_file(
            historical_path
        )

        current_df = self._load_file(
            current_path
        )

        required_historical = [
            historical_parcel_column,
            historical_land_use_column,
        ]

        required_current = [
            current_parcel_column,
            current_land_use_column,
        ]

        self._validate_columns(
            historical_df,
            required_historical,
            "historical",
        )

        self._validate_columns(
            current_df,
            required_current,
            "current",
        )

        return self._calculate_change(
            historical_df=historical_df,
            current_df=current_df,
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

    # ========================================================
    # LOAD FILE
    # ========================================================

    def _load_file(
        self,
        path: Path,
    ) -> pd.DataFrame:

        extension = path.suffix.lower()

        if extension == ".csv":

            return pd.read_csv(path)

        if extension in [".xlsx", ".xls"]:

            return pd.read_excel(path)

        raise ValueError(
            "Only CSV and Excel files are supported "
            "for land-use change detection."
        )

    # ========================================================
    # VALIDATE COLUMNS
    # ========================================================

    def _validate_columns(
        self,
        dataframe: pd.DataFrame,
        columns,
        dataset_name: str,
    ):

        missing_columns = [
            column
            for column in columns
            if column not in dataframe.columns
        ]

        if missing_columns:

            raise ValueError(
                f"Missing columns in {dataset_name} dataset: "
                f"{missing_columns}"
            )

    # ========================================================
    # CALCULATE CHANGE
    # ========================================================

    def _calculate_change(
        self,
        historical_df: pd.DataFrame,
        current_df: pd.DataFrame,
        historical_parcel_column: str,
        historical_land_use_column: str,
        current_parcel_column: str,
        current_land_use_column: str,
    ) -> Dict[str, Any]:

        historical = historical_df[
            [
                historical_parcel_column,
                historical_land_use_column,
            ]
        ].copy()

        current = current_df[
            [
                current_parcel_column,
                current_land_use_column,
            ]
        ].copy()

        historical.columns = [
            "parcel_id",
            "historical_land_use",
        ]

        current.columns = [
            "parcel_id",
            "current_land_use",
        ]

        # Convert parcel IDs to strings so that
        # "1001" and 1001 are treated consistently.
        historical["parcel_id"] = (
            historical["parcel_id"]
            .astype(str)
            .str.strip()
        )

        current["parcel_id"] = (
            current["parcel_id"]
            .astype(str)
            .str.strip()
        )

        historical["historical_land_use"] = (
            historical["historical_land_use"]
            .fillna("Unknown")
            .astype(str)
            .str.strip()
        )

        current["current_land_use"] = (
            current["current_land_use"]
            .fillna("Unknown")
            .astype(str)
            .str.strip()
        )

        # ----------------------------------------------------
        # Merge historical and current records
        # ----------------------------------------------------

        merged = historical.merge(
            current,
            on="parcel_id",
            how="inner",
        )

        if merged.empty:

            raise ValueError(
                "No matching parcel IDs were found "
                "between the historical and current datasets."
            )

        # ----------------------------------------------------
        # Detect changes
        # ----------------------------------------------------

        merged["changed"] = (
            merged["historical_land_use"]
            != merged["current_land_use"]
        )

        changed = merged[
            merged["changed"]
        ].copy()

        unchanged_count = int(
            (~merged["changed"]).sum()
        )

        changed_count = int(
            merged["changed"].sum()
        )

        matched_count = int(
            len(merged)
        )

        # ----------------------------------------------------
        # Conversion rate
        # ----------------------------------------------------

        if matched_count > 0:

            conversion_rate = (
                changed_count
                / matched_count
            ) * 100

        else:

            conversion_rate = 0

        # ----------------------------------------------------
        # Transition matrix
        # ----------------------------------------------------

        transitions = {}

        for _, row in changed.iterrows():

            historical_use = (
                row["historical_land_use"]
            )

            current_use = (
                row["current_land_use"]
            )

            transition_key = (
                f"{historical_use} → "
                f"{current_use}"
            )

            transitions[transition_key] = (
                transitions.get(
                    transition_key,
                    0,
                )
                + 1
            )

        # ----------------------------------------------------
        # Changed parcel records
        # ----------------------------------------------------

        changed_parcels = []

        for _, row in changed.iterrows():

            changed_parcels.append(
                {
                    "parcel_id": row["parcel_id"],
                    "previous_land_use": (
                        row["historical_land_use"]
                    ),
                    "current_land_use": (
                        row["current_land_use"]
                    ),
                }
            )

        # ----------------------------------------------------
        # Land-use distribution comparison
        # ----------------------------------------------------

        historical_distribution = (
            historical[
                "historical_land_use"
            ]
            .value_counts()
            .to_dict()
        )

        current_distribution = (
            current[
                "current_land_use"
            ]
            .value_counts()
            .to_dict()
        )

        # ----------------------------------------------------
        # Build result
        # ----------------------------------------------------

        return {
            "summary": {
                "historical_records": int(
                    len(historical)
                ),
                "current_records": int(
                    len(current)
                ),
                "matched_parcels": matched_count,
                "changed_parcels": changed_count,
                "unchanged_parcels": unchanged_count,
                "land_use_conversion_rate": round(
                    conversion_rate,
                    2,
                ),
            },

            "transitions": transitions,

            "historical_distribution": (
                historical_distribution
            ),

            "current_distribution": (
                current_distribution
            ),

            "changed_parcels": changed_parcels,

            "model": {
                "type": (
                    "Historical-current land-use "
                    "transition analysis"
                ),
                "status": "pilot",
                "prediction": False,
            },
        }