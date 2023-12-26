import asyncio
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.types import BotCommand
from aiogram.fsm.storage.redis import RedisStorage

from core.config_data.settings import get_settings

from core.middlewares.register_check import RegisterCheck
from core.middlewares.throttling import ThrottlingMiddleware

from core.handlers import basic, callback, parsers

from core.db.redis import create_redis_pool
from core.db.postgresql import get_session_maker

from core.commands import bot_commands

async def main():
    logging.basicConfig(level=logging.INFO, 
                        format="%(asctime)s - [%(levelname)s] - %(name)s"
                               "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
    )

    config = get_settings('core/config_data/.env')

    commands = []
    commands.append(BotCommand(command=bot_commands[0], description=bot_commands[1]))


    bot = Bot(token=config.bot.token, parse_mode='HTML')
    await bot.set_my_commands(commands=commands)
    
    pool = await create_redis_pool(config)
    storage = RedisStorage(redis=pool)

    dp = Dispatcher(storage=storage)
    dp.message.middleware.register(RegisterCheck())
    dp.message.middleware.register(ThrottlingMiddleware(storage=storage))
    dp.message.filter(F.chat.type == "private")
    dp.include_routers(basic.router,
                       callback.router, 
                       parsers.router
                       )
                
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await storage.redis.flushdb()
        await dp.start_polling(bot, sessionmaker=get_session_maker(), storage=storage)
    finally:
        await bot.session.close()
       

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print('Бот остановлен!')