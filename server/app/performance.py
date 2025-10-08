"""
Performance monitoring and optimization module
"""

import time
import asyncio
import logging
from functools import wraps
from typing import Any, Callable, Dict, List
from contextlib import asynccontextmanager
from app.cache import cache
import psutil
import os

logger = logging.getLogger(__name__)

# Performance metrics storage
performance_metrics = {
    "api_calls": {},
    "function_times": {},
    "cache_hits": 0,
    "cache_misses": 0,
    "memory_usage": [],
    "cpu_usage": []
}


def monitor_performance(func_name: str = None):
    """Decorator to monitor function performance"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            name = func_name or f"{func.__module__}.{func.__name__}"
            start_time = time.time()
            
            try:
                result = await func(*args, **kwargs)
                execution_time = time.time() - start_time
                
                # Store metrics
                if name not in performance_metrics["function_times"]:
                    performance_metrics["function_times"][name] = []
                
                performance_metrics["function_times"][name].append({
                    "execution_time": execution_time,
                    "timestamp": time.time(),
                    "success": True
                })
                
                # Log slow operations
                if execution_time > 1.0:  # Log operations taking more than 1 second
                    logger.warning(f"Slow operation: {name} took {execution_time:.3f}s")
                
                return result
                
            except Exception as e:
                execution_time = time.time() - start_time
                
                # Store error metrics
                if name not in performance_metrics["function_times"]:
                    performance_metrics["function_times"][name] = []
                
                performance_metrics["function_times"][name].append({
                    "execution_time": execution_time,
                    "timestamp": time.time(),
                    "success": False,
                    "error": str(e)
                })
                
                logger.error(f"Function {name} failed after {execution_time:.3f}s: {e}")
                raise
        
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            name = func_name or f"{func.__module__}.{func.__name__}"
            start_time = time.time()
            
            try:
                result = func(*args, **kwargs)
                execution_time = time.time() - start_time
                
                # Store metrics
                if name not in performance_metrics["function_times"]:
                    performance_metrics["function_times"][name] = []
                
                performance_metrics["function_times"][name].append({
                    "execution_time": execution_time,
                    "timestamp": time.time(),
                    "success": True
                })
                
                # Log slow operations
                if execution_time > 1.0:
                    logger.warning(f"Slow operation: {name} took {execution_time:.3f}s")
                
                return result
                
            except Exception as e:
                execution_time = time.time() - start_time
                
                # Store error metrics
                if name not in performance_metrics["function_times"]:
                    performance_metrics["function_times"][name] = []
                
                performance_metrics["function_times"][name].append({
                    "execution_time": execution_time,
                    "timestamp": time.time(),
                    "success": False,
                    "error": str(e)
                })
                
                logger.error(f"Function {name} failed after {execution_time:.3f}s: {e}")
                raise
        
        # Return appropriate wrapper based on function type
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper
    
    return decorator


@asynccontextmanager
async def performance_context(operation_name: str):
    """Context manager for performance monitoring"""
    start_time = time.time()
    
    try:
        yield
    finally:
        execution_time = time.time() - start_time
        
        # Store metrics
        if operation_name not in performance_metrics["function_times"]:
            performance_metrics["function_times"][operation_name] = []
        
        performance_metrics["function_times"][operation_name].append({
            "execution_time": execution_time,
            "timestamp": time.time(),
            "success": True
        })


def get_system_metrics() -> Dict[str, Any]:
    """Get current system performance metrics"""
    try:
        # Memory usage
        memory = psutil.virtual_memory()
        
        # CPU usage
        cpu_percent = psutil.cpu_percent(interval=1)
        
        # Disk usage
        disk = psutil.disk_usage('/')
        
        # Process info
        process = psutil.Process(os.getpid())
        process_memory = process.memory_info()
        
        return {
            "timestamp": time.time(),
            "memory": {
                "total": memory.total,
                "available": memory.available,
                "used": memory.used,
                "percentage": memory.percent
            },
            "cpu": {
                "percentage": cpu_percent,
                "count": psutil.cpu_count()
            },
            "disk": {
                "total": disk.total,
                "used": disk.used,
                "free": disk.free,
                "percentage": (disk.used / disk.total) * 100
            },
            "process": {
                "memory_rss": process_memory.rss,
                "memory_vms": process_memory.vms,
                "cpu_percent": process.cpu_percent(),
                "num_threads": process.num_threads()
            }
        }
    except Exception as e:
        logger.error(f"Failed to get system metrics: {e}")
        return {}


def get_performance_summary() -> Dict[str, Any]:
    """Get performance summary"""
    summary = {
        "timestamp": time.time(),
        "system_metrics": get_system_metrics(),
        "function_metrics": {},
        "cache_stats": {
            "hits": performance_metrics["cache_hits"],
            "misses": performance_metrics["cache_misses"],
            "hit_rate": 0
        }
    }
    
    # Calculate cache hit rate
    total_cache_requests = performance_metrics["cache_hits"] + performance_metrics["cache_misses"]
    if total_cache_requests > 0:
        summary["cache_stats"]["hit_rate"] = performance_metrics["cache_hits"] / total_cache_requests
    
    # Calculate function averages
    for func_name, times in performance_metrics["function_times"].items():
        if times:
            successful_times = [t["execution_time"] for t in times if t.get("success", True)]
            if successful_times:
                summary["function_metrics"][func_name] = {
                    "avg_time": sum(successful_times) / len(successful_times),
                    "min_time": min(successful_times),
                    "max_time": max(successful_times),
                    "total_calls": len(times),
                    "success_rate": len(successful_times) / len(times)
                }
    
    return summary


def optimize_database_query(query_func: Callable) -> Callable:
    """Decorator to optimize database queries with caching"""
    @wraps(query_func)
    async def wrapper(*args, **kwargs):
        # Generate cache key
        cache_key = f"db_query:{query_func.__name__}:{hash(str(args) + str(kwargs))}"
        
        # Try cache first
        cached_result = cache.get(cache_key)
        if cached_result is not None:
            performance_metrics["cache_hits"] += 1
            return cached_result
        
        # Execute query
        result = await query_func(*args, **kwargs)
        
        # Cache result for 5 minutes
        cache.set(cache_key, result, 300)
        performance_metrics["cache_misses"] += 1
        
        return result
    
    return wrapper


def batch_process(items: List[Any], batch_size: int = 10, delay: float = 0.1) -> List[Any]:
    """Process items in batches to avoid overwhelming the system"""
    results = []
    
    for i in range(0, len(items), batch_size):
        batch = items[i:i + batch_size]
        results.extend(batch)
        
        # Add delay between batches
        if i + batch_size < len(items):
            time.sleep(delay)
    
    return results


async def async_batch_process(items: List[Any], batch_size: int = 10, delay: float = 0.1) -> List[Any]:
    """Async version of batch processing"""
    results = []
    
    for i in range(0, len(items), batch_size):
        batch = items[i:i + batch_size]
        results.extend(batch)
        
        # Add delay between batches
        if i + batch_size < len(items):
            await asyncio.sleep(delay)
    
    return results


def cleanup_old_metrics():
    """Clean up old performance metrics to prevent memory leaks"""
    current_time = time.time()
    cutoff_time = current_time - (24 * 60 * 60)  # Keep only last 24 hours
    
    for func_name in list(performance_metrics["function_times"].keys()):
        times = performance_metrics["function_times"][func_name]
        performance_metrics["function_times"][func_name] = [
            t for t in times if t["timestamp"] > cutoff_time
        ]
        
        # Remove empty entries
        if not performance_metrics["function_times"][func_name]:
            del performance_metrics["function_times"][func_name]
    
    # Clean up system metrics (keep only last 100 entries)
    if len(performance_metrics["memory_usage"]) > 100:
        performance_metrics["memory_usage"] = performance_metrics["memory_usage"][-100:]
    
    if len(performance_metrics["cpu_usage"]) > 100:
        performance_metrics["cpu_usage"] = performance_metrics["cpu_usage"][-100:]

