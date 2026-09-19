from pathlib import Path
from typing import Any, Dict

import pandas as pd


class LandIntelligenceService:

    def analyze_file(
        self,
        file_path: str,
        detected_fields: Dict[str, str]
    ) -> Dict[str, Any]:

        path = Path(file_path)

        if not path.exists():
            raise ValueError(
                f"File does not exist: {file_path}"
            )

        extension = path.suffix.lower()

        dataframe = self._load_dataframe(
            path,
            extension
        )

        return self._analyze_dataframe(
            dataframe,
            detected_fields
        )

    # ---------------------------------------------------------
    # Load dataset
    # ---------------------------------------------------------

    def _load_dataframe(
        self,
        path: Path,
        extension: str
    ) -> pd.DataFrame:

        if extension == ".csv":

            return pd.read_csv(path)

        if extension in [".xlsx", ".xls"]:

            return pd.read_excel(path)

        raise ValueError(
            "Land intelligence analysis currently "
            "supports CSV and Excel files."
        )

    # ---------------------------------------------------------
    # Main analysis
    # ---------------------------------------------------------

    def _analyze_dataframe(
        self,
        dataframe: pd.DataFrame,
        detected_fields: Dict[str, str]
    ) -> Dict[str, Any]:

        result = {
            "records": int(len(dataframe)),
            "indicators": {},
            "land_use": {},
            "geography": {},
            "data_quality": {},
            "warnings": []
        }

        # -----------------------------------------------------
        # Parcel analysis
        # -----------------------------------------------------

        parcel_column = detected_fields.get(
            "parcel_id"
        )

        if parcel_column and parcel_column in dataframe.columns:

            result["indicators"]["parcels_analyzed"] = int(
                dataframe[parcel_column]
                .nunique(dropna=True)
            )

        else:

            result["indicators"]["parcels_analyzed"] = None

            result["warnings"].append(
                "Parcel ID field was not detected."
            )

        # -----------------------------------------------------
        # Dispute analysis
        # -----------------------------------------------------

        dispute_column = detected_fields.get(
            "dispute_count"
        )

        if dispute_column and dispute_column in dataframe.columns:

            dispute_series = pd.to_numeric(
                dataframe[dispute_column],
                errors="coerce"
            ).fillna(0)

            total_disputes = float(
                dispute_series.sum()
            )

            parcels_with_disputes = int(
                (dispute_series > 0).sum()
            )

            average_disputes = float(
                dispute_series.mean()
            )

            max_disputes = float(
                dispute_series.max()
            )

            result["indicators"]["total_disputes"] = (
                int(total_disputes)
            )

            result["indicators"]["parcels_with_disputes"] = (
                parcels_with_disputes
            )

            result["indicators"]["average_disputes"] = round(
                average_disputes,
                2
            )

            result["indicators"]["maximum_disputes"] = (
                int(max_disputes)
            )

            if len(dataframe) > 0:

                dispute_percentage = (
                    parcels_with_disputes
                    / len(dataframe)
                ) * 100

            else:

                dispute_percentage = 0

            result["indicators"]["dispute_pressure"] = round(
                dispute_percentage,
                2
            )

        else:

            result["indicators"]["total_disputes"] = None

            result["indicators"]["dispute_pressure"] = None

            result["warnings"].append(
                "Dispute count field was not detected."
            )

        # -----------------------------------------------------
        # Land-use analysis
        # -----------------------------------------------------

        land_use_column = detected_fields.get(
            "land_use"
        )

        if land_use_column and land_use_column in dataframe.columns:

            land_use_series = (
                dataframe[land_use_column]
                .dropna()
                .astype(str)
                .str.strip()
            )

            distribution = (
                land_use_series
                .value_counts()
                .to_dict()
            )

            total_land_use_records = (
                len(land_use_series)
            )

            percentages = {}

            if total_land_use_records > 0:

                for category, count in distribution.items():

                    percentages[str(category)] = round(
                        (count / total_land_use_records) * 100,
                        2
                    )

            result["land_use"] = {
                "field": land_use_column,
                "categories": distribution,
                "percentages": percentages
            }

        else:

            result["land_use"] = {
                "field": None,
                "categories": {},
                "percentages": {}
            }

            result["warnings"].append(
                "Land-use field was not detected."
            )

        # -----------------------------------------------------
        # Population analysis
        # -----------------------------------------------------

        population_column = detected_fields.get(
            "population"
        )

        if population_column and population_column in dataframe.columns:

            population_series = pd.to_numeric(
                dataframe[population_column],
                errors="coerce"
            ).dropna()

            if not population_series.empty:

                result["indicators"]["population_total"] = round(
                    float(population_series.sum()),
                    2
                )

                result["indicators"]["population_average"] = round(
                    float(population_series.mean()),
                    2
                )

                result["indicators"]["population_maximum"] = round(
                    float(population_series.max()),
                    2
                )

            else:

                result["indicators"]["population_total"] = 0
                result["indicators"]["population_average"] = 0
                result["indicators"]["population_maximum"] = 0

        else:

            result["indicators"]["population_total"] = None

            result["warnings"].append(
                "Population field was not detected."
            )

        # -----------------------------------------------------
        # Population growth
        # -----------------------------------------------------

        population_growth_column = detected_fields.get(
            "population_growth"
        )

        if (
            population_growth_column
            and population_growth_column in dataframe.columns
        ):

            growth_series = pd.to_numeric(
                dataframe[population_growth_column],
                errors="coerce"
            ).dropna()

            if not growth_series.empty:

                result["indicators"][
                    "average_population_growth"
                ] = round(
                    float(growth_series.mean()),
                    2
                )

                result["indicators"][
                    "maximum_population_growth"
                ] = round(
                    float(growth_series.max()),
                    2
                )

            else:

                result["indicators"][
                    "average_population_growth"
                ] = 0

        else:

            result["indicators"][
                "average_population_growth"
            ] = None

        # -----------------------------------------------------
        # Area analysis
        # -----------------------------------------------------

        area_column = detected_fields.get(
            "area"
        )

        if area_column and area_column in dataframe.columns:

            area_series = pd.to_numeric(
                dataframe[area_column],
                errors="coerce"
            ).dropna()

            if not area_series.empty:

                result["indicators"]["total_area"] = round(
                    float(area_series.sum()),
                    2
                )

                result["indicators"]["average_area"] = round(
                    float(area_series.mean()),
                    2
                )

                result["indicators"]["maximum_area"] = round(
                    float(area_series.max()),
                    2
                )

            else:

                result["indicators"]["total_area"] = 0
                result["indicators"]["average_area"] = 0
                result["indicators"]["maximum_area"] = 0

        else:

            result["indicators"]["total_area"] = None

        # -----------------------------------------------------
        # Geographic analysis
        # -----------------------------------------------------

        latitude_column = detected_fields.get(
            "latitude"
        )

        longitude_column = detected_fields.get(
            "longitude"
        )

        if (
            latitude_column
            and longitude_column
            and latitude_column in dataframe.columns
            and longitude_column in dataframe.columns
        ):

            latitude = pd.to_numeric(
                dataframe[latitude_column],
                errors="coerce"
            )

            longitude = pd.to_numeric(
                dataframe[longitude_column],
                errors="coerce"
            )

            valid_coordinates = (
                latitude.notna()
                & longitude.notna()
            )

            valid_count = int(
                valid_coordinates.sum()
            )

            result["geography"] = {
                "has_coordinates": True,
                "valid_coordinate_records": valid_count,
                "latitude_range": [
                    round(float(latitude[valid_coordinates].min()), 6)
                    if valid_count > 0
                    else None,
                    round(float(latitude[valid_coordinates].max()), 6)
                    if valid_count > 0
                    else None
                ],
                "longitude_range": [
                    round(float(longitude[valid_coordinates].min()), 6)
                    if valid_count > 0
                    else None,
                    round(float(longitude[valid_coordinates].max()), 6)
                    if valid_count > 0
                    else None
                ]
            }

        else:

            result["geography"] = {
                "has_coordinates": False,
                "valid_coordinate_records": 0,
                "latitude_range": [None, None],
                "longitude_range": [None, None]
            }

            result["warnings"].append(
                "Latitude/longitude fields were not detected."
            )

        # -----------------------------------------------------
        # Data quality
        # -----------------------------------------------------

        missing_values = int(
            dataframe.isnull().sum().sum()
        )

        duplicate_rows = int(
            dataframe.duplicated().sum()
        )

        result["data_quality"] = {
            "missing_values": missing_values,
            "duplicate_rows": duplicate_rows,
            "missing_percentage": round(
                (
                    missing_values
                    / dataframe.size
                    * 100
                )
                if dataframe.size > 0
                else 0,
                2
            )
        }

        return result