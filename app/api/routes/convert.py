from fastapi import APIRouter, UploadFile, File, Form, BackgroundTasks, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.models.database import get_db
from app.models.schemas import ConversionLog
from app.core.converter import convert
from app.core.classifier import classify_text
from app.utils.file_utils import save_upload, cleanup_file, get_file_size_mb
from app.utils.validators import get_supported_conversions
import os
import time

router = APIRouter()


def log_conversion(db: Session, log_data: dict):
    log = ConversionLog(**log_data)
    db.add(log)
    db.commit()


@router.post("/convert")
async def convert_file(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    output_format: str = Form(...),
    db: Session = Depends(get_db),
):
    contents = await file.read()
    input_path = save_upload(contents, file.filename)

    try:
        start = time.time()
        result = convert(input_path, output_format)
        duration_ms = int((time.time() - start) * 1000)

        # Classify in background
        log_data = {
            "filename":      file.filename,
            "input_format":  result["input_format"],
            "output_format": output_format,
            "file_size_kb":  round(get_file_size_mb(input_path) * 1024, 2),
            "duration_ms":   duration_ms,
            "status":        "success",
        }
        background_tasks.add_task(log_conversion, db, log_data)
        background_tasks.add_task(cleanup_file, input_path)

        return FileResponse(
            result["output_path"],
            filename=os.path.basename(result["output_path"]),
            media_type="application/octet-stream",
        )
    except Exception as e:
        log_data = {
            "filename":      file.filename,
            "input_format":  "",
            "output_format": output_format,
            "status":        "error",
            "error_message": str(e),
        }
        background_tasks.add_task(log_conversion, db, log_data)
        cleanup_file(input_path)
        return {"error": str(e), "status": "failed"}


@router.get("/formats")
def get_formats():
    return {
        "supported_conversions": get_supported_conversions(),
        "total": len(get_supported_conversions()),
    }