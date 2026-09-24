from pathlib import Path
from typing import Any, Dict, List

import pandas as pd
from sklearn.ensemble import IsolationForest


class LandRiskService:
    """
    Explainable pilot land-risk scoring engine.

    IMPORTANT:
    This is a composite risk-index model for demonstration
    and decision-support purposes.

    The score is NOT a statistically validated probability
    of a land dispute.
    """

    # ========================================================
    # PILOT WEIGHTS
    # ========================================================

    DISPUTE_WEIGHT = 0.35
    POPULATION_WEIGHT = 0.20
    LAND_USE_WEIGHT = 0.20
    ANOMALY_WEIGHT = 0.25

    # ========================================================
    # PUBLIC FILE ANALYSIS METHOD
    # ========================================================

    def analyze_file(
        self,
        file_path: str,
        detected_fields: Dict[str, str],
    ) -> Dict[str, Any]:

        path = Path(file_path)

        if not path.exists():
            raise ValueError(
                f"File does not exist: {file_path}"
            )

        dataframe = self._load_dataframe(
            path,
            path.suffix.lower(),
        )

        return self._calculate_risk(
            dataframe=dataframe,
            detected_fields=detected_fields,
        )

    # ========================================================
    # COMPATIBILITY METHOD
    # ========================================================

    def analyze(
        self,
        file_path: str,
        detected_fields: Dict[str, str],
    ) -> Dict[str, Any]:
        """
        Compatibility wrapper.

        Some parts of the backend may call:
            risk_service.analyze(...)

        Others may call:
            risk_service.analyze_file(...)

        Both are supported.
        """

        return self.analyze_file(
            file_path=file_path,
            detected_fields=detected_fields,
        )

    # ========================================================
    # LOAD DATAFRAME
    # ========================================================

    def _load_dataframe(
        self,
        path: Path,
        extension: str,
    ) -> pd.DataFrame:

        if extension == ".csv":
            return pd.read_csv(path)

        if extension in [".xlsx", ".xls"]:
            return pd.read_excel(path)

        raise ValueError(
            "Land risk analysis currently supports "
            "CSV and Excel files."
        )

    # ========================================================
    # MAIN RISK CALCULATION
    # ========================================================

    def _calculate_risk(
        self,
        dataframe: pd.DataFrame,
        detected_fields: Dict[str, str],
    ) -> Dict[str, Any]:

        if dataframe.empty:
            raise ValueError(
                "The uploaded dataset contains no records."
            )

        df = dataframe.copy()

        # ----------------------------------------------------
        # DETECTED FIELDS
        # ----------------------------------------------------

        parcel_column = detected_fields.get(
            "parcel_id"
        )

        dispute_column = detected_fields.get(
            "dispute_count"
        )

        population_column = detected_fields.get(
            "population"
        )

        land_use_column = detected_fields.get(
            "land_use"
        )

        # ----------------------------------------------------
        # INITIALIZE COMPONENT SCORES
        # ----------------------------------------------------

        df["_dispute_score"] = 0.0
        df["_population_score"] = 0.0
        df["_land_use_score"] = 0.0
        df["_anomaly_score"] = 0.0
        df["_is_anomaly"] = False

        # ====================================================
        # 1. DISPUTE PRESSURE
        # ====================================================

        if (
            dispute_column
            and dispute_column in df.columns
        ):

            disputes = pd.to_numeric(
                df[dispute_column],
                errors="coerce",
            ).fillna(0)

            max_disputes = float(
                disputes.max()
            )

            if max_disputes > 0:

                df["_dispute_score"] = (
                    disputes / max_disputes
                ) * 100

        # ====================================================
        # 2. POPULATION PRESSURE
        # ====================================================

        if (
            population_column
            and population_column in df.columns
        ):

            population = pd.to_numeric(
                df[population_column],
                errors="coerce",
            ).fillna(0)

            min_population = float(
                population.min()
            )

            max_population = float(
                population.max()
            )

            population_range = (
                max_population
                - min_population
            )

            if population_range > 0:

                df["_population_score"] = (
                    (
                        population
                        - min_population
                    )
                    / population_range
                ) * 100

            else:

                df["_population_score"] = 0.0

        # ====================================================
        # 3. LAND-USE PRESSURE
        # ====================================================

        if (
            land_use_column
            and land_use_column in df.columns
        ):

            land_use = (
                df[land_use_column]
                .fillna("Unknown")
                .astype(str)
                .str.strip()
                .str.lower()
            )

            # Pilot classification values.
            # These are demonstration values and are not
            # universal land-governance rules.

            land_use_scores = {

                "agricultural": 35,

                "forest": 15,

                "residential": 75,

                "industrial": 100,

                "commercial": 90,

                "mixed": 70,

                "urban": 85,

                "institutional": 70,

                "infrastructure": 80,

                "unknown": 30,
            }

            df["_land_use_score"] = (
                land_use.map(
                    lambda value:
                    land_use_scores.get(
                        value,
                        50,
                    )
                )
            )

        # ====================================================
        # 4. ANOMALY DETECTION
        # ====================================================

        numeric_features = []

        for field in [
            dispute_column,
            population_column,
        ]:

            if (
                field
                and field in df.columns
            ):

                numeric_features.append(
                    field
                )

        if numeric_features:

            feature_dataframe = (
                df[numeric_features]
                .apply(
                    pd.to_numeric,
                    errors="coerce",
                )
                .fillna(0)
            )

            # Isolation Forest requires enough observations
            # to produce a useful anomaly signal.

            if len(feature_dataframe) >= 5:

                contamination = min(
                    0.10,
                    max(
                        1 / len(
                            feature_dataframe
                        ),
                        0.01,
                    ),
                )

                model = IsolationForest(
                    contamination=contamination,
                    random_state=42,
                )

                predictions = (
                    model.fit_predict(
                        feature_dataframe
                    )
                )

                anomaly_scores = (
                    model.decision_function(
                        feature_dataframe
                    )
                )

                min_score = float(
                    anomaly_scores.min()
                )

                max_score = float(
                    anomaly_scores.max()
                )

                score_range = (
                    max_score
                    - min_score
                )

                if score_range > 0:

                    normalized = (
                        (
                            max_score
                            - anomaly_scores
                        )
                        / score_range
                    ) * 100

                else:

                    normalized = pd.Series(
                        0.0,
                        index=df.index,
                    )

                df["_anomaly_score"] = (
                    normalized
                )

                df["_is_anomaly"] = (
                    predictions == -1
                )

        # ====================================================
        # 5. COMPOSITE RISK SCORE
        # ====================================================

        df["_risk_score"] = (

            df["_dispute_score"]
            * self.DISPUTE_WEIGHT

            +

            df["_population_score"]
            * self.POPULATION_WEIGHT

            +

            df["_land_use_score"]
            * self.LAND_USE_WEIGHT

            +

            df["_anomaly_score"]
            * self.ANOMALY_WEIGHT
        )

        df["_risk_score"] = (
            df["_risk_score"]
            .clip(0, 100)
            .round(2)
        )

        # ====================================================
        # 6. RISK LEVEL
        # ====================================================

        df["_risk_level"] = (
            df["_risk_score"]
            .apply(
                self._risk_level
            )
        )

        # ====================================================
        # 7. BUILD PARCEL RECORDS
        # ====================================================

        risk_records: List[
            Dict[str, Any]
        ] = []

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

        for index, row in df.iterrows():

            explanation = (
                self._build_explanation(
                    row
                )
            )

            # ------------------------------------------------
            # PARCEL ID
            # ------------------------------------------------

            if (
                parcel_column
                and parcel_column in df.columns
            ):

                parcel_id = str(
                    row[parcel_column]
                )

            else:

                parcel_id = (
                    f"Record-{index + 1}"
                )

            # ------------------------------------------------
            # RISK RECORD
            # ------------------------------------------------

            record: Dict[str, Any] = {

                "parcel_id":
                    parcel_id,

                "risk_score":
                    float(
                        row["_risk_score"]
                    ),

                "risk_level":
                    row["_risk_level"],

                "components": {

                    "dispute_pressure":
                        round(
                            float(
                                row[
                                    "_dispute_score"
                                ]
                            ),
                            2,
                        ),

                    "population_pressure":
                        round(
                            float(
                                row[
                                    "_population_score"
                                ]
                            ),
                            2,
                        ),

                    "land_use_pressure":
                        round(
                            float(
                                row[
                                    "_land_use_score"
                                ]
                            ),
                            2,
                        ),

                    "anomaly_pressure":
                        round(
                            float(
                                row[
                                    "_anomaly_score"
                                ]
                            ),
                            2,
                        ),
                },

                "anomaly_detected":
                    bool(
                        row[
                            "_is_anomaly"
                        ]
                    ),

                "why":
                    explanation,
            }

            # ------------------------------------------------
            # LOCATION
            # ------------------------------------------------

            if (
                latitude_column
                and longitude_column
                and latitude_column in df.columns
                and longitude_column in df.columns
            ):

                latitude = pd.to_numeric(
                    row[latitude_column],
                    errors="coerce",
                )

                longitude = pd.to_numeric(
                    row[longitude_column],
                    errors="coerce",
                )

                if (
                    pd.notna(latitude)
                    and pd.notna(longitude)
                ):

                    record["location"] = {

                        "latitude":
                            float(latitude),

                        "longitude":
                            float(longitude),
                    }

            risk_records.append(
                record
            )

        # ====================================================
        # 8. SORT BY RISK
        # ====================================================

        risk_records.sort(
            key=lambda item:
                item["risk_score"],
            reverse=True,
        )

        # ====================================================
        # 9. RISK DISTRIBUTION
        # ====================================================

        risk_distribution = {

            "low": 0,

            "moderate": 0,

            "high": 0,

            "critical": 0,
        }

        for record in risk_records:

            level = (
                record[
                    "risk_level"
                ]
                .lower()
            )

            if level in risk_distribution:

                risk_distribution[
                    level
                ] += 1

        # ====================================================
        # 10. HIGH / CRITICAL COUNT
        # ====================================================

        high_risk_count = (

            risk_distribution[
                "high"
            ]

            +

            risk_distribution[
                "critical"
            ]
        )

        # ====================================================
        # 11. ANOMALY COUNT
        # ====================================================

        anomaly_count = sum(

            1

            for record
            in risk_records

            if record[
                "anomaly_detected"
            ]
        )

        # ====================================================
        # 12. AVERAGE RISK
        # ====================================================

        if risk_records:

            average_risk = (

                sum(
                    record[
                        "risk_score"
                    ]

                    for record
                    in risk_records
                )

                /

                len(
                    risk_records
                )
            )

        else:

            average_risk = 0.0

        # ====================================================
        # 13. FINAL RESPONSE
        # ====================================================

        return {

            "model": {

                "type":
                    "Explainable composite "
                    "land-risk index",

                "status":
                    "pilot",

                "statistical_probability":
                    False,

                "weights": {

                    "dispute_pressure":
                        self.DISPUTE_WEIGHT,

                    "population_pressure":
                        self.POPULATION_WEIGHT,

                    "land_use_pressure":
                        self.LAND_USE_WEIGHT,

                    "anomaly_pressure":
                        self.ANOMALY_WEIGHT,
                },
            },

            "summary": {

                "records_analyzed":
                    len(
                        risk_records
                    ),

                "average_risk_score":
                    round(
                        average_risk,
                        2,
                    ),

                "high_or_critical_records":
                    high_risk_count,

                "anomalies_detected":
                    anomaly_count,

                "risk_distribution":
                    risk_distribution,
            },

            # Main format
            "records":
                risk_records,

            # Compatibility format
            "parcel_risks":
                risk_records,
        }

    # ========================================================
    # RISK LEVEL
    # ========================================================

    @staticmethod
    def _risk_level(
        score: float,
    ) -> str:

        if score >= 80:
            return "Critical"

        if score >= 60:
            return "High"

        if score >= 30:
            return "Moderate"

        return "Low"

    # ========================================================
    # EXPLANATION
    # ========================================================

    @staticmethod
    def _build_explanation(
        row: pd.Series,
    ) -> List[str]:

        explanations: List[
            str
        ] = []

        dispute_score = float(
            row[
                "_dispute_score"
            ]
        )

        population_score = float(
            row[
                "_population_score"
            ]
        )

        land_use_score = float(
            row[
                "_land_use_score"
            ]
        )

        anomaly_score = float(
            row[
                "_anomaly_score"
            ]
        )

        # ----------------------------------------------------
        # DISPUTE
        # ----------------------------------------------------

        if dispute_score >= 70:

            explanations.append(
                "High observed dispute pressure."
            )

        elif dispute_score >= 40:

            explanations.append(
                "Moderate observed dispute pressure."
            )

        elif dispute_score > 0:

            explanations.append(
                "Some historical dispute activity is present."
            )

        # ----------------------------------------------------
        # POPULATION
        # ----------------------------------------------------

        if population_score >= 70:

            explanations.append(
                "High population pressure relative "
                "to the uploaded dataset."
            )

        elif population_score >= 40:

            explanations.append(
                "Moderate population pressure relative "
                "to the uploaded dataset."
            )

        # ----------------------------------------------------
        # LAND USE
        # ----------------------------------------------------

        if land_use_score >= 80:

            explanations.append(
                "Land-use category indicates relatively "
                "high development pressure in this pilot model."
            )

        elif land_use_score >= 50:

            explanations.append(
                "Land-use category indicates moderate "
                "development pressure in this pilot model."
            )

        # ----------------------------------------------------
        # ANOMALY
        # ----------------------------------------------------

        if anomaly_score >= 70:

            explanations.append(
                "Unusual data pattern detected by "
                "the anomaly model."
            )

        elif anomaly_score >= 40:

            explanations.append(
                "Somewhat unusual data pattern detected."
            )

        # ----------------------------------------------------
        # DEFAULT
        # ----------------------------------------------------

        if not explanations:

            explanations.append(
                "No major risk indicators were detected "
                "by the current pilot model."
            )

        return explanations