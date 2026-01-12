import pytesseract
from PIL import Image
import shutil
import os


def _configure_tesseract():
    """
    Configure Tesseract dynamically for Windows, Linux, Docker, and Render.
    """
    # If explicitly set (advanced users)
    if os.getenv("TESSERACT_CMD"):
        pytesseract.pytesseract.tesseract_cmd = os.getenv("TESSERACT_CMD")
        return

    # Auto-detect from PATH
    tesseract_path = shutil.which("tesseract")
    if tesseract_path:
        pytesseract.pytesseract.tesseract_cmd = tesseract_path
        return

    # Windows fallback
    windows_default = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    if os.path.exists(windows_default):
        pytesseract.pytesseract.tesseract_cmd = windows_default
        return

    raise RuntimeError(
        "Tesseract OCR is not installed or not available in PATH"
    )


# Configure once at import time
_configure_tesseract()


def extract_text_from_image(image: Image.Image) -> str:
    """
    Perform OCR on a PIL Image and return extracted text.
    """
    return pytesseract.image_to_string(image, lang="eng")
