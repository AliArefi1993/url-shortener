import os

from redis import Redis  # type: ignore
from slowapi import Limiter
from slowapi.util import get_remote_address

redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
redis_client = Redis.from_url(redis_url)
limiter = Limiter(key_func=get_remote_address, storage_uri=redis_url)
