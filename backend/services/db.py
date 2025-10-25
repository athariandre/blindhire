# Simple in-memory database for demo purposes
# In production, this would be a real database

submissions_db = {}
jobs_db = {}

def get_submission(submission_id: str):
    """Get submission by ID"""
    return submissions_db.get(submission_id)

def save_submission(submission_data: dict):
    """Save submission data"""
    submissions_db[submission_data["submission_id"]] = submission_data

def mark_claimed(submission_id: str):
    """Mark submission as claimed"""
    if submission_id in submissions_db:
        submissions_db[submission_id]["status"] = "claimed"

def save_job(job_data: dict):
    """Save job data"""
    jobs_db[job_data["job_id"]] = job_data

def get_job_summary(job_id: str):
    """Get job summary by ID"""
    return jobs_db.get(job_id)

def get_all_jobs():
    """Get all jobs"""
    return list(jobs_db.values())

def get_submissions_by_job(job_id: str = None):
    """Get all submissions, optionally filtered by job_id"""
    if job_id:
        return [sub for sub in submissions_db.values() if sub.get("job_id") == job_id]
    return list(submissions_db.values())

def get_submissions_by_wallet(wallet_address: str):
    """Get all submissions for a specific wallet address"""
    return [sub for sub in submissions_db.values() if sub.get("wallet_address") == wallet_address]
