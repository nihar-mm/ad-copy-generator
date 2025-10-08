"""
Authentication routes for Ad Copy Regenerator
"""

from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.auth import authenticate_user, create_access_token, get_current_active_user
from app.config import settings
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 hours


@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Login endpoint for authentication"""
    try:
        # Authenticate user
        user = authenticate_user(form_data.username, form_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Create access token
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user["username"], "role": user["role"]}, 
            expires_delta=access_token_expires
        )
        
        logger.info(f"User {user['username']} logged in successfully")
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            "user": {
                "username": user["username"],
                "role": user["role"],
                "permissions": user["permissions"]
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Login failed"
        )


@router.get("/me")
async def read_users_me(current_user: dict = Depends(get_current_active_user)):
    """Get current user information"""
    return {
        "username": current_user["username"],
        "role": current_user["role"],
        "permissions": current_user["permissions"]
    }


@router.post("/logout")
async def logout(current_user: dict = Depends(get_current_active_user)):
    """Logout endpoint"""
    logger.info(f"User {current_user['username']} logged out")
    return {"message": "Successfully logged out"}
