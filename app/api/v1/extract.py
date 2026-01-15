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
    prefix="/invoice",
    tags=["Invoice Intelligence"],
    dependencies=[Depends(verify_api_key)],
)


@router.post(
    "/extract",
    summary="Extract OCR text from invoice documents",
    description=(
        "Accepts invoice images or PDFs and extracts raw OCR text.\n\n"
        "Supported formats:\n"
        "- image/png\n"
        "- image/jpeg\n"
        "- application/pdf"
    ),
    response_model=InvoiceOCRResponse,
)
async def extract_invoice(file: UploadFile = File(...)):
    """
    Extract raw OCR text from invoice images or PDFs.

    Processing steps:
    1. Validate file type
    2. Convert PDF pages to images (if applicable)
    3. Preprocess image(s)
    4. Extract text using Tesseract OCR
    """

    if not file.content_type:
        raise HTTPException(
            status_code=400,
            detail="File content type could not be detected",
        )

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

    try:
        content = await file.read()
        extracted_text_parts: List[str] = []

        # PDF handling
        if file.content_type == "application/pdf":
            images = pdf_to_images(content)

            if not images:
                raise HTTPException(
                    status_code=400,
                    detail="No images could be extracted from the PDF",
                )

            for image in images:
                processed = preprocess_image(image)
                text = extract_text_from_image(processed)
                if text:
                    extracted_text_parts.append(text)

        # Image handling
        else:
            image = Image.open(io.BytesIO(content))
            processed = preprocess_image(image)
            text = extract_text_from_image(processed)
            if text:
                extracted_text_parts.append(text)

        extracted_text = "\n".join(extracted_text_parts).strip()

        if not extracted_text:
            raise HTTPException(
                status_code=422,
                detail="No text could be extracted from the document",
            )

        return InvoiceOCRResponse(
            filename=file.filename,
            content_type=file.content_type,
            raw_text=extracted_text,
        )

    except HTTPException:
        raise

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"OCR processing failed: {str(exc)}",
        )
