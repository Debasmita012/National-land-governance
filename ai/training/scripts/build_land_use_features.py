import pandas as pd
import numpy as np
from pathlib import Path


# ============================================================
# PATHS
# ============================================================

ROOT = Path(__file__).resolve().parents[3]

INPUT = (
    ROOT
    / "ai"
    / "training"
    / "data"
    / "land_use"
    / "state_land_use_coordinates.csv"
)

OUTPUT = (
    ROOT
    / "ai"
    / "training"
    / "processed"
    / "state_land_use_features.csv"
)


# ============================================================
# LOAD
# ============================================================

print("=" * 100)
print("LAND-USE ML FEATURE ENGINEERING")
print("=" * 100)

print()
print("Input:")
print(INPUT)

if not INPUT.exists():
    raise FileNotFoundError(
        f"Input file not found:\n{INPUT}"
    )

df = pd.read_csv(INPUT)

print()
print(
    f"Raw rows: {len(df)}"
)


# ============================================================
# PARSE RAW VALUES
# ============================================================

def parse_values(value):

    if pd.isna(value):
        return []

    return [
        float(x)
        for x in str(value).split("|")
        if str(x).strip() != ""
    ]


parsed = df["raw_values"].apply(
    parse_values
)


# We need all 10 columns 12-21.

bad = parsed.apply(
    lambda x: len(x) != 10
)

if bad.any():

    print()
    print(
        f"WARNING: {bad.sum()} rows do not "
        f"contain exactly 10 Table-5 values."
    )

    print(
        df.loc[
            bad,
            [
                "state",
                "year",
                "raw_values"
            ]
        ].head(20).to_string(
            index=False
        )
    )

    # Keep only complete rows.
    df = df.loc[
        ~bad
    ].copy()

    parsed = parsed.loc[
        ~bad
    ]


# ============================================================
# TABLE 5 COLUMNS 12-21
# ============================================================

df["fallow_other_than_current"] = [
    x[0] for x in parsed
]

df["current_fallow"] = [
    x[1] for x in parsed
]

df["total_fallow"] = [
    x[2] for x in parsed
]

df["net_area_sown"] = [
    x[3] for x in parsed
]

df["gross_cropped_area"] = [
    x[4] for x in parsed
]

df["area_sown_more_than_once"] = [
    x[5] for x in parsed
]

df["agricultural_land"] = [
    x[6] for x in parsed
]

df["cultivated_land"] = [
    x[7] for x in parsed
]

df["uncultivable_land"] = [
    x[8] for x in parsed
]

df["uncultivated_land"] = [
    x[9] for x in parsed
]


# ============================================================
# SORT
# ============================================================

df = df.sort_values(
    [
        "state",
        "year"
    ]
).reset_index(
    drop=True
)


# ============================================================
# BASIC RATIOS
# ============================================================

EPS = 1e-9


df["cropping_intensity"] = (
    df["gross_cropped_area"]
    / (
        df["net_area_sown"]
        + EPS
    )
)


df["double_cropped_share"] = (
    df["area_sown_more_than_once"]
    / (
        df["net_area_sown"]
        + EPS
    )
)


df["fallow_share"] = (
    df["total_fallow"]
    / (
        df["agricultural_land"]
        + EPS
    )
)


df["current_fallow_share"] = (
    df["current_fallow"]
    / (
        df["agricultural_land"]
        + EPS
    )
)


df["cultivated_land_share"] = (
    df["cultivated_land"]
    / (
        df["agricultural_land"]
        + EPS
    )
)


df["uncultivated_share"] = (
    df["uncultivated_land"]
    / (
        df["agricultural_land"]
        + EPS
    )
)


# ============================================================
# YEAR-OVER-YEAR CHANGES
# ============================================================

grouped = df.groupby(
    "state",
    group_keys=False
)


df["net_area_sown_change"] = (
    grouped["net_area_sown"]
    .pct_change()
    .replace(
        [np.inf, -np.inf],
        np.nan
    )
)


df["gross_cropped_area_change"] = (
    grouped["gross_cropped_area"]
    .pct_change()
    .replace(
        [np.inf, -np.inf],
        np.nan
    )
)


df["agricultural_land_change"] = (
    grouped["agricultural_land"]
    .pct_change()
    .replace(
        [np.inf, -np.inf],
        np.nan
    )
)


df["cultivated_land_change"] = (
    grouped["cultivated_land"]
    .pct_change()
    .replace(
        [np.inf, -np.inf],
        np.nan
    )
)


df["fallow_change"] = (
    grouped["total_fallow"]
    .pct_change()
    .replace(
        [np.inf, -np.inf],
        np.nan
    )
)


# ============================================================
# ABSOLUTE YEAR-OVER-YEAR CHANGES
# ============================================================

df["net_area_sown_delta"] = (
    grouped["net_area_sown"]
    .diff()
)


df["gross_cropped_area_delta"] = (
    grouped["gross_cropped_area"]
    .diff()
)


df["agricultural_land_delta"] = (
    grouped["agricultural_land"]
    .diff()
)


df["cultivated_land_delta"] = (
    grouped["cultivated_land"]
    .diff()
)


df["fallow_delta"] = (
    grouped["total_fallow"]
    .diff()
)


# ============================================================
# LONG-TERM CHANGE
# ============================================================

first_values = grouped[
    "agricultural_land"
].transform(
    "first"
)

df["agricultural_land_from_baseline"] = (
    (
        df["agricultural_land"]
        - first_values
    )
    / (
        first_values
        + EPS
    )
)


first_net = grouped[
    "net_area_sown"
].transform(
    "first"
)

df["net_area_sown_from_baseline"] = (
    (
        df["net_area_sown"]
        - first_net
    )
    / (
        first_net
        + EPS
    )
)


first_fallow = grouped[
    "total_fallow"
].transform(
    "first"
)

df["fallow_from_baseline"] = (
    (
        df["total_fallow"]
        - first_fallow
    )
    / (
        first_fallow
        + EPS
    )
)


# ============================================================
# ROLLING TRENDS
# ============================================================

df["agricultural_land_3yr_mean"] = (
    grouped["agricultural_land"]
    .transform(
        lambda x:
        x.rolling(
            3,
            min_periods=1
        ).mean()
    )
)


df["fallow_3yr_mean"] = (
    grouped["total_fallow"]
    .transform(
        lambda x:
        x.rolling(
            3,
            min_periods=1
        ).mean()
    )
)


df["cropping_intensity_3yr_mean"] = (
    grouped["cropping_intensity"]
    .transform(
        lambda x:
        x.rolling(
            3,
            min_periods=1
        ).mean()
    )
)


# ============================================================
# DATA QUALITY
# ============================================================

numeric_columns = [
    "fallow_other_than_current",
    "current_fallow",
    "total_fallow",
    "net_area_sown",
    "gross_cropped_area",
    "area_sown_more_than_once",
    "agricultural_land",
    "cultivated_land",
    "uncultivable_land",
    "uncultivated_land",
    "cropping_intensity",
    "double_cropped_share",
    "fallow_share",
    "current_fallow_share",
    "cultivated_land_share",
    "uncultivated_share",
]


for column in numeric_columns:

    df[column] = pd.to_numeric(
        df[column],
        errors="coerce"
    )


# ============================================================
# CLEAN INFINITE VALUES
# ============================================================

df = df.replace(
    [np.inf, -np.inf],
    np.nan
)


# ============================================================
# FEATURE LIST
# ============================================================

feature_columns = [
    "fallow_other_than_current",
    "current_fallow",
    "total_fallow",
    "net_area_sown",
    "gross_cropped_area",
    "area_sown_more_than_once",
    "agricultural_land",
    "cultivated_land",
    "uncultivable_land",
    "uncultivated_land",
    "cropping_intensity",
    "double_cropped_share",
    "fallow_share",
    "current_fallow_share",
    "cultivated_land_share",
    "uncultivated_share",
    "net_area_sown_change",
    "gross_cropped_area_change",
    "agricultural_land_change",
    "cultivated_land_change",
    "fallow_change",
    "net_area_sown_delta",
    "gross_cropped_area_delta",
    "agricultural_land_delta",
    "cultivated_land_delta",
    "fallow_delta",
    "agricultural_land_from_baseline",
    "net_area_sown_from_baseline",
    "fallow_from_baseline",
    "agricultural_land_3yr_mean",
    "fallow_3yr_mean",
    "cropping_intensity_3yr_mean",
]


# ============================================================
# OUTPUT
# ============================================================

OUTPUT.parent.mkdir(
    parents=True,
    exist_ok=True
)

output_columns = [
    "state",
    "year",
] + feature_columns

df[
    output_columns
].to_csv(
    OUTPUT,
    index=False
)


# ============================================================
# SUMMARY
# ============================================================

print()
print("=" * 100)
print("FEATURE ENGINEERING COMPLETE")
print("=" * 100)

print()
print(
    f"Rows: {len(df)}"
)

print(
    f"States: {df['state'].nunique()}"
)

print(
    f"Features: {len(feature_columns)}"
)

print()
print(
    "Feature columns:"
)

for feature in feature_columns:

    print(
        f"  - {feature}"
    )

print()
print(
    "Output:"
)

print(
    OUTPUT
)

print()
print("=" * 100)
print("NEXT: BUILD CONFLICT LABEL DATASET")
print("=" * 100)