from fastapi import APIRouter, UploadFile, File

router = APIRouter()

@router.post("/extract")
async def extract_invoice(file: UploadFile = File(...)):
    return {
        "invoice_type": "utility",
        "confidence_score": 0.92
    }
