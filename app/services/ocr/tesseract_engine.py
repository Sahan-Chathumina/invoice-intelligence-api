import pytesseract
from PIL import Image

# Explicit binding (safe even if PATH breaks elsewhere)
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

def extract_text_from_image(image: Image.Image) -> str:
    """
    Extract raw text from a PIL image using Tesseract OCR.
    """
    return pytesseract.image_to_string(
        image,
        lang="eng",
        config="--oem 3 --psm 6"
    ).strip()
