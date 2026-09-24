import json
import joblib
import pandas as pd

from pathlib import Path

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline

from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    classification_report,
)


# ============================================================
# PATHS
# ============================================================

ROOT = Path(__file__).resolve().parents[3]

DATASET = (
    ROOT
    / "ai"
    / "training"
    / "processed"
    / "training_dataset.csv"
)

MODEL_DIR = (
    ROOT
    / "ai"
    / "training"
    / "models"
)

MODEL_DIR.mkdir(
    parents=True,
    exist_ok=True
)

RF_MODEL_PATH = (
    MODEL_DIR
    / "land_conflict_random_forest.joblib"
)

LR_MODEL_PATH = (
    MODEL_DIR
    / "land_conflict_logistic_regression.joblib"
)

METRICS_PATH = (
    MODEL_DIR
    / "model_metrics.json"
)


# ============================================================
# CONFIGURATION
# ============================================================

MIN_TOTAL_SAMPLES = 30
MIN_SAMPLES_PER_CLASS = 10


# ============================================================
# HEADER
# ============================================================

print("=" * 90)
print("LAND CONFLICT ML TRAINING PIPELINE")
print("=" * 90)


# ============================================================
# LOAD DATA
# ============================================================

if not DATASET.exists():

    raise FileNotFoundError(
        f"Training dataset not found:\n{DATASET}"
    )


df = pd.read_csv(DATASET)


print()
print("Dataset:")
print(DATASET)

print()
print(
    f"Total rows: {len(df)}"
)


# ============================================================
# FILTER TO LABELLED DATA
# ============================================================

if "target_available" not in df.columns:

    raise ValueError(
        "Column 'target_available' is missing."
    )


labelled = df[
    df["target_available"] == True
].copy()


print(
    f"Labelled rows: {len(labelled)}"
)


if len(labelled) == 0:

    print()
    print("=" * 90)
    print("MODEL TRAINING BLOCKED")
    print("=" * 90)

    print()
    print("Reason: no labelled observations.")

    raise SystemExit(0)


# ============================================================
# TARGET
# ============================================================

TARGET = "conflict_next_period"


if TARGET not in labelled.columns:

    raise ValueError(
        f"Target column '{TARGET}' not found."
    )


labelled = labelled.dropna(
    subset=[TARGET]
)


labelled[TARGET] = (
    labelled[TARGET]
    .astype(int)
)


class_counts = (
    labelled[TARGET]
    .value_counts()
    .sort_index()
)


print()
print("Target distribution:")

print(
    class_counts.to_string()
)


# ============================================================
# MINIMUM DATA SAFETY CHECK
# ============================================================

if len(labelled) < MIN_TOTAL_SAMPLES:

    print()
    print("=" * 90)
    print("MODEL TRAINING BLOCKED")
    print("=" * 90)

    print()
    print(
        f"Required minimum labelled samples: "
        f"{MIN_TOTAL_SAMPLES}"
    )

    print(
        f"Available labelled samples: "
        f"{len(labelled)}"
    )

    print()
    print(
        "Add more source-attributed conflict records "
        "before training."
    )

    raise SystemExit(0)


for class_value in [0, 1]:

    count = int(
        class_counts.get(
            class_value,
            0
        )
    )

    if count < MIN_SAMPLES_PER_CLASS:

        print()
        print("=" * 90)
        print("MODEL TRAINING BLOCKED")
        print("=" * 90)

        print()
        print(
            f"Class {class_value} has only "
            f"{count} samples."
        )

        print(
            f"Minimum required per class: "
            f"{MIN_SAMPLES_PER_CLASS}"
        )

        raise SystemExit(0)


# ============================================================
# FEATURES
# ============================================================

EXCLUDED_COLUMNS = {
    TARGET,
    "target_available",
    "conflict_observed",
    "conflict_count",
    "people_affected",
    "conflict_land_area_ha",
    "state",
}


candidate_features = [
    column
    for column in labelled.columns
    if column not in EXCLUDED_COLUMNS
]


# Keep only numeric ML features.
feature_columns = [
    column
    for column in candidate_features
    if pd.api.types.is_numeric_dtype(
        labelled[column]
    )
]


if len(feature_columns) == 0:

    raise ValueError(
        "No numeric ML features found."
    )


X = labelled[
    feature_columns
]

y = labelled[
    TARGET
]


print()
print(
    f"Features: {len(feature_columns)}"
)

print()

for feature in feature_columns:

    print(
        f"  - {feature}"
    )


# ============================================================
# PREPROCESSING
# ============================================================

preprocessor = ColumnTransformer(
    transformers=[
        (
            "numeric",
            Pipeline(
                steps=[
                    (
                        "imputer",
                        SimpleImputer(
                            strategy="median"
                        )
                    ),
                    (
                        "scaler",
                        StandardScaler()
                    )
                ]
            ),
            feature_columns
        )
    ],
    remainder="drop"
)


# ============================================================
# MODELS
# ============================================================

logistic_model = Pipeline(
    steps=[
        (
            "preprocessor",
            preprocessor
        ),
        (
            "classifier",
            LogisticRegression(
                max_iter=2000,
                class_weight="balanced",
                random_state=42
            )
        )
    ]
)


random_forest_model = Pipeline(
    steps=[
        (
            "preprocessor",
            preprocessor
        ),
        (
            "classifier",
            RandomForestClassifier(
                n_estimators=300,
                max_depth=8,
                min_samples_leaf=2,
                class_weight="balanced",
                random_state=42
            )
        )
    ]
)


# ============================================================
# IMPORTANT:
# We do NOT perform a random train/test split here.
#
# The current dataset is a small temporal panel.
# Once enough observations exist, we should use a temporal
# holdout rather than random shuffling.
# ============================================================


# ============================================================
# TEMPORAL TRAIN/TEST SPLIT
# ============================================================

if "year" not in labelled.columns:

    raise ValueError(
        "Year column required for temporal validation."
    )


labelled = labelled.sort_values(
    "year"
).reset_index(
    drop=True
)


split_index = int(
    len(labelled) * 0.8
)


if split_index <= 0 or split_index >= len(labelled):

    raise ValueError(
        "Unable to create temporal train/test split."
    )


train_df = labelled.iloc[
    :split_index
].copy()

test_df = labelled.iloc[
    split_index:
].copy()


X_train = train_df[
    feature_columns
]

y_train = train_df[
    TARGET
]

X_test = test_df[
    feature_columns
]

y_test = test_df[
    TARGET
]


print()
print(
    f"Training rows: {len(train_df)}"
)

print(
    f"Testing rows: {len(test_df)}"
)


# ============================================================
# CHECK TRAINING CLASS COVERAGE
# ============================================================

if y_train.nunique() < 2:

    print()
    print(
        "MODEL TRAINING BLOCKED"
    )

    print(
        "Temporal training split contains "
        "only one target class."
    )

    print(
        "More historical conflict observations "
        "are required."
    )

    raise SystemExit(0)


# ============================================================
# TRAIN
# ============================================================

print()
print("=" * 90)
print("TRAINING LOGISTIC REGRESSION")
print("=" * 90)

logistic_model.fit(
    X_train,
    y_train
)


print()
print("=" * 90)
print("TRAINING RANDOM FOREST")
print("=" * 90)

random_forest_model.fit(
    X_train,
    y_train
)


# ============================================================
# EVALUATION FUNCTION
# ============================================================

def evaluate_model(
    name,
    model
):

    predictions = model.predict(
        X_test
    )

    probabilities = model.predict_proba(
        X_test
    )[:, 1]

    metrics = {
        "accuracy": float(
            accuracy_score(
                y_test,
                predictions
            )
        ),
        "precision": float(
            precision_score(
                y_test,
                predictions,
                zero_division=0
            )
        ),
        "recall": float(
            recall_score(
                y_test,
                predictions,
                zero_division=0
            )
        ),
        "f1": float(
            f1_score(
                y_test,
                predictions,
                zero_division=0
            )
        )
    }


    if y_test.nunique() == 2:

        metrics["roc_auc"] = float(
            roc_auc_score(
                y_test,
                probabilities
            )
        )

    else:

        metrics["roc_auc"] = None


    print()
    print(
        f"===== {name} ====="
    )

    for key, value in metrics.items():

        print(
            f"{key}: {value}"
        )


    print()

    print(
        classification_report(
            y_test,
            predictions,
            zero_division=0
        )
    )


    return metrics


# ============================================================
# EVALUATE
# ============================================================

logistic_metrics = evaluate_model(
    "LOGISTIC REGRESSION",
    logistic_model
)


random_forest_metrics = evaluate_model(
    "RANDOM FOREST",
    random_forest_model
)


# ============================================================
# SAVE MODELS
# ============================================================

joblib.dump(
    logistic_model,
    LR_MODEL_PATH
)

joblib.dump(
    random_forest_model,
    RF_MODEL_PATH
)


# ============================================================
# SAVE METADATA
# ============================================================

metadata = {

    "project":
        "National Digital Platform for Research, Policy Innovation & Evidence-Based Land Governance",

    "task":
        "Next-period land-conflict prediction",

    "target":
        TARGET,

    "feature_columns":
        feature_columns,

    "training_rows":
        len(train_df),

    "testing_rows":
        len(test_df),

    "class_distribution":
        {
            str(k): int(v)
            for k, v in class_counts.items()
        },

    "models":
        {
            "logistic_regression":
                logistic_metrics,

            "random_forest":
                random_forest_metrics
        },

    "validation":
        "Temporal holdout",

    "random_state":
        42
}


with open(
    METRICS_PATH,
    "w",
    encoding="utf-8"
) as file:

    json.dump(
        metadata,
        file,
        indent=2
    )


# ============================================================
# COMPLETE
# ============================================================

print()
print("=" * 90)
print("ML TRAINING COMPLETE")
print("=" * 90)

print()
print(
    f"Logistic model:\n{LR_MODEL_PATH}"
)

print()
print(
    f"Random Forest model:\n{RF_MODEL_PATH}"
)

print()
print(
    f"Metrics:\n{METRICS_PATH}"
)