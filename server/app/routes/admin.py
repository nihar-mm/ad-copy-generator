from fastapi import APIRouter, HTTPException, Depends, Request
from typing import Dict, List, Optional
from app.config import settings
import logging

router = APIRouter(prefix="/admin", tags=["admin"])
logger = logging.getLogger(__name__)

# In-memory storage for admin settings (in production, use database)
_admin_settings = {
    "character_caps": {
        "Headline": 60,
        "Subhead": 120,
        "CTA": 20,
        "Legal": 200
    },
    "banned_words": [
        "guaranteed", "miracle", "instant", "100%", "best", "cheapest",
        "free", "limited time", "act now", "urgent", "exclusive"
    ],
    "must_include": [],
    "risk_mode": "standard",
    "locale_rules": {
        "en-IN": {
            "currency": "INR",
            "date_format": "DD/MM/YYYY",
            "banned_phrases": ["foreign goods", "imported"]
        },
        "hi-IN": {
            "currency": "INR", 
            "date_format": "DD/MM/YYYY",
            "banned_phrases": ["विदेशी सामान", "आयातित"]
        }
    }
}

@router.get("/settings")
async def get_admin_settings():
    """Get current admin settings"""
    return _admin_settings

@router.put("/settings/character-caps")
async def update_character_caps(caps: Dict[str, int]):
    """Update character limits for different content types"""
    try:
        for content_type, limit in caps.items():
            if content_type in _admin_settings["character_caps"]:
                if limit < 10 or limit > 500:
                    raise HTTPException(status_code=400, detail=f"Invalid limit for {content_type}: must be between 10-500")
                _admin_settings["character_caps"][content_type] = limit
        
        logger.info(f"Updated character caps: {caps}")
        return {"message": "Character caps updated", "caps": _admin_settings["character_caps"]}
    except Exception as e:
        logger.error(f"Error updating character caps: {e}")
        raise HTTPException(status_code=500, detail="Failed to update character caps")

@router.put("/settings/banned-words")
async def update_banned_words(words: List[str]):
    """Update list of banned words/phrases"""
    try:
        # Validate words
        for word in words:
            if len(word.strip()) < 2:
                raise HTTPException(status_code=400, detail=f"Banned word too short: {word}")
        
        _admin_settings["banned_words"] = [w.strip().lower() for w in words if w.strip()]
        logger.info(f"Updated banned words: {len(_admin_settings['banned_words'])} words")
        return {"message": "Banned words updated", "count": len(_admin_settings["banned_words"])}
    except Exception as e:
        logger.error(f"Error updating banned words: {e}")
        raise HTTPException(status_code=500, detail="Failed to update banned words")

@router.put("/settings/must-include")
async def update_must_include(words: List[str]):
    """Update list of words that must be included"""
    try:
        _admin_settings["must_include"] = [w.strip() for w in words if w.strip()]
        logger.info(f"Updated must-include words: {len(_admin_settings['must_include'])} words")
        return {"message": "Must-include words updated", "count": len(_admin_settings["must_include"])}
    except Exception as e:
        logger.error(f"Error updating must-include words: {e}")
        raise HTTPException(status_code=500, detail="Failed to update must-include words")

@router.put("/settings/risk-mode")
async def update_risk_mode(mode: str):
    """Update risk mode (standard, strict, lenient)"""
    valid_modes = ["standard", "strict", "lenient"]
    if mode not in valid_modes:
        raise HTTPException(status_code=400, detail=f"Invalid risk mode. Must be one of: {valid_modes}")
    
    _admin_settings["risk_mode"] = mode
    logger.info(f"Updated risk mode to: {mode}")
    return {"message": "Risk mode updated", "mode": mode}

@router.get("/stats")
async def get_admin_stats():
    """Get system statistics"""
    return {
        "total_jobs": 0,  # TODO: Implement actual stats
        "active_jobs": 0,
        "failed_jobs": 0,
        "settings": {
            "character_caps_count": len(_admin_settings["character_caps"]),
            "banned_words_count": len(_admin_settings["banned_words"]),
            "must_include_count": len(_admin_settings["must_include"]),
            "risk_mode": _admin_settings["risk_mode"]
        }
    }

@router.post("/reload-context")
async def reload_context(request: Request):
    """Rebuild or update the vector store from context files."""
    try:
        context_manager = getattr(request.app.state, "context_manager", None)
        if not context_manager:
            raise HTTPException(status_code=503, detail="Context manager not initialized")
        updated = context_manager.load_or_ingest(force_reload=True)
        return {"message": "Context reloaded", "updated": updated}
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Failed to reload context: {e}")
        raise HTTPException(status_code=500, detail="Failed to reload context")


