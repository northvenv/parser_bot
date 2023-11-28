import aioredis
from core.config_data.settings import get_settings
from aiogram.fsm.storage.redis import Redis, RedisStorage


config = get_settings('core/config_data/.env')

async def create_redis_pool():
    return aioredis.ConnectionPool(host = config.redis.redis_host,
                                        port = config.redis.redis_port,
                                        db = config.redis.redis_db,
                                        password = config.redis.redis_password)

class ConnectRedis():
    def __init__(self, pool):
        self.pool = pool
    
    async def create_redis_pool(self):
        return aioredis.Redis(connection_pool=self.pool)

    async def redis_get(self, key):
        try:
            conn = await self.create_redis_pool()
            return await conn.get(key)
        finally:
            await self.redis_close()

    async def redis_set(self, key, value) -> None:
        conn = await self.create_redis_pool()
        await conn.set(key, value)
        await self.redis_close()

    async def redis_delete(self, key) -> None:
        conn = await self.create_redis_pool()
        await conn.delete(key)
        await self.redis_close()


    async def redis_close(self) -> None:
        await self.create_redis_pool().close()
        