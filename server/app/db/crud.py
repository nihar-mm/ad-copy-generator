from app.db.session import SessionLocal
from app.db.models import Job
from typing import Optional

def create_job(job_id:str, image_key:str, params:dict)->Job:
    with SessionLocal() as db:
        job = Job(job_id=job_id, image_key=image_key, params=params, status="queued")
        db.add(job); db.commit(); db.refresh(job)
        return job

def get_job(job_id:str)->Optional[Job]:
    with SessionLocal() as db:
        return db.get(Job, job_id)

def update_job(job_id:str, **fields):
    with SessionLocal() as db:
        job = db.get(Job, job_id)
        if not job: return None
        for k,v in fields.items(): setattr(job, k, v)
        db.add(job); db.commit(); db.refresh(job)
        return job

def finish_job(job_id:str, status:str, result:dict):
    return update_job(job_id, status=status, result=result)
