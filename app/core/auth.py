import os
from fastapi import Header, HTTPException, status

# Local / self-hosted API key (used only outside RapidAPI)
LOCAL_API_KEY = os.getenv("INVOICE_API_KEY")


def verify_api_key(
    x_api_key: str | None = Header(default=None, alias="X-API-Key"),
    x_rapidapi_key: str | None = Header(default=None, alias="X-RapidAPI-Key"),
):
    """
    Authentication strategy:
    - If request comes via RapidAPI, trust X-RapidAPI-Key
    - Otherwise, require X-API-Key (local / Docker / self-hosted)
    """

    # RapidAPI request → auto-authenticated
    if x_rapidapi_key:
        return

    # Local / Docker usage
    if not LOCAL_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server API key not configured",
        )

    if x_api_key != LOCAL_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key",
        )
