"""
API tests for health check endpoints
"""

import pytest
from fastapi.testclient import TestClient


class TestHealthEndpoints:
    """Test health check API endpoints."""
    
    def test_basic_health_check(self, client):
        """Test basic health check endpoint."""
        response = client.get("/api/health/")
        
        assert response.status_code == 200
        data = response.json()
        
        assert "status" in data
        assert "timestamp" in data
        assert "version" in data
        assert "environment" in data
        
        assert data["status"] == "healthy"
        assert data["version"] == "1.0.0"
        assert data["environment"] == "dev"
        assert isinstance(data["timestamp"], (int, float))
    
    def test_detailed_health_check(self, client):
        """Test detailed health check endpoint."""
        response = client.get("/api/health/detailed")
        
        assert response.status_code == 200
        data = response.json()
        
        assert "status" in data
        assert "timestamp" in data
        assert "version" in data
        assert "environment" in data
        assert "components" in data
        assert "system_metrics" in data
        assert "performance" in data
        
        assert data["status"] in ["healthy", "degraded"]  # Can be degraded if Redis is not running
        
        # Check components
        components = data["components"]
        assert "database" in components
        assert "cache" in components
        assert "storage" in components
        
        # Check system metrics
        system_metrics = data["system_metrics"]
        assert isinstance(system_metrics, dict)
        
        # Check performance data
        performance = data["performance"]
        assert "cache_stats" in performance
        assert "function_metrics" in performance
    
    def test_context_health_check(self, client):
        """Test context health check endpoint."""
        response = client.get("/api/health/context")
        
        # This endpoint might return different status codes depending on context manager
        assert response.status_code in [200, 500]  # 500 if context not initialized
        
        if response.status_code == 200:
            data = response.json()
            assert "ok" in data
            if data["ok"]:
                assert "chunks" in data
        else:
            data = response.json()
            assert "ok" in data
            assert data["ok"] is False
            assert "reason" in data
    
    def test_health_check_response_headers(self, client):
        """Test that health check endpoints include security headers."""
        response = client.get("/api/health/")
        
        assert response.status_code == 200
        
        # Check for security headers
        headers = response.headers
        assert "X-Content-Type-Options" in headers
        assert "X-Frame-Options" in headers
        assert "X-XSS-Protection" in headers
        assert "Strict-Transport-Security" in headers
    
    def test_detailed_health_check_performance(self, client):
        """Test that detailed health check doesn't take too long."""
        import time
        
        start_time = time.time()
        response = client.get("/api/health/detailed")
        end_time = time.time()
        
        assert response.status_code == 200
        response_time = end_time - start_time
        
        # Should respond within 5 seconds
        assert response_time < 5.0
    
    def test_health_check_timestamp_format(self, client):
        """Test that health check timestamps are valid."""
        response = client.get("/api/health/")
        
        assert response.status_code == 200
        data = response.json()
        
        timestamp = data["timestamp"]
        assert isinstance(timestamp, (int, float))
        assert timestamp > 0
        
        # Should be a reasonable timestamp (not too old, not in the future)
        import time
        current_time = time.time()
        assert abs(current_time - timestamp) < 60  # Within 1 minute
