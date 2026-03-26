import cv2
import numpy as np
import pytesseract
from PIL import Image
from pathlib import Path
from app.config import settings

pytesseract.pytesseract.tesseract_cmd = settings.TESSERACT_PATH


def load_image(image_path: str) -> np.ndarray:
    """Load image from path into OpenCV format."""
    img = cv2.imread(image_path)
    if img is None:
        # fallback via Pillow (handles more formats)
        pil_img = Image.open(image_path).convert("RGB")
        img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
    return img


def deskew(image: np.ndarray) -> np.ndarray:
    """Straighten a rotated/skewed image."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.bitwise_not(gray)
    coords = np.column_stack(np.where(gray > 0))
    if len(coords) == 0:
        return image
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    return cv2.warpAffine(
        image, M, (w, h),
        flags=cv2.INTER_CUBIC,
        borderMode=cv2.BORDER_REPLICATE
    )


def preprocess(image_path: str) -> Image.Image:
    """
    Smart preprocessing:
    - For clean digital images: return as-is (Tesseract reads them fine)
    - For dark/noisy images: apply deskew + threshold
    """
    pil_img = Image.open(image_path).convert("RGB")
    img_array = np.array(pil_img)

    # Check average brightness — clean images are mostly white (>200)
    gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
    avg_brightness = gray.mean()

    if avg_brightness > 180:
        # Clean image — return PIL directly, no processing needed
        return pil_img

    # Dark/scanned image — apply full preprocessing
    img_cv = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
    img_cv = deskew(img_cv)
    gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
    denoised = cv2.fastNlMeansDenoising(gray, h=10)
    _, thresh = cv2.threshold(
        denoised, 0, 255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )
    return Image.fromarray(thresh)


def extract_text(image_path: str, psm: int = 6) -> str:
    """Extract plain text from image using Tesseract."""
    img = preprocess(image_path)
    config = f"--psm {psm} --oem 3"
    return pytesseract.image_to_string(img, config=config)


def extract_words_with_boxes(image_path: str) -> list[dict]:
    """Extract each word with bounding box and confidence score."""
    img = preprocess(image_path)
    data = pytesseract.image_to_data(
        img,
        output_type=pytesseract.Output.DICT,
        config="--psm 6"
    )
    words = []
    for i in range(len(data["text"])):
        word = data["text"][i].strip()
        conf = int(data["conf"][i])
        if word and conf > 30:
            words.append({
                "text": word,
                "conf": conf,
                "x":    data["left"][i],
                "y":    data["top"][i],
                "w":    data["width"][i],
                "h":    data["height"][i],
            })
    return words