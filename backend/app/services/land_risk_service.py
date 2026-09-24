from pathlib import Path
from typing import Any, Dict, List

import sys

import numpy as np
import pandas as pd

from sklearn.ensemble import IsolationForest


# ============================================================
# PROJECT PATH
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[3]

MODEL_PATH = (
    PROJECT_ROOT
    / "ai"
    / "training"
    / "models"
    / "land_conflict_random_forest.joblib"
)


# ============================================================
# OPTIONAL ML IMPORT
# ============================================================

try:

    import joblib

except ImportError:

    joblib = None


# ============================================================
# LAND RISK SERVICE
# ============================================================

class LandRiskService:

    """
    Explainable integrated land-risk engine.

    Current components:

        Composite Risk Index
        + Anomaly Detection
        + Optional ML Conflict Prediction
        + Land-use Change information

    The supervised ML component is optional.

    If a valid trained ML model does not exist,
    the existing composite-risk engine continues
    operating normally.
    """


    # --------------------------------------------------------
    # Existing composite-risk weights
    # --------------------------------------------------------

    DISPUTE_WEIGHT = 0.35

    POPULATION_WEIGHT = 0.20

    LAND_USE_WEIGHT = 0.20

    ANOMALY_WEIGHT = 0.25


    # --------------------------------------------------------
    # ML integration weight
    # --------------------------------------------------------

    ML_WEIGHT = 0.30

    EXISTING_WEIGHT = 0.70


    # --------------------------------------------------------
    # Constructor
    # --------------------------------------------------------

    def __init__(self):

        self.ml_model = None

        self.ml_available = False

        self._load_ml_model()


    # ========================================================
    # FILE ANALYSIS
    # ========================================================

    def analyze_file(
        self,
        file_path: str,
        detected_fields: Dict[str, str],
    ) -> Dict[str, Any]:
        """
        Analyze a CSV/Excel land dataset and return parcel-level
        risk records in the format expected by the integrated
        land-risk and GIS hotspot services.
        """

        path = Path(file_path)

        if not path.exists():
            raise ValueError(
                f"File does not exist: {file_path}"
            )

        extension = path.suffix.lower()

        if extension == ".csv":
            dataframe = pd.read_csv(path)

        elif extension in {".xlsx", ".xls"}:
            dataframe = pd.read_excel(path)

        else:
            raise ValueError(
                "Land risk analysis currently supports "
                "CSV and Excel files."
            )

        if dataframe.empty:
            raise ValueError(
                "The uploaded dataset contains no records."
            )

        records = []

        for _, row in dataframe.iterrows():

            record: Dict[str, Any] = {}

            # Map detected source columns into the canonical
            # names used by the risk engine.
            for canonical_name in [
                "parcel_id",
                "survey_number",
                "land_use",
                "dispute_count",
                "population",
                "population_growth",
                "latitude",
                "longitude",
                "area",
                "flood_risk",
                "forest_cover",
            ]:
                source_column = detected_fields.get(
                    canonical_name
                )

                if (
                    source_column
                    and source_column in dataframe.columns
                ):
                    value = row[source_column]

                    if pd.isna(value):
                        value = None

                    record[canonical_name] = value

            # Keep additional numeric columns available for a
            # future trained ML model if its feature names match.
            for column in dataframe.columns:

                if column in record:
                    continue

                value = row[column]

                if pd.isna(value):
                    continue

                if isinstance(
                    value,
                    (int, float, np.integer, np.floating),
                ):
                    record[column] = float(value)

            records.append(record)

        parcel_risks = self.calculate_risks(
            records
        )

        risk_distribution = {
            "low": 0,
            "moderate": 0,
            "high": 0,
            "critical": 0,
        }

        anomaly_count = 0

        for risk in parcel_risks:

            level = str(
                risk.get(
                    "risk_level",
                    "Low",
                )
            ).lower()

            if level in risk_distribution:
                risk_distribution[level] += 1

            if risk.get(
                "anomaly_detected",
                False,
            ):
                anomaly_count += 1

        average_risk = (
            sum(
                float(
                    risk.get(
                        "risk_score",
                        0,
                    )
                    or 0
                )
                for risk in parcel_risks
            )
            / len(parcel_risks)
            if parcel_risks
            else 0.0
        )

        return {
            "model": {
                "type": (
                    "Integrated explainable "
                    "land-risk index"
                ),
                "status": "pilot",
                "statistical_probability": False,
                "ml_model_available": (
                    self.ml_available
                ),
            },

            "summary": {
                "records_analyzed": len(
                    parcel_risks
                ),
                "average_risk_score": round(
                    average_risk,
                    2,
                ),
                "anomalies_detected": (
                    anomaly_count
                ),
                "risk_distribution": (
                    risk_distribution
                ),
            },

            "records": parcel_risks,

            # This is the key compatibility field used by
            # IntegratedLandRiskService and the GIS hotspot route.
            "parcel_risks": parcel_risks,
        }

    # ========================================================
    # ML MODEL LOADING
    # ========================================================

    def _load_ml_model(self):

        """
        Load the trained Random Forest model if available.

        Failure to load the model does NOT break the
        land-risk engine.
        """

        self.ml_model = None

        self.ml_available = False


        if joblib is None:

            return


        if not MODEL_PATH.exists():

            return


        try:

            self.ml_model = joblib.load(
                MODEL_PATH
            )

            self.ml_available = True

        except Exception:

            self.ml_model = None

            self.ml_available = False


    # ========================================================
    # NORMALIZATION
    # ========================================================

    @staticmethod
    def _normalize(
        value: float,
        minimum: float,
        maximum: float
    ) -> float:

        if maximum <= minimum:

            return 0.0


        normalized = (
            (value - minimum)
            /
            (maximum - minimum)
        )


        return float(
            max(
                0.0,
                min(
                    1.0,
                    normalized
                )
            )
        )


    # ========================================================
    # LAND-USE PRESSURE
    # ========================================================

    @staticmethod
    def _land_use_score(
        land_use: str
    ) -> float:

        if not land_use:

            return 30.0


        value = (
            str(land_use)
            .strip()
            .lower()
        )


        scores = {

            "agricultural": 35.0,

            "forest": 15.0,

            "residential": 75.0,

            "industrial": 100.0,

            "commercial": 90.0,

            "mixed": 70.0,

            "urban": 85.0,

            "institutional": 70.0,

            "infrastructure": 80.0,

        }


        return scores.get(
            value,
            30.0
        )


    # ========================================================
    # ANOMALY DETECTION
    # ========================================================

    def _detect_anomalies(
        self,
        records: List[Dict[str, Any]]
    ) -> Dict[str, Any]:

        if len(records) < 5:

            return {
                "available": False,
                "anomaly_count": 0,
                "scores": [0.0] * len(records)
            }


        values = []

        for record in records:

            values.append(
                [
                    float(
                        record.get(
                            "dispute_count",
                            0
                        )
                        or 0
                    ),

                    float(
                        record.get(
                            "population",
                            0
                        )
                        or 0
                    )
                ]
            )


        matrix = np.asarray(
            values,
            dtype=float
        )


        model = IsolationForest(
            contamination=0.1,
            random_state=42
        )


        predictions = model.fit_predict(
            matrix
        )


        anomaly_scores = model.decision_function(
            matrix
        )


        anomaly_flags = (
            predictions == -1
        )


        return {
            "available": True,
            "anomaly_count": int(
                anomaly_flags.sum()
            ),
            "scores": anomaly_scores.tolist(),
            "flags": anomaly_flags.tolist()
        }


    # ========================================================
    # ML FEATURE BUILDER
    # ========================================================

    def _build_ml_features(
        self,
        record: Dict[str, Any]
    ) -> pd.DataFrame:

        """
        Convert a parcel record into the feature structure
        expected by the trained model.

        The exact columns are aligned with the training
        feature names when the model exposes them.
        """

        if not self.ml_available:

            return pd.DataFrame()


        if not hasattr(
            self.ml_model,
            "feature_names_in_"
        ):

            return pd.DataFrame()


        feature_names = list(
            self.ml_model.feature_names_in_
        )


        row = {}


        for feature in feature_names:

            value = record.get(
                feature,
                0
            )


            if value is None:

                value = 0


            try:

                value = float(
                    value
                )

            except (
                ValueError,
                TypeError
            ):

                value = 0.0


            row[feature] = value


        return pd.DataFrame(
            [row],
            columns=feature_names
        )


    # ========================================================
    # ML PREDICTION
    # ========================================================

    def _predict_ml(
        self,
        record: Dict[str, Any]
    ) -> Dict[str, Any]:

        if not self.ml_available:

            return {
                "available": False,
                "prediction": None,
                "probability": None,
                "status": "model_not_available"
            }


        try:

            X = self._build_ml_features(
                record
            )


            if X.empty:

                return {
                    "available": False,
                    "prediction": None,
                    "probability": None,
                    "status": "feature_mapping_unavailable"
                }


            prediction = self.ml_model.predict(
                X
            )[0]


            probability = (
                self.ml_model
                .predict_proba(X)[0][1]
            )


            return {
                "available": True,
                "prediction": int(
                    prediction
                ),
                "probability": round(
                    float(
                        probability
                    ),
                    4
                ),
                "status": "active"
            }


        except Exception as exc:

            return {
                "available": False,
                "prediction": None,
                "probability": None,
                "status": "prediction_error",
                "error": str(exc)
            }


    # ========================================================
    # SINGLE RECORD RISK
    # ========================================================

    def calculate_risk(
        self,
        record: Dict[str, Any],
        all_records: List[Dict[str, Any]] | None = None
    ) -> Dict[str, Any]:

        if all_records is None:

            all_records = [record]


        # ----------------------------------------------------
        # Dispute pressure
        # ----------------------------------------------------

        dispute_count = float(
            record.get(
                "dispute_count",
                0
            )
            or 0
        )


        maximum_disputes = max(
            [
                float(
                    item.get(
                        "dispute_count",
                        0
                    )
                    or 0
                )
                for item in all_records
            ],
            default=0.0
        )


        dispute_pressure = (
            self._normalize(
                dispute_count,
                0.0,
                maximum_disputes
            )
            * 100.0
            if maximum_disputes > 0
            else 0.0
        )


        # ----------------------------------------------------
        # Population pressure
        # ----------------------------------------------------

        population = float(
            record.get(
                "population",
                0
            )
            or 0
        )


        populations = [
            float(
                item.get(
                    "population",
                    0
                )
                or 0
            )
            for item in all_records
        ]


        max_population = max(
            populations,
            default=0.0
        )


        population_pressure = (
            self._normalize(
                population,
                0.0,
                max_population
            )
            * 100.0
            if max_population > 0
            else 0.0
        )


        # ----------------------------------------------------
        # Land-use pressure
        # ----------------------------------------------------

        land_use = record.get(
            "land_use"
        )


        land_use_pressure = (
            self._land_use_score(
                land_use
            )
        )


        # ----------------------------------------------------
        # Anomaly pressure
        # ----------------------------------------------------

        anomaly_result = (
            self._detect_anomalies(
                all_records
            )
        )


        anomaly_pressure = 0.0

        anomaly_detected = False


        if anomaly_result["available"]:

            record_index = all_records.index(
                record
            )

            flags = anomaly_result.get(
                "flags",
                []
            )

            if (
                record_index
                <
                len(flags)
            ):

                anomaly_detected = bool(
                    flags[
                        record_index
                    ]
                )


            if anomaly_detected:

                anomaly_pressure = 100.0


        # ----------------------------------------------------
        # Existing composite score
        # ----------------------------------------------------

        composite_score = (

            self.DISPUTE_WEIGHT
            * dispute_pressure

            +

            self.POPULATION_WEIGHT
            * population_pressure

            +

            self.LAND_USE_WEIGHT
            * land_use_pressure

            +

            self.ANOMALY_WEIGHT
            * anomaly_pressure
        )


        composite_score = round(
            float(
                max(
                    0.0,
                    min(
                        100.0,
                        composite_score
                    )
                )
            ),
            2
        )


        # ----------------------------------------------------
        # ML prediction
        # ----------------------------------------------------

        ml_result = self._predict_ml(
            record
        )


        # ----------------------------------------------------
        # Final integrated score
        # ----------------------------------------------------

        if (
            ml_result["available"]
            and
            ml_result["probability"]
            is not None
        ):

            ml_score = (
                float(
                    ml_result[
                        "probability"
                    ]
                )
                * 100.0
            )


            final_score = (
                self.EXISTING_WEIGHT
                * composite_score
                +
                self.ML_WEIGHT
                * ml_score
            )


            scoring_mode = (
                "Integrated composite + ML"
            )

        else:

            final_score = (
                composite_score
            )

            ml_score = None

            scoring_mode = (
                "Composite risk only"
            )


        final_score = round(
            float(
                max(
                    0.0,
                    min(
                        100.0,
                        final_score
                    )
                )
            ),
            2
        )


        # ----------------------------------------------------
        # Risk level
        # ----------------------------------------------------

        if final_score >= 80:

            risk_level = "Critical"

        elif final_score >= 60:

            risk_level = "High"

        elif final_score >= 30:

            risk_level = "Moderate"

        else:

            risk_level = "Low"


        # ----------------------------------------------------
        # Explanation
        # ----------------------------------------------------

        why = []


        if dispute_pressure >= 60:

            why.append(
                "High dispute pressure"
            )


        if population_pressure >= 60:

            why.append(
                "High population pressure"
            )


        if land_use_pressure >= 75:

            why.append(
                "High land-use pressure"
            )


        if anomaly_detected:

            why.append(
                "Anomalous dispute/population pattern"
            )


        if (
            ml_result["available"]
            and
            ml_result["probability"]
            >= 0.60
        ):

            why.append(
                "ML model indicates elevated "
                "next-period conflict risk"
            )


        if not why:

            why.append(
                "No dominant high-risk indicator detected"
            )


        # ----------------------------------------------------
        # Result
        # ----------------------------------------------------

        return {

            "parcel_id":
                record.get(
                    "parcel_id"
                ),

            "risk_score":
                final_score,

            "risk_level":
                risk_level,

            "scoring_mode":
                scoring_mode,

            "components": {

                "dispute_pressure":
                    round(
                        dispute_pressure,
                        2
                    ),

                "population_pressure":
                    round(
                        population_pressure,
                        2
                    ),

                "land_use_pressure":
                    round(
                        land_use_pressure,
                        2
                    ),

                "anomaly_pressure":
                    round(
                        anomaly_pressure,
                        2
                    ),

                "composite_score":
                    composite_score,

                "ml_probability":
                    ml_result[
                        "probability"
                    ],

                "ml_score":
                    ml_score
            },

            "ml_prediction":
                ml_result,

            "anomaly_detected":
                anomaly_detected,

            "why":
                why,

            "metadata": {

                "type":
                    "Integrated explainable "
                    "land-risk index",

                "ml_model_available":
                    self.ml_available,

                "ml_model_path":
                    str(
                        MODEL_PATH
                    ),

                "statistical_probability":
                    False
            }
        }


    # ========================================================
    # MULTIPLE RECORDS
    # ========================================================

    def calculate_risks(
        self,
        records: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:

        results = []


        for record in records:

            results.append(
                self.calculate_risk(
                    record,
                    records
                )
            )


        return results


# ============================================================
# SERVICE INSTANCE
# ============================================================

land_risk_service = (
    LandRiskService()
)