import joblib
import pandas as pd

from pathlib import Path


# ============================================================
# PATHS
# ============================================================

ROOT = Path(__file__).resolve().parents[3]

MODEL_PATH = (
    ROOT
    / "ai"
    / "training"
    / "models"
    / "land_conflict_random_forest.joblib"
)


# ============================================================
# PREDICTION FUNCTION
# ============================================================

def predict_conflict_risk(
    feature_data
):

    # --------------------------------------------------------
    # Check model
    # --------------------------------------------------------

    if not MODEL_PATH.exists():

        return {
            "success": False,
            "model_available": False,
            "prediction_available": False,
            "message": (
                "No trained land-conflict ML model is "
                "available yet. More real conflict labels "
                "are required before training."
            )
        }


    # --------------------------------------------------------
    # Convert input
    # --------------------------------------------------------

    if isinstance(
        feature_data,
        dict
    ):

        feature_data = [
            feature_data
        ]


    X = pd.DataFrame(
        feature_data
    )


    # --------------------------------------------------------
    # Load model
    # --------------------------------------------------------

    model = joblib.load(
        MODEL_PATH
    )


    # --------------------------------------------------------
    # Predict
    # --------------------------------------------------------

    prediction = model.predict(
        X
    )


    probability = model.predict_proba(
        X
    )[:, 1]


    results = []


    for pred, prob in zip(
        prediction,
        probability
    ):

        if prob >= 0.80:

            level = "Critical"

        elif prob >= 0.60:

            level = "High"

        elif prob >= 0.30:

            level = "Moderate"

        else:

            level = "Low"


        results.append(
            {
                "conflict_prediction": int(pred),

                "conflict_probability": round(
                    float(prob),
                    4
                ),

                "risk_level": level
            }
        )


    return {
        "success": True,
        "model_available": True,
        "prediction_available": True,
        "model": "Random Forest",
        "predictions": results
    }


# ============================================================
# TEST ENTRY POINT
# ============================================================

if __name__ == "__main__":

    print("=" * 80)
    print("LAND CONFLICT PREDICTION SERVICE")
    print("=" * 80)


    if not MODEL_PATH.exists():

        print()
        print(
            "MODEL STATUS: NOT AVAILABLE"
        )

        print()
        print(
            "Reason:"
        )

        print(
            "The training dataset currently contains "
            "only 5 labelled observations."
        )

        print()
        print(
            "The prediction service is ready, but it "
            "will activate automatically after a valid "
            "model is trained."
        )

    else:

        print()
        print(
            "MODEL STATUS: AVAILABLE"
        )