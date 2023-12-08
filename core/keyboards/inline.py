from functools import cache

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

@cache
def stores_kb():
    kb = [
            [
                InlineKeyboardButton(text = 'Wilberries', callback_data = 'wb_parse'),
                InlineKeyboardButton(text = 'Avito', callback_data = 'avito_parse')
            ],
        ]

    return InlineKeyboardMarkup(inline_keyboard=kb)



