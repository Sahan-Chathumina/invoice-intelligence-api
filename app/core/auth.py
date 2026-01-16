import os
from typing import Annotated
from fastapi import Header, HTTPException, status

# Internal API key (Render / Docker / self-hosted only)
LOCAL_API_KEY = os.getenv("INVOICE_API_KEY")


def verify_api_key(
    # Visible in Swagger (RapidAPI users)
    x_rapidapi_key: Annotated[
        str | None,
        Header(
            alias="X-RapidAPI-Key",
            include_in_schema=True,
            description="Automatically provided by RapidAPI",
        ),
    ] = None,

    # Hidden from Swagger (internal use only)
    x_api_key: Annotated[
        str | None,
        Header(
            alias="X-API-Key",
            include_in_schema=False,
        ),
    ] = None,
):
    """
    Auth logic:
    - RapidAPI traffic is trusted via X-RapidAPI-Key
    - Direct traffic must provide X-API-Key (Render env var)
    """

    # RapidAPI request → allow
    if x_rapidapi_key:
        return

    # Direct request → require internal key
    if not LOCAL_API_KEY or x_api_key != LOCAL_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key",
        )
