from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends, Request, status, BackgroundTasks
from slowapi.util import get_remote_address
from slowapi import Limiter
from app.services.storage import put_object, get_presigned_url
from app.db import crud
from app.workers.tasks import run_pipeline, run_pipeline_fn
from app.config import settings
from app.exceptions import (
    raise_validation_error, 
    raise_processing_error, 
    raise_internal_error,
    raise_not_found_error,
    ValidationError,
    StorageError,
    ProcessingError
)
import uuid
import logging
import os

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)
logger = logging.getLogger(__name__)

@router.post("/create", status_code=status.HTTP_201_CREATED)
@limiter.limit(f"{settings.RATE_LIMIT_PER_MINUTE}/minute")
async def create_job(
    request: Request,
    background_tasks: BackgroundTasks,
    image: UploadFile = File(...),
    brand_voice: str | None = Form(default=None),
    product_name: str = Form(default=""),
    product_id: str = Form(default=""),
    product_category: str = Form(default="vibrators"),
    tone: str = Form(default=""),
    must_include: str = Form(default=""),
    persona: str = Form(default=""),
    platform: str = Form(default="Meta"),
    locales: str = Form(default="en-IN"),
    risk_mode: str = Form(default="standard"),
    n_variants: int = Form(default=10),
):
    """Create a new ad copy generation job with rate limiting and validation"""
    try:
        # Validate image
        if not image or not image.content_type:
            raise_validation_error("No image file provided")
        
        if image.content_type not in {"image/png", "image/jpeg", "image/jpg"}:
            raise_validation_error(
                "Invalid image type", 
                {"allowed_types": ["image/png", "image/jpeg"], "received": image.content_type}
            )
        
        # Validate file size (max 10MB) if size known
        if hasattr(image, 'size') and image.size and image.size > 10 * 1024 * 1024:
            raise_validation_error(
                "Image too large", 
                {"max_size_mb": 10, "received_size_mb": round(image.size / (1024 * 1024), 2)}
            )
        
        # Validate n_variants
        try:
            n_variants = int(n_variants)
        except (ValueError, TypeError):
            n_variants = 10
            logger.warning(f"Invalid n_variants value, defaulting to 10")
        
        if n_variants < 1 or n_variants > 12:
            n_variants = min(max(n_variants, 1), 12)
            logger.warning(f"n_variants out of range, clamped to {n_variants}")
        
        # Validate product_category
        valid_categories = ["vibrators", "lubricants", "massage_oils", "candles", "games", "accessories"]
        if product_category.lower() not in valid_categories:
            product_category = "vibrators"  # Default fallback
            logger.warning(f"Invalid product_category, defaulting to vibrators")
        
        job_id = str(uuid.uuid4())
        key = f"uploads/{job_id}_{image.filename}"
        
        # Read and store image
        try:
            body = await image.read()
            if not body or len(body) == 0:
                raise_validation_error("Empty file uploaded")
            
            # Store the image
            put_object(key, body, content_type=image.content_type)
            logger.info(f"Image stored successfully: {key}")
            
        except Exception as e:
            logger.error(f"Failed to store image: {str(e)}")
            raise StorageError(f"Failed to store image: {str(e)}")
        
        # Parse brand_voice JSON if provided
        parsed_brand_voice = None
        if brand_voice is not None:
            try:
                import json as _json
                parsed_brand_voice = _json.loads(brand_voice)
            except Exception:
                logger.warning("Invalid brand_voice JSON provided; ignoring.")
                parsed_brand_voice = None

        # Create job record
        try:
            job_params = {
                "brand_voice": parsed_brand_voice,
                "product_name": product_name,
                "product_id": product_id,
                "product_category": product_category,
                "tone": tone,
                "must_include": [w.strip() for w in must_include.split(",") if w.strip()],
                "persona": persona, 
                "platform": platform,
                "locales": [l.strip() for l in locales.split(",") if l.strip()],
                "risk_mode": risk_mode, 
                "n_variants": n_variants
            }
            
            crud.create_job(job_id=job_id, image_key=key, params=job_params)
            logger.info(f"Job record created successfully: {job_id}")
            
        except Exception as e:
            logger.error(f"Failed to create job record: {str(e)}")
            raise ProcessingError(f"Failed to create job record: {str(e)}")
        
        # Queue pipeline execution based on mode
        queue_mode = os.getenv("QUEUE_MODE", "inline")
        if queue_mode == "inline":
            # Run async in the API process using BackgroundTasks
            logger.info(f"Adding background task for job {job_id}")
            try:
                background_tasks.add_task(run_pipeline_fn, job_id)
                logger.info(f"Background task added successfully for job {job_id}")
            except Exception as e:
                logger.error(f"Failed to add background task for job {job_id}: {e}")
                # Fallback: run synchronously
                logger.info(f"Running pipeline synchronously for job {job_id}")
                try:
                    run_pipeline_fn(job_id)
                    logger.info(f"Pipeline completed synchronously for job {job_id}")
                except Exception as sync_error:
                    logger.error(f"Pipeline failed for job {job_id}: {sync_error}")
        else:
            # Use real queue (Redis/Celery)
            run_pipeline.delay(job_id)
            logger.info(f"Created job {job_id} in queue mode")
        
        logger.info(f"Created job {job_id} for image {image.filename}")
        
        return {
            "job_id": job_id, 
            "status": "queued", 
            "image_url": get_presigned_url(key),
            "poll_url": f"/api/jobs/{job_id}",
            "params": job_params
        }
        
    except (ValidationError, StorageError, ProcessingError):
        # These are handled by our custom exception handlers
        raise
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error creating job: {e}")
        raise_internal_error(f"Failed to create job: {str(e)}")

@router.get("/{job_id}")
async def get_job(job_id: str):
    """Get job status and results"""
    try:
        # Validate job_id format
        if not job_id or len(job_id) < 10:
            raise_validation_error("Invalid job ID format")
        
        job = crud.get_job(job_id)
        if not job:
            raise_not_found_error("Job", job_id)
        
        return job.to_dict()
        
    except (ValidationError, HTTPException):
        raise
    except Exception as e:
        logger.error(f"Error retrieving job {job_id}: {e}")
        raise_internal_error(f"Failed to retrieve job: {str(e)}")
