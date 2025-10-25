import hashlib
import json


def compute_hashes(job_id: str, score: float, decision: str, model_id: str, resume_text: str):
    """
    Returns: resume_hash, model_hash, score_hash
    Uses sorted JSON with fixed separators and 4-decimal rounding.
    """
    # compute resume hash
    resume_hash = hashlib.sha256(resume_text.encode('utf-8')).hexdigest()
    
    # compute model hash
    model_hash = hashlib.sha256(model_id.encode('utf-8')).hexdigest()
    
    # compute score hash using canonical JSON
    score_payload = json.dumps({
        "job_id": job_id,
        "similarity_score": round(score, 4),
        "decision": decision,
        "model_hash": model_hash,
        "resume_hash": resume_hash
    }, sort_keys=True, separators=(',', ':'))
    
    score_hash = hashlib.sha256(score_payload.encode('utf-8')).hexdigest()
    
    return resume_hash, model_hash, score_hash


def sha256_hash(text: str) -> str:
    """
    Helper function to compute SHA-256 hash of text
    """
    return hashlib.sha256(text.encode('utf-8')).hexdigest()
