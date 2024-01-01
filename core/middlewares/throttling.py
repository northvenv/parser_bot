from typing import Callable, Dict, Awaitable, Any

from aiogram import BaseMiddleware
from aiogram.types import Message
from aiogram.fsm.storage.redis import RedisStorage

class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, storage: RedisStorage):
        self.storage = storage
    
    async def __call__(
            self, 
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any],
    ) -> Any:
        user = f'user{event.from_user.id}'

        check_user = await self.storage.redis.get(user)

        if not check_user:
            await self.storage.redis.set(user, value=1)
            await handler(event, data)
            await self.storage.redis.delete(user)
        else:
            return await event.answer('Подожди пока загрузится предыдущий файл')
            
               



        