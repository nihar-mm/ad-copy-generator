"""
Error handling middleware for the Ad Copy Regenerator API
"""

import logging
import traceback
from typing import Union
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from sqlalchemy.exc import SQLAlchemyError
from app.exceptions import AdCopyException
import time

logger = logging.getLogger(__name__)


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """Handle HTTP exceptions"""
    logger.warning(f"HTTP exception: {exc.status_code} - {exc.detail}")
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": "http_error",
            "message": str(exc.detail),
            "status_code": exc.status_code,
            "path": str(request.url.path),
            "method": request.method,
            "timestamp": time.time()
        }
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """Handle validation exceptions"""
    logger.warning(f"Validation error: {exc.errors()}")
    
    return JSONResponse(
        status_code=422,
        content={
            "error": "validation_error",
            "message": "Request validation failed",
            "details": exc.errors(),
            "path": str(request.url.path),
            "method": request.method,
            "timestamp": time.time()
        }
    )


async def adcopy_exception_handler(request: Request, exc: AdCopyException) -> JSONResponse:
    """Handle custom AdCopy exceptions"""
    logger.error(f"AdCopy exception: {exc.message} - {exc.details}")
    
    return JSONResponse(
        status_code=500,
        content={
            "error": "adcopy_error",
            "message": exc.message,
            "details": exc.details,
            "path": str(request.url.path),
            "method": request.method,
            "timestamp": time.time()
        }
    )


async def database_exception_handler(request: Request, exc: SQLAlchemyError) -> JSONResponse:
    """Handle database exceptions"""
    logger.error(f"Database error: {str(exc)}")
    
    return JSONResponse(
        status_code=500,
        content={
            "error": "database_error",
            "message": "Database operation failed",
            "details": {"error": str(exc)},
            "path": str(request.url.path),
            "method": request.method,
            "timestamp": time.time()
        }
    )


async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle all other exceptions"""
    logger.error(f"Unhandled exception: {str(exc)}")
    logger.error(f"Traceback: {traceback.format_exc()}")
    
    return JSONResponse(
        status_code=500,
        content={
            "error": "internal_error",
            "message": "An unexpected error occurred",
            "details": {"error": str(exc)},
            "path": str(request.url.path),
            "method": request.method,
            "timestamp": time.time()
        }
    )


def setup_error_handlers(app):
    """Setup all error handlers for the FastAPI app"""
    
    # Add exception handlers
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(AdCopyException, adcopy_exception_handler)
    app.add_exception_handler(SQLAlchemyError, database_exception_handler)
    app.add_exception_handler(Exception, general_exception_handler)
    
    logger.info("Error handlers configured successfully")


async def log_request_exceptions(request: Request, call_next):
    """Middleware to log request exceptions"""
    try:
        response = await call_next(request)
        return response
    except Exception as exc:
        logger.error(f"Request exception in {request.method} {request.url.path}: {exc}")
        raise
