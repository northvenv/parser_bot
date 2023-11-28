from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


first_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='Парсинг магазина', 
            callback_data='parse_store'
        )
    ], 
    [
        InlineKeyboardButton(
            text='Помощь', 
            callback_data='help'
        )
    ], 
])

parse_site_inline_kb = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='OZON',
            callback_data='ozon_parse'
        )
    ],
    [
        InlineKeyboardButton(
            text='WILBERRIES',
            callback_data='wb_parse'
        )
    ],
    [
        InlineKeyboardButton(
            text='YANDEX MARKET',
            callback_data='ym_parse'
        )
    ],
    [
        InlineKeyboardButton(
            text='AVITO',
            callback_data='avito_parse'
        )
    ],

])

file_type_inline = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='XML', 
            callback_data='xml'
        )
    ]
])






