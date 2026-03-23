import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer
from reportlab.lib import colors
from app.utils.file_utils import make_output_path
import json


def excel_to_csv(input_path: str) -> str:
    """Convert first sheet of Excel to CSV."""
    output_path = make_output_path(input_path, "csv")
    df = pd.read_excel(input_path, sheet_name=0)
    df.to_csv(output_path, index=False)
    return output_path


def excel_to_json(input_path: str) -> str:
    """Convert all sheets of Excel to JSON."""
    output_path = make_output_path(input_path, "json")
    xl = pd.ExcelFile(input_path)
    result = {}
    for sheet in xl.sheet_names:
        df = xl.parse(sheet)
        result[sheet] = df.to_dict(orient="records")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, default=str)
    return output_path


def excel_to_html(input_path: str) -> str:
    """Convert Excel to styled HTML table."""
    output_path = make_output_path(input_path, "html")
    df = pd.read_excel(input_path, sheet_name=0)
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


def excel_to_pdf(input_path: str) -> str:
    """Convert Excel data to PDF table."""
    output_path = make_output_path(input_path, "pdf")
    df = pd.read_excel(input_path, sheet_name=0)
    df = df.fillna("").astype(str)

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


def csv_to_excel(input_path: str) -> str:
    """Convert CSV to Excel."""
    output_path = make_output_path(input_path, "xlsx")
    df = pd.read_csv(input_path)
    df.to_excel(output_path, index=False)
    return output_path