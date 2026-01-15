import os
from fastapi import Header, HTTPException, status

LOCAL_API_KEY = os.getenv("INVOICE_API_KEY")


def verify_api_key(
    x_api_key: str | None = Header(
        default=None,
        alias="X-API-Key",
        include_in_schema=True,   # shown in Swagger
    ),
    x_rapidapi_key: str | None = Header(
        default=None,
        alias="X-RapidAPI-Key",
        include_in_schema=False,  # HIDDEN from Swagger
    ),
):
    """
    Authentication strategy:
    - RapidAPI requests are authenticated by the gateway
    - Local/self-hosted requests require X-API-Key
    """

    # RapidAPI gateway already validated the request
    if x_rapidapi_key:
        return

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
