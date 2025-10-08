"""
Unit tests for custom exceptions
"""

import pytest
from app.exceptions import (
    AdCopyException, ValidationError, ProcessingError, LLMError,
    StorageError, DatabaseError, raise_validation_error, raise_processing_error,
    raise_internal_error, raise_not_found_error, raise_rate_limit_error
)
from fastapi import HTTPException


class TestCustomExceptions:
    """Test custom exception classes."""
    
    def test_adcopy_exception(self):
        """Test base AdCopyException."""
        message = "Test error message"
        details = {"field": "test_field", "value": "test_value"}
        
        exception = AdCopyException(message, details)
        
        assert exception.message == message
        assert exception.details == details
        assert str(exception) == message
    
    def test_validation_error(self):
        """Test ValidationError."""
        message = "Validation failed"
        details = {"errors": ["field1 is required", "field2 is invalid"]}
        
        exception = ValidationError(message, details)
        
        assert isinstance(exception, AdCopyException)
        assert exception.message == message
        assert exception.details == details
    
    def test_processing_error(self):
        """Test ProcessingError."""
        message = "Processing failed"
        details = {"step": "image_processing", "reason": "timeout"}
        
        exception = ProcessingError(message, details)
        
        assert isinstance(exception, AdCopyException)
        assert exception.message == message
        assert exception.details == details
    
    def test_llm_error(self):
        """Test LLMError."""
        message = "LLM API failed"
        details = {"model": "gpt-4", "error_code": 429}
        
        exception = LLMError(message, details)
        
        assert isinstance(exception, AdCopyException)
        assert exception.message == message
        assert exception.details == details
    
    def test_storage_error(self):
        """Test StorageError."""
        message = "Storage operation failed"
        details = {"operation": "upload", "file": "test.png"}
        
        exception = StorageError(message, details)
        
        assert isinstance(exception, AdCopyException)
        assert exception.message == message
        assert exception.details == details
    
    def test_database_error(self):
        """Test DatabaseError."""
        message = "Database operation failed"
        details = {"query": "SELECT * FROM users", "error": "connection timeout"}
        
        exception = DatabaseError(message, details)
        
        assert isinstance(exception, AdCopyException)
        assert exception.message == message
        assert exception.details == details
    
    def test_exception_without_details(self):
        """Test exceptions without details."""
        message = "Simple error message"
        
        exception = ValidationError(message)
        
        assert exception.message == message
        assert exception.details == {}
    
    def test_exception_with_none_details(self):
        """Test exceptions with None details."""
        message = "Error with None details"
        
        exception = ProcessingError(message, None)
        
        assert exception.message == message
        assert exception.details == {}


class TestExceptionHelpers:
    """Test exception helper functions."""
    
    def test_raise_validation_error(self):
        """Test raise_validation_error helper."""
        message = "Validation failed"
        details = {"field": "email", "error": "invalid format"}
        
        with pytest.raises(HTTPException) as exc_info:
            raise_validation_error(message, details)
        
        exception = exc_info.value
        assert exception.status_code == 400
        assert exception.detail["error"] == "validation_error"
        assert exception.detail["message"] == message
        assert exception.detail["details"] == details
    
    def test_raise_processing_error(self):
        """Test raise_processing_error helper."""
        message = "Processing failed"
        details = {"step": "ocr", "error": "timeout"}
        
        with pytest.raises(HTTPException) as exc_info:
            raise_processing_error(message, details)
        
        exception = exc_info.value
        assert exception.status_code == 422
        assert exception.detail["error"] == "processing_error"
        assert exception.detail["message"] == message
        assert exception.detail["details"] == details
    
    def test_raise_internal_error(self):
        """Test raise_internal_error helper."""
        message = "Internal server error"
        details = {"component": "database", "error": "connection lost"}
        
        with pytest.raises(HTTPException) as exc_info:
            raise_internal_error(message, details)
        
        exception = exc_info.value
        assert exception.status_code == 500
        assert exception.detail["error"] == "internal_error"
        assert exception.detail["message"] == message
        assert exception.detail["details"] == details
    
    def test_raise_not_found_error(self):
        """Test raise_not_found_error helper."""
        resource = "User"
        identifier = "user123"
        
        with pytest.raises(HTTPException) as exc_info:
            raise_not_found_error(resource, identifier)
        
        exception = exc_info.value
        assert exception.status_code == 404
        assert exception.detail["error"] == "not_found"
        assert exception.detail["message"] == "User not found"
        assert exception.detail["details"]["identifier"] == identifier
    
    def test_raise_rate_limit_error(self):
        """Test raise_rate_limit_error helper."""
        with pytest.raises(HTTPException) as exc_info:
            raise_rate_limit_error()
        
        exception = exc_info.value
        assert exception.status_code == 429
        assert exception.detail["error"] == "rate_limit_exceeded"
        assert exception.detail["message"] == "Too many requests. Please try again later."
        assert exception.detail["details"]["retry_after"] == 60
    
    def test_raise_validation_error_without_details(self):
        """Test raise_validation_error without details."""
        message = "Simple validation error"
        
        with pytest.raises(HTTPException) as exc_info:
            raise_validation_error(message)
        
        exception = exc_info.value
        assert exception.status_code == 400
        assert exception.detail["error"] == "validation_error"
        assert exception.detail["message"] == message
        assert exception.detail["details"] == {}
    
    def test_raise_processing_error_with_none_details(self):
        """Test raise_processing_error with None details."""
        message = "Processing error with None details"
        
        with pytest.raises(HTTPException) as exc_info:
            raise_processing_error(message, None)
        
        exception = exc_info.value
        assert exception.status_code == 422
        assert exception.detail["error"] == "processing_error"
        assert exception.detail["message"] == message
        assert exception.detail["details"] == {}
