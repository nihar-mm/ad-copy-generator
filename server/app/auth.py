"""
Authentication and authorization module for Ad Copy Regenerator
"""

from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.config import settings
import logging

logger = logging.getLogger(__name__)

# Security configuration
SECURITY_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 hours

# Password hashing - using simple hash for testing
import hashlib

def simple_hash(password: str) -> str:
    """Simple password hash for testing - use bcrypt in production"""
    if password is None:
        return None
    return hashlib.sha256(password.encode()).hexdigest()

def simple_verify(password: str, hashed: str) -> bool:
    """Simple password verification for testing"""
    if password is None or hashed is None:
        return False
    return simple_hash(password) == hashed

# For production, use: pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
pwd_context = None

# Bearer token scheme
security = HTTPBearer()

# For development - in production, these would be stored securely
ADMIM_CREDENTIALS = {
    "admin": {
        "username": "admin",
        "hashed_password": simple_hash("admin123"),
        "role": "admin",
        "permissions": ["read", "write", "admin"]
    },
    "demo": {
        "username": "demo", 
        "hashed_password": simple_hash("demo123"),
        "role": "user",
        "permissions": ["read", "write"]
    }
}


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return simple_verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a password"""
    return simple_hash(password)


def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token"""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=SECURITY_ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> Optional[Dict[str, Any]]:
    """Verify and decode a JWT token"""
    if token is None:
        return None
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[SECURITY_ALGORITHM])
        return payload
    except JWTError as e:
        logger.warning(f"Token verification failed: {e}")
        return None


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict[str, Any]:
    """Get current user from JWT token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = verify_token(credentials.credentials)
        if payload is None:
            raise credentials_exception
        
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
            
        # In production, this would query a database
        user = ADMIM_CREDENTIALS.get(username)
        if user is None:
            raise credentials_exception
            
        return user
        
    except JWTError:
        raise credentials_exception


async def get_current_active_user(current_user: Dict[str, Any] = Depends(get_current_user)) -> Dict[str, Any]:
    """Get current active user"""
    # Add any additional user validation here
    return current_user


async def require_admin_permission(current_user: Dict[str, Any] = Depends(get_current_user)) -> Dict[str, Any]:
    """Require admin permissions"""
    if "admin" not in current_user.get("permissions", []):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin permissions required"
        )
    return current_user


def authenticate_user(username: str, password: str) -> Optional[Dict[str, Any]]:
    """Authenticate a user with username and password"""
    user = ADMIM_CREDENTIALS.get(username)
    if not user:
        return None
    if not verify_password(password, user["hashed_password"]):
        return None
    return user


# Rate limiting helpers
def get_rate_limit_key(request, endpoint: str = None) -> str:
    """Generate a rate limit key for a request"""
    # Use user ID if authenticated, otherwise IP address
    if hasattr(request.state, 'user') and request.state.user:
        return f"user:{request.state.user['username']}:{endpoint or 'default'}"
    else:
        return f"ip:{request.client.host}:{endpoint or 'default'}"


# Input sanitization
def sanitize_input(text: str) -> str:
    """Sanitize user input to prevent XSS and injection attacks"""
    if not text:
        return ""
    
    # Remove potentially dangerous characters
    import re
    text = re.sub(r'<[^>]+>', '', text)  # Remove HTML tags
    text = re.sub(r'[<>"\']', '', text)  # Remove dangerous characters
    text = text.strip()  # Remove whitespace
    
    return text


def validate_file_type(content_type: str, allowed_types: list) -> bool:
    """Validate file type"""
    return content_type in allowed_types


def validate_file_size(size: int, max_size: int) -> bool:
    """Validate file size"""
    return size <= max_size


# Security headers middleware
def add_security_headers(response):
    """Add security headers to response"""
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    return response
  
