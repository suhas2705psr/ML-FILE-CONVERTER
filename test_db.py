from app.models.database import create_tables, SessionLocal
from app.models.schemas import ConversionLog
import os

# Create tables
create_tables()
print("✅ Tables created")

# Insert a test record
db = SessionLocal()
log = ConversionLog(
    filename="test.pdf",
    input_format="pdf",
    output_format="docx",
    document_type="invoice",
    confidence=0.87,
    file_size_kb=24.5,
    duration_ms=120,
    status="success",
)
db.add(log)
db.commit()
db.refresh(log)
print(f"✅ Record inserted — ID: {log.id}")

# Read it back
count = db.query(ConversionLog).count()
print(f"✅ Total records in DB: {count}")
db.close()