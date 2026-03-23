from app.utils.file_utils import (
    get_file_format,
    get_file_size_mb,
    SUPPORTED_FORMATS,
)

# All valid conversion pairs (input_format, output_format)
SUPPORTED_CONVERSIONS = {
    ("pdf",   "docx"), ("pdf",   "txt"),  ("pdf",   "csv"),  ("pdf",   "json"),
    ("docx",  "pdf"),  ("docx",  "txt"),  ("docx",  "html"), ("docx",  "csv"),
    ("xlsx",  "csv"),  ("xlsx",  "json"), ("xlsx",  "pdf"),  ("xlsx",  "html"),
    ("csv",   "xlsx"), ("csv",   "json"), ("csv",   "html"), ("csv",   "pdf"),
    ("image", "txt"),  ("image", "pdf"),  ("image", "docx"), ("image", "json"),
    ("html",  "pdf"),  ("html",  "txt"),  ("html",  "docx"),
    ("json",  "csv"),  ("json",  "xlsx"), ("json",  "html"), ("json",  "txt"),
    ("xml",   "json"), ("xml",   "csv"),  ("xml",   "html"),
    ("pptx",  "pdf"),  ("pptx",  "txt"),  ("pptx",  "html"),
    ("txt",   "pdf"),  ("txt",   "docx"), ("txt",   "html"),
}


def validate_conversion(input_path: str, output_format: str) -> str:
    """
    Validate that the conversion is supported.
    Returns the detected input format.
    Raises ValueError with a clear message if not.
    """
    input_format = get_file_format(input_path)

    if output_format not in SUPPORTED_FORMATS:
        raise ValueError(
            f"Unknown output format: '{output_format}'. "
            f"Supported: {', '.join(sorted(SUPPORTED_FORMATS))}"
        )

    if (input_format, output_format) == (input_format, input_format):
        raise ValueError("Input and output formats are the same.")

    if (input_format, output_format) not in SUPPORTED_CONVERSIONS:
        raise ValueError(
            f"Conversion not supported: {input_format} → {output_format}"
        )

    return input_format


def validate_file_size(file_path: str, max_mb: int = 50) -> None:
    """Raise if file exceeds size limit."""
    size = get_file_size_mb(file_path)
    if size > max_mb:
        raise ValueError(
            f"File too large: {size:.1f}MB. Maximum allowed: {max_mb}MB."
        )


def get_supported_conversions() -> list[dict]:
    """Return all supported conversions as a list of dicts."""
    return [
        {"input": inp, "output": out}
        for inp, out in sorted(SUPPORTED_CONVERSIONS)
    ]