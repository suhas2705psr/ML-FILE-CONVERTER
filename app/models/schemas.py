from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from sqlalchemy.sql import func
from app.models.database import Base


class ConversionLog(Base):
    __tablename__ = "conversion_logs"

    id             = Column(Integer, primary_key=True, index=True)
    filename       = Column(String(255), nullable=False)
    input_format   = Column(String(50),  nullable=False)
    output_format  = Column(String(50),  nullable=False)
    document_type  = Column(String(100), nullable=True)
    confidence     = Column(Float,       nullable=True)
    file_size_kb   = Column(Float,       nullable=True)
    duration_ms    = Column(Integer,     nullable=True)
    status         = Column(String(50),  default="success")
    error_message  = Column(Text,        nullable=True)
    created_at     = Column(DateTime,    server_default=func.now())


class ClassificationLog(Base):
    __tablename__ = "classification_logs"

    id            = Column(Integer, primary_key=True, index=True)
    filename      = Column(String(255), nullable=False)
    document_type = Column(String(100), nullable=False)
    confidence    = Column(Float,       nullable=False)
    file_size_kb  = Column(Float,       nullable=True)
    created_at    = Column(DateTime,    server_default=func.now())