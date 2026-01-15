import os
from fastapi import HTTPException, Security, status
from fastapi.security.api_key import APIKeyHeader

# Environment variable for local / Docker usage
LOCAL_API_KEY = os.getenv("INVOICE_API_KEY")

# Security headers (hidden from Swagger)
x_api_key_header = APIKeyHeader(
    name="X-API-Key",
    auto_error=False,
    scheme_name=None,
)

x_rapidapi_key_header = APIKeyHeader(
    name="X-RapidAPI-Key",
    auto_error=False,
    scheme_name=None,
)


def verify_api_key(
    x_api_key: str | None = Security(x_api_key_header),
    x_rapidapi_key: str | None = Security(x_rapidapi_key_header),
) -> None:
    """
    Authentication logic:
    - RapidAPI calls include X-RapidAPI-Key → trusted
    - Direct / Docker calls must include X-API-Key
    """

    # RapidAPI request → trust RapidAPI gateway
    if x_rapidapi_key:
        return

    # Local / Docker request
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
