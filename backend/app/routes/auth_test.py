from fastapi import APIRouter, Depends

from app.services.rbac_service import (
    get_current_user,
    require_roles
)


router = APIRouter(
    prefix="/auth-test",
    tags=["RBAC Test"]
)


# ============================================================
# ANY AUTHENTICATED USER
# ============================================================

@router.get("/me")
def get_me(
    current_user = Depends(
        get_current_user
    )
):

    return {
        "authenticated": True,
        "user": current_user
    }


# ============================================================
# ADMIN ONLY
# ============================================================

@router.get("/admin")
def admin_test(
    current_user = Depends(
        require_roles(
            ["ADMIN"]
        )
    )
):

    return {
        "message":
            "Admin access granted.",
        "user":
            current_user
    }


# ============================================================
# RESEARCHER + ADMIN
# ============================================================

@router.get("/research")
def research_test(
    current_user = Depends(
        require_roles(
            [
                "ADMIN",
                "RESEARCHER"
            ]
        )
    )
):

    return {
        "message":
            "Research access granted.",
        "user":
            current_user
    }


# ============================================================
# POLICY MAKER + ADMIN
# ============================================================

@router.get("/policy")
def policy_test(
    current_user = Depends(
        require_roles(
            [
                "ADMIN",
                "POLICY_MAKER"
            ]
        )
    )
):

    return {
        "message":
            "Policy access granted.",
        "user":
            current_user
    }