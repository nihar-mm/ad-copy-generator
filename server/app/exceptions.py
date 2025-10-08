"""
Custom exception classes for the Ad Copy Regenerator API
"""

from fastapi import HTTPException, status
from typing import Any, Dict, Optional


class AdCopyException(Exception):
    """Base exception for Ad Copy Regenerator"""
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        self.message = message
        self.details = details or {}
        super().__init__(self.message)


class ValidationError(AdCopyException):
    """Raised when input validation fails"""
    pass


class ProcessingError(AdCopyException):
    """Raised when image processing fails"""
    pass


class LLMError(AdCopyException):
    """Raised when LLM API calls fail"""
    pass


class StorageError(AdCopyException):
    """Raised when file storage operations fail"""
    pass


class DatabaseError(AdCopyException):
    """Raised when database operations fail"""
    pass


# HTTP Exception helpers
def raise_validation_error(message: str, details: Optional[Dict[str, Any]] = None) -> HTTPException:
    """Raise a 400 Bad Request error"""
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail={
            "error": "validation_error",
            "message": message,
            "details": details or {}
        }
    )


def raise_processing_error(message: str, details: Optional[Dict[str, Any]] = None) -> HTTPException:
    """Raise a 422 Unprocessable Entity error"""
    raise HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail={
            "error": "processing_error",
            "message": message,
            "details": details or {}
        }
    )


def raise_internal_error(message: str, details: Optional[Dict[str, Any]] = None) -> HTTPException:
    """Raise a 500 Internal Server Error"""
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail={
            "error": "internal_error",
            "message": message,
            "details": details or {}
        }
    )


def raise_not_found_error(resource: str, identifier: str) -> HTTPException:
    """Raise a 404 Not Found error"""
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail={
            "error": "not_found",
            "message": f"{resource} not found",
            "details": {"identifier": identifier}
        }
    )


def raise_rate_limit_error() -> HTTPException:
    """Raise a 429 Too Many Requests error"""
    raise HTTPException(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        detail={
            "error": "rate_limit_exceeded",
            "message": "Too many requests. Please try again later.",
            "details": {"retry_after": 60}
        }
    )
