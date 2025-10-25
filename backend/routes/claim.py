from fastapi import APIRouter, HTTPException
from services.crypto_utils import verify_signature
from services.db import get_submission, mark_claimed

router = APIRouter()

@router.post("/claim")
async def claim(data: dict):
    submission_id = data.get("submission_id")
    signature = data.get("signature")

    if not submission_id or not signature:
        raise HTTPException(status_code=400, detail="Missing submission_id or signature.")

    submission = get_submission(submission_id)
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found.")

    # ✅ Verify signature matches wallet
    valid = verify_signature(submission_id, signature, submission["wallet_address"])
    if not valid:
        raise HTTPException(status_code=403, detail="Invalid signature.")

    mark_claimed(submission_id)

    return {"success": True, "message": "Position claimed successfully"}
