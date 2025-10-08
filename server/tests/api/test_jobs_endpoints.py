"""
API tests for jobs endpoints
"""

import pytest
from fastapi.testclient import TestClient
import io


class TestJobsEndpoints:
    """Test jobs API endpoints."""
    
    def test_get_nonexistent_job(self, client):
        """Test getting a nonexistent job."""
        response = client.get("/api/jobs/nonexistent-job-id")
        
        assert response.status_code == 404  # Job not found
        data = response.json()
        assert "detail" in data
    
    def test_get_job_invalid_format(self, client):
        """Test getting a job with invalid ID format."""
        response = client.get("/api/jobs/invalid")
        
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert data["detail"]["error"] == "validation_error"
    
    def test_create_job_no_file(self, client):
        """Test creating a job without a file."""
        response = client.post("/api/jobs/create")
        
        assert response.status_code == 422  # Validation error - missing required field
    
    def test_create_job_invalid_file_type(self, client, sample_image):
        """Test creating a job with invalid file type."""
        # Mock an invalid file type
        response = client.post(
            "/api/jobs/create",
            files={"image": ("test.txt", io.BytesIO(b"not an image"), "text/plain")},
            data={
                "product_name": "Test Product",
                "product_category": "vibrators",
                "persona": "Test Persona",
                "platform": "Meta",
                "locales": "en-IN",
                "risk_mode": "standard",
                "n_variants": 8
            }
        )
        
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert data["detail"]["error"] == "validation_error"
    
    def test_create_job_empty_file(self, client):
        """Test creating a job with empty file."""
        response = client.post(
            "/api/jobs/create",
            files={"image": ("empty.png", io.BytesIO(b""), "image/png")},
            data={
                "product_name": "Test Product",
                "product_category": "vibrators",
                "persona": "Test Persona",
                "platform": "Meta",
                "locales": "en-IN",
                "risk_mode": "standard",
                "n_variants": 8
            }
        )
        
        assert response.status_code == 500  # Internal server error due to storage failure
        # Response might be plain text or JSON depending on error handling
        if response.headers.get("content-type", "").startswith("application/json"):
            data = response.json()
            assert "detail" in data
        else:
            # Plain text error response
            assert "Internal Server Error" in response.text
    
    def test_create_job_invalid_variants(self, client, sample_image):
        """Test creating a job with invalid number of variants."""
        response = client.post(
            "/api/jobs/create",
            files={"image": ("test.png", sample_image, "image/png")},
            data={
                "product_name": "Test Product",
                "product_category": "vibrators",
                "persona": "Test Persona",
                "platform": "Meta",
                "locales": "en-IN",
                "risk_mode": "standard",
                "n_variants": 50  # Invalid - too many variants
            }
        )
        
        # Should still succeed but clamp the value
        assert response.status_code == 201
        data = response.json()
        assert "job_id" in data
        assert "status" in data
        assert data["status"] == "queued"
    
    def test_create_job_invalid_category(self, client, sample_image):
        """Test creating a job with invalid product category."""
        response = client.post(
            "/api/jobs/create",
            files={"image": ("test.png", sample_image, "image/png")},
            data={
                "product_name": "Test Product",
                "product_category": "invalid_category",
                "persona": "Test Persona",
                "platform": "Meta",
                "locales": "en-IN",
                "risk_mode": "standard",
                "n_variants": 8
            }
        )
        
        # Should still succeed but use default category
        assert response.status_code == 201
        data = response.json()
        assert "job_id" in data
    
    def test_create_job_with_brand_voice(self, client, sample_image):
        """Test creating a job with brand voice JSON."""
        brand_voice = '{"tone": "playful", "style": "modern"}'
        
        response = client.post(
            "/api/jobs/create",
            files={"image": ("test.png", sample_image, "image/png")},
            data={
                "product_name": "Test Product",
                "product_category": "vibrators",
                "brand_voice": brand_voice,
                "persona": "Test Persona",
                "platform": "Meta",
                "locales": "en-IN",
                "risk_mode": "standard",
                "n_variants": 8
            }
        )
        
        assert response.status_code == 201
        data = response.json()
        assert "job_id" in data
        assert "params" in data
        assert "brand_voice" in data["params"]
    
    def test_create_job_with_invalid_brand_voice(self, client, sample_image):
        """Test creating a job with invalid brand voice JSON."""
        invalid_brand_voice = '{"tone": "playful", "style":}'  # Invalid JSON
        
        response = client.post(
            "/api/jobs/create",
            files={"image": ("test.png", sample_image, "image/png")},
            data={
                "product_name": "Test Product",
                "product_category": "vibrators",
                "brand_voice": invalid_brand_voice,
                "persona": "Test Persona",
                "platform": "Meta",
                "locales": "en-IN",
                "risk_mode": "standard",
                "n_variants": 8
            }
        )
        
        # Should still succeed but ignore invalid JSON
        assert response.status_code == 201
        data = response.json()
        assert "job_id" in data
    
    def test_create_job_minimal_data(self, client, sample_image):
        """Test creating a job with minimal required data."""
        response = client.post(
            "/api/jobs/create",
            files={"image": ("test.png", sample_image, "image/png")},
            data={
                "product_name": "Test Product"
            }
        )
        
        assert response.status_code == 201
        data = response.json()
        assert "job_id" in data
        assert "status" in data
        assert "image_url" in data
        assert "poll_url" in data
        assert "params" in data
        
        assert data["status"] == "queued"
        assert data["poll_url"] == f"/api/jobs/{data['job_id']}"
    
    def test_jobs_endpoint_security_headers(self, client):
        """Test that jobs endpoints include security headers."""
        response = client.get("/api/jobs/nonexistent")
        
        # Check for security headers
        headers = response.headers
        assert "X-Content-Type-Options" in headers
        assert "X-Frame-Options" in headers
        assert "X-XSS-Protection" in headers
        assert "Strict-Transport-Security" in headers
