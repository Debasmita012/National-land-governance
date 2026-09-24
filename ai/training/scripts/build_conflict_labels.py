import pandas as pd
from pathlib import Path


# ============================================================
# PATHS
# ============================================================

ROOT = Path(__file__).resolve().parents[3]

LAND_USE_FILE = (
    ROOT
    / "ai"
    / "training"
    / "processed"
    / "state_land_use_features.csv"
)

CONFLICT_FILE = (
    ROOT
    / "ai"
    / "training"
    / "data"
    / "conflicts"
    / "conflict_records.csv"
)

OUTPUT_FILE = (
    ROOT
    / "ai"
    / "training"
    / "processed"
    / "training_dataset.csv"
)


print("=" * 90)
print("BUILDING CONFLICT-LABEL DATASET")
print("=" * 90)


# ============================================================
# CHECK FILES
# ============================================================

if not LAND_USE_FILE.exists():
    raise FileNotFoundError(
        f"Land-use feature file not found:\n{LAND_USE_FILE}"
    )

if not CONFLICT_FILE.exists():
    raise FileNotFoundError(
        f"Conflict file not found:\n{CONFLICT_FILE}"
    )


# ============================================================
# LOAD DATA
# ============================================================

land = pd.read_csv(LAND_USE_FILE)
conflicts = pd.read_csv(CONFLICT_FILE)

print()
print(f"Land-use feature rows: {len(land)}")
print(f"Conflict records: {len(conflicts)}")


# ============================================================
# NORMALIZE STATE NAMES
# ============================================================

def normalize_state(value):

    if pd.isna(value):
        return None

    return (
        str(value)
        .strip()
        .lower()
        .replace("&", "and")
        .replace("  ", " ")
    )


land["state_key"] = land["state"].apply(
    normalize_state
)

conflicts["state_key"] = conflicts["state"].apply(
    normalize_state
)


# ============================================================
# NORMALIZE YEARS
# ============================================================

land["year"] = pd.to_numeric(
    land["year"],
    errors="coerce"
)

conflicts["year_started"] = pd.to_numeric(
    conflicts["year_started"],
    errors="coerce"
)


# ============================================================
# AGGREGATE OBSERVED CONFLICTS
# ============================================================

conflict_yearly = (
    conflicts
    .dropna(
        subset=[
            "state_key",
            "year_started"
        ]
    )
    .groupby(
        [
            "state_key",
            "year_started"
        ]
    )
    .agg(
        conflict_count=(
            "conflict_id",
            "nunique"
        ),
        people_affected=(
            "people_affected",
            "sum"
        ),
        conflict_land_area_ha=(
            "land_area_ha",
            "sum"
        )
    )
    .reset_index()
)


conflict_yearly = conflict_yearly.rename(
    columns={
        "year_started": "conflict_year"
    }
)


print()
print("Observed conflict years:")

print(
    conflict_yearly[
        [
            "state_key",
            "conflict_year",
            "conflict_count"
        ]
    ]
    .sort_values(
        [
            "state_key",
            "conflict_year"
        ]
    )
    .to_string(index=False)
)


# ============================================================
# JOIN CURRENT-YEAR CONFLICT INFORMATION
# ============================================================

merged = land.merge(
    conflict_yearly,
    left_on=[
        "state_key",
        "year"
    ],
    right_on=[
        "state_key",
        "conflict_year"
    ],
    how="left"
)


# ============================================================
# CONFLICT OBSERVATION FLAG
# ============================================================

merged["conflict_observed"] = (
    merged["conflict_count"].notna()
)


# Missing conflict count means that no conflict record was
# observed for that state/year in our collected source.

merged["conflict_count"] = (
    merged["conflict_count"]
    .fillna(0)
)


merged["people_affected"] = (
    merged["people_affected"]
    .fillna(0)
)


merged["conflict_land_area_ha"] = (
    merged["conflict_land_area_ha"]
    .fillna(0)
)


# ============================================================
# DETERMINE TARGET COVERAGE
# ============================================================
#
# Target for year T:
#
# conflict_next_period = 1
#
# if a documented conflict starts in year T+1.
#
# We only create a target when T+1 is within the observed
# conflict-year range for that state.
#
# This prevents us from incorrectly treating years outside
# the conflict-source coverage as negative examples.
#


conflict_year_sets = (
    conflict_yearly
    .groupby("state_key")["conflict_year"]
    .apply(set)
    .to_dict()
)


def calculate_target(row):

    state = row["state_key"]
    year = int(row["year"])

    observed_years = conflict_year_sets.get(
        state,
        set()
    )

    if not observed_years:
        return pd.NA

    next_year = year + 1

    # We can only know the target if the following year
    # is within the observed temporal coverage.
    min_year = min(observed_years)
    max_year = max(observed_years)

    if next_year < min_year:
        return pd.NA

    if year >= max_year:
        return pd.NA

    if next_year in observed_years:
        return 1

    return 0


merged["conflict_next_period"] = (
    merged.apply(
        calculate_target,
        axis=1
    )
)


# ============================================================
# TARGET AVAILABILITY
# ============================================================

merged["target_available"] = (
    merged["conflict_next_period"]
    .notna()
)


# ============================================================
# CONVERT TARGET TYPE
# ============================================================

merged["conflict_next_period"] = (
    pd.to_numeric(
        merged["conflict_next_period"],
        errors="coerce"
    )
    .astype("Int64")
)


# ============================================================
# REMOVE TEMPORARY JOIN COLUMNS
# ============================================================

temporary_columns = [
    "state_key",
    "conflict_year"
]

merged = merged.drop(
    columns=[
        column
        for column in temporary_columns
        if column in merged.columns
    ]
)


# ============================================================
# SAVE
# ============================================================

OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)

merged.to_csv(
    OUTPUT_FILE,
    index=False
)


# ============================================================
# SUMMARY
# ============================================================

print()
print("=" * 90)
print("TRAINING DATASET CREATED")
print("=" * 90)

print()
print(
    f"Total rows: {len(merged)}"
)

print(
    "Rows with observed conflict data: "
    f"{int(merged['conflict_observed'].sum())}"
)

print(
    "Rows with available future target: "
    f"{int(merged['target_available'].sum())}"
)


# ============================================================
# TARGET DISTRIBUTION
# ============================================================

available = merged[
    merged["target_available"]
].copy()


print()

if len(available) == 0:

    print(
        "No usable future-conflict targets were found."
    )

else:

    print(
        "Target distribution:"
    )

    print(
        available[
            "conflict_next_period"
        ]
        .value_counts()
        .sort_index()
        .to_string()
    )


# ============================================================
# STATES WITH USABLE TARGETS
# ============================================================

print()

if len(available):

    # Reload state from original land table using row alignment
    # through state/year.

    state_target_summary = (
        merged[
            merged["target_available"]
        ]
        .groupby("state")
        .agg(
            rows=(
                "conflict_next_period",
                "size"
            ),
            positive_targets=(
                "conflict_next_period",
                "sum"
            )
        )
        .sort_index()
    )

    print(
        "Usable target coverage by state:"
    )

    print(
        state_target_summary.to_string()
    )


# ============================================================
# OUTPUT
# ============================================================

print()
print("Output:")
print(OUTPUT_FILE)

print()
print("=" * 90)
print("LABEL BUILD COMPLETE")
print("=" * 90)