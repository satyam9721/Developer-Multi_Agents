from typing import Any, Dict, Optional
import json
from app.config.settings import settings
from app.utils.logger import logger

class RedisService:
    """Redis client abstraction with in-memory fallback for local bootability."""

    def __init__(self):
        self.url = settings.REDIS_URL
        self._in_memory_store: Dict[str, str] = {}
        self._connected = False
        # TODO: Initialize aioredis connection pool when Redis server is active

    async def get(self, key: str) -> Optional[str]:
        """Get value from cache."""
        return self._in_memory_store.get(key)

    async def set(self, key: str, value: str, ttl_seconds: Optional[int] = None) -> bool:
        """Set value in cache."""
        self._in_memory_store[key] = value
        return True

    async def delete(self, key: str) -> bool:
        """Delete key from cache."""
        if key in self._in_memory_store:
            del self._in_memory_store[key]
            return True
        return False

redis_service = RedisService()
