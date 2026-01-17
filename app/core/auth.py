from fastapi import Header, HTTPException, status
import os

LOCAL_API_KEY = os.getenv("INVOICE_API_KEY")

def verify_api_key(
    x_api_key: str | None = Header(default=None, alias="X-API-Key"),
    x_rapidapi_key: str | None = Header(default=None, alias="X-RapidAPI-Key"),
):
    """
    Auth rules:
    - RapidAPI traffic uses X-RapidAPI-Key (Swagger should not expose it)
    - Direct traffic uses X-API-Key
    """

    # RapidAPI request (trusted)
    if x_rapidapi_key:
        return

    # Direct access (Render / local)
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
