from aiogram import Router
from aiogram.filters import Filter
from aiogram.types import Message

class SymbolFilter(Filter):
    def __init__(self, symbol: str) -> None:
        self.symbol = symbol

    async def __call__(self, message: Message) -> bool:
        if self.symbol in message.text:
            await message.reply('В названии продукта не должно быть символа /')
            return False
        return True
            
        