"""Session memory – Redis with in-memory fallback."""

from __future__ import annotations

import json
from typing import Dict, Optional

from app.core.config import settings

_local_store: Dict[str, str] = {}
_redis_client = None


def _get_redis():
    global _redis_client
    if _redis_client is not None:
        return _redis_client
    if settings.redis_url:
        try:
            import redis
            _redis_client = redis.from_url(settings.redis_url, decode_responses=True)
            _redis_client.ping()
            return _redis_client
        except Exception:
            _redis_client = None
    return None


def store_session(session_id: str, data: dict, ttl: int = 3600) -> None:
    payload = json.dumps(data)
    r = _get_redis()
    if r:
        r.setex(session_id, ttl, payload)
    else:
        _local_store[session_id] = payload


def get_session(session_id: str) -> Optional[dict]:
    r = _get_redis()
    if r:
        raw = r.get(session_id)
    else:
        raw = _local_store.get(session_id)
    if raw:
        return json.loads(raw)
    return None


def delete_session(session_id: str) -> None:
    r = _get_redis()
    if r:
        r.delete(session_id)
    else:
        _local_store.pop(session_id, None)
