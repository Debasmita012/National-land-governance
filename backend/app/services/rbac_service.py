from typing import List

from fastapi import Depends, HTTPException
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer
)

from app.services.auth_service import (
    decode_access_token
)


security = HTTPBearer()


# ============================================================
# CURRENT USER
# ============================================================

def get_current_user(
    credentials:
        HTTPAuthorizationCredentials = Depends(
            security
        )
):

    token = credentials.credentials

    payload = decode_access_token(
        token
    )


    if not payload:

        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token."
        )


    username = payload.get(
        "sub"
    )

    role = payload.get(
        "role"
    )


    if not username or not role:

        raise HTTPException(
            status_code=401,
            detail="Invalid authentication payload."
        )


    return {
        "username": username,
        "role": role
    }


# ============================================================
# ROLE CHECK
# ============================================================

def require_roles(
    allowed_roles: List[str]
):

    def role_checker(
        current_user = Depends(
            get_current_user
        )
    ):

        if (
            current_user["role"]
            not in allowed_roles
        ):

            raise HTTPException(
                status_code=403,
                detail=(
                    "Access denied. "
                    "Required role: "
                    +
                    ", ".join(
                        allowed_roles
                    )
                )
            )


        return current_user


    return role_checker