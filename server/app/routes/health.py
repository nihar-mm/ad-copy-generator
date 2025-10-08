from fastapi import APIRouter, Request
from app.config import settings
from app.performance import get_performance_summary, get_system_metrics
from app.cache import cache
from app.db.session import check_database_health, get_database_stats
import logging
import time

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/")
def health():
    """Basic health check"""
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "version": "1.0.0",
        "environment": settings.APP_ENV
    }

@router.get("/detailed")
def detailed_health():
    """Detailed health check with system metrics"""
    try:
        system_metrics = get_system_metrics()
        performance_summary = get_performance_summary()
        
        # Check critical components
        cache_status = "healthy" if cache.redis else "degraded"
        db_health = check_database_health()
        db_status = "healthy" if db_health["healthy"] else "unhealthy"
        
        # Get database statistics
        db_stats = {}
        try:
            db_stats = get_database_stats()
        except Exception as e:
            logger.warning(f"Could not get database stats: {e}")
        
        overall_status = "healthy"
        if not db_health["healthy"]:
            overall_status = "unhealthy"
        elif cache_status == "degraded":
            overall_status = "degraded"
        
        return {
            "status": overall_status,
            "timestamp": time.time(),
            "version": "1.0.0",
            "environment": settings.APP_ENV,
            "components": {
                "database": {
                    "status": db_status,
                    "response_time_ms": db_health["response_time_ms"],
                    "type": db_health["database_type"],
                    "error": db_health["error"],
                    "pool_stats": db_stats
                },
                "cache": {
                    "status": cache_status,
                    "backend": "redis" if cache.redis else "in-memory"
                },
                "storage": {
                    "backend": settings.STORAGE_BACKEND
                }
            },
            "system_metrics": system_metrics,
            "performance": performance_summary
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {
            "status": "unhealthy",
            "timestamp": time.time(),
            "error": str(e)
        }

@router.get("/context")
def context_health(request: Request):
    cm = getattr(request.app.state, "context_manager", None)
    if not cm:
        return {"ok": False, "reason": "context_manager_not_initialized"}
    try:
        count = cm.collection.count()
        return {"ok": True, "chunks": count}
    except Exception:
        return {"ok": False, "reason": "context_unavailable"}
