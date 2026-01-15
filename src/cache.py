"""
Performance optimization with caching
"""
import redis
import json
import hashlib
import os
from functools import wraps
from datetime import timedelta


# Redis connection (falls back to in-memory if Redis unavailable)
try:
    REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
    REDIS_PORT = int(os.getenv('REDIS_PORT', '6379'))
    REDIS_DB = int(os.getenv('REDIS_DB', '0'))
    
    redis_client = redis.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        db=REDIS_DB,
        decode_responses=True,
        socket_connect_timeout=2
    )
    redis_client.ping()  # Test connection
    REDIS_AVAILABLE = True
except:
    REDIS_AVAILABLE = False
    # Fallback to in-memory cache
    _memory_cache = {}


def cache_key(*args, **kwargs):
    """Generate cache key from arguments"""
    key_data = str(args) + str(sorted(kwargs.items()))
    return hashlib.md5(key_data.encode()).hexdigest()


def cache(ttl=300):
    """
    Decorator to cache function results
    ttl: time to live in seconds (default 5 minutes)
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Generate cache key
            key = f"{f.__name__}:{cache_key(*args, **kwargs)}"
            
            # Try to get from cache
            if REDIS_AVAILABLE:
                try:
                    cached = redis_client.get(key)
                    if cached:
                        return json.loads(cached)
                except:
                    pass
            else:
                if key in _memory_cache:
                    cached_data, expiry = _memory_cache[key]
                    if expiry > 0:  # Not expired
                        _memory_cache[key] = (cached_data, expiry - 1)
                        return cached_data
            
            # Execute function
            result = f(*args, **kwargs)
            
            # Store in cache
            if REDIS_AVAILABLE:
                try:
                    redis_client.setex(key, ttl, json.dumps(result))
                except:
                    pass
            else:
                _memory_cache[key] = (result, ttl)
            
            return result
        
        return decorated_function
    return decorator


def invalidate_cache(pattern='*'):
    """Invalidate cache entries matching pattern"""
    if REDIS_AVAILABLE:
        try:
            keys = redis_client.keys(pattern)
            if keys:
                redis_client.delete(*keys)
        except:
            pass
    else:
        _memory_cache.clear()


def get_cache_stats():
    """Get cache statistics"""
    if REDIS_AVAILABLE:
        try:
            info = redis_client.info('stats')
            return {
                'type': 'redis',
                'hits': info.get('keyspace_hits', 0),
                'misses': info.get('keyspace_misses', 0),
                'keys': redis_client.dbsize()
            }
        except:
            return {'type': 'redis', 'status': 'unavailable'}
    else:
        return {
            'type': 'memory',
            'keys': len(_memory_cache)
        }


# Async helper (for future async implementation)
class AsyncHelper:
    """Helper for async operations"""
    
    @staticmethod
    def run_in_background(func, *args, **kwargs):
        """Run function in background thread"""
        import threading
        thread = threading.Thread(target=func, args=args, kwargs=kwargs)
        thread.daemon = True
        thread.start()
        return thread


# Response compression
def compress_response(data, min_size=1000):
    """Compress response if larger than min_size"""
    import gzip
    
    if len(data) < min_size:
        return data, False
    
    try:
        compressed = gzip.compress(data.encode() if isinstance(data, str) else data)
        if len(compressed) < len(data):
            return compressed, True
    except:
        pass
    
    return data, False
