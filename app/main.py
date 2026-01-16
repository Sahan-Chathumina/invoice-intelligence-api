from fastapi import FastAPI
from app.api.v1.router import router as api_v1_router

app = FastAPI(
    title="Invoice Intelligence API",
    description="Invoice OCR and structured data extraction API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.include_router(api_v1_router)

@app.get("/ping", include_in_schema=False)
def ping():
    return {"status": "ok"}
