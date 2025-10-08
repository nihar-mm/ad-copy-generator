"""
Unit tests for authentication module
"""

import pytest
from app.auth import (
    verify_password, get_password_hash, create_access_token, verify_token,
    sanitize_input, validate_file_type, validate_file_size, authenticate_user
)


class TestPasswordHashing:
    """Test password hashing functionality."""
    
    def test_password_hashing(self):
        """Test password hashing and verification."""
        password = "test123"
        hashed = get_password_hash(password)
        
        assert hashed != password
        assert len(hashed) > 0
        assert verify_password(password, hashed)
        assert not verify_password("wrong", hashed)
    
    def test_password_verification(self):
        """Test password verification with different inputs."""
        password = "secure_password"
        hashed = get_password_hash(password)
        
        # Correct password
        assert verify_password(password, hashed)
        
        # Wrong password
        assert not verify_password("wrong_password", hashed)
        
        # Empty password
        assert not verify_password("", hashed)
        
        # None password
        assert not verify_password(None, hashed)


class TestJWTTokens:
    """Test JWT token functionality."""
    
    def test_token_creation(self):
        """Test JWT token creation."""
        data = {"sub": "testuser", "role": "user"}
        token = create_access_token(data)
        
        assert token is not None
        assert len(token) > 0
        assert isinstance(token, str)
    
    def test_token_verification(self):
        """Test JWT token verification."""
        data = {"sub": "testuser", "role": "admin"}
        token = create_access_token(data)
        
        payload = verify_token(token)
        assert payload is not None
        assert payload["sub"] == "testuser"
        assert payload["role"] == "admin"
    
    def test_invalid_token(self):
        """Test invalid token handling."""
        invalid_token = "invalid.token.here"
        payload = verify_token(invalid_token)
        assert payload is None
        
        # Empty token
        payload = verify_token("")
        assert payload is None
        
        # None token
        payload = verify_token(None)
        assert payload is None


class TestInputSanitization:
    """Test input sanitization functionality."""
    
    def test_xss_prevention(self):
        """Test XSS prevention in input sanitization."""
        malicious_input = '<script>alert("xss")</script>Hello World'
        sanitized = sanitize_input(malicious_input)
        
        assert '<script>' not in sanitized
        assert 'alert' in sanitized  # Content should be preserved
        assert 'Hello World' in sanitized
    
    def test_html_tag_removal(self):
        """Test HTML tag removal."""
        html_input = '<div><p>Hello</p></div><span>World</span>'
        sanitized = sanitize_input(html_input)
        
        assert '<div>' not in sanitized
        assert '<p>' not in sanitized
        assert '<span>' not in sanitized
        assert 'Hello' in sanitized
        assert 'World' in sanitized
    
    def test_dangerous_characters(self):
        """Test removal of dangerous characters."""
        dangerous_input = 'Hello "World" <test>'
        sanitized = sanitize_input(dangerous_input)
        
        assert '"' not in sanitized
        assert '<' not in sanitized
        assert '>' not in sanitized
        assert 'Hello' in sanitized
        assert 'World' in sanitized
    
    def test_empty_input(self):
        """Test empty input handling."""
        assert sanitize_input("") == ""
        assert sanitize_input(None) == ""


class TestFileValidation:
    """Test file validation functionality."""
    
    def test_file_type_validation(self):
        """Test file type validation."""
        allowed_types = ['image/png', 'image/jpeg', 'image/jpg']
        
        # Valid types
        assert validate_file_type('image/png', allowed_types)
        assert validate_file_type('image/jpeg', allowed_types)
        assert validate_file_type('image/jpg', allowed_types)
        
        # Invalid types
        assert not validate_file_type('text/html', allowed_types)
        assert not validate_file_type('application/pdf', allowed_types)
        assert not validate_file_type('', allowed_types)
    
    def test_file_size_validation(self):
        """Test file size validation."""
        max_size = 10 * 1024 * 1024  # 10MB
        
        # Valid sizes
        assert validate_file_size(1024, max_size)  # 1KB
        assert validate_file_size(max_size, max_size)  # Exactly 10MB
        assert validate_file_size(0, max_size)  # Empty file
        
        # Invalid sizes
        assert not validate_file_size(max_size + 1, max_size)  # 10MB + 1 byte
        assert not validate_file_size(max_size * 2, max_size)  # 20MB


class TestUserAuthentication:
    """Test user authentication functionality."""
    
    def test_valid_user_authentication(self):
        """Test authentication with valid credentials."""
        user = authenticate_user("admin", "admin123")
        
        assert user is not None
        assert user["username"] == "admin"
        assert user["role"] == "admin"
        assert "admin" in user["permissions"]
    
    def test_invalid_password(self):
        """Test authentication with invalid password."""
        user = authenticate_user("admin", "wrongpassword")
        assert user is None
    
    def test_nonexistent_user(self):
        """Test authentication with nonexistent user."""
        user = authenticate_user("nonexistent", "password")
        assert user is None
    
    def test_empty_credentials(self):
        """Test authentication with empty credentials."""
        user = authenticate_user("", "password")
        assert user is None
        
        user = authenticate_user("admin", "")
        assert user is None
