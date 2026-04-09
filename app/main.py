from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.models.database import create_tables

app = FastAPI(
    title="ML File Converter API",
    description="Convert, classify and extract data from 11 file formats using ML",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    create_tables()

@app.get("/")
def root():
    return {
        "app": "ML File Converter",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": ["/convert", "/classify", "/history", "/stats", "/formats"],
    }

@app.get("/health")
def health():
    return {"status": "ok"}

from app.api.routes import convert, classify, history
app.include_router(convert.router,   prefix="/api", tags=["Convert"])
app.include_router(classify.router,  prefix="/api", tags=["Classify"])
app.include_router(history.router,   prefix="/api", tags=["History"])