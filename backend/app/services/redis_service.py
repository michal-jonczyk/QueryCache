import redis
from core.config import settings


class RedisService:
    def __init__(self):
        self.redis = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            decode_responses=True,
            )

    async def set(self, key: str, value: str, ttl: int = 300):
        self.redis.set(key, value, ex=ttl)


    async def get(self, key: str) -> str | None:
        return self.redis.get(key)


    async def delete(self, key: str):
        self.redis.delete(key)


    async def ping(self) -> bool:
        return self.redis.ping()


redis_service = RedisService()