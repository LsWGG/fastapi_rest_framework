from typing import Optional
from aioredis import Redis, from_url
from core.setting import settings


class RedisCache(object):
    __doc__ = "redis 连接建立"

    def __init__(self):
        self.redis_conn: Optional[Redis] = None
        self.address: Optional[str] = f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}"

    async def init_cache(self):
        """
        建立连接
        :return:
        """
        if settings.REDIS_PWD:
            self.redis_conn = await from_url(self.address, db=settings.REDIS_DEFAULT_DB, password=settings.REDIS_PWD,
                                             encoding="utf-8", decode_responses=True)

        else:
            self.redis_conn = await from_url(self.address, db=settings.REDIS_DEFAULT_DB, encoding="utf-8",
                                             decode_responses=True)

    async def keys(self, pattern):
        return await self.redis_conn.keys(pattern)

    async def set(self, key, value):
        return await self.redis_conn.set(key, value)

    async def get(self, key):
        return await self.redis_conn.get(key)

    async def close(self):
        await self.redis_conn.close()


redis_cache = RedisCache()
