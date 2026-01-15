from fastapi import Header, HTTPException, status
import os

API_KEY = os.getenv("API_KEY")


def verify_api_key(x_api_key: str = Header(..., alias="X-API-Key")):
    if API_KEY is None:
        raise RuntimeError("API_KEY environment variable not set")

    if x_api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key",
        )
