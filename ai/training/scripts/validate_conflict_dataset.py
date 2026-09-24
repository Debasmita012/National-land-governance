import pandas as pd
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]

INPUT = (
    ROOT
    / "ai"
    / "training"
    / "data"
    / "conflicts"
    / "conflict_records.csv"
)


REQUIRED_COLUMNS = [
    "conflict_id",
    "state",
    "district",
    "conflict_title",
    "year_started",
    "year_ended",
    "conflict_status",
    "sector",
    "conflict_type",
    "people_affected",
    "land_area_ha",
    "investment_crore",
    "source_url",
    "source_name",
    "source_date",
]


print("=" * 80)
print("CONFLICT DATASET VALIDATION")
print("=" * 80)

print()
print("Input:")
print(INPUT)


if not INPUT.exists():
    raise FileNotFoundError(
        f"Conflict dataset not found:\n{INPUT}"
    )


df = pd.read_csv(INPUT)

print()
print(f"Rows: {len(df)}")


# ------------------------------------------------------------
# Columns
# ------------------------------------------------------------

missing = [
    column
    for column in REQUIRED_COLUMNS
    if column not in df.columns
]

if missing:

    raise ValueError(
        "Missing required columns:\n"
        + "\n".join(missing)
    )

print("Column check: PASS")


# ------------------------------------------------------------
# Empty dataset
# ------------------------------------------------------------

if len(df) == 0:

    print()
    print("Dataset currently contains no conflict records.")
    print()
    print(
        "This is intentional. Do not train the supervised "
        "model until real source-attributed conflict records "
        "have been added."
    )

    print()
    print("=" * 80)
    print("VALIDATION COMPLETE")
    print("=" * 80)

    raise SystemExit(0)


# ------------------------------------------------------------
# Conflict ID
# ------------------------------------------------------------

if df["conflict_id"].isna().any():

    raise ValueError(
        "Missing conflict_id values."
    )

if df["conflict_id"].duplicated().any():

    duplicates = df.loc[
        df["conflict_id"].duplicated(),
        "conflict_id"
    ].tolist()

    raise ValueError(
        f"Duplicate conflict IDs: {duplicates}"
    )

print("Conflict ID check: PASS")


# ------------------------------------------------------------
# State
# ------------------------------------------------------------

if df["state"].isna().any():

    raise ValueError(
        "Missing state values."
    )

print("State check: PASS")


# ------------------------------------------------------------
# Start year
# ------------------------------------------------------------

df["year_started"] = pd.to_numeric(
    df["year_started"],
    errors="coerce"
)

if df["year_started"].isna().any():

    raise ValueError(
        "Invalid or missing year_started values."
    )


invalid_years = df.loc[
    ~df["year_started"].between(
        1900,
        2030
    )
]

if len(invalid_years):

    raise ValueError(
        "Invalid conflict start years detected."
    )

print("Start-year check: PASS")


# ------------------------------------------------------------
# End year
# ------------------------------------------------------------

if "year_ended" in df.columns:

    end_year = pd.to_numeric(
        df["year_ended"],
        errors="coerce"
    )

    invalid_end = (
        end_year.notna()
        &
        ~end_year.between(
            1900,
            2030
        )
    )

    if invalid_end.any():

        raise ValueError(
            "Invalid year_ended values detected."
        )


# ------------------------------------------------------------
# Numeric fields
# ------------------------------------------------------------

numeric_columns = [
    "people_affected",
    "land_area_ha",
    "investment_crore",
]


for column in numeric_columns:

    df[column] = pd.to_numeric(
        df[column],
        errors="coerce"
    )

    negative = (
        df[column].notna()
        &
        (df[column] < 0)
    )

    if negative.any():

        raise ValueError(
            f"Negative values found in {column}."
        )


print("Numeric field check: PASS")


# ------------------------------------------------------------
# Source check
# ------------------------------------------------------------

if df["source_url"].isna().any():

    raise ValueError(
        "Every conflict record must have a source_url."
    )


if df["source_name"].isna().any():

    raise ValueError(
        "Every conflict record must have a source_name."
    )


print("Source provenance check: PASS")


# ------------------------------------------------------------
# Summary
# ------------------------------------------------------------

print()
print("States:")
print(
    df["state"]
    .value_counts()
    .to_string()
)

print()
print(
    "Year range:",
    int(df["year_started"].min()),
    "-",
    int(df["year_started"].max())
)

print()
print("=" * 80)
print("VALIDATION SUCCESS")
print("=" * 80)