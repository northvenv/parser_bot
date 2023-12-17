from aiogram import Bot, Router, F
import time
from aiogram.types import Message, BufferedInputFile
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter
from core.filters.filter import SymbolFilter
from core.parser.parseavito import ParseAvito
from core.parser.parsewb import ParseWB
from core.utils.xlsx_utils import create_excel_file
from core.keyboards.inline import stores_kb
from core.keyboards.reply import start_kb
from core.db1 import get_coins, update_coins
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from core.states import ClientState, StoreState

router = Router()

@router.message(Command(commands=['start', 'run']))
async def get_start(message: Message, state: FSMContext, sessionmaker: async_sessionmaker[AsyncSession]):
    START_TEXT = """

Я <b>парсер</b>
И вот что я умею 👇

    """
    keyboard = start_kb()

    # await register_user(user_id=message.from_user.id, 
    #                     username=message.from_user.username, 
    #                     coins=100, 
    #                     sessionmaker=sessionmaker)
    
    await message.answer(f'Привет, <b>{message.from_user.first_name}</b>!' + START_TEXT,
                        reply_markup=keyboard)
    
    await state.set_state(ClientState.START_ORDER)

@router.message(F.text.lower() == "парсинг магазина")
async def parse_store(message: Message, state: FSMContext):
    keyboard = stores_kb()
    await message.answer('Выбери сайт из предложенного списка', 
                        reply_markup=keyboard)
    await state.set_state(ClientState.PARSE_SELECTED)

@router.message(F.text.lower() == "помощь")
async def help(message: Message):
    HELP_TEXT = """

    <b>Инструкция по использованию бота:</b>
    1)Напишите команду <b>/start</b>
    2)Нажмите на кнопку "Парсинг магазина"
    3)Выберите магазин из предложенного списка
    4)Напишите название товара

    """
    await message.answer(HELP_TEXT)
    
@router.message(SymbolFilter('/'), (StoreState.AVITO_SELECTED))
async def parse_avito(message: Message, bot: Bot, sessionmaker: async_sessionmaker[AsyncSession]):
    user_id = message.from_user.id
    
    await update_coins(user_id=user_id,
                       sessionmaker=sessionmaker)
    
    coins = await get_coins(user_id=user_id,
                            sessionmaker=sessionmaker)

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

@router.message(SymbolFilter('/'), StateFilter(StoreState.WB_SELECTED))
async def parse_wb(message: Message, bot: Bot, sessionmaker: async_sessionmaker[AsyncSession]):
    user_id = message.from_user.id

    await update_coins(user_id=user_id,
                        sessionmaker=sessionmaker)
    
    coins = await get_coins(user_id=user_id,
                            sessionmaker=sessionmaker)
    
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
    







