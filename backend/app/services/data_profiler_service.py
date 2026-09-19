from pathlib import Path
from typing import Any, Dict

import pandas as pd


class DataProfilerService:

    FIELD_ALIASES = {
        "parcel_id": [
            "parcel_id",
            "parcel",
            "parcel_no",
            "parcel_number",
            "ulpin",
            "ulpin_no",
            "ulpin_number",
        ],
        "survey_number": [
            "survey",
            "survey_no",
            "survey_number",
            "survey_id",
        ],
        "land_use": [
            "land_use",
            "landuse",
            "land_type",
            "land_category",
            "use_type",
        ],
        "dispute_count": [
            "dispute",
            "disputes",
            "dispute_count",
            "land_dispute",
            "land_disputes",
            "case_count",
            "cases",
        ],
        "population": [
            "population",
            "population_count",
            "pop",
            "population_total",
        ],
        "population_growth": [
            "population_growth",
            "population_growth_rate",
            "pop_growth",
            "pop_growth_rate",
        ],
        "latitude": [
            "latitude",
            "lat",
            "y",
        ],
        "longitude": [
            "longitude",
            "long",
            "lon",
            "lng",
            "x",
        ],
        "area": [
            "area",
            "area_ha",
            "area_hectare",
            "area_hectares",
            "land_area",
        ],
        "flood_risk": [
            "flood",
            "flood_risk",
            "flood_exposure",
            "flood_zone",
        ],
        "forest_cover": [
            "forest",
            "forest_cover",
            "forest_area",
            "forest_percentage",
        ],
    }

    def profile_file(self, file_path: str) -> Dict[str, Any]:
        """
        Automatically inspect an uploaded file and generate
        a basic land-data profile.
        """

        path = Path(file_path)

        if not path.exists():
            raise ValueError(
                f"File does not exist: {file_path}"
            )

        extension = path.suffix.lower()

        if extension == ".csv":
            return self._profile_csv(path)

        if extension in [".xlsx", ".xls"]:
            return self._profile_excel(path)

        if extension in [".geojson", ".json"]:
            return self._profile_geojson(path)

        if extension == ".pdf":
            return self._profile_pdf(path)

        raise ValueError(
            f"Unsupported file type: {extension}"
        )

    # ---------------------------------------------------------
    # CSV
    # ---------------------------------------------------------

    def _profile_csv(self, path: Path) -> Dict[str, Any]:

        try:
            dataframe = pd.read_csv(path)

        except Exception as error:
            raise ValueError(
                f"Unable to read CSV file: {str(error)}"
            )

        return self._build_tabular_profile(
            dataframe=dataframe,
            file_type="CSV"
        )

    # ---------------------------------------------------------
    # Excel
    # ---------------------------------------------------------

    def _profile_excel(self, path: Path) -> Dict[str, Any]:

        try:
            dataframe = pd.read_excel(path)

        except Exception as error:
            raise ValueError(
                f"Unable to read Excel file: {str(error)}"
            )

        return self._build_tabular_profile(
            dataframe=dataframe,
            file_type="Excel"
        )

    # ---------------------------------------------------------
    # GeoJSON
    # ---------------------------------------------------------

    def _profile_geojson(self, path: Path) -> Dict[str, Any]:

        try:
            import geopandas as gpd

            dataframe = gpd.read_file(path)

            geometry_type = None

            if "geometry" in dataframe.columns:
                geometry_types = (
                    dataframe.geometry
                    .geom_type
                    .dropna()
                    .unique()
                    .tolist()
                )

                if geometry_types:
                    geometry_type = geometry_types

            profile = self._build_tabular_profile(
                dataframe=dataframe.drop(
                    columns=["geometry"],
                    errors="ignore"
                ),
                file_type="GeoJSON"
            )

            profile["geospatial"] = {
                "is_geospatial": True,
                "geometry_types": geometry_type,
                "coordinate_reference_system": (
                    str(dataframe.crs)
                    if dataframe.crs
                    else None
                )
            }

            return profile

        except ImportError:
            raise ValueError(
                "GeoPandas is required for GeoJSON profiling."
            )

        except Exception as error:
            raise ValueError(
                f"Unable to read GeoJSON file: {str(error)}"
            )

    # ---------------------------------------------------------
    # PDF
    # ---------------------------------------------------------

    def _profile_pdf(self, path: Path) -> Dict[str, Any]:

        try:
            from pypdf import PdfReader

            reader = PdfReader(str(path))

            page_count = len(reader.pages)

            text_length = 0

            for page in reader.pages:
                text = page.extract_text() or ""
                text_length += len(text)

            return {
                "file_type": "PDF",
                "pages": page_count,
                "text_characters": text_length,
                "columns": [],
                "rows": None,
                "detected_fields": {},
                "data_quality": {
                    "missing_values": None,
                    "duplicate_rows": None
                },
                "geospatial": {
                    "is_geospatial": False
                }
            }

        except ImportError:
            raise ValueError(
                "pypdf is required for PDF profiling."
            )

        except Exception as error:
            raise ValueError(
                f"Unable to read PDF file: {str(error)}"
            )

    # ---------------------------------------------------------
    # Tabular profile
    # ---------------------------------------------------------

    def _build_tabular_profile(
        self,
        dataframe: pd.DataFrame,
        file_type: str
    ) -> Dict[str, Any]:

        columns = dataframe.columns.tolist()

        detected_fields = self._detect_fields(columns)

        missing_values = int(
            dataframe.isnull().sum().sum()
        )

        duplicate_rows = int(
            dataframe.duplicated().sum()
        )

        column_details = []

        for column in columns:

            series = dataframe[column]

            column_details.append({
                "name": str(column),
                "data_type": str(series.dtype),
                "non_null": int(series.notnull().sum()),
                "missing": int(series.isnull().sum()),
                "unique_values": int(
                    series.nunique(dropna=True)
                )
            })

        return {
            "file_type": file_type,
            "rows": int(len(dataframe)),
            "columns_count": len(columns),
            "columns": columns,
            "column_details": column_details,
            "detected_fields": detected_fields,
            "data_quality": {
                "missing_values": missing_values,
                "duplicate_rows": duplicate_rows
            },
            "geospatial": {
                "is_geospatial": self._has_coordinates(
                    detected_fields
                )
            }
        }

    # ---------------------------------------------------------
    # Field detection
    # ---------------------------------------------------------

    def _detect_fields(
        self,
        columns
    ) -> Dict[str, str]:

        normalized_columns = {}

        for column in columns:

            normalized = (
                str(column)
                .strip()
                .lower()
                .replace(" ", "_")
                .replace("-", "_")
            )

            normalized_columns[normalized] = str(column)

        detected = {}

        for field, aliases in self.FIELD_ALIASES.items():

            for alias in aliases:

                normalized_alias = (
                    alias
                    .strip()
                    .lower()
                    .replace(" ", "_")
                    .replace("-", "_")
                )

                if normalized_alias in normalized_columns:

                    detected[field] = (
                        normalized_columns[
                            normalized_alias
                        ]
                    )

                    break

        return detected

    # ---------------------------------------------------------
    # Geographic detection
    # ---------------------------------------------------------

    def _has_coordinates(
        self,
        detected_fields: Dict[str, str]
    ) -> bool:

        return (
            "latitude" in detected_fields
            and "longitude" in detected_fields
        )