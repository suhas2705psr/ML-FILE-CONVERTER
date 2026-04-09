from fastapi import APIRouter, UploadFile, File, BackgroundTasks, Depends
from sqlalchemy.orm import Session
from app.models.database import get_db
from app.models.schemas import ClassificationLog
from app.core.classifier import classify_file
from app.utils.file_utils import save_upload, cleanup_file, get_file_size_mb

router = APIRouter()


def log_classification(db: Session, log_data: dict):
    log = ClassificationLog(**log_data)
    db.add(log)
    db.commit()


@router.post("/classify")
async def classify_document(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    contents = await file.read()
    input_path = save_upload(contents, file.filename)

    try:
        result = classify_file(input_path)

        log_data = {
            "filename":      file.filename,
            "document_type": result["document_type"],
            "confidence":    result["confidence"],
            "file_size_kb":  round(get_file_size_mb(input_path) * 1024, 2),
        }
        background_tasks.add_task(log_classification, db, log_data)
        background_tasks.add_task(cleanup_file, input_path)

        return {
            "filename":        file.filename,
            "document_type":   result["document_type"],
            "confidence":      result["confidence"],
            "top3":            result["top3"],
            "recommendations": result["recommendations"],
        }
    except Exception as e:
        cleanup_file(input_path)
        return {"error": str(e), "status": "failed"}