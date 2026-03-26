import os
import joblib
import numpy as np
from pathlib import Path
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from app.config import settings

MODEL_PATH = settings.MODELS_DIR / "classifier.joblib"

# ─── Document type → keywords mapping ────────────────────────────────────────
# Each type has representative text samples for training
TRAINING_DATA = {
    "invoice": [
        "invoice number amount due total payable billing date tax GST payment",
        "bill to invoice date due date subtotal discount total amount payable",
        "invoice customer purchase order item quantity unit price total",
        "payment invoice issued billing address tax invoice amount outstanding",
        "invoice no date client description rate hours amount total due",
        "INV total payable tax invoice customer billing payment terms due date",
        "invoice number bill amount tax rate total payable payment due",
        "billing statement account number due date minimum payment total balance",
    ],
    "resume": [
        "education experience skills bachelor master degree university college",
        "work experience projects internship python java programming languages",
        "resume curriculum vitae objective summary professional experience",
        "skills technical proficient languages frameworks tools technologies",
        "employment history job title company name years experience responsibilities",
        "academic qualifications certifications training professional development",
        "contact email phone linkedin github portfolio personal information",
        "bachelor technology computer science engineering CGPA percentage grade",
    ],
    "report": [
        "executive summary introduction methodology findings conclusion recommendations",
        "analysis results discussion research report quarterly annual performance",
        "report findings data analysis charts graphs tables appendix references",
        "business report market analysis competitive landscape strategic recommendations",
        "financial report revenue profit loss balance sheet quarterly results",
        "project report status update progress milestone deliverables timeline",
        "research report abstract literature review methodology results conclusion",
        "annual report shareholders stakeholders financial performance highlights",
    ],
    "contract": [
        "agreement terms conditions parties hereby agree obligations responsibilities",
        "contract effective date parties agreement clause section binding terms",
        "whereas agreement entered parties terms conditions obligations liabilities",
        "contract party agrees terms conditions warranties representations covenants",
        "agreement signed parties terms obligations governing law jurisdiction",
        "service agreement contractor client scope work payment terms deliverables",
        "non-disclosure agreement confidential information parties obligations",
        "employment contract terms conditions salary benefits obligations duties",
    ],
    "spreadsheet": [
        "row column cell value formula sum average count total data table",
        "sheet data rows columns headers values numeric calculations totals",
        "table data entries records columns rows numeric text values",
        "spreadsheet cells values formulas calculations pivot chart data",
        "data row column header value numeric text date formatted cells",
        "worksheet cells range values formulas functions data analysis",
        "monthly quarterly annual data table rows columns numeric values",
        "budget expenses income forecast data table numeric values totals",
    ],
    "presentation": [
        "slide agenda introduction overview key points summary conclusion",
        "presentation deck slide title bullets points agenda topics",
        "slide overview objectives key findings recommendations next steps",
        "presentation introduction background problem solution benefits",
        "deck slides topics overview conclusions thank you questions",
        "presentation agenda slide content title points bullets summary",
        "keynote presentation overview strategy vision mission goals",
        "slides introduction problem statement solution implementation results",
    ],
    "article": [
        "published author journal article abstract introduction discussion",
        "research paper authors abstract keywords introduction methodology",
        "news article published reporter journalist headline paragraph story",
        "blog post author published date introduction content conclusion",
        "magazine article feature story journalist author publication",
        "academic article published peer reviewed journal references bibliography",
        "opinion article editorial journalist author newspaper column",
        "technical article author abstract introduction method results conclusion",
    ],
    "form": [
        "name address date signature field fill please complete form submit",
        "application form name date address signature required fields",
        "form please fill name contact details address signature date",
        "registration form participant name email phone address submit",
        "questionnaire survey form questions answers tick check box submit",
        "feedback form name email comments suggestions rating submit",
        "application form required fields personal details contact information",
        "form fields name address contact details signature date submitted",
    ],
    "email": [
        "from to subject dear regards sincerely attached please find",
        "email from to cc subject date dear regards best wishes",
        "dear sir madam please find attached regarding matter response",
        "hello hi team please could kindly let know regards thanks",
        "subject from sent received inbox reply forward attachment email",
        "dear team attached please review comments feedback regards",
        "to from subject date message body reply forward email thread",
        "email message inbox sent subject dear regards best sincerely",
    ],
    "code": [
        "function def class import return variable type string int boolean",
        "python java code function class method variable import library",
        "def function return import class object method attribute parameter",
        "code program script function variable loop condition if else",
        "import library module function class method return variable",
        "algorithm function implementation class object method variable type",
        "javascript html css function variable event handler DOM element",
        "database query select insert update delete table column where",
    ],
    "financial": [
        "balance sheet assets liabilities equity revenue profit loss cash",
        "financial statement income revenue expenses profit loss margin",
        "cash flow statement operating investing financing activities",
        "profit loss statement revenue cost gross margin net income",
        "financial report assets liabilities equity dividends shares",
        "budget forecast revenue expenses variance analysis financial",
        "tax return income deductions credits refund filing assessment",
        "bank statement account transactions balance credit debit",
    ],
    "other": [
        "document content text information data details general",
        "file content information general document text data",
        "content text general information details document",
        "miscellaneous general content text information data",
        "general document mixed content various information text",
        "unstructured content general text information document",
        "various mixed content general text data information",
        "document general purpose text content information misc",
    ],
}


def build_training_set() -> tuple[list[str], list[str]]:
    """Convert TRAINING_DATA dict into texts + labels lists."""
    texts, labels = [], []
    for label, samples in TRAINING_DATA.items():
        for sample in samples:
            texts.append(sample)
            labels.append(label)
    return texts, labels


def train_classifier() -> Pipeline:
    """Train TF-IDF + Logistic Regression pipeline and save to disk."""
    texts, labels = build_training_set()

    X_train, X_test, y_train, y_test = train_test_split(
        texts, labels, test_size=0.2, random_state=42, stratify=labels
    )

    pipeline = Pipeline([
        ("tfidf", TfidfVectorizer(
            max_features=5000,
            ngram_range=(1, 2),
            sublinear_tf=True,
            min_df=1,
        )),
        ("clf", LogisticRegression(
            max_iter=1000,
            C=1.0,
            class_weight="balanced",
        )),
    ])

    pipeline.fit(X_train, y_train)

    # Evaluate
    y_pred = pipeline.predict(X_test)
    print("\n=== Classifier Training Report ===")
    print(classification_report(y_test, y_pred))

    # Save model
    joblib.dump(pipeline, MODEL_PATH)
    print(f"Model saved to: {MODEL_PATH}")
    return pipeline


def load_classifier() -> Pipeline:
    """Load trained classifier from disk, train if not found."""
    if not MODEL_PATH.exists():
        print("No model found — training now...")
        return train_classifier()
    return joblib.load(MODEL_PATH)


def classify_text(text: str) -> dict:
    """
    Classify a text sample.
    Returns document type, confidence, and recommended output formats.
    """
    pipeline = load_classifier()
    text_sample = text[:1000].strip()
    if not text_sample:
        return {"document_type": "other", "confidence": 0.0, "recommendations": ["pdf", "txt"]}

    proba = pipeline.predict_proba([text_sample])[0]
    classes = pipeline.classes_
    top_idx = np.argmax(proba)

    doc_type = classes[top_idx]
    confidence = round(float(proba[top_idx]), 3)

    # Top 3 predictions
    top3_idx = np.argsort(proba)[::-1][:3]
    top3 = [{"type": classes[i], "confidence": round(float(proba[i]), 3)}
            for i in top3_idx]

    recommendations = {
        "invoice":      ["pdf", "csv", "xlsx"],
        "resume":       ["pdf", "docx"],
        "report":       ["pdf", "docx"],
        "contract":     ["pdf", "docx"],
        "spreadsheet":  ["xlsx", "csv", "json"],
        "presentation": ["pdf", "pptx"],
        "article":      ["pdf", "docx", "html"],
        "form":         ["pdf", "docx"],
        "email":        ["txt", "pdf"],
        "code":         ["txt", "html"],
        "financial":    ["xlsx", "pdf", "csv"],
        "other":        ["pdf", "txt"],
    }

    return {
        "document_type":  doc_type,
        "confidence":     confidence,
        "top3":           top3,
        "recommendations": recommendations.get(doc_type, ["pdf", "txt"]),
    }


def classify_file(file_path: str) -> dict:
    """
    Extract text from a file and classify it.
    Handles PDF, DOCX, TXT, images automatically.
    """
    ext = Path(file_path).suffix.lower()
    text = ""

    try:
        if ext == ".pdf":
            import pdfplumber
            with pdfplumber.open(file_path) as pdf:
                text = " ".join(p.extract_text() or "" for p in pdf.pages[:3])
        elif ext == ".docx":
            from docx import Document
            doc = Document(file_path)
            text = " ".join(p.text for p in doc.paragraphs[:50])
        elif ext in [".xlsx", ".xls"]:
            import pandas as pd
            df = pd.read_excel(file_path, nrows=10)
            text = " ".join(str(v) for v in df.values.flatten())
        elif ext == ".csv":
            import pandas as pd
            df = pd.read_csv(file_path, nrows=10)
            text = " ".join(df.columns.tolist())
        elif ext == ".txt":
            with open(file_path, encoding="utf-8", errors="ignore") as f:
                text = f.read(1000)
        elif ext in [".png", ".jpg", ".jpeg"]:
            from app.core.ocr import extract_text
            text = extract_text(file_path)
        else:
            text = Path(file_path).stem.replace("_", " ")
    except Exception as e:
        text = Path(file_path).stem.replace("_", " ")

    result = classify_text(text)
    result["file_path"] = file_path
    return result