from fastapi import APIRouter
from app.api.v1.extract import router as invoice_router

api_router = APIRouter()

api_router.include_router(invoice_router)
