import redis
import json
from typing import Optional, Any
from app.config import get_settings

settings = get_settings()

_redis_client: Optional[redis.Redis] = None

def get_redis() -> Optional[redis.Redis]:
    global _redis_client
    if _redis_client is None:
        try:
            _redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True, socket_connect_timeout=2)
            _redis_client.ping()
        except Exception:
            _redis_client = None
    return _redis_client

def cache_get(key: str) -> Optional[Any]:
    r = get_redis()
    if r is None:
        return None
    try:
        val = r.get(key)
        return json.loads(val) if val else None
    except Exception:
        return None

def cache_set(key: str, value: Any, ttl: int = 900) -> bool:
    r = get_redis()
    if r is None:
        return False
    try:
        r.setex(key, ttl, json.dumps(value))
        return True
    except Exception:
        return False

def cache_delete(key: str) -> None:
    r = get_redis()
    if r:
        try:
            r.delete(key)
        except Exception:
            pass
