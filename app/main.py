from fastapi import FastAPI
from app.api.v1.router import router as api_v1_router

app = FastAPI(
    title="Invoice & Receipt Intelligence API",
    version="1.0.0",
    description="Extract structured data from invoices and receipts",
)

# Versioned API
app.include_router(api_v1_router)

# Public health check
@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}
