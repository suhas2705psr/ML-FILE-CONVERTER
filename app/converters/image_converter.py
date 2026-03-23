import pytesseract
import cv2
import numpy as np
from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from docx import Document
from app.config import settings
from app.utils.file_utils import make_output_path
import json

pytesseract.pytesseract.tesseract_cmd = settings.TESSERACT_PATH


def preprocess_image(image_path: str) -> np.ndarray:
    """Clean up image for better OCR accuracy."""
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    denoised = cv2.fastNlMeansDenoising(gray, h=10)
    _, thresh = cv2.threshold(
        denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )
    return thresh


def extract_text_from_image(image_path: str) -> str:
    """Run OCR and return extracted text."""
    img = preprocess_image(image_path)
    return pytesseract.image_to_string(img, config="--psm 6")


def image_to_txt(input_path: str) -> str:
    """Extract text from image and save as TXT."""
    output_path = make_output_path(input_path, "txt")
    text = extract_text_from_image(input_path)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)
    return output_path


def image_to_pdf(input_path: str) -> str:
    """Convert image with OCR text to PDF."""
    output_path = make_output_path(input_path, "pdf")
    text = extract_text_from_image(input_path)
    styles = getSampleStyleSheet()
    story = []
    for line in text.split("\n"):
        if line.strip():
            story.append(Paragraph(line.strip(), styles["Normal"]))
            story.append(Spacer(1, 4))
    doc = SimpleDocTemplate(output_path, pagesize=letter)
    doc.build(story)
    return output_path


def image_to_docx(input_path: str) -> str:
    """Convert image with OCR text to DOCX."""
    output_path = make_output_path(input_path, "docx")
    text = extract_text_from_image(input_path)
    doc = Document()
    for line in text.split("\n"):
        if line.strip():
            doc.add_paragraph(line.strip())
    doc.save(output_path)
    return output_path


def image_to_json(input_path: str) -> str:
    """Extract OCR text with bounding boxes to JSON."""
    output_path = make_output_path(input_path, "json")
    img = preprocess_image(input_path)
    data = pytesseract.image_to_data(
        img, output_type=pytesseract.Output.DICT
    )
    words = [
        {
            "text": data["text"][i],
            "confidence": data["conf"][i],
            "x": data["left"][i],
            "y": data["top"][i],
        }
        for i in range(len(data["text"]))
        if data["text"][i].strip() and int(data["conf"][i]) > 0
    ]
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(words, f, indent=2)
    return output_path