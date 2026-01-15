from fastapi import APIRouter, Depends
from app.core.auth import verify_api_key

api_router = APIRouter(
    prefix="/invoice",
    tags=["Invoice Intelligence"],
    dependencies=[Depends(verify_api_key)],
)

from app.api.v1.extract import router as extract_router

api_router.include_router(extract_router)
