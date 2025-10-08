"""
Unit tests for database layer
"""

import pytest
from app.db.session import check_database_health, get_database_stats, get_db_context
from app.db.crud import (
    create_job, get_job, update_job, finish_job, 
    get_jobs_by_status, delete_job, get_job_count
)
from app.db.models import Base, Job
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import uuid


class TestDatabaseHealth:
    """Test database health check functionality."""
    
    def test_database_health_check(self):
        """Test basic database health check."""
        result = check_database_health()
        
        assert isinstance(result, dict)
        assert "healthy" in result
        assert "response_time_ms" in result
        assert "error" in result
        assert "database_type" in result
        
        # Should be healthy for SQLite in tests
        assert result["healthy"] is True
        assert result["response_time_ms"] > 0
        assert result["error"] is None
        assert result["database_type"] == "sqlite"
    
    def test_database_stats(self):
        """Test database connection pool statistics."""
        stats = get_database_stats()
        
        assert isinstance(stats, dict)
        assert "pool_size" in stats
        assert "checked_in_connections" in stats
        assert "checked_out_connections" in stats
        assert "overflow_connections" in stats
        assert "total_connections" in stats
        
        # Pool size should be positive
        assert stats["pool_size"] >= 0
        assert stats["total_connections"] >= 0


class TestDatabaseContext:
    """Test database context manager."""
    
    def test_context_manager_success(self):
        """Test successful transaction with context manager."""
        job_id = f"test_{uuid.uuid4().hex[:8]}"
        
        try:
            with get_db_context() as db:
                job = Job(job_id=job_id, image_key="test.png", params={}, status="queued")
                db.add(job)
            
            # Job should be committed
            retrieved_job = get_job(job_id)
            assert retrieved_job is not None
            assert retrieved_job.job_id == job_id
            
        finally:
            # Cleanup
            delete_job(job_id)
    
    def test_context_manager_rollback(self):
        """Test transaction rollback on error."""
        job_id = f"test_{uuid.uuid4().hex[:8]}"
        
        try:
            with get_db_context() as db:
                job = Job(job_id=job_id, image_key="test.png", params={}, status="queued")
                db.add(job)
                raise Exception("Test error")
        except Exception:
            pass
        
        # Job should not be committed
        retrieved_job = get_job(job_id)
        assert retrieved_job is None


class TestCRUDOperations:
    """Test CRUD operations with error handling."""
    
    def test_create_job(self):
        """Test creating a job."""
        job_id = f"test_{uuid.uuid4().hex[:8]}"
        
        try:
            job = create_job(job_id, "test.png", {"test": "data"})
            
            assert job is not None
            assert job.job_id == job_id
            assert job.image_key == "test.png"
            assert job.params == {"test": "data"}
            assert job.status == "queued"
            
        finally:
            delete_job(job_id)
    
    def test_create_duplicate_job(self):
        """Test creating a duplicate job returns existing."""
        job_id = f"test_{uuid.uuid4().hex[:8]}"
        
        try:
            job1 = create_job(job_id, "test1.png", {"test": "data1"})
            job2 = create_job(job_id, "test2.png", {"test": "data2"})
            
            # Should return existing job
            assert job1.job_id == job2.job_id
            assert job1.image_key == job2.image_key  # Original data preserved
            
        finally:
            delete_job(job_id)
    
    def test_get_job(self):
        """Test getting a job by ID."""
        job_id = f"test_{uuid.uuid4().hex[:8]}"
        
        try:
            create_job(job_id, "test.png", {"test": "data"})
            job = get_job(job_id)
            
            assert job is not None
            assert job.job_id == job_id
            
        finally:
            delete_job(job_id)
    
    def test_get_nonexistent_job(self):
        """Test getting a nonexistent job."""
        job = get_job("nonexistent_job_id")
        assert job is None
    
    def test_update_job(self):
        """Test updating a job."""
        job_id = f"test_{uuid.uuid4().hex[:8]}"
        
        try:
            create_job(job_id, "test.png", {"test": "data"})
            updated_job = update_job(job_id, status="processing", result={"updated": True})
            
            assert updated_job is not None
            assert updated_job.status == "processing"
            assert updated_job.result == {"updated": True}
            
        finally:
            delete_job(job_id)
    
    def test_update_nonexistent_job(self):
        """Test updating a nonexistent job."""
        result = update_job("nonexistent_job_id", status="done")
        assert result is None
    
    def test_finish_job(self):
        """Test finishing a job."""
        job_id = f"test_{uuid.uuid4().hex[:8]}"
        
        try:
            create_job(job_id, "test.png", {"test": "data"})
            finished_job = finish_job(job_id, "done", {"result": "success"})
            
            assert finished_job is not None
            assert finished_job.status == "done"
            assert finished_job.result == {"result": "success"}
            
        finally:
            delete_job(job_id)
    
    def test_finish_job_invalid_status(self):
        """Test finishing a job with invalid status."""
        job_id = f"test_{uuid.uuid4().hex[:8]}"
        
        try:
            create_job(job_id, "test.png", {"test": "data"})
            finished_job = finish_job(job_id, "invalid_status", {"result": "test"})
            
            # Should default to "failed"
            assert finished_job.status == "failed"
            
        finally:
            delete_job(job_id)
    
    def test_get_jobs_by_status(self):
        """Test getting jobs by status."""
        job_ids = [f"test_{uuid.uuid4().hex[:8]}" for _ in range(3)]
        
        try:
            # Create jobs with different statuses
            for i, job_id in enumerate(job_ids):
                create_job(job_id, f"test{i}.png", {"test": i})
                if i < 2:
                    update_job(job_id, status="done")
            
            # Get jobs with "done" status
            done_jobs = get_jobs_by_status("done")
            done_job_ids = [j.job_id for j in done_jobs if j.job_id in job_ids]
            
            assert len(done_job_ids) >= 2
            
        finally:
            for job_id in job_ids:
                delete_job(job_id)
    
    def test_delete_job(self):
        """Test deleting a job."""
        job_id = f"test_{uuid.uuid4().hex[:8]}"
        
        create_job(job_id, "test.png", {"test": "data"})
        deleted = delete_job(job_id)
        
        assert deleted is True
        assert get_job(job_id) is None
    
    def test_delete_nonexistent_job(self):
        """Test deleting a nonexistent job."""
        deleted = delete_job("nonexistent_job_id")
        assert deleted is False
    
    def test_get_job_count(self):
        """Test getting total job count."""
        initial_count = get_job_count()
        
        job_id = f"test_{uuid.uuid4().hex[:8]}"
        
        try:
            create_job(job_id, "test.png", {"test": "data"})
            new_count = get_job_count()
            
            assert new_count == initial_count + 1
            
        finally:
            delete_job(job_id)
            final_count = get_job_count()
            assert final_count == initial_count

