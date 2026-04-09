# ML-Powered Universal File Converter

![Python](https://img.shields.io/badge/Python-3.13-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.128-green)
![MySQL](https://img.shields.io/badge/MySQL-8.0-orange)
![Streamlit](https://img.shields.io/badge/Streamlit-1.46-red)

A production-grade document intelligence platform that converts, classifies,
and extracts structured data from 11 file formats using TF-IDF ML classification
and Tesseract OCR.

## Features
- Convert between 11 formats: PDF, DOCX, Excel, Images, CSV, HTML, JSON, XML, PPTX, TXT
- Auto-classify document type with TF-IDF + Logistic Regression (95% accuracy)
- Extract structured tables from scanned documents using Tesseract OCR
- REST API with auto-generated Swagger docs (FastAPI)
- Web UI with drag-and-drop (Streamlit)
- Every conversion logged to MySQL via SQLAlchemy ORM
- 33 supported conversion pairs

## Quick Start

### 1. Clone the repo
```bash
git clone https://github.com/suhas2705psr/ML-FILE-CONVERTER
cd ML-FILE-CONVERTER
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure environment
```bash
copy .env.example .env
# Edit .env with your MySQL password
```

### 4. Start the API
```bash
uvicorn app.main:app --reload
```

### 5. Start the UI
```bash
streamlit run streamlit_app/app.py
```

- API: http://localhost:8000/docs
- UI:  http://localhost:8501

## Supported Conversions

| Input | Output Formats |
|-------|---------------|
| PDF | DOCX, TXT, CSV, JSON |
| DOCX | PDF, TXT, HTML, CSV |
| Excel | CSV, JSON, PDF, HTML |
| Image | TXT, PDF, DOCX, JSON |
| CSV | Excel, JSON, HTML, PDF |
| JSON | CSV, Excel, HTML, TXT |
| HTML | PDF, DOCX, TXT |
| XML | JSON, CSV, HTML |
| PPTX | PDF, TXT, HTML |
| TXT | PDF, DOCX, HTML |

## Results

| Metric | Value |
|--------|-------|
| File formats supported | 11 |
| Conversion pairs | 33 |
| Classifier accuracy | 95% |
| Table extraction | OCR + bounding box clustering |
| API endpoints | 6 |

## Tech Stack
- **ML/NLP:** scikit-learn, TF-IDF, Logistic Regression
- **OCR:** Tesseract, OpenCV, Pillow
- **API:** FastAPI, Pydantic, Uvicorn
- **Database:** MySQL, SQLAlchemy
- **UI:** Streamlit
- **File Processing:** pdfplumber, python-docx, openpyxl, pandas

## Author
P. Sri Ranga Suhas — [GitHub](https://github.com/suhas2705psr) | 
[LinkedIn](https://www.linkedin.com/in/suhas-psr-1867bb307/)