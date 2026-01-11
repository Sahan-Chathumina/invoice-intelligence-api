from fastapi import APIRouter, UploadFile, File, HTTPException
from PIL import Image
import io

from app.services.ocr.image_preprocessor import preprocess_image
from app.services.ocr.tesseract_engine import extract_text_from_image
from app.services.ocr.pdf_handler import pdf_to_images

router = APIRouter(prefix="/invoice", tags=["Invoice Intelligence"])


@router.post("/extract")
async def extract_invoice(file: UploadFile = File(...)):
    """
    Extract raw OCR text from invoice images or PDFs.

    Supported formats:
    - image/png
    - image/jpeg
    - application/pdf
    """

    if not file.content_type:
        raise HTTPException(status_code=400, detail="File type not detected")

    if file.content_type not in [
        "image/png",
        "image/jpeg",
        "application/pdf",
    ]:
        raise HTTPException(
            status_code=415,
            detail=f"Unsupported file type: {file.content_type}",
        )

    content = await file.read()
    extracted_text_parts: list[str] = []

    try:
        # PDF handling
        if file.content_type == "application/pdf":
            images = pdf_to_images(content)

            if not images:
                raise HTTPException(
                    status_code=400,
                    detail="No images extracted from PDF",
                )

            for image in images:
                processed_image = preprocess_image(image)
                text = extract_text_from_image(processed_image)
                extracted_text_parts.append(text)

        # Image handling
        else:
            image = Image.open(io.BytesIO(content))
            processed_image = preprocess_image(image)
            text = extract_text_from_image(processed_image)
            extracted_text_parts.append(text)

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"OCR processing failed: {str(e)}",
        )

    extracted_text = "\n".join(extracted_text_parts).strip()

    if not extracted_text:
        raise HTTPException(
            status_code=422,
            detail="No text could be extracted from the document",
        )

    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "raw_text": extracted_text,
    }
