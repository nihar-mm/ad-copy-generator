"""
Unit tests for cache module
"""

import pytest
import time
from app.cache import CacheManager, cache_result, invalidate_cache_pattern


class TestCacheManager:
    """Test cache manager functionality."""
    
    def test_cache_set_get(self):
        """Test basic cache set and get operations."""
        cache = CacheManager()
        
        # Test setting and getting a value
        key = "test_key"
        value = {"message": "Hello World", "timestamp": time.time()}
        
        cache.set(key, value, 60)
        retrieved_value = cache.get(key)
        
        assert retrieved_value == value
    
    def test_cache_exists(self):
        """Test cache exists functionality."""
        cache = CacheManager()
        key = "test_key"
        
        # Initially doesn't exist
        assert not cache.exists(key)
        
        # After setting, should exist
        cache.set(key, "test_value", 60)
        assert cache.exists(key)
    
    def test_cache_delete(self):
        """Test cache delete functionality."""
        cache = CacheManager()
        key = "test_key"
        
        # Set a value
        cache.set(key, "test_value", 60)
        assert cache.exists(key)
        
        # Delete the value
        deleted = cache.delete(key)
        assert deleted
        assert not cache.exists(key)
    
    def test_cache_ttl(self):
        """Test cache TTL functionality."""
        cache = CacheManager()
        key = "test_key"
        value = "test_value"
        
        # Set with short TTL
        cache.set(key, value, 1)  # 1 second TTL
        assert cache.get(key) == value
        
        # Wait for expiration
        time.sleep(1.1)
        assert cache.get(key) is None
    
    def test_cache_serialization(self):
        """Test cache serialization of complex objects."""
        cache = CacheManager()
        key = "complex_key"
        value = {
            "string": "Hello",
            "number": 42,
            "list": [1, 2, 3],
            "dict": {"nested": "value"},
            "boolean": True,
            "none": None
        }
        
        cache.set(key, value, 60)
        retrieved_value = cache.get(key)
        
        assert retrieved_value == value
        assert retrieved_value["string"] == "Hello"
        assert retrieved_value["number"] == 42
        assert retrieved_value["list"] == [1, 2, 3]
        assert retrieved_value["dict"]["nested"] == "value"
        assert retrieved_value["boolean"] is True
        assert retrieved_value["none"] is None


class TestCacheDecorator:
    """Test cache decorator functionality."""
    
    def test_cache_result_decorator(self):
        """Test the cache_result decorator."""
        call_count = 0
        
        @cache_result("test_function", 60)
        def test_function(x):
            nonlocal call_count
            call_count += 1
            return x * 2
        
        # First call should execute function
        result1 = test_function(5)
        assert result1 == 10
        assert call_count == 1
        
        # Second call should use cache
        result2 = test_function(5)
        assert result2 == 10
        assert call_count == 1  # Should not increment
        
        # Different parameter should execute function again
        result3 = test_function(3)
        assert result3 == 6
        assert call_count == 2
    
    def test_cache_result_with_different_parameters(self):
        """Test cache decorator with different parameters."""
        @cache_result("test_function", 60)
        def test_function(x, y=None):
            return f"{x}_{y}"
        
        # Different combinations should be cached separately
        result1 = test_function(1, y="a")
        result2 = test_function(1, y="b")
        result3 = test_function(2, y="a")
        
        assert result1 == "1_a"
        assert result2 == "1_b"
        assert result3 == "2_a"
        assert result1 != result2 != result3


class TestCacheUtilities:
    """Test cache utility functions."""
    
    def test_invalidate_cache_pattern(self):
        """Test cache pattern invalidation."""
        from app.cache import cache
        
        # Set multiple keys with pattern
        cache.set("user:1:profile", {"name": "Alice"}, 60)
        cache.set("user:2:profile", {"name": "Bob"}, 60)
        cache.set("user:1:settings", {"theme": "dark"}, 60)
        cache.set("other:key", {"value": "test"}, 60)
        
        # Invalidate pattern
        invalidated = invalidate_cache_pattern("user:*")
        
        # Check that pattern keys are invalidated
        assert cache.get("user:1:profile") is None
        assert cache.get("user:2:profile") is None
        assert cache.get("user:1:settings") is None
        
        # Check that non-pattern keys are still there
        assert cache.get("other:key") is not None


class TestCacheErrorHandling:
    """Test cache error handling."""
    
    def test_cache_with_none_values(self):
        """Test cache handling of None values."""
        cache = CacheManager()
        key = "none_key"
        
        # Should handle None values
        cache.set(key, None, 60)
        retrieved_value = cache.get(key)
        assert retrieved_value is None
    
    def test_cache_with_empty_string(self):
        """Test cache handling of empty strings."""
        cache = CacheManager()
        key = "empty_key"
        
        cache.set(key, "", 60)
        retrieved_value = cache.get(key)
        assert retrieved_value == ""
    
    def test_cache_with_invalid_key(self):
        """Test cache handling of invalid keys."""
        cache = CacheManager()
        
        # Should handle empty key
        cache.set("", "value", 60)
        assert cache.get("") == "value"
        
        # Should handle None key
        cache.set(None, "value", 60)
        assert cache.get(None) == "value"
