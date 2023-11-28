from aiogram import Bot, Dispatcher
import aioredis
import asyncio
import logging
from core.config_data.settings import get_settings
from aiogram.fsm.storage.redis import RedisStorage
from core.handlers import basic, callback
from core.utils.redis_utils import ConnectRedis, create_redis_pool
# from core.handlers.pay import order, pre_checkout_query, succesful_payment

config = get_settings('core/config_data/.env')

# async def create_pool():
#     # return await asyncpg.create_pool(user = config.db.db_user, 
#     #                                 password = config.db.db_password, 
#     #                                 database = config.db.database,
#     #                                 host = config.db.db_host, 
#     #                                 port = config.db.db_port, 
#     #                                 command_timeout = 60)

#     return await asyncpg.create_pool(host = config.redis.redis_host,
#                                      port = config.redis.redis_port,
#                                      db = config.redis.redis_db,
#                                      password = config.redis.redis_password)
# async def create_redis_pool():
#     return aioredis.ConnectionPool(host = config.redis.redis_host,
#                                         port = config.redis.redis_port,
#                                         db = config.redis.redis_db,
#                                         password = config.redis.redis_password)

async def start():
    logging.basicConfig(level=logging.INFO, 
                        format="%(asctime)s - [%(levelname)s] - %(name)s"
                               "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
    )
    #Redis
    pool = await create_redis_pool()
    redis = ConnectRedis(pool)
    storage = RedisStorage(redis=redis)
    
    bot = Bot(token=config.bot.token, parse_mode='HTML')
    dp = Dispatcher(storage=storage)
    
    # pool_connect = await create_pool()
    
    # dp.update.middleware.register(DbSession(pool_connect))
    dp.include_router(basic.router)
    dp.include_router(callback.router)
    
    # dp.pre_checkout_query.register(pre_checkout_query)
    
    # dp.message.register(succesful_payment, Filter(type=)))
    
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        await bot.session.close()



if __name__ == '__main__':
    try:
        asyncio.run(start())
    except (KeyboardInterrupt, SystemExit):
        print('Бот остановлен!')