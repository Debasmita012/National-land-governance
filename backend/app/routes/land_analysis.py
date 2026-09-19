from app.services.land_hotspot_service import (
    LandHotspotService,
)


from app.services.integrated_land_risk_service import (
    IntegratedLandRiskService,
)

from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.services.data_profiler_service import (
    DataProfilerService,
)

from app.services.land_intelligence_service import (
    LandIntelligenceService,
)

from app.services.land_risk_service import (
    LandRiskService,
)

from app.services.land_use_change_service import (
    LandUseChangeService,
)


# ============================================================
# RISK RESULT NORMALIZATION
# ============================================================

def _extract_parcel_risks(risk_result):
    """Normalize different risk-service response shapes."""
    if not isinstance(risk_result, dict):
        return []

    for key in ("parcel_risks", "records", "risk_records"):
        candidate = risk_result.get(key)
        if isinstance(candidate, list) and candidate:
            return candidate

    for key in ("risk_analysis", "integrated_risk", "result", "analysis"):
        nested = risk_result.get(key)
        if not isinstance(nested, dict):
            continue
        for nested_key in ("parcel_risks", "records", "risk_records"):
            candidate = nested.get(nested_key)
            if isinstance(candidate, list) and candidate:
                return candidate

    return []


# ============================================================
# ROUTER
# ============================================================

router = APIRouter(
    prefix="/land-analysis",
    tags=["Land Intelligence"],
)


# ============================================================
# PROJECT / UPLOAD CONFIGURATION
# ============================================================

# Project structure:
#
# national-land-governance/
# ├── backend/
# │   └── app/
# │       └── routes/
# │           └── land_analysis.py
# └── data/
#     └── uploads/
#
# parents[3] points to:
# national-land-governance/

PROJECT_ROOT = Path(__file__).resolve().parents[3]

UPLOAD_DIR = (
    PROJECT_ROOT
    / "data"
    / "uploads"
)

UPLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


# ============================================================
# ALLOWED FILE TYPES
# ============================================================

ALLOWED_EXTENSIONS = {
    ".csv",
    ".xlsx",
    ".xls",
    ".geojson",
    ".json",
    ".pdf",
}


# ============================================================
# SERVICES
# ============================================================

profiler_service = DataProfilerService()

intelligence_service = LandIntelligenceService()
risk_service = LandRiskService()
land_use_change_service = LandUseChangeService()
integrated_risk_service = IntegratedLandRiskService()
hotspot_service = LandHotspotService()


# ============================================================
# 1. BASIC FILE UPLOAD
# ============================================================

@router.post("/upload")
async def upload_land_data(
    file: UploadFile = File(...),
):
    """
    Upload a land-governance dataset.

    This endpoint only validates and stores the uploaded
    file.

    It does NOT perform profiling or analysis.
    """

    # --------------------------------------------------------
    # Validate filename
    # --------------------------------------------------------

    if not file.filename:

        raise HTTPException(
            status_code=400,
            detail="No filename provided.",
        )

    original_name = file.filename

    # --------------------------------------------------------
    # Determine extension
    # --------------------------------------------------------

    extension = Path(
        original_name
    ).suffix.lower()

    # --------------------------------------------------------
    # Validate extension
    # --------------------------------------------------------

    if extension not in ALLOWED_EXTENSIONS:

        raise HTTPException(
            status_code=400,
            detail=(
                f"Unsupported file type: {extension}. "
                f"Allowed types: "
                f"{sorted(ALLOWED_EXTENSIONS)}"
            ),
        )

    # --------------------------------------------------------
    # Generate unique filename
    # --------------------------------------------------------

    unique_name = (
        f"{uuid4().hex}{extension}"
    )

    destination = (
        UPLOAD_DIR
        / unique_name
    )

    # --------------------------------------------------------
    # Save file
    # --------------------------------------------------------

    try:

        contents = await file.read()

        with open(
            destination,
            "wb",
        ) as output_file:

            output_file.write(
                contents
            )

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=(
                "Failed to save uploaded file: "
                f"{str(error)}"
            ),
        )

    # --------------------------------------------------------
    # Response
    # --------------------------------------------------------

    return {
        "success": True,

        "message": (
            "Land data uploaded successfully."
        ),

        "file": {
            "original_name": original_name,
            "stored_name": unique_name,
            "extension": extension,
            "size_bytes": len(contents),
            "path": str(destination),
        },

        "next_step": (
            "The uploaded file is ready for "
            "automatic data profiling and "
            "land intelligence analysis."
        ),
    }


# ============================================================
# 2. DATA PROFILING
# ============================================================

@router.post("/profile")
async def profile_land_data(
    file: UploadFile = File(...),
):
    """
    Upload a dataset and automatically generate
    a structural data profile.

    Supported:
        CSV
        Excel
        GeoJSON
        JSON
        PDF
    """

    # --------------------------------------------------------
    # Validate filename
    # --------------------------------------------------------

    if not file.filename:

        raise HTTPException(
            status_code=400,
            detail="No filename provided.",
        )

    original_name = file.filename

    # --------------------------------------------------------
    # Determine extension
    # --------------------------------------------------------

    extension = Path(
        original_name
    ).suffix.lower()

    # --------------------------------------------------------
    # Validate extension
    # --------------------------------------------------------

    if extension not in ALLOWED_EXTENSIONS:

        raise HTTPException(
            status_code=400,
            detail=(
                f"Unsupported file type: {extension}. "
                f"Allowed types: "
                f"{sorted(ALLOWED_EXTENSIONS)}"
            ),
        )

    # --------------------------------------------------------
    # Generate unique filename
    # --------------------------------------------------------

    unique_name = (
        f"{uuid4().hex}{extension}"
    )

    destination = (
        UPLOAD_DIR
        / unique_name
    )

    try:

        # ----------------------------------------------------
        # Save uploaded file
        # ----------------------------------------------------

        contents = await file.read()

        with open(
            destination,
            "wb",
        ) as output_file:

            output_file.write(
                contents
            )

        # ----------------------------------------------------
        # Generate profile
        # ----------------------------------------------------

        profile = (
            profiler_service.profile_file(
                str(destination)
            )
        )

        # ----------------------------------------------------
        # Return result
        # ----------------------------------------------------

        return {
            "success": True,

            "filename": original_name,

            "stored_filename": unique_name,

            "profile": profile,
        }

    except ValueError as error:

        if destination.exists():
            destination.unlink()

        raise HTTPException(
            status_code=400,
            detail=str(error),
        )

    except Exception as error:

        if destination.exists():
            destination.unlink()

        raise HTTPException(
            status_code=500,
            detail=(
                "Profiling failed: "
                f"{str(error)}"
            ),
        )


# ============================================================
# 3. FULL LAND INTELLIGENCE + RISK ANALYSIS
# ============================================================

@router.post("/analyze")
async def analyze_land_data(
    file: UploadFile = File(...),
):
    """
    Upload a CSV/Excel land dataset and generate:

        1. Automatic data profile
        2. Detected land-related fields
        3. Parcel statistics
        4. Dispute statistics
        5. Land-use distribution
        6. Population indicators
        7. Area indicators
        8. Geographic indicators
        9. Data-quality indicators
        10. Explainable land-risk analysis
    """

    # --------------------------------------------------------
    # Validate filename
    # --------------------------------------------------------

    if not file.filename:

        raise HTTPException(
            status_code=400,
            detail="No filename provided.",
        )

    original_name = file.filename

    # --------------------------------------------------------
    # Determine extension
    # --------------------------------------------------------

    extension = Path(
        original_name
    ).suffix.lower()

    # --------------------------------------------------------
    # Land intelligence currently supports
    # CSV and Excel
    # --------------------------------------------------------

    if extension not in {
        ".csv",
        ".xlsx",
        ".xls",
    }:

        raise HTTPException(
            status_code=400,
            detail=(
                "Land intelligence analysis currently "
                "supports CSV and Excel files."
            ),
        )

    # --------------------------------------------------------
    # Generate unique filename
    # --------------------------------------------------------

    unique_name = (
        f"{uuid4().hex}{extension}"
    )

    destination = (
        UPLOAD_DIR
        / unique_name
    )

    try:

        # ====================================================
        # STEP 1 — SAVE FILE
        # ====================================================

        contents = await file.read()

        with open(
            destination,
            "wb",
        ) as output_file:

            output_file.write(
                contents
            )

        # ====================================================
        # STEP 2 — PROFILE DATASET
        # ====================================================

        profile = (
            profiler_service.profile_file(
                str(destination)
            )
        )

        # ====================================================
        # STEP 3 — GET DETECTED FIELDS
        # ====================================================

        detected_fields = (
            profile.get(
                "detected_fields",
                {},
            )
        )

        # ====================================================
        # STEP 4 — LAND INTELLIGENCE
        # ====================================================

        analysis = (
            intelligence_service.analyze_file(
                file_path=str(
                    destination
                ),
                detected_fields=(
                    detected_fields
                ),
            )
        )

        # ====================================================
        # STEP 5 — LAND RISK ANALYSIS
        # ====================================================

        risk_analysis = (
            risk_service.analyze_file(
                file_path=str(
                    destination
                ),
                detected_fields=(
                    detected_fields
                ),
            )
        )

        # ====================================================
        # STEP 6 — RETURN COMPLETE RESULT
        # ====================================================

        return {
            "success": True,

            "filename": original_name,

            "stored_filename": unique_name,

            "profile": profile,

            "analysis": analysis,

            "risk_analysis": risk_analysis,
        }

    except ValueError as error:

        if destination.exists():
            destination.unlink()

        raise HTTPException(
            status_code=400,
            detail=str(error),
        )

    except Exception as error:

        if destination.exists():
            destination.unlink()

        raise HTTPException(
            status_code=500,
            detail=(
                "Land intelligence analysis failed: "
                f"{str(error)}"
            ),
        )


# ============================================================
# 4. HISTORICAL vs CURRENT LAND-USE CHANGE
# ============================================================

@router.post("/land-use-change")
async def detect_land_use_change(
    historical_file: UploadFile = File(...),
    current_file: UploadFile = File(...),
):
    """
    Compare historical and current land-use datasets.

    The system automatically detects:

        - parcel identifier column
        - land-use column
        - changed parcels
        - unchanged parcels
        - conversion rate
        - land-use transitions
        - historical distribution
        - current distribution

    Supported:
        CSV
        Excel
    """

    # ========================================================
    # VALIDATE HISTORICAL FILE
    # ========================================================

    if not historical_file.filename:

        raise HTTPException(
            status_code=400,
            detail=(
                "Historical filename is missing."
            ),
        )

    # ========================================================
    # VALIDATE CURRENT FILE
    # ========================================================

    if not current_file.filename:

        raise HTTPException(
            status_code=400,
            detail=(
                "Current filename is missing."
            ),
        )

    # ========================================================
    # DETERMINE EXTENSIONS
    # ========================================================

    historical_extension = Path(
        historical_file.filename
    ).suffix.lower()

    current_extension = Path(
        current_file.filename
    ).suffix.lower()

    supported_extensions = {
        ".csv",
        ".xlsx",
        ".xls",
    }

    # ========================================================
    # VALIDATE HISTORICAL EXTENSION
    # ========================================================

    if (
        historical_extension
        not in supported_extensions
    ):

        raise HTTPException(
            status_code=400,
            detail=(
                "Historical dataset must be "
                "CSV or Excel."
            ),
        )

    # ========================================================
    # VALIDATE CURRENT EXTENSION
    # ========================================================

    if (
        current_extension
        not in supported_extensions
    ):

        raise HTTPException(
            status_code=400,
            detail=(
                "Current dataset must be "
                "CSV or Excel."
            ),
        )

    # ========================================================
    # GENERATE UNIQUE FILE NAMES
    # ========================================================

    historical_name = (
        f"{uuid4().hex}"
        f"{historical_extension}"
    )

    current_name = (
        f"{uuid4().hex}"
        f"{current_extension}"
    )

    historical_path = (
        UPLOAD_DIR
        / historical_name
    )

    current_path = (
        UPLOAD_DIR
        / current_name
    )

    try:

        # ====================================================
        # STEP 1 — SAVE HISTORICAL DATASET
        # ====================================================

        historical_contents = (
            await historical_file.read()
        )

        with open(
            historical_path,
            "wb",
        ) as output_file:

            output_file.write(
                historical_contents
            )

        # ====================================================
        # STEP 2 — SAVE CURRENT DATASET
        # ====================================================

        current_contents = (
            await current_file.read()
        )

        with open(
            current_path,
            "wb",
        ) as output_file:

            output_file.write(
                current_contents
            )

        # ====================================================
        # STEP 3 — PROFILE HISTORICAL DATASET
        # ====================================================

        historical_profile = (
            profiler_service.profile_file(
                str(historical_path)
            )
        )

        # ====================================================
        # STEP 4 — PROFILE CURRENT DATASET
        # ====================================================

        current_profile = (
            profiler_service.profile_file(
                str(current_path)
            )
        )

        # ====================================================
        # STEP 5 — DETECT HISTORICAL FIELDS
        # ====================================================

        historical_fields = (
            historical_profile.get(
                "detected_fields",
                {},
            )
        )

        # ====================================================
        # STEP 6 — DETECT CURRENT FIELDS
        # ====================================================

        current_fields = (
            current_profile.get(
                "detected_fields",
                {},
            )
        )

        # ====================================================
        # STEP 7 — DETECT HISTORICAL PARCEL ID
        # ====================================================

        historical_parcel_column = (
            historical_fields.get(
                "parcel_id"
            )
        )

        # ====================================================
        # STEP 8 — DETECT CURRENT PARCEL ID
        # ====================================================

        current_parcel_column = (
            current_fields.get(
                "parcel_id"
            )
        )

        # ====================================================
        # STEP 9 — DETECT HISTORICAL LAND USE
        # ====================================================

        historical_land_use_column = (
            historical_fields.get(
                "land_use"
            )
        )

        # ====================================================
        # STEP 10 — DETECT CURRENT LAND USE
        # ====================================================

        current_land_use_column = (
            current_fields.get(
                "land_use"
            )
        )

        # ====================================================
        # STEP 11 — VALIDATE DETECTION
        # ====================================================

        missing_fields = []

        if not historical_parcel_column:

            missing_fields.append(
                "historical parcel ID"
            )

        if not historical_land_use_column:

            missing_fields.append(
                "historical land-use"
            )

        if not current_parcel_column:

            missing_fields.append(
                "current parcel ID"
            )

        if not current_land_use_column:

            missing_fields.append(
                "current land-use"
            )

        if missing_fields:

            raise ValueError(
                "Unable to automatically detect: "
                + ", ".join(
                    missing_fields
                )
            )

        # ====================================================
        # STEP 12 — PERFORM CHANGE ANALYSIS
        # ====================================================

        result = (
            land_use_change_service.analyze_change(
                historical_file=str(
                    historical_path
                ),
                current_file=str(
                    current_path
                ),
                historical_parcel_column=(
                    historical_parcel_column
                ),
                historical_land_use_column=(
                    historical_land_use_column
                ),
                current_parcel_column=(
                    current_parcel_column
                ),
                current_land_use_column=(
                    current_land_use_column
                ),
            )
        )

        # ====================================================
        # STEP 13 — RETURN COMPLETE RESULT
        # ====================================================

        return {
            "success": True,

            "historical": {
                "filename": (
                    historical_file.filename
                ),
                "detected_fields": (
                    historical_fields
                ),
                "profile": (
                    historical_profile
                ),
            },

            "current": {
                "filename": (
                    current_file.filename
                ),
                "detected_fields": (
                    current_fields
                ),
                "profile": (
                    current_profile
                ),
            },

            "change_analysis": result,
        }

    except ValueError as error:

        # ----------------------------------------------------
        # Clean up uploaded files
        # ----------------------------------------------------

        if historical_path.exists():
            historical_path.unlink()

        if current_path.exists():
            current_path.unlink()

        raise HTTPException(
            status_code=400,
            detail=str(error),
        )

    except Exception as error:

        # ----------------------------------------------------
        # Clean up uploaded files
        # ----------------------------------------------------

        if historical_path.exists():
            historical_path.unlink()

        if current_path.exists():
            current_path.unlink()

        raise HTTPException(
            status_code=500,
            detail=(
                "Land-use change analysis failed: "
                f"{str(error)}"
            ),
        )
# ============================================================
# 5. COMPLETE LAND INTELLIGENCE ANALYSIS
# ============================================================

@router.post("/complete")
async def complete_land_analysis(
    current_file: UploadFile = File(...),
    historical_file: UploadFile | None = File(None),
):
    """
    Complete land intelligence workflow.

    Current dataset:
        - profiling
        - land intelligence
        - base risk analysis

    Optional historical dataset:
        - automatic land-use detection
        - land-use change
        - integrated risk analysis
    """

    if not current_file.filename:

        raise HTTPException(
            status_code=400,
            detail="Current filename is missing.",
        )

    current_extension = Path(
        current_file.filename
    ).suffix.lower()

    if current_extension not in {
        ".csv",
        ".xlsx",
        ".xls",
    }:

        raise HTTPException(
            status_code=400,
            detail=(
                "Current dataset must be CSV or Excel."
            ),
        )

    current_name = (
        f"{uuid4().hex}"
        f"{current_extension}"
    )

    current_path = (
        UPLOAD_DIR
        / current_name
    )

    historical_path = None

    try:

        # ====================================================
        # SAVE CURRENT FILE
        # ====================================================

        current_contents = (
            await current_file.read()
        )

        with open(
            current_path,
            "wb",
        ) as output_file:

            output_file.write(
                current_contents
            )

        # ====================================================
        # PROFILE CURRENT FILE
        # ====================================================

        current_profile = (
            profiler_service.profile_file(
                str(current_path)
            )
        )

        current_fields = (
            current_profile.get(
                "detected_fields",
                {},
            )
        )

        # ====================================================
        # BASIC LAND INTELLIGENCE
        # ====================================================

        intelligence = (
            intelligence_service.analyze_file(
                file_path=str(
                    current_path
                ),
                detected_fields=current_fields,
            )
        )

        # ====================================================
        # HISTORICAL FILE
        # ====================================================

        historical_profile = None
        historical_fields = None

        if historical_file:

            if not historical_file.filename:

                raise HTTPException(
                    status_code=400,
                    detail=(
                        "Historical filename is missing."
                    ),
                )

            historical_extension = Path(
                historical_file.filename
            ).suffix.lower()

            if historical_extension not in {
                ".csv",
                ".xlsx",
                ".xls",
            }:

                raise HTTPException(
                    status_code=400,
                    detail=(
                        "Historical dataset must "
                        "be CSV or Excel."
                    ),
                )

            historical_name = (
                f"{uuid4().hex}"
                f"{historical_extension}"
            )

            historical_path = (
                UPLOAD_DIR
                / historical_name
            )

            historical_contents = (
                await historical_file.read()
            )

            with open(
                historical_path,
                "wb",
            ) as output_file:

                output_file.write(
                    historical_contents
                )

            historical_profile = (
                profiler_service.profile_file(
                    str(
                        historical_path
                    )
                )
            )

            historical_fields = (
                historical_profile.get(
                    "detected_fields",
                    {},
                )
            )

        # ====================================================
        # INTEGRATED RISK
        # ====================================================

        integrated_risk = (
            integrated_risk_service.analyze(
                current_file=str(
                    current_path
                ),
                current_detected_fields=(
                    current_fields
                ),
                historical_file=(
                    str(historical_path)
                    if historical_path
                    else None
                ),
                historical_detected_fields=(
                    historical_fields
                ),
            )
        )

        # ====================================================
        # RETURN
        # ====================================================

        return {
            "success": True,

            "current": {
                "filename": (
                    current_file.filename
                ),
                "stored_filename": (
                    current_name
                ),
                "profile": (
                    current_profile
                ),
                "analysis": (
                    intelligence
                ),
            },

            "historical": (
                {
                    "filename": (
                        historical_file.filename
                    ),
                    "stored_filename": (
                        historical_path.name
                    ),
                    "profile": (
                        historical_profile
                    ),
                }
                if historical_file
                else None
            ),

            "risk_analysis": (
                integrated_risk
            ),
        }

    except ValueError as error:

        if current_path.exists():
            current_path.unlink()

        if (
            historical_path
            and historical_path.exists()
        ):
            historical_path.unlink()

        raise HTTPException(
            status_code=400,
            detail=str(error),
        )

    except Exception as error:

        if current_path.exists():
            current_path.unlink()

        if (
            historical_path
            and historical_path.exists()
        ):
            historical_path.unlink()

        raise HTTPException(
            status_code=500,
            detail=(
                "Complete land analysis failed: "
                f"{str(error)}"
            ),
        )   
# ============================================================
# 6. GIS RISK HOTSPOTS
# ============================================================

@router.post("/hotspots")
async def generate_land_hotspots(
    current_file: UploadFile = File(...),
    historical_file: UploadFile | None = File(None),
):
    """
    Generate GeoJSON risk hotspots from uploaded
    land data.

    Current dataset must contain detectable:

        - parcel ID
        - latitude
        - longitude

    Optional historical dataset enables
    land-use change integration.
    """

    # ========================================================
    # VALIDATE CURRENT FILE
    # ========================================================

    if not current_file.filename:

        raise HTTPException(
            status_code=400,
            detail="Current filename is missing.",
        )

    current_extension = Path(
        current_file.filename
    ).suffix.lower()

    if current_extension not in {
        ".csv",
        ".xlsx",
        ".xls",
    }:

        raise HTTPException(
            status_code=400,
            detail=(
                "Current dataset must be CSV or Excel."
            ),
        )

    # ========================================================
    # SAVE CURRENT FILE
    # ========================================================

    current_name = (
        f"{uuid4().hex}"
        f"{current_extension}"
    )

    current_path = (
        UPLOAD_DIR
        / current_name
    )

    historical_path = None

    try:

        current_contents = (
            await current_file.read()
        )

        with open(
            current_path,
            "wb",
        ) as output_file:

            output_file.write(
                current_contents
            )

        # ====================================================
        # PROFILE CURRENT DATASET
        # ====================================================

        current_profile = (
            profiler_service.profile_file(
                str(current_path)
            )
        )

        current_fields = (
            current_profile.get(
                "detected_fields",
                {},
            )
        )

        # ====================================================
        # VALIDATE COORDINATES
        # ====================================================

        latitude_column = (
            current_fields.get(
                "latitude"
            )
        )

        longitude_column = (
            current_fields.get(
                "longitude"
            )
        )

        parcel_column = (
            current_fields.get(
                "parcel_id"
            )
        )

        if not latitude_column:

            raise ValueError(
                "Latitude field could not be detected "
                "in the current dataset."
            )

        if not longitude_column:

            raise ValueError(
                "Longitude field could not be detected "
                "in the current dataset."
            )

        if not parcel_column:

            raise ValueError(
                "Parcel ID field could not be detected "
                "in the current dataset."
            )

        # ====================================================
        # OPTIONAL HISTORICAL DATA
        # ====================================================

        historical_profile = None
        historical_fields = None

        if historical_file:

            if not historical_file.filename:

                raise HTTPException(
                    status_code=400,
                    detail=(
                        "Historical filename is missing."
                    ),
                )

            historical_extension = Path(
                historical_file.filename
            ).suffix.lower()

            if historical_extension not in {
                ".csv",
                ".xlsx",
                ".xls",
            }:

                raise HTTPException(
                    status_code=400,
                    detail=(
                        "Historical dataset must "
                        "be CSV or Excel."
                    ),
                )

            historical_name = (
                f"{uuid4().hex}"
                f"{historical_extension}"
            )

            historical_path = (
                UPLOAD_DIR
                / historical_name
            )

            historical_contents = (
                await historical_file.read()
            )

            with open(
                historical_path,
                "wb",
            ) as output_file:

                output_file.write(
                    historical_contents
                )

            historical_profile = (
                profiler_service.profile_file(
                    str(
                        historical_path
                    )
                )
            )

            historical_fields = (
                historical_profile.get(
                    "detected_fields",
                    {},
                )
            )

        # ====================================================
        # RUN INTEGRATED RISK ANALYSIS
        # ====================================================

        risk_result = (
            integrated_risk_service.analyze(
                current_file=str(
                    current_path
                ),
                current_detected_fields=(
                    current_fields
                ),
                historical_file=(
                    str(historical_path)
                    if historical_path
                    else None
                ),
                historical_detected_fields=(
                    historical_fields
                ),
            )
        )

        # ====================================================
        # EXTRACT PARCEL RISKS
        # ====================================================

        parcel_risks = _extract_parcel_risks(
            risk_result
        )

        risk_source = "integrated_land_risk_service"

        # If the integrated service returns no parcel-level records,
        # fall back to the existing LandRiskService. This prevents
        # the GIS layer from showing valid coordinates with Unknown
        # risk values.
        if not parcel_risks:

            fallback_risk_result = (
                risk_service.analyze_file(
                    file_path=str(current_path),
                    detected_fields=current_fields,
                )
            )

            parcel_risks = _extract_parcel_risks(
                fallback_risk_result
            )

            risk_source = "land_risk_service_fallback"

        if not parcel_risks:
            raise ValueError(
                "The land-risk engine returned no "
                "parcel-level risk records."
            )

        # ====================================================
        # CREATE GEOJSON
        # ====================================================

        geojson = (
            hotspot_service.create_geojson(
                file_path=str(
                    current_path
                ),
                detected_fields=(
                    current_fields
                ),
                parcel_risks=(
                    parcel_risks
                ),
            )
        )

        # ====================================================
        # RETURN
        # ====================================================

        return {
            "success": True,

            "filename": (
                current_file.filename
            ),

            "detected_fields": (
                current_fields
            ),

            "historical_available": (
                historical_file is not None
            ),

            "risk_summary": {
                "parcel_risks": len(
                    parcel_risks
                ),

                "risk_source": risk_source,

                "mapped_records": (
                    geojson[
                        "metadata"
                    ][
                        "mapped_records"
                    ]
                ),

                "skipped_records": (
                    geojson[
                        "metadata"
                    ][
                        "skipped_records"
                    ]
                ),

                "risk_distribution": (
                    geojson[
                        "metadata"
                    ][
                        "risk_distribution"
                    ]
                ),
            },

            "geojson": geojson,

            "risk_engine": {
                "source": risk_source,
                "parcel_risk_records": len(parcel_risks),
                "integrated_service_returned_records": bool(
                    _extract_parcel_risks(risk_result)
                ),
            },
        }

    except ValueError as error:

        if current_path.exists():
            current_path.unlink()

        if (
            historical_path
            and historical_path.exists()
        ):
            historical_path.unlink()

        raise HTTPException(
            status_code=400,
            detail=str(error),
        )

    except Exception as error:

        if current_path.exists():
            current_path.unlink()

        if (
            historical_path
            and historical_path.exists()
        ):
            historical_path.unlink()

        raise HTTPException(
            status_code=500,
            detail=(
                "GIS hotspot generation failed: "
                f"{str(error)}"
            ),
        ) 