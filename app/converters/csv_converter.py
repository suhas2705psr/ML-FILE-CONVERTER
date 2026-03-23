import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from app.utils.file_utils import make_output_path
import json


def csv_to_json(input_path: str) -> str:
    """Convert CSV to JSON."""
    output_path = make_output_path(input_path, "json")
    df = pd.read_csv(input_path)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(df.to_dict(orient="records"), f, indent=2, default=str)
    return output_path


def csv_to_html(input_path: str) -> str:
    """Convert CSV to styled HTML table."""
    output_path = make_output_path(input_path, "html")
    df = pd.read_csv(input_path)
    html = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset='utf-8'>
  <style>
    body {{ font-family: Arial, sans-serif; padding: 20px; }}
    table {{ border-collapse: collapse; width: 100%; }}
    th {{ background-color: #1A1A2E; color: white; padding: 8px 12px; }}
    td {{ border: 1px solid #ddd; padding: 8px 12px; }}
    tr:nth-child(even) {{ background-color: #f2f2f2; }}
  </style>
</head>
<body>
{df.to_html(index=False)}
</body>
</html>"""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    return output_path


def csv_to_pdf(input_path: str) -> str:
    """Convert CSV to PDF table."""
    output_path = make_output_path(input_path, "pdf")
    df = pd.read_csv(input_path).fillna("").astype(str)
    data = [list(df.columns)] + df.values.tolist()
    table = Table(data)
    table.setStyle(TableStyle([
        ("BACKGROUND",  (0, 0), (-1, 0), colors.HexColor("#1A1A2E")),
        ("TEXTCOLOR",   (0, 0), (-1, 0), colors.white),
        ("FONTNAME",    (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE",    (0, 0), (-1, -1), 8),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#EEF2FF")]),
        ("GRID",        (0, 0), (-1, -1), 0.5, colors.grey),
        ("PADDING",     (0, 0), (-1, -1), 6),
    ]))
    doc = SimpleDocTemplate(output_path, pagesize=letter)
    doc.build([table])
    return output_path