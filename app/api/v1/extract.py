from fastapi import APIRouter

router = APIRouter()

@router.post("/extract")
def extract_invoice():
    return {"message": "Invoice extraction endpoint (WIP)"}
