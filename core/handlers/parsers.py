import time

from aiogram import Bot, Router
from aiogram.types import Message, BufferedInputFile
from aiogram.filters import StateFilter

from core.db.postgresql import get_coins, update_coins
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from core.filters.filter import SymbolFilter
from core.states import StoreState

from core.utils import create_excel_file
from core.parser.parseavito import ParseAvito
from core.parser.parsewb import ParseWB

router = Router()

#avito parser handler
@router.message(SymbolFilter('/', '\\'), StateFilter(StoreState.AVITO_SELECTED))
async def parse_avito(message: Message, 
                      bot: Bot, 
                      sessionmaker: async_sessionmaker[AsyncSession]
                      ):
    user_id = message.from_user.id
    
    await update_coins(user_id=user_id,
                       sessionmaker=sessionmaker)
    
    coins = await get_coins(user_id=user_id,
                            sessionmaker=sessionmaker)

    if coins > 0:
        PRE_TEXT = f"""
        Файл скоро будет готов, подождите немного)

Осталось <b>{coins}</b> монет из 100 на сегодня.
        
        """
        await message.answer(PRE_TEXT)

        chat_id = message.chat.id
        query = message.text
        parser = ParseAvito()
        products = parser.get_data_with_selenium(query)

        file = await create_excel_file(products)
        document = BufferedInputFile(file, filename=f'{query}.xlsx')
        await bot.send_document(chat_id, document)
    else:
        await message.answer("Недостаточно монет(\nЧтобы получить больше монет, оформите Premium /premium")

#wilderries parser handler
@router.message(SymbolFilter('/', '\\'), StateFilter(StoreState.WB_SELECTED))
async def parse_wb(message: Message, 
                   bot: Bot, 
                   sessionmaker: async_sessionmaker[AsyncSession]
                   ):
    user_id = message.from_user.id

    await update_coins(user_id=user_id,
                        sessionmaker=sessionmaker)
    
    coins = await get_coins(user_id=user_id,
                            sessionmaker=sessionmaker)
    if coins > 0:
        PRE_TEXT = f"""
        Файл скоро будет готов, подождите немного)

Осталось <b>{coins}</b> монет из 100 на сегодня.
        """
        await message.answer(PRE_TEXT)
        chat_id = message.chat.id
        query = message.text
        parser = ParseWB()
        products = parser.parse(query)
        file = await create_excel_file(products)
        document = BufferedInputFile(file, filename=f'{query}.xlsx')
        time.sleep(1)
        await bot.send_document(chat_id, document)
    else:
        await message.answer("Недостаточно монет(\nЧтобы получить больше монет, оформите Premium /premium")