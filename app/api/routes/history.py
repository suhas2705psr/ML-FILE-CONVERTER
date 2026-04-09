from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.database import get_db
from app.models.schemas import ConversionLog, ClassificationLog

router = APIRouter()


@router.get("/history")
def get_history(
    db: Session = Depends(get_db),
    limit: int = Query(20, ge=1, le=100),
    status: str = Query(None),
    input_format: str = Query(None),
):
    query = db.query(ConversionLog).order_by(ConversionLog.created_at.desc())
    if status:
        query = query.filter(ConversionLog.status == status)
    if input_format:
        query = query.filter(ConversionLog.input_format == input_format)
    logs = query.limit(limit).all()
    return {
        "total": len(logs),
        "logs": [
            {
                "id":            l.id,
                "filename":      l.filename,
                "input_format":  l.input_format,
                "output_format": l.output_format,
                "document_type": l.document_type,
                "confidence":    l.confidence,
                "file_size_kb":  l.file_size_kb,
                "duration_ms":   l.duration_ms,
                "status":        l.status,
                "created_at":    str(l.created_at),
            }
            for l in logs
        ],
    }


@router.get("/stats")
def get_stats(db: Session = Depends(get_db)):
    total       = db.query(ConversionLog).count()
    success     = db.query(ConversionLog).filter(ConversionLog.status == "success").count()
    errors      = db.query(ConversionLog).filter(ConversionLog.status == "error").count()
    avg_duration = db.query(func.avg(ConversionLog.duration_ms)).scalar()
    top_format  = db.query(
        ConversionLog.input_format,
        func.count(ConversionLog.input_format).label("count")
    ).group_by(ConversionLog.input_format).order_by(func.count(ConversionLog.input_format).desc()).first()

    return {
        "total_conversions": total,
        "successful":        success,
        "errors":            errors,
        "success_rate":      round(success / total * 100, 1) if total > 0 else 0,
        "avg_duration_ms":   round(avg_duration or 0, 1),
        "most_used_format":  top_format[0] if top_format else None,
    }