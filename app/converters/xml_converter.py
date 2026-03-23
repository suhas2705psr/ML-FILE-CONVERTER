import pandas as pd
import lxml.etree as ET
from app.utils.file_utils import make_output_path
import json


def xml_to_json(input_path: str) -> str:
    """Convert XML to JSON."""
    output_path = make_output_path(input_path, "json")
    tree = ET.parse(input_path)
    root = tree.getroot()

    def element_to_dict(el):
        result = {}
        for child in el:
            tag = child.tag.split("}")[-1]  # strip namespace
            result[tag] = element_to_dict(child) if len(child) else child.text
        return result or el.text

    data = {root.tag.split("}")[-1]: element_to_dict(root)}
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    return output_path


def xml_to_csv(input_path: str) -> str:
    """Convert XML records to CSV using pandas."""
    output_path = make_output_path(input_path, "csv")
    tree = ET.parse(input_path)
    root = tree.getroot()
    records = []
    for child in root:
        record = {}
        for el in child:
            tag = el.tag.split("}")[-1]
            record[tag] = el.text
        if record:
            records.append(record)
    df = pd.DataFrame(records)
    df.to_csv(output_path, index=False)
    return output_path


def xml_to_html(input_path: str) -> str:
    """Convert XML to readable HTML."""
    output_path = make_output_path(input_path, "html")
    tree = ET.parse(input_path)
    root = tree.getroot()
    rows = ""
    for child in root:
        rows += "<tr>"
        for el in child:
            rows += f"<td>{el.text or ''}</td>"
        rows += "</tr>"
    headers = ""
    first = next(iter(root), None)
    if first is not None:
        for el in first:
            headers += f"<th>{el.tag.split('}')[-1]}</th>"
    html = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset='utf-8'>
  <style>
    body {{ font-family: Arial; padding: 20px; }}
    table {{ border-collapse: collapse; width: 100%; }}
    th {{ background: #1A1A2E; color: white; padding: 8px; }}
    td {{ border: 1px solid #ddd; padding: 8px; }}
    tr:nth-child(even) {{ background: #f2f2f2; }}
  </style>
</head>
<body>
<table><thead><tr>{headers}</tr></thead><tbody>{rows}</tbody></table>
</body>
</html>"""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    return output_path