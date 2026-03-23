from app.converters.pdf_converter   import pdf_to_txt, pdf_to_docx, pdf_to_csv, pdf_to_json
from app.converters.docx_converter  import docx_to_txt, docx_to_pdf, docx_to_html, docx_to_csv
from app.converters.excel_converter import excel_to_csv, excel_to_json, excel_to_html, excel_to_pdf, csv_to_excel
from app.converters.csv_converter   import csv_to_json, csv_to_html, csv_to_pdf
from app.converters.json_converter  import json_to_csv, json_to_excel, json_to_html, json_to_txt
from app.converters.html_converter  import html_to_txt, html_to_pdf, html_to_docx
from app.converters.xml_converter   import xml_to_json, xml_to_csv, xml_to_html
from app.converters.pptx_converter  import pptx_to_txt, pptx_to_pdf, pptx_to_html
from app.converters.image_converter import image_to_txt, image_to_pdf, image_to_docx, image_to_json
from app.utils.file_utils           import get_file_format, make_output_path
from app.utils.validators           import validate_conversion
import time

# ─── Registry ────────────────────────────────────────────────────────────────
CONVERTERS = {
    # PDF
    ("pdf",   "txt"):  pdf_to_txt,
    ("pdf",   "docx"): pdf_to_docx,
    ("pdf",   "csv"):  pdf_to_csv,
    ("pdf",   "json"): pdf_to_json,

    # DOCX
    ("docx",  "txt"):  docx_to_txt,
    ("docx",  "pdf"):  docx_to_pdf,
    ("docx",  "html"): docx_to_html,
    ("docx",  "csv"):  docx_to_csv,

    # Excel
    ("xlsx",  "csv"):  excel_to_csv,
    ("xlsx",  "json"): excel_to_json,
    ("xlsx",  "html"): excel_to_html,
    ("xlsx",  "pdf"):  excel_to_pdf,

    # CSV
    ("csv",   "xlsx"): csv_to_excel,
    ("csv",   "json"): csv_to_json,
    ("csv",   "html"): csv_to_html,
    ("csv",   "pdf"):  csv_to_pdf,

    # JSON
    ("json",  "csv"):  json_to_csv,
    ("json",  "xlsx"): json_to_excel,
    ("json",  "html"): json_to_html,
    ("json",  "txt"):  json_to_txt,

    # HTML
    ("html",  "txt"):  html_to_txt,
    ("html",  "pdf"):  html_to_pdf,
    ("html",  "docx"): html_to_docx,

    # XML
    ("xml",   "json"): xml_to_json,
    ("xml",   "csv"):  xml_to_csv,
    ("xml",   "html"): xml_to_html,

    # PPTX
    ("pptx",  "txt"):  pptx_to_txt,
    ("pptx",  "pdf"):  pptx_to_pdf,
    ("pptx",  "html"): pptx_to_html,

    # Image
    ("image", "txt"):  image_to_txt,
    ("image", "pdf"):  image_to_pdf,
    ("image", "docx"): image_to_docx,
    ("image", "json"): image_to_json,
}


def convert(input_path: str, output_format: str) -> dict:
    """
    Main conversion function.
    Returns dict with output_path, input_format, duration_ms.
    """
    # Validate
    input_format = validate_conversion(input_path, output_format)

    # Look up converter
    fn = CONVERTERS.get((input_format, output_format))
    if not fn:
        raise ValueError(f"No converter found for {input_format} → {output_format}")

    # Run conversion and time it
    start = time.time()
    output_path = fn(input_path)
    duration_ms = int((time.time() - start) * 1000)

    return {
        "input_path":    input_path,
        "output_path":   output_path,
        "input_format":  input_format,
        "output_format": output_format,
        "duration_ms":   duration_ms,
        "status":        "success",
    }


def get_all_conversions() -> list[dict]:
    """Return all supported conversion pairs."""
    return [
        {"input": inp, "output": out}
        for inp, out in sorted(CONVERTERS.keys())
    ]