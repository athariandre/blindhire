import asyncio
import hashlib
import random

async def call_ml_service(resume_text: str, job_id: str) -> dict:
    """Call ML service for resume analysis (mock implementation)"""
    # In a real implementation, this would call the actual ML service
    # For demo purposes, we'll simulate ML processing
    
    # Simulate ML processing delay
    await asyncio.sleep(2)
    
    # Generate mock hashes
    resume_hash = hashlib.sha256(resume_text.encode()).hexdigest()
    model_hash = hashlib.sha256(f"model_v1_{job_id}".encode()).hexdigest()
    
    # Generate mock similarity score (0.0 to 1.0)
    similarity_score = random.uniform(0.3, 0.95)
    
    # Determine decision based on score
    if similarity_score >= 0.8:
        decision = "auto_pass"
    elif similarity_score >= 0.5:
        decision = "pending"  # Needs human review
    else:
        decision = "auto_reject"
    
    # Generate score hash
    score_hash = hashlib.sha256(f"{similarity_score}{resume_hash}".encode()).hexdigest()
    
    return {
        "resume_hash": resume_hash,
        "model_hash": model_hash,
        "score_hash": score_hash,
        "similarity_score": similarity_score,
        "decision": decision
    }
