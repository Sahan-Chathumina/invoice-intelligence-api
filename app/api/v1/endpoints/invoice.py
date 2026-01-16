from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from PIL import Image
import io
from typing import List

from app.core.auth import verify_api_key
from app.services.ocr.image_preprocessor import preprocess_image
from app.services.ocr.tesseract_engine import extract_text_from_image
from app.services.ocr.pdf_handler import pdf_to_images
from app.models.response import InvoiceOCRResponse

router = APIRouter(
    dependencies=[Depends(verify_api_key)]
)

@router.post(
    "/extract",
    summary="Extract OCR text from invoice documents",
    description=(
        "Uploads an invoice image or PDF and extracts raw OCR text.\n\n"
        "Supported formats:\n"
        "- image/png\n"
        "- image/jpeg\n"
        "- application/pdf"
    ),
    response_model=InvoiceOCRResponse,
)
async def extract_invoice(file: UploadFile = File(...)):

    if not file.content_type:
        raise HTTPException(status_code=400, detail="Missing content type")

    allowed_types = {
        "image/png",
        "image/jpeg",
        "application/pdf",
    }

    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=415,
            detail=f"Unsupported file type: {file.content_type}",
        )

    content = await file.read()
    extracted_text_parts: List[str] = []

    try:
        if file.content_type == "application/pdf":
            images = pdf_to_images(content)
            if not images:
                raise HTTPException(status_code=400, detail="PDF contains no images")

            for img in images:
                processed = preprocess_image(img)
                text = extract_text_from_image(processed)
                if text:
                    extracted_text_parts.append(text)
        else:
            image = Image.open(io.BytesIO(content))
            processed = preprocess_image(image)
            text = extract_text_from_image(processed)
            if text:
                extracted_text_parts.append(text)

        raw_text = "\n".join(extracted_text_parts).strip()

        if not raw_text:
            raise HTTPException(status_code=422, detail="No text extracted")

        return InvoiceOCRResponse(
            filename=file.filename,
            content_type=file.content_type,
            raw_text=raw_text,
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
