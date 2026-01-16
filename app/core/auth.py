from fastapi import Header, HTTPException, status
from fastapi.security.api_key import APIKeyHeader
import os

LOCAL_API_KEY = os.getenv("INVOICE_API_KEY")

rapidapi_key_header = APIKeyHeader(
    name="X-RapidAPI-Key",
    auto_error=False,
)

local_key_header = APIKeyHeader(
    name="X-API-Key",
    auto_error=False,
)

def verify_api_key(
    x_rapidapi_key: str = rapidapi_key_header,
    x_api_key: str = local_key_header,
):
    # RapidAPI traffic
    if x_rapidapi_key:
        return

    # Local / Render direct traffic
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
