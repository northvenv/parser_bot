from aioredis.client import Redis

async def create_redis_pool(config):
    return await Redis(host = config.redis.redis_host,
                port = config.redis.redis_port,
                db = config.redis.redis_db,
                password = config.redis.redis_password)

