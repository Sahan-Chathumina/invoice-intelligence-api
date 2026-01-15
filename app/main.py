from fastapi import FastAPI
from app.api.v1.router import api_router

app = FastAPI(
    title="Invoice & Receipt Intelligence API",
    version="1.0.0",
    description="Extract structured data from invoices and receipts"
)

app.include_router(api_router, prefix="/api/v1")

@app.get("/health")
def health_check():
    return {"status": "ok"}
