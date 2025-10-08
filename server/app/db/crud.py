from app.db.session import SessionLocal, get_db_context
from app.db.models import Job
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from typing import Optional, List
import logging

logger = logging.getLogger(__name__)


def create_job(job_id: str, image_key: str, params: dict) -> Job:
    """Create a new job with error handling"""
    try:
        with SessionLocal() as db:
            # Check if job already exists
            existing_job = db.get(Job, job_id)
            if existing_job:
                logger.warning(f"Job {job_id} already exists, returning existing job")
                # Detach from session to avoid issues
                db.expunge(existing_job)
                return existing_job
            
            job = Job(job_id=job_id, image_key=image_key, params=params, status="queued")
            db.add(job)
            db.commit()
            db.refresh(job)
            logger.info(f"Created job {job_id}")
            # Detach from session to avoid issues
            db.expunge(job)
            return job
    except IntegrityError as e:
        logger.error(f"Integrity error creating job {job_id}: {e}")
        raise ValueError(f"Job {job_id} violates database constraints")
    except SQLAlchemyError as e:
        logger.error(f"Database error creating job {job_id}: {e}")
        raise RuntimeError(f"Failed to create job: {str(e)}")


def get_job(job_id: str) -> Optional[Job]:
    """Get a job by ID with error handling"""
    try:
        with SessionLocal() as db:
            job = db.get(Job, job_id)
            if job:
                logger.debug(f"Retrieved job {job_id}")
            else:
                logger.debug(f"Job {job_id} not found")
            return job
    except SQLAlchemyError as e:
        logger.error(f"Database error retrieving job {job_id}: {e}")
        raise RuntimeError(f"Failed to retrieve job: {str(e)}")


def update_job(job_id: str, **fields):
    """Update a job with error handling"""
    try:
        with SessionLocal() as db:
            job = db.get(Job, job_id)
            if not job:
                logger.warning(f"Job {job_id} not found for update")
                return None
            
            for k, v in fields.items():
                if hasattr(job, k):
                    setattr(job, k, v)
                else:
                    logger.warning(f"Ignoring unknown field {k} for job {job_id}")
            
            db.add(job)
            db.commit()
            db.refresh(job)
            logger.info(f"Updated job {job_id} with fields: {list(fields.keys())}")
            # Detach from session to avoid issues
            db.expunge(job)
            return job
    except SQLAlchemyError as e:
        logger.error(f"Database error updating job {job_id}: {e}")
        raise RuntimeError(f"Failed to update job: {str(e)}")


def finish_job(job_id: str, status: str, result: dict):
    """Finish a job with status and result"""
    if status not in ["done", "failed", "failed_precheck", "low_legibility"]:
        logger.warning(f"Invalid job status: {status}, defaulting to 'failed'")
        status = "failed"
    
    return update_job(job_id, status=status, result=result)


def get_jobs_by_status(status: str, limit: int = 100) -> List[Job]:
    """Get jobs by status"""
    try:
        with SessionLocal() as db:
            jobs = db.query(Job).filter(Job.status == status).limit(limit).all()
            logger.info(f"Retrieved {len(jobs)} jobs with status {status}")
            return jobs
    except SQLAlchemyError as e:
        logger.error(f"Database error retrieving jobs by status {status}: {e}")
        raise RuntimeError(f"Failed to retrieve jobs: {str(e)}")


def delete_job(job_id: str) -> bool:
    """Delete a job by ID"""
    try:
        with get_db_context() as db:
            job = db.get(Job, job_id)
            if not job:
                logger.warning(f"Job {job_id} not found for deletion")
                return False
            
            db.delete(job)
            logger.info(f"Deleted job {job_id}")
            return True
    except SQLAlchemyError as e:
        logger.error(f"Database error deleting job {job_id}: {e}")
        raise RuntimeError(f"Failed to delete job: {str(e)}")


def get_job_count() -> int:
    """Get total number of jobs"""
    try:
        with SessionLocal() as db:
            count = db.query(Job).count()
            logger.debug(f"Total jobs: {count}")
            return count
    except SQLAlchemyError as e:
        logger.error(f"Database error getting job count: {e}")
        raise RuntimeError(f"Failed to get job count: {str(e)}")
