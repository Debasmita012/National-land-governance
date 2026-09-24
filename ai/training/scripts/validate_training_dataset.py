from pathlib import Path
import json
import sys

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[3]

DATASET_PATH = (
    PROJECT_ROOT
    / "ai"
    / "training"
    / "data"
    / "training_dataset.csv"
)

SCHEMA_PATH = (
    PROJECT_ROOT
    / "ai"
    / "training"
    / "data"
    / "training_schema.json"
)


def load_schema():
    if not SCHEMA_PATH.exists():
        raise FileNotFoundError(
            f"Training schema not found:\n{SCHEMA_PATH}"
        )

    with open(SCHEMA_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def validate_required_columns(df, schema):
    required_columns = [
        feature["name"]
        for feature in schema["features"]
        if feature.get("required", False)
    ]

    required_columns.append(schema["target"]["name"])

    missing = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing:
        raise ValueError(
            "Missing required columns:\n"
            + "\n".join(f"- {column}" for column in missing)
        )


def validate_target(df, target_name):
    if target_name not in df.columns:
        raise ValueError(
            f"Target column '{target_name}' is missing."
        )

    if df.empty:
        print(
            "\nWARNING: Training dataset currently contains no records."
        )
        print(
            "This is expected until legitimate conflict labels "
            "are added."
        )
        return

    values = set(df[target_name].dropna().unique())

    invalid = values - {0, 1}

    if invalid:
        raise ValueError(
            f"Invalid target values found: {invalid}. "
            "Target must contain only 0 or 1."
        )


def validate_duplicates(df):
    key_columns = ["district", "state", "year"]

    if not all(column in df.columns for column in key_columns):
        return

    duplicate_count = df.duplicated(
        subset=key_columns
    ).sum()

    if duplicate_count > 0:
        raise ValueError(
            f"Found {duplicate_count} duplicate district-year records."
        )


def validate_year(df):
    if "year" not in df.columns or df.empty:
        return

    if not pd.api.types.is_numeric_dtype(df["year"]):
        raise ValueError("Year must be numeric.")

    invalid_years = df[
        (df["year"] < 1950) |
        (df["year"] > 2100)
    ]

    if not invalid_years.empty:
        raise ValueError(
            "Invalid year values detected."
        )


def main():
    print("=" * 70)
    print("INDIA LAND CONFLICT TRAINING DATA VALIDATOR")
    print("=" * 70)

    print(f"\nProject root:")
    print(PROJECT_ROOT)

    print(f"\nDataset:")
    print(DATASET_PATH)

    print(f"\nSchema:")
    print(SCHEMA_PATH)

    if not DATASET_PATH.exists():
        raise FileNotFoundError(
            f"\nTraining dataset not found:\n{DATASET_PATH}"
        )

    schema = load_schema()

    df = pd.read_csv(DATASET_PATH)

    print(f"\nRows: {len(df)}")
    print(f"Columns: {len(df.columns)}")

    validate_required_columns(df, schema)

    target_name = schema["target"]["name"]

    validate_target(
        df,
        target_name
    )

    validate_duplicates(df)

    validate_year(df)

    print("\nColumns detected:")
    for column in df.columns:
        print(f"  ✓ {column}")

    if not df.empty:
        print("\nTarget distribution:")

        print(
            df[target_name]
            .value_counts(dropna=False)
            .sort_index()
        )

    print("\n" + "=" * 70)
    print("VALIDATION PASSED")
    print("=" * 70)

    if df.empty:
        print(
            "\nSTATUS: Schema is ready, but there are no training "
            "records yet."
        )
    else:
        print(
            "\nSTATUS: Dataset is structurally ready for "
            "feature engineering."
        )


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print("\nVALIDATION FAILED")
        print(str(exc))
        sys.exit(1)