from fastapi import APIRouter
from app.api.v1.extract import router as extract_router

api_router = APIRouter()

api_router.include_router(extract_router)
