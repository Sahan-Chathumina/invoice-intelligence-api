from fastapi import APIRouter, UploadFile, File, HTTPException, status
from PIL import Image, UnidentifiedImageError
from typing import List
import io

from app.services.ocr.image_preprocessor import preprocess_image
from app.services.ocr.tesseract_engine import extract_text_from_image
from app.services.ocr.pdf_handler import pdf_to_images

router = APIRouter(
    prefix="/invoice",
    tags=["Invoice Intelligence"],
)


SUPPORTED_CONTENT_TYPES = {
    "image/png",
    "image/jpeg",
    "application/pdf",
}


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
)
async def extract_invoice(file: UploadFile = File(...)):
    """
    Extract raw OCR text from invoice images or PDFs.

    This endpoint performs:
    1. File validation
    2. PDF-to-image conversion (if applicable)
    3. Image preprocessing
    4. OCR text extraction using Tesseract

    Returns extracted raw text suitable for downstream parsing.
    """

    # --- Validate content type ---
    if not file.content_type:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unable to detect file content type",
        )

    if file.content_type not in SUPPORTED_CONTENT_TYPES:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"Unsupported file type: {file.content_type}",
        )

    # --- Read file content ---
    try:
        content: bytes = await file.read()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to read uploaded file",
        )

    if not content:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file is empty",
        )

    extracted_text_parts: List[str] = []

    try:
        # --- PDF handling ---
        if file.content_type == "application/pdf":
            images = pdf_to_images(content)

            if not images:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="No images could be extracted from the PDF",
                )

            for image in images:
                processed_image = preprocess_image(image)
                text = extract_text_from_image(processed_image)
                if text:
                    extracted_text_parts.append(text)

        # --- Image handling ---
        else:
            try:
                image = Image.open(io.BytesIO(content))
            except UnidentifiedImageError:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="Invalid or corrupted image file",
                )

            processed_image = preprocess_image(image)
            text = extract_text_from_image(processed_image)
            if text:
                extracted_text_parts.append(text)

    except HTTPException:
        # Re-raise controlled exceptions
        raise

    except Exception as e:
        # Catch-all for OCR engine / system failures
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"OCR processing failed: {str(e)}",
        )

    # --- Final text aggregation ---
    extracted_text = "\n".join(extracted_text_parts).strip()

    if not extracted_text:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="No text could be extracted from the document",
        )

    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "raw_text": extracted_text,
    }
