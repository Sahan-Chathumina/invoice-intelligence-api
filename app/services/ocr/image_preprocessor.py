import cv2
import numpy as np
from PIL import Image

def preprocess_image(image: Image.Image) -> Image.Image:
    """
    Improve image quality before OCR:
    - grayscale
    - binarization (Otsu)
    """
    img = np.array(image)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(
        gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )
    return Image.fromarray(thresh)
