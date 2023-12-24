from aioredis.client import Redis

async def create_redis_pool(config):
    return await Redis(host = config.redis.redis_host,
                port = config.redis.redis_port,
                db = config.redis.redis_db,
                password = config.redis.redis_password)

async def add_user(user_id, redis: Redis):
    await redis.set(user_id, 'On process')
    # await redis.close()

async def delete_user(user_id, redis: Redis):
    await redis.delete(user_id)
    # await redis.close()

async def get_user(user_id, redis: Redis):
    await redis.get(user_id)
    # await redis.close()

