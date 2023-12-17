from aiogram import Bot, Dispatcher, F
from aiogram.types import BotCommand
import asyncio
import logging
from core.config_data.settings import get_settings
from aiogram.fsm.storage.redis import RedisStorage
from aioredis.client import Redis
from core.middlewares.register_check import RegisterCheck
from core.handlers import basic, callback
from core.db1 import get_session_maker
from core.commands import bot_commands

async def create_redis_pool(config):
    return await Redis(host = config.redis.redis_host,
                port = config.redis.redis_port,
                db = config.redis.redis_db,
                password = config.redis.redis_password)

async def main():
    logging.basicConfig(level=logging.INFO, 
                        format="%(asctime)s - [%(levelname)s] - %(name)s"
                               "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
    )
    config = get_settings('core/config_data/.env')

    commands = []
    for cmd in bot_commands:
        commands.append(BotCommand(command=cmd[0], description=cmd[1]))


    bot = Bot(token=config.bot.token, parse_mode='HTML')
    await bot.set_my_commands(commands=commands)
    
    pool = await create_redis_pool(config)
    storage = RedisStorage(redis=pool)
    
    dp = Dispatcher(storage=storage)
    dp.message.middleware.register(RegisterCheck())
    dp.message.filter(F.chat.type == "private")
    dp.include_routers(basic.router,
                       callback.router)
                
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot, sessionmaker=get_session_maker())
    finally:
        await bot.session.close()



if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print('Бот остановлен!')