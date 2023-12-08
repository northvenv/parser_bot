from typing import Callable, Awaitable, Dict, Any
from aiogram.types import TelegramObject, Message
from aiogram import BaseMiddleware

class CoinsMiddleware(BaseMiddleware):
    def __init__(self):
        self.coins = 100

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        self.coins -= 1
        data['coins'] = self.coins
        return await handler(event, data)
        