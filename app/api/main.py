from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.services.qc_service import run_qc


app = FastAPI(
    title="AI Dataset QC Platform",
    description="API for validating image and annotation datasets.",
    version="0.1.0",
)


class QCRequest(BaseModel):
    dataset_path: str


@app.get("/")
def root():
    return {
        "service": "AI Dataset QC Platform",
        "status": "running",
    }


@app.get("/health")
def health():
    return {
        "status": "ok",
    }


@app.post("/qc")
def run_dataset_qc(request: QCRequest):
    dataset_path = Path(request.dataset_path)

    try:
        result = run_qc(dataset_path)

    except FileNotFoundError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error),
        )

    return {
        "status": "completed",
        "result": result,
    }