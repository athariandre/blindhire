from fastapi import APIRouter, HTTPException, Query
from services.blockchain_service import mark_accepted, create_job_contract
from services.db import save_job, get_job_summary, get_all_jobs, get_submissions_by_job, get_submissions_by_wallet

router = APIRouter()

@router.post("/accept")
async def accept(data: dict):
    submission_id = data.get("submission_id")
    if not submission_id:
        raise HTTPException(status_code=400, detail="Missing submission_id.")

    await mark_accepted(submission_id)
    return {"success": True, "message": "Submission accepted"}

@router.post("/job")
async def create_job(data: dict):
    title = data.get("title")
    desc = data.get("description")
    if not title or not desc:
        raise HTTPException(status_code=400, detail="Missing title or description.")

    # ✅ Deploy new job contract on-chain
    job_id, contract_address = await create_job_contract(data)

    save_job({
        "job_id": job_id,
        "title": title,
        "description": desc,
        "requirements": data.get("requirements"),
        "location": data.get("location"),
        "salary": data.get("salary"),
        "contract_address": contract_address
    })

    return {"job_id": job_id, "success": True}

@router.get("/job/{job_id}/summary")
async def job_summary(job_id: str):
    job = get_job_summary(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found.")
    return job

@router.get("/jobs")
async def list_jobs():
    """Get all jobs created by recruiters"""
    jobs = get_all_jobs()
    return {"jobs": jobs}

@router.get("/submissions")
async def list_submissions(job_id: str = Query(None), wallet_address: str = Query(None)):
    """Get all submissions, optionally filtered by job_id or wallet_address"""
    if wallet_address:
        submissions = get_submissions_by_wallet(wallet_address)
    else:
        submissions = get_submissions_by_job(job_id)
    return {"submissions": submissions}
