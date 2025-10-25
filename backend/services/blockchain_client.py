import asyncio
import hashlib
from services.db import save_submission

async def record_evaluation(submission_id: str, ml_result: dict, wallet_address: str, job_id: str, enc_email: str = None) -> str:
    """Record evaluation on blockchain (mock implementation)"""
    # In a real implementation, this would interact with a blockchain
    # For demo purposes, we'll simulate a transaction hash
    
    # Simulate blockchain delay
    await asyncio.sleep(1)
    
    # Generate a mock transaction hash
    tx_hash = hashlib.sha256(f"{submission_id}{wallet_address}".encode()).hexdigest()
    
    # Save submission to database
    save_submission({
        "submission_id": submission_id,
        "job_id": job_id,
        "wallet_address": wallet_address,
        "resume_hash": ml_result.get("resume_hash", ""),
        "model_hash": ml_result.get("model_hash", ""),
        "score_hash": ml_result.get("score_hash", ""),
        "score": ml_result.get("similarity_score", 0),
        "decision": ml_result.get("decision", "pending"),
        "status": "pending",
        "tx_hash": tx_hash,
        "enc_email": enc_email
    })
    
    return tx_hash

async def verify_evaluation(submission_id: str, resume_hash: str, model_hash: str, score_hash: str) -> bool:
    """Verify evaluation on blockchain (mock implementation)"""
    # In a real implementation, this would verify hashes on the blockchain
    # For demo purposes, we'll return True after a short delay
    await asyncio.sleep(0.5)
    return True

async def mark_accepted(submission_id: str):
    """Mark submission as accepted on blockchain"""
    # In a real implementation, this would update the blockchain
    await asyncio.sleep(0.5)
    # For demo, we'll just update the database
    from services.db import submissions_db
    if submission_id in submissions_db:
        submissions_db[submission_id]["decision"] = "accepted"

async def create_job_contract(job_data: dict):
    """Create job contract on blockchain (mock implementation)"""
    # In a real implementation, this would deploy a smart contract
    await asyncio.sleep(1)
    
    # Generate mock job ID and contract address
    job_id = hashlib.sha256(f"{job_data['title']}{job_data['description']}".encode()).hexdigest()[:16]
    contract_address = "0x" + hashlib.sha256(job_id.encode()).hexdigest()[:40]
    
    return job_id, contract_address
