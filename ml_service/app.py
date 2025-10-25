from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from typing import Optional

from parser import anonymize_resume, extract_top_terms
from vectorizer import compute_similarity, get_model_identifier, load_model
from hashing import compute_hashes
from config import USE_FALLBACK, get_model_name


# initialize fastapi app
app = FastAPI(title="BlindHire ML Microservice", version="1.0.0")

# load model on startup
@app.on_event("startup")
async def startup_event():
    """
    Load the ML model on startup for efficiency
    Note: Model will be lazy-loaded on first request if not available on startup
    """
    try:
        load_model()
        print("Model loaded successfully")
    except Exception as e:
        print(f"Warning: Model not loaded on startup: {e}")
        print("Model will be loaded on first request")


# request/response models
class ParseScoreRequest(BaseModel):
    resume_text: str
    job_id: str


class ParseScoreResponse(BaseModel):
    similarity_score: float
    decision: str
    resume_hash: str
    model_hash: str
    score_hash: str
    explain: dict


class ExplainTermsRequest(BaseModel):
    resume_text: str


class ExplainTermsResponse(BaseModel):
    top_terms: list


class HealthResponse(BaseModel):
    status: str
    model: str


def load_job_description(job_id: str) -> str:
    """
    Load job description from file based on job_id
    For now, using a single job description file
    """
    try:
        with open('job_desc.txt', 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"Job description not found for job_id: {job_id}")


def determine_decision(similarity_score: float) -> str:
    """
    Determine decision category based on similarity score
    """
    if similarity_score >= 0.75:
        return "auto_pass"
    elif similarity_score <= 0.3:
        return "auto_fail"
    else:
        return "review"


@app.post("/parse_and_score", response_model=ParseScoreResponse)
async def parse_and_score(request: ParseScoreRequest):
    """
    Main endpoint that accepts a resume text and job ID, computes similarity,
    determines decision category, and returns hashes.
    """
    try:
        # load job description
        job_description = load_job_description(request.job_id)
        
        # anonymize resume
        anonymized_resume = anonymize_resume(request.resume_text)
        
        # compute similarity
        similarity_score = compute_similarity(anonymized_resume, job_description)
        
        # determine decision
        decision = determine_decision(similarity_score)
        
        # get model identifier
        model_id = get_model_identifier()
        
        # compute hashes
        resume_hash, model_hash, score_hash = compute_hashes(
            job_id=request.job_id,
            score=similarity_score,
            decision=decision,
            model_id=model_id,
            resume_text=anonymized_resume
        )
        
        # extract top terms for explanation
        top_terms = extract_top_terms(anonymized_resume)
        
        return ParseScoreResponse(
            similarity_score=similarity_score,
            decision=decision,
            resume_hash=f"0x{resume_hash}",
            model_hash=f"0x{model_hash}",
            score_hash=f"0x{score_hash}",
            explain={"top_terms": top_terms}
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")


@app.get("/health", response_model=HealthResponse)
async def health():
    """
    Health check endpoint used by the backend to verify model readiness.
    """
    model_name = f"sentence-transformers/{get_model_name()}"
    if USE_FALLBACK:
        model_name += " (using TF-IDF fallback for testing)"
    
    return HealthResponse(
        status="ok",
        model=model_name
    )


@app.post("/explain_terms", response_model=ExplainTermsResponse)
async def explain_terms(request: ExplainTermsRequest):
    """
    Optional helper for UI visualization or debugging. 
    Returns top frequent tokens from the anonymized resume.
    """
    try:
        # anonymize resume first
        anonymized_resume = anonymize_resume(request.resume_text)
        
        # extract top terms
        top_terms = extract_top_terms(anonymized_resume)
        
        return ExplainTermsResponse(top_terms=top_terms)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error extracting terms: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
