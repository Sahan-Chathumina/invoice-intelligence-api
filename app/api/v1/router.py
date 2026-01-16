from fastapi import APIRouter
from app.api.v1.endpoints import invoice

router = APIRouter()

router.include_router(
    invoice.router,
    prefix="/invoice",
    tags=["Invoice"]
)
