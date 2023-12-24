from typing import Callable, Dict, Awaitable, Any
from aiogram import BaseMiddleware
from aiogram.filters import Command
from aiogram.types import Message, Update, BotCommand
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.redis import RedisStorage
from core.states import ClientState, StoreState


class StateMiddleware(BaseMiddleware):

    async def __call__(
            self, 
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any],
    ) -> Any:
        symbols = ['/start', '/help', 'Парсинг магазина', 'Помощь']
        states = [ClientState.HELP_SELECTED, ClientState.START_ORDER]
        
        # if event.text not in symbols:
        #     return await event.answer('Не понимаю тебя, нажми на кнопку <b>Помощь</b>, чтобы узнать как мною пользоваться')
        # elif data['state']:
        #     if data['state'] in states and event.text not in symbols:
        #     return await handler(event, data)
        # else:
        #     return await event.answer('Не торопись) Напиши команду /start')
        
        
        pass

    async def on_process_message(self, message: Message, data: dict):
        if 'entities' in message:
            for entity in message['entities']:
                if entity['type'] == 'bot_command':
                    return False

        # обработка сообщения пользователя
        await message.reply(f"Пользовательское сообщение: {message.text}")
        return True