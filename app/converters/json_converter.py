import pandas as pd
from app.utils.file_utils import make_output_path
import json


def json_to_csv(input_path: str) -> str:
    """Convert JSON array to CSV."""
    output_path = make_output_path(input_path, "csv")
    with open(input_path, encoding="utf-8") as f:
        data = json.load(f)
    # Handle nested dict (multi-sheet style) or flat list
    if isinstance(data, dict):
        data = list(data.values())[0]
    df = pd.json_normalize(data)
    df.to_csv(output_path, index=False)
    return output_path


def json_to_excel(input_path: str) -> str:
    """Convert JSON to Excel."""
    output_path = make_output_path(input_path, "xlsx")
    with open(input_path, encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, dict):
        data = list(data.values())[0]
    df = pd.json_normalize(data)
    df.to_excel(output_path, index=False)
    return output_path


def json_to_html(input_path: str) -> str:
    """Convert JSON to HTML table."""
    output_path = make_output_path(input_path, "html")
    with open(input_path, encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, dict):
        data = list(data.values())[0]
    df = pd.json_normalize(data)
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


def json_to_txt(input_path: str) -> str:
    """Convert JSON to readable plain text."""
    output_path = make_output_path(input_path, "txt")
    with open(input_path, encoding="utf-8") as f:
        data = json.load(f)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(json.dumps(data, indent=2))
    return output_path