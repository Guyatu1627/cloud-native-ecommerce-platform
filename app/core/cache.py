import json
from typing import Optional, Any
from app.core.redis import redis_client

DEFAULT_CACHE_EXPIRE = 300  # 5 minutes

def get_cache(key: str) -> Optional[Any]:
    data = redis_client.get(key)
    if data:
        return json.loads(data)
    return None

def set_cache(key: str, value: Any, expire: int = DEFAULT_CACHE_EXPIRE) -> None:
    redis_client.setex(key, expire, json.dumps(value))

def invalidate_cache_pattern(pattern: str) -> None:
    keys = redis_client.keys(pattern)
    if keys:
        redis_client.delete(*keys)