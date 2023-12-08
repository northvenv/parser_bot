from aiogram import Bot, Dispatcher, F
import asyncpg
import asyncio
import logging
from core.config_data.settings import get_settings
from aiogram.fsm.storage.redis import RedisStorage
from aioredis.client import Redis
from core.middlewares.dbmiddleware import DbSession
from core.middlewares.coinsmw import CoinsMiddleware
from core.handlers import basic, callback


async def create_pool(config):
    return await asyncpg.create_pool(user = config.db.db_user, 
                                    password = config.db.db_password, 
                                    database = config.db.database,
                                    host = config.db.db_host, 
                                    port = config.db.db_port, 
                                    command_timeout = 60)

async def create_redis_pool(config):
    return Redis(host = config.redis.redis_host,
                                        port = config.redis.redis_port,
                                        db = config.redis.redis_db,
                                        password = config.redis.redis_password)

async def main():
    logging.basicConfig(level=logging.INFO, 
                        format="%(asctime)s - [%(levelname)s] - %(name)s"
                               "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
    )
    config = get_settings('core/config_data/.env')

    bot = Bot(token=config.bot.token, parse_mode='HTML')
    
    pool = await create_redis_pool(config)
    storage = RedisStorage(redis=pool)
    
    dp = Dispatcher(storage=storage)

    dp.message.filter(F.chat.type == "private")
    
    pool_connect = await create_pool(config)
    
    dp.update.middleware.register(DbSession(pool_connect))
    dp.message.middleware.register(CoinsMiddleware())
    
    dp.include_router(basic.router)
    dp.include_router(callback.router)
    
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        await bot.session.close()



if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print('Бот остановлен!')