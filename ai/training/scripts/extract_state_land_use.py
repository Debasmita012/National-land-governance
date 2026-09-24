import csv
import re
from pathlib import Path
from collections import defaultdict

import pdfplumber


# ============================================================
# PATHS
# ============================================================

ROOT = Path(__file__).resolve().parents[3]

PDF = (
    ROOT
    / "ai"
    / "training"
    / "data"
    / "land_use"
    / "LUS-Publication-2024-25.pdf"
)

OUTPUT = (
    ROOT
    / "ai"
    / "training"
    / "data"
    / "land_use"
    / "state_land_use_coordinates.csv"
)

DEBUG = (
    ROOT
    / "ai"
    / "training"
    / "data"
    / "land_use"
    / "table5_coordinate_debug.csv"
)


# ============================================================
# STATES
# ============================================================

STATES = {
    "ANDHRA PRADESH": "Andhra Pradesh",
    "ARUNACHAL PRADESH": "Arunachal Pradesh",
    "ASSAM": "Assam",
    "BIHAR": "Bihar",
    "CHHATTISGARH": "Chhattisgarh",
    "GOA": "Goa",
    "GUJARAT": "Gujarat",
    "HARYANA": "Haryana",
    "HIMACHAL PRADESH": "Himachal Pradesh",
    "JHARKHAND": "Jharkhand",
    "KARNATAKA": "Karnataka",
    "KERALA": "Kerala",
    "MADHYA PRADESH": "Madhya Pradesh",
    "MAHARASHTRA": "Maharashtra",
    "MANIPUR": "Manipur",
    "MEGHALAYA": "Meghalaya",
    "MIZORAM": "Mizoram",
    "NAGALAND": "Nagaland",
    "ODISHA": "Odisha",
    "PUNJAB": "Punjab",
    "RAJASTHAN": "Rajasthan",
    "SIKKIM": "Sikkim",
    "TAMIL NADU": "Tamil Nadu",
    "TELANGANA": "Telangana",
    "TRIPURA": "Tripura",
    "UTTARAKHAND": "Uttarakhand",
    "UTTAR PRADESH": "Uttar Pradesh",
    "WEST BENGAL": "West Bengal",
    "NICOBAR ISLANDS": "Nicobar Islands",
    "CHANDIGARH": "Chandigarh",
    "DADRA & NAGAR HAVELI": "Dadra & Nagar Haveli",
    "DAMAN & DIU": "Daman & Diu",
    "DELHI": "Delhi",
    "JAMMU & KASHMIR": "Jammu & Kashmir",
    "LADAKH": "Ladakh",
    "LAKSHADWEEP": "Lakshadweep",
    "PUDUCHERRY": "Puducherry",
}


# ============================================================
# HELPERS
# ============================================================

def clean(text):
    return " ".join(
        str(text or "")
        .replace("\xa0", " ")
        .split()
    )


def number_token(text):

    text = clean(text).replace(",", "")

    return re.fullmatch(
        r"-?\d+(?:\.\d+)?",
        text
    )


def year_token(text):

    text = clean(text)

    return re.fullmatch(
        r"20\d{2}-\d{2}(?:\(p\))?",
        text
    )


def normalized(text):

    text = clean(text).upper()

    text = text.replace("*", "")

    return text


# ============================================================
# GROUP PDF WORDS INTO VISUAL LINES
# ============================================================

def group_words_into_lines(words):

    lines = []

    for word in sorted(
        words,
        key=lambda w: (
            round(w["top"], 1),
            w["x0"]
        )
    ):

        top = word["top"]

        placed = False

        for line in lines:

            if abs(
                line["top"] - top
            ) <= 2.5:

                line["words"].append(
                    word
                )

                placed = True
                break

        if not placed:

            lines.append(
                {
                    "top": top,
                    "words": [word],
                }
            )

    for line in lines:

        line["words"].sort(
            key=lambda w: w["x0"]
        )

        line["text"] = clean(
            " ".join(
                w["text"]
                for w in line["words"]
            )
        )

    return sorted(
        lines,
        key=lambda x: x["top"]
    )


# ============================================================
# FIND STATE IN VISUAL LINES
# ============================================================

def find_state(lines, index):

    # Check current line and next two lines because
    # HIMACHAL PRADESH, MADHYA PRADESH, etc. can be
    # split by PDF text positioning.

    candidates = []

    for size in range(1, 4):

        if index + size <= len(lines):

            text = " ".join(
                lines[j]["text"]
                for j in range(
                    index,
                    index + size
                )
            )

            candidates.append(
                normalized(text)
            )

    # Longest state names first.
    for candidate in candidates:

        for raw_state in sorted(
            STATES,
            key=len,
            reverse=True
        ):

            if candidate == raw_state:

                return STATES[raw_state], size

    return None, 0


# ============================================================
# MAIN
# ============================================================

print("=" * 100)
print("COORDINATE-BASED TABLE 5 EXTRACTION")
print("=" * 100)

print()
print("PDF:")
print(PDF)

if not PDF.exists():

    raise FileNotFoundError(
        PDF
    )


records = []

debug = []


with pdfplumber.open(PDF) as pdf:

    # Table 5 is around these pages.
    for page_number in range(
        149,
        156
    ):

        print()
        print(
            f"Processing PDF page {page_number}..."
        )

        page = pdf.pages[
            page_number - 1
        ]

        words = page.extract_words(
            x_tolerance=2,
            y_tolerance=2,
            keep_blank_chars=False
        )

        print(
            f"  Words extracted: {len(words)}"
        )

        lines = group_words_into_lines(
            words
        )

        print(
            f"  Visual lines: {len(lines)}"
        )


        # ----------------------------------------------------
        # Find state positions.
        # ----------------------------------------------------

        i = 0

        page_states = []

        while i < len(lines):

            state, consumed = find_state(
                lines,
                i
            )

            if state:

                page_states.append(
                    {
                        "state": state,
                        "line_index": i,
                        "top": lines[i]["top"],
                    }
                )

                i += max(
                    consumed,
                    1
                )

            else:

                i += 1


        print(
            "  States detected:",
            [
                s["state"]
                for s in page_states
            ]
        )


        # ----------------------------------------------------
        # Save visual-line debug information.
        # ----------------------------------------------------

        for line_index, line in enumerate(
            lines
        ):

            debug.append(
                [
                    page_number,
                    line_index,
                    round(
                        line["top"],
                        2
                    ),
                    line["text"],
                ]
            )


        # ----------------------------------------------------
        # Associate year rows with states.
        # ----------------------------------------------------

        for state_index, state_info in enumerate(
            page_states
        ):

            state = state_info["state"]

            start_index = (
                state_info["line_index"]
                + 1
            )

            if (
                state_index
                + 1
                < len(page_states)
            ):

                end_index = (
                    page_states[
                        state_index + 1
                    ]["line_index"]
                )

            else:

                end_index = len(lines)


            current_year = None

            for line_index in range(
                start_index,
                end_index
            ):

                line = lines[
                    line_index
                ]

                text = line["text"]

                # ------------------------------------------------
                # Detect year
                # ------------------------------------------------

                year_match = re.search(
                    r"\b(2015|2016|2017|2018|2019|2020|2021|2022|2023|2024)"
                    r"-"
                    r"(16|17|18|19|20|21|22|23|24|25)"
                    r"(?:\(p\))?",
                    text
                )

                if not year_match:

                    continue


                year = int(
                    year_match.group(1)
                )

                current_year = year


                # ------------------------------------------------
                # Extract numeric tokens from the SAME visual
                # line, preserving x positions.
                # ------------------------------------------------

                numeric_words = []

                for word in line["words"]:

                    token = clean(
                        word["text"]
                    ).replace(",", "")

                    if number_token(
                        token
                    ):

                        numeric_words.append(
                            word
                        )


                # Need actual land-use numbers.
                #
                # Year appears as two numeric components in
                # some PDF extraction layouts, so don't count
                # the year itself.
                #

                values = []

                for word in numeric_words:

                    token = clean(
                        word["text"]
                    ).replace(",", "")

                    if token == str(year):
                        continue

                    # Skip the second part of the year.
                    if token == str(
                        (year + 1) % 100
                    ):
                        continue

                    values.append(
                        token
                    )


                if len(values) < 7:

                    continue


                record = {
                    "state": state,
                    "year": year,
                    "values": values,
                    "page": page_number,
                    "y": round(
                        line["top"],
                        2
                    ),
                }

                records.append(
                    record
                )


# ============================================================
# DEDUPLICATE
# ============================================================

unique = {}

for record in records:

    key = (
        record["state"],
        record["year"]
    )

    if key not in unique:

        unique[key] = record


records = list(
    unique.values()
)


records.sort(
    key=lambda r: (
        r["state"],
        r["year"]
    )
)


# ============================================================
# SUMMARY
# ============================================================

print()
print("=" * 100)
print("EXTRACTION SUMMARY")
print("=" * 100)

print()
print(
    f"Unique state/year records: "
    f"{len(records)}"
)


from collections import Counter

counts = Counter(
    r["state"]
    for r in records
)

print()
print("STATE COUNTS")
print("-" * 60)

for state, count in sorted(
    counts.items()
):

    print(
        f"{state:<35} {count}"
    )


# ============================================================
# WEST BENGAL
# ============================================================

wb = [
    r
    for r in records
    if r["state"] == "West Bengal"
]

print()
print("WEST BENGAL")

print(
    "Records:",
    len(wb)
)

print(
    "Years:",
    [
        r["year"]
        for r in wb
    ]
)


# ============================================================
# SAVE DEBUG VISUAL LINES
# ============================================================

DEBUG.parent.mkdir(
    parents=True,
    exist_ok=True
)

with open(
    DEBUG,
    "w",
    newline="",
    encoding="utf-8"
) as f:

    writer = csv.writer(
        f
    )

    writer.writerow(
        [
            "page",
            "line_index",
            "y",
            "text",
        ]
    )

    writer.writerows(
        debug
    )


# ============================================================
# SAVE RAW COORDINATE DATA
# ============================================================

with open(
    OUTPUT,
    "w",
    newline="",
    encoding="utf-8"
) as f:

    writer = csv.writer(
        f
    )

    writer.writerow(
        [
            "state",
            "year",
            "raw_values",
            "pdf_page",
            "y_position",
        ]
    )

    for record in records:

        writer.writerow(
            [
                record["state"],
                record["year"],
                "|".join(
                    record["values"]
                ),
                record["page"],
                record["y"],
            ]
        )


print()
print(
    "Coordinate debug:"
)

print(
    DEBUG
)

print()
print(
    "Raw coordinate dataset:"
)

print(
    OUTPUT
)

print()
print("=" * 100)
print("DONE")
print("=" * 100)