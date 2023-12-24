from aiogram import Router
from aiogram.filters import Filter
from aiogram.types import Message
from core.states import StoreState

class SymbolFilter(Filter):
    def __init__(self, *args: str) -> None:
        self.symbols = [*args]

    async def __call__(self, message: Message) -> bool:
        commands = ['/start', '/help']
        if message.text not in commands:    
            for symbol in self.symbols:
                if symbol in message.text:
                    await message.reply('В названии продукта не должно быть символа /')
                    return False
        return True
            
        