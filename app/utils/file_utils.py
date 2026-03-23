import os
import shutil
import mimetypes
from pathlib import Path
from app.config import settings

# Maps file extensions to format names used throughout the app
EXTENSION_FORMAT_MAP = {
    ".pdf":  "pdf",
    ".docx": "docx",
    ".doc":  "docx",
    ".xlsx": "xlsx",
    ".xls":  "xlsx",
    ".csv":  "csv",
    ".png":  "image",
    ".jpg":  "image",
    ".jpeg": "image",
    ".tiff": "image",
    ".bmp":  "image",
    ".html": "html",
    ".htm":  "html",
    ".json": "json",
    ".xml":  "xml",
    ".pptx": "pptx",
    ".ppt":  "pptx",
    ".txt":  "txt",
}

SUPPORTED_FORMATS = list(set(EXTENSION_FORMAT_MAP.values()))


def get_file_format(file_path: str) -> str:
    """Detect format from file extension."""
    ext = Path(file_path).suffix.lower()
    fmt = EXTENSION_FORMAT_MAP.get(ext)
    if not fmt:
        raise ValueError(f"Unsupported file format: {ext}")
    return fmt


def get_file_size_mb(file_path: str) -> float:
    """Return file size in MB."""
    return os.path.getsize(file_path) / (1024 * 1024)


def validate_file(file_path: str) -> None:
    """Check file exists and is within size limit."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    size = get_file_size_mb(file_path)
    if size > settings.MAX_FILE_SIZE_MB:
        raise ValueError(f"File too large: {size:.1f}MB (max {settings.MAX_FILE_SIZE_MB}MB)")


def save_upload(file_bytes: bytes, filename: str) -> str:
    """Save uploaded bytes to tmp dir, return path."""
    dest = settings.UPLOAD_DIR / filename
    with open(dest, "wb") as f:
        f.write(file_bytes)
    return str(dest)


def cleanup_file(file_path: str) -> None:
    """Delete a temp file safely."""
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception:
        pass


def make_output_path(input_path: str, output_format: str) -> str:
    """Generate output file path from input path and target format."""
    stem = Path(input_path).stem
    ext_map = {
        "pdf": ".pdf", "docx": ".docx", "xlsx": ".xlsx",
        "csv": ".csv", "txt": ".txt", "html": ".html",
        "json": ".json", "image": ".png", "pptx": ".pptx",
    }
    ext = ext_map.get(output_format, f".{output_format}")
    return str(settings.UPLOAD_DIR / f"{stem}_converted{ext}")