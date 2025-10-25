from fastapi import APIRouter, HTTPException
from services.blockchain_client import mark_accepted, create_job_contract
from services.db import save_job, get_job_summary

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
