from pydantic_settings import BaseSettings
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    # App
    APP_NAME: str = "ML File Converter"
    DEBUG: bool = True

    # Tesseract
    TESSERACT_PATH: str = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

    # Database
    DATABASE_URL: str = "mysql+pymysql://root:password@localhost:3306/ml_converter"

    # File limits
    MAX_FILE_SIZE_MB: int = 50
    UPLOAD_DIR: Path = BASE_DIR / "tmp"
    MODELS_DIR: Path = BASE_DIR / "models"

    class Config:
        env_file = ".env"

settings = Settings()

# Create dirs if they don't exist
settings.UPLOAD_DIR.mkdir(exist_ok=True)
settings.MODELS_DIR.mkdir(exist_ok=True)