"""Redis caching service for API responses"""
import redis
import json
import os
from typing import Optional, Any
import hashlib


class CacheService:
    """Redis cache for API responses and search results"""
    
    def __init__(self):
        redis_host = os.getenv("REDIS_HOST", "localhost")
        redis_port = int(os.getenv("REDIS_PORT", "6379"))
        cache_enabled = os.getenv("CACHE_ENABLED", "true").lower() == "true"
        
        self.enabled = cache_enabled
        self.default_ttl = int(os.getenv("CACHE_TTL", "3600"))
        
        if not self.enabled:
            print("⚠️  Cache disabled via configuration")
            self.redis = None
            return
        
        try:
            self.redis = redis.Redis(
                host=redis_host,
                port=redis_port,
                decode_responses=True,
                socket_connect_timeout=2
            )
            self.redis.ping()
            print(f"✅ Redis cache connected at {redis_host}:{redis_port}")
        except Exception as e:
            print(f"⚠️  Redis not available: {str(e)}")
            print("   Caching disabled - continuing without cache")
            self.enabled = False
            self.redis = None
    
    def _generate_key(self, prefix: str, data: dict) -> str:
        """
        Generate cache key from request data
        
        Args:
            prefix: Key prefix (e.g., 'research', 'document')
            data: Request data dict
            
        Returns:
            Cache key string
        """
        # Sort dict keys for consistent hashing
        data_str = json.dumps(data, sort_keys=True)
        hash_key = hashlib.md5(data_str.encode()).hexdigest()
        return f"elitecontent:{prefix}:{hash_key}"
    
    def get(self, key: str) -> Optional[Any]:
        """
        Get cached value
        
        Args:
            key: Cache key
            
        Returns:
            Cached value or None
        """
        if not self.enabled or not self.redis:
            return None
        
        try:
            value = self.redis.get(key)
            if value:
                print(f"✅ Cache HIT: {key[:50]}...")
                return json.loads(value)
            else:
                print(f"❌ Cache MISS: {key[:50]}...")
                return None
        except Exception as e:
            print(f"⚠️  Cache get error: {str(e)}")
            return None
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None):
        """
        Set cached value with TTL
        
        Args:
            key: Cache key
            value: Value to cache
            ttl: Time to live in seconds (default: from config)
        """
        if not self.enabled or not self.redis:
            return
        
        try:
            ttl = ttl or self.default_ttl
            self.redis.setex(key, ttl, json.dumps(value))
            print(f"✅ Cached: {key[:50]}... (TTL: {ttl}s)")
        except Exception as e:
            print(f"⚠️  Cache set error: {str(e)}")
    
    def delete(self, key: str):
        """
        Delete cached value
        
        Args:
            key: Cache key
        """
        if not self.enabled or not self.redis:
            return
        
        try:
            self.redis.delete(key)
            print(f"✅ Cache deleted: {key[:50]}...")
        except Exception as e:
            print(f"⚠️  Cache delete error: {str(e)}")
    
    def clear_pattern(self, pattern: str):
        """
        Clear all keys matching pattern
        
        Args:
            pattern: Key pattern (e.g., 'elitecontent:research:*')
        """
        if not self.enabled or not self.redis:
            return
        
        try:
            keys = self.redis.keys(pattern)
            if keys:
                self.redis.delete(*keys)
                print(f"✅ Cleared {len(keys)} keys matching: {pattern}")
        except Exception as e:
            print(f"⚠️  Cache clear error: {str(e)}")
    
    def get_stats(self) -> dict:
        """Get cache statistics"""
        if not self.enabled or not self.redis:
            return {"enabled": False}
        
        try:
            info = self.redis.info()
            return {
                "enabled": True,
                "connected": True,
                "used_memory": info.get("used_memory_human", "N/A"),
                "total_keys": self.redis.dbsize(),
                "hits": info.get("keyspace_hits", 0),
                "misses": info.get("keyspace_misses", 0)
            }
        except Exception as e:
            return {
                "enabled": True,
                "connected": False,
                "error": str(e)
            }
