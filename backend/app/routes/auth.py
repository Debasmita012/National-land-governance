from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.auth_service import (
    verify_password,
    create_access_token
)


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


# ============================================================
# DEMO USERS
# ============================================================

USERS = {

    "admin": {
        "username": "admin",
        "password": "admin123",
        "role": "ADMIN"
    },

    "researcher": {
        "username": "researcher",
        "password": "research123",
        "role": "RESEARCHER"
    },

    "policymaker": {
        "username": "policymaker",
        "password": "policy123",
        "role": "POLICY_MAKER"
    }
}


# ============================================================
# REQUEST
# ============================================================

class LoginRequest(
    BaseModel
):

    username: str

    password: str


# ============================================================
# LOGIN
# ============================================================

@router.post("/login")
def login(
    request: LoginRequest
):

    user = USERS.get(
        request.username
    )


    if not user:

        raise HTTPException(
            status_code=401,
            detail="Invalid username or password."
        )


    # --------------------------------------------------------
    # Demo credentials
    # --------------------------------------------------------

    if (
        request.password
        !=
        user["password"]
    ):

        raise HTTPException(
            status_code=401,
            detail="Invalid username or password."
        )


    token = create_access_token(
        username=user["username"],
        role=user["role"]
    )


    return {

        "access_token": token,

        "token_type": "bearer",

        "user": {
            "username":
                user["username"],

            "role":
                user["role"]
        }
    }