"""
API tests for authentication endpoints
"""

import pytest
from fastapi.testclient import TestClient


class TestAuthEndpoints:
    """Test authentication API endpoints."""
    
    def test_login_success(self, client):
        """Test successful login."""
        response = client.post(
            "/api/auth/login",
            data={"username": "admin", "password": "admin123"}
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert "access_token" in data
        assert "token_type" in data
        assert "expires_in" in data
        assert "user" in data
        
        assert data["token_type"] == "bearer"
        assert data["user"]["username"] == "admin"
        assert data["user"]["role"] == "admin"
        assert "admin" in data["user"]["permissions"]
    
    def test_login_invalid_credentials(self, client):
        """Test login with invalid credentials."""
        response = client.post(
            "/api/auth/login",
            data={"username": "admin", "password": "wrongpassword"}
        )
        
        assert response.status_code == 401
        data = response.json()
        assert "detail" in data
    
    def test_login_nonexistent_user(self, client):
        """Test login with nonexistent user."""
        response = client.post(
            "/api/auth/login",
            data={"username": "nonexistent", "password": "password"}
        )
        
        assert response.status_code == 401
    
    def test_login_empty_credentials(self, client):
        """Test login with empty credentials."""
        response = client.post(
            "/api/auth/login",
            data={"username": "", "password": ""}
        )
        
        assert response.status_code == 401
    
    def test_login_missing_fields(self, client):
        """Test login with missing fields."""
        # Missing password
        response = client.post(
            "/api/auth/login",
            data={"username": "admin"}
        )
        
        assert response.status_code == 422  # Validation error
    
    def test_get_current_user(self, client, auth_headers):
        """Test getting current user information."""
        response = client.get("/api/auth/me", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        
        assert "username" in data
        assert "role" in data
        assert "permissions" in data
        
        assert data["username"] == "admin"
        assert data["role"] == "admin"
    
    def test_get_current_user_without_token(self, client):
        """Test getting current user without authentication token."""
        response = client.get("/api/auth/me")
        
        assert response.status_code == 403  # Forbidden
    
    def test_get_current_user_with_invalid_token(self, client):
        """Test getting current user with invalid token."""
        headers = {"Authorization": "Bearer invalid_token"}
        response = client.get("/api/auth/me", headers=headers)
        
        assert response.status_code == 401
    
    def test_logout(self, client, auth_headers):
        """Test logout endpoint."""
        response = client.post("/api/auth/logout", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Successfully logged out"
    
    def test_logout_without_token(self, client):
        """Test logout without authentication token."""
        response = client.post("/api/auth/logout")
        
        assert response.status_code == 403
    
    def test_demo_user_login(self, client):
        """Test login with demo user."""
        response = client.post(
            "/api/auth/login",
            data={"username": "demo", "password": "demo123"}
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["user"]["username"] == "demo"
        assert data["user"]["role"] == "user"
        assert "read" in data["user"]["permissions"]
        assert "write" in data["user"]["permissions"]
        assert "admin" not in data["user"]["permissions"]
