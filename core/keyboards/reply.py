from functools import cache

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

@cache
def start_kb():
    """
    Кнопки с выбором функции
    """
    
    kb = [
            [
                KeyboardButton(text="Парсинг магазина"),
                KeyboardButton(text="Помощь")
            ],
        ]
    
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
