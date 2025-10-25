from fastapi import APIRouter, HTTPException, Query
from services.blockchain_client import verify_evaluation
from services.db import get_submission

router = APIRouter()

@router.get("/status")
async def get_status(submission_id: str = Query(...)):
    submission = get_submission(submission_id)
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found.")

    # ✅ Verify hashes on chain
    verified = await verify_evaluation(
        submission_id,
        submission["resume_hash"],
        submission["model_hash"],
        submission["score_hash"]
    )

    return {
        "decision": submission["decision"],
        "tx_hash": submission["tx_hash"],
        "verified": verified
    }
