from fastapi import APIRouter, UploadFile, Form, HTTPException
from services.ml_client import call_ml_service
from services.blockchain_client import record_evaluation
from utils.hash import keccak256
from PyPDF2 import PdfReader
import io
import mimetypes

router = APIRouter()

MAX_FILE_SIZE_MB = 5

@router.post("/apply")
async def apply(
    resume_pdf: UploadFile,
    job_id: str = Form(...),
    wallet_address: str = Form(...),
    enc_email: str = Form(None)
):
    # ✅ Validate file type
    if resume_pdf.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")
    content = await resume_pdf.read()
    if len(content) > MAX_FILE_SIZE_MB * 1024 * 1024:
        raise HTTPException(status_code=400, detail=f"File exceeds {MAX_FILE_SIZE_MB} MB limit.")

    # ✅ Extract text
    reader = PdfReader(io.BytesIO(content))
    resume_text = " ".join(page.extract_text() for page in reader.pages if page.extract_text())

    # ✅ Call ML service
    ml_result = await call_ml_service(resume_text, job_id)

    # ✅ Create submission_id
    submission_id = keccak256(wallet_address + job_id + ml_result["resume_hash"])

    # ✅ Record evaluation on blockchain
    tx_hash = await record_evaluation(submission_id, ml_result, wallet_address, enc_email)

    # ✅ Return result to frontend
    return {
        "submission_id": submission_id,
        "score": round(ml_result["similarity_score"], 3),
        "decision": ml_result["decision"],
        "tx_hash": tx_hash
    }
