import pdfplumber
from docx import Document
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from app.utils.file_utils import make_output_path
import json
import csv


def pdf_to_txt(input_path: str) -> str:
    """Extract all text from PDF and save as .txt"""
    output_path = make_output_path(input_path, "txt")
    with pdfplumber.open(input_path) as pdf:
        text = "\n\n".join(
            page.extract_text() or "" for page in pdf.pages
        )
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)
    return output_path


def pdf_to_docx(input_path: str) -> str:
    """Convert PDF text content to a DOCX file."""
    output_path = make_output_path(input_path, "docx")
    doc = Document()
    with pdfplumber.open(input_path) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text() or ""
            if i > 0:
                doc.add_page_break()
            for line in text.split("\n"):
                doc.add_paragraph(line)
    doc.save(output_path)
    return output_path


def pdf_to_csv(input_path: str) -> str:
    """Extract tables from PDF and save as CSV."""
    output_path = make_output_path(input_path, "csv")
    rows = []
    with pdfplumber.open(input_path) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                rows.extend(table)
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(rows)
    return output_path


def pdf_to_json(input_path: str) -> str:
    """Extract text per page from PDF and save as JSON."""
    output_path = make_output_path(input_path, "json")
    pages = []
    with pdfplumber.open(input_path) as pdf:
        for i, page in enumerate(pdf.pages):
            pages.append({
                "page": i + 1,
                "text": page.extract_text() or "",
                "tables": page.extract_tables() or [],
            })
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(pages, f, indent=2)
    return output_path