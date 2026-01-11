from fastapi import APIRouter, UploadFile, File, HTTPException
from PIL import Image
import io

from app.services.ocr.image_preprocessor import preprocess_image
from app.services.ocr.tesseract_engine import extract_text_from_image
from app.services.ocr.pdf_handler import pdf_to_images

router = APIRouter()

@router.post("/extract")
async def extract_invoice(file: UploadFile = File(...)):
    content = await file.read()
    extracted_text = ""

    if file.content_type == "application/pdf":
        images = pdf_to_images(content)
        for img in images:
            processed = preprocess_image(img)
            extracted_text += extract_text_from_image(processed) + "\n"
    else:
        image = Image.open(io.BytesIO(content))
        processed = preprocess_image(image)
        extracted_text = extract_text_from_image(processed)

    return {
        "raw_text": extracted_text
    }

