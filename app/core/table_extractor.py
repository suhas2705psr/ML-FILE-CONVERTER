import numpy as np
import pandas as pd
import json
from app.core.ocr import extract_words_with_boxes


def cluster_by_rows(words: list[dict], tolerance: int = 10) -> list[list[dict]]:
    """Group words into rows by their Y coordinate."""
    if not words:
        return []
    sorted_words = sorted(words, key=lambda w: w["y"])
    rows = []
    current_row = [sorted_words[0]]
    for word in sorted_words[1:]:
        if abs(word["y"] - current_row[0]["y"]) <= tolerance:
            current_row.append(word)
        else:
            rows.append(sorted(current_row, key=lambda w: w["x"]))
            current_row = [word]
    rows.append(sorted(current_row, key=lambda w: w["x"]))
    return rows


def cluster_into_columns(rows: list[list[dict]], col_count: int) -> list[list[str]]:
    """Assign words in each row to columns based on X position."""
    if not rows:
        return []
    anchor_row = max(rows, key=len)
    col_centers = [w["x"] + w["w"] // 2 for w in anchor_row]
    if len(col_centers) < col_count:
        max_x = max(w["x"] + w["w"] for r in rows for w in r)
        col_centers = [
            int(max_x * (i + 0.5) / col_count)
            for i in range(col_count)
        ]
    table = []
    for row in rows:
        cells = [""] * col_count
        for word in row:
            word_center = word["x"] + word["w"] // 2
            col_idx = min(
                range(col_count),
                key=lambda i: abs(col_centers[i] - word_center)
            )
            cells[col_idx] += (" " if cells[col_idx] else "") + word["text"]
        table.append(cells)
    return table


def extract_table_from_image(image_path: str, col_count: int = None) -> pd.DataFrame:
    """Full pipeline: image → OCR → row clustering → DataFrame."""
    words = extract_words_with_boxes(image_path)
    if not words:
        return pd.DataFrame()
    rows = cluster_by_rows(words, tolerance=12)
    if col_count is None:
        col_count = max(len(r) for r in rows)
        col_count = max(2, min(col_count, 10))
    table_data = cluster_into_columns(rows, col_count)
    if not table_data:
        return pd.DataFrame()
    df = pd.DataFrame(table_data[1:], columns=table_data[0])
    return df


def extract_table_to_csv(image_path: str, output_path: str, col_count: int = None) -> str:
    """Extract table from image and save as CSV."""
    df = extract_table_from_image(image_path, col_count)
    df.to_csv(output_path, index=False)
    return output_path


def extract_table_to_json(image_path: str, output_path: str, col_count: int = None) -> str:
    """Extract table from image and save as JSON."""
    df = extract_table_from_image(image_path, col_count)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(df.to_dict(orient="records"), f, indent=2)
    return output_path