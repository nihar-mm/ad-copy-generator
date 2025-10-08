"""
Caching module for Ad Copy Regenerator
"""

import json
import logging
import time
import re
from typing import Any, Optional, Union
from datetime import timedelta
import redis
from app.config import settings

logger = logging.getLogger(__name__)

# Redis connection
redis_client = None

def get_redis_client():
    """Get Redis client with connection pooling"""
    global redis_client
    
    if redis_client is None:
        try:
            redis_client = redis.Redis.from_url(
                settings.REDIS_URL,
                decode_responses=True,
                socket_connect_timeout=5,
                socket_timeout=5,
                retry_on_timeout=True,
                health_check_interval=30
            )
            # Test connection
            redis_client.ping()
            logger.info("Redis connection established")
        except Exception as e:
            logger.warning(f"Redis connection failed: {e}. Using in-memory cache.")
            redis_client = None
    
    return redis_client


class CacheManager:
    """Cache manager with Redis and fallback to in-memory"""
    
    def __init__(self):
        self.redis = get_redis_client()
        self.memory_cache = {} if not self.redis else None
        self.cache_ttl = 3600  # 1 hour default TTL
    
    def _serialize(self, value: Any) -> str:
        """Serialize value for storage"""
        return json.dumps(value)
    
    def _deserialize(self, value: str) -> Any:
        """Deserialize value from storage"""
        try:
            return json.loads(value)
        except (json.JSONDecodeError, TypeError):
            return value
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        try:
            if self.redis:
                value = self.redis.get(key)
                return self._deserialize(value) if value else None
            else:
                # Fallback to memory cache with TTL support
                if key in self.memory_cache:
                    entry = self.memory_cache[key]
                    if entry["expires"] is None or time.time() < entry["expires"]:
                        return entry["value"]
                    else:
                        # Expired, remove it
                        del self.memory_cache[key]
                return None
        except Exception as e:
            logger.warning(f"Cache get error for key {key}: {e}")
            return None
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """Set value in cache"""
        try:
            serialized_value = self._serialize(value)
            ttl = ttl or self.cache_ttl
            
            if self.redis:
                return self.redis.setex(key, ttl, serialized_value)
            else:
                # Fallback to memory cache with TTL support
                expires = None
                if ttl:
                    expires = time.time() + ttl
                self.memory_cache[key] = {"value": value, "expires": expires}
                return True
        except Exception as e:
            logger.warning(f"Cache set error for key {key}: {e}")
            return False
    
    def delete(self, key: str) -> bool:
        """Delete value from cache"""
        try:
            if self.redis:
                return bool(self.redis.delete(key))
            else:
                # Fallback to memory cache
                if key in self.memory_cache:
                    del self.memory_cache[key]
                    return True
                return False
        except Exception as e:
            logger.warning(f"Cache delete error for key {key}: {e}")
            return False
    
    def exists(self, key: str) -> bool:
        """Check if key exists in cache"""
        try:
            if self.redis:
                return bool(self.redis.exists(key))
            else:
                return key in self.memory_cache
        except Exception as e:
            logger.warning(f"Cache exists error for key {key}: {e}")
            return False
    
    def clear(self) -> bool:
        """Clear all cache"""
        try:
            if self.redis:
                return bool(self.redis.flushdb())
            else:
                self.memory_cache.clear()
                return True
        except Exception as e:
            logger.warning(f"Cache clear error: {e}")
            return False
    
    def delete_pattern(self, pattern: str) -> int:
        """Delete keys matching pattern (Redis wildcard style)"""
        deleted_count = 0
        try:
            if self.redis:
                keys = self.redis.keys(pattern)
                if keys:
                    deleted_count = self.redis.delete(*keys)
            else:
                # Fallback to memory cache pattern matching
                pattern_regex = pattern.replace('*', '.*')
                keys_to_delete = []
                for key in self.memory_cache.keys():
                    if re.match(pattern_regex, key):
                        keys_to_delete.append(key)
                
                for key in keys_to_delete:
                    del self.memory_cache[key]
                    deleted_count += 1
        except Exception as e:
            logger.warning(f"Cache pattern delete error for pattern {pattern}: {e}")
        return deleted_count


# Global cache instance
cache = CacheManager()


def cache_result(key: str, ttl: int = 3600):
    """Decorator to cache function results"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            # Generate cache key from function name and arguments
            cache_key = f"{func.__name__}:{hash(str(args) + str(kwargs))}"
            
            # Try to get from cache first
            cached_result = cache.get(cache_key)
            if cached_result is not None:
                logger.debug(f"Cache hit for {cache_key}")
                return cached_result
            
            # Execute function and cache result
            result = func(*args, **kwargs)
            cache.set(cache_key, result, ttl)
            logger.debug(f"Cached result for {cache_key}")
            return result
        
        return wrapper
    return decorator


def invalidate_cache_pattern(pattern: str) -> int:
    """Invalidate cache keys matching pattern"""
    return cache.delete_pattern(pattern)


# Cache key generators
def job_cache_key(job_id: str) -> str:
    """Generate cache key for job"""
    return f"job:{job_id}"


def user_cache_key(user_id: str) -> str:
    """Generate cache key for user"""
    return f"user:{user_id}"


def api_cache_key(endpoint: str, params: dict) -> str:
    """Generate cache key for API endpoint"""
    params_str = "_".join(f"{k}:{v}" for k, v in sorted(params.items()))
    return f"api:{endpoint}:{hash(params_str)}"
