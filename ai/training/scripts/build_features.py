from pathlib import Path
import sys

import numpy as np
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[3]

INPUT_PATH = (
    PROJECT_ROOT
    / "ai"
    / "training"
    / "data"
    / "training_dataset.csv"
)

OUTPUT_PATH = (
    PROJECT_ROOT
    / "ai"
    / "training"
    / "processed"
    / "ml_features.csv"
)


REQUIRED_COLUMNS = [
    "district",
    "state",
    "year",
    "population",
    "population_growth",
    "forest_area",
    "agricultural_area",
    "non_agricultural_area",
    "cultivable_wasteland",
    "irrigated_area",
    "land_use_change",
    "previous_conflict_count",
    "conflict_next_period",
]


NUMERIC_COLUMNS = [
    "year",
    "population",
    "population_growth",
    "forest_area",
    "agricultural_area",
    "non_agricultural_area",
    "cultivable_wasteland",
    "irrigated_area",
    "land_use_change",
    "previous_conflict_count",
    "conflict_next_period",
]


def load_dataset():
    if not INPUT_PATH.exists():
        raise FileNotFoundError(
            f"Training dataset not found:\n{INPUT_PATH}"
        )

    df = pd.read_csv(INPUT_PATH)

    missing = [
        column
        for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    if missing:
        raise ValueError(
            "Missing required columns:\n"
            + "\n".join(f"- {column}" for column in missing)
        )

    return df


def convert_numeric_columns(df):
    for column in NUMERIC_COLUMNS:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

    return df


def calculate_land_use_shares(df):
    total_land = (
        df["forest_area"].fillna(0)
        + df["agricultural_area"].fillna(0)
        + df["non_agricultural_area"].fillna(0)
        + df["cultivable_wasteland"].fillna(0)
    )

    safe_total = total_land.replace(0, np.nan)

    df["forest_share"] = (
        df["forest_area"] / safe_total * 100
    )

    df["agricultural_share"] = (
        df["agricultural_area"] / safe_total * 100
    )

    df["non_agricultural_share"] = (
        df["non_agricultural_area"] / safe_total * 100
    )

    df["wasteland_share"] = (
        df["cultivable_wasteland"] / safe_total * 100
    )

    return df


def calculate_irrigation_ratio(df):
    agricultural_area = (
        df["agricultural_area"]
        .replace(0, np.nan)
    )

    df["irrigation_ratio"] = (
        df["irrigated_area"]
        / agricultural_area
        * 100
    )

    return df


def calculate_population_density_proxy(df):
    total_land = (
        df["forest_area"].fillna(0)
        + df["agricultural_area"].fillna(0)
        + df["non_agricultural_area"].fillna(0)
        + df["cultivable_wasteland"].fillna(0)
    )

    total_land = total_land.replace(0, np.nan)

    df["population_per_land_unit"] = (
        df["population"]
        / total_land
    )

    return df


def calculate_conflict_features(df):
    df = df.sort_values(
        ["district", "state", "year"]
    ).copy()

    grouped = df.groupby(
        ["state", "district"],
        sort=False
    )

    # Previous-period conflict count.
    df["previous_conflict_count_lag"] = (
        grouped["previous_conflict_count"]
        .shift(1)
    )

    # Change in historical conflict pressure.
    df["conflict_trend"] = (
        df["previous_conflict_count"]
        - df["previous_conflict_count_lag"]
    )

    # Years since the previous recorded conflict signal.
    conflict_year = np.where(
        df["previous_conflict_count"].fillna(0) > 0,
        df["year"],
        np.nan
    )

    df["_conflict_year"] = conflict_year

    df["_last_conflict_year"] = (
        pd.Series(conflict_year, index=df.index)
        .groupby(
            [df["state"], df["district"]]
        )
        .ffill()
    )

    df["conflict_recency"] = (
        df["year"] - df["_last_conflict_year"]
    )

    df["conflict_recency"] = (
        df["conflict_recency"]
        .replace([np.inf, -np.inf], np.nan)
    )

    df.drop(
        columns=[
            "_conflict_year",
            "_last_conflict_year"
        ],
        inplace=True
    )

    return df


def clean_engineered_features(df):
    engineered_columns = [
        "forest_share",
        "agricultural_share",
        "non_agricultural_share",
        "wasteland_share",
        "irrigation_ratio",
        "population_per_land_unit",
        "previous_conflict_count_lag",
        "conflict_trend",
        "conflict_recency",
    ]

    for column in engineered_columns:
        df[column] = (
            df[column]
            .replace([np.inf, -np.inf], np.nan)
        )

    return df


def build_features():
    print("=" * 70)
    print("LAND CONFLICT ML FEATURE ENGINEERING")
    print("=" * 70)

    df = load_dataset()

    print(f"\nInput rows: {len(df)}")
    print(f"Input columns: {len(df.columns)}")

    df = convert_numeric_columns(df)

    df = calculate_land_use_shares(df)

    df = calculate_irrigation_ratio(df)

    df = calculate_population_density_proxy(df)

    df = calculate_conflict_features(df)

    df = clean_engineered_features(df)

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_csv(
        OUTPUT_PATH,
        index=False
    )

    print(f"\nOutput saved to:")
    print(OUTPUT_PATH)

    print(f"\nOutput rows: {len(df)}")
    print(f"Output columns: {len(df.columns)}")

    print("\nEngineered features:")

    engineered = [
        "forest_share",
        "agricultural_share",
        "non_agricultural_share",
        "wasteland_share",
        "irrigation_ratio",
        "population_per_land_unit",
        "previous_conflict_count_lag",
        "conflict_trend",
        "conflict_recency",
    ]

    for column in engineered:
        print(f"  ✓ {column}")

    print("\nFeature engineering completed.")


if __name__ == "__main__":
    try:
        build_features()
    except Exception as exc:
        print("\nFEATURE ENGINEERING FAILED")
        print(str(exc))
        sys.exit(1)