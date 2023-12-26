from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command

from core.keyboards.inline import stores_kb
from core.keyboards.reply import start_kb

from core.states import ClientState

router = Router()

#start handler
@router.message(Command(commands=['start']))
async def start(message: Message, state: FSMContext):
    START_TEXT = """

Я <b>парсер</b>
Могу спарсить любой товар, который ты укажешь😏

Перед началом рекомендую нажать на кнопку <b>Помощь</b> 
и узнать как мною пользоваться

    """
    keyboard = start_kb()

    await message.answer(f'Привет, <b>{message.from_user.first_name}</b>!' + START_TEXT,
                        reply_markup=keyboard)
    
    await state.set_state(ClientState.START_ORDER)

#parse handler
@router.message(F.text.lower() == "парсинг магазина")
async def parse_store(message: Message, state: FSMContext):
    keyboard = stores_kb()
    await message.answer('Выбери сайт из предложенного списка', 
                        reply_markup=keyboard)
    await state.set_state(ClientState.PARSE_SELECTED)

#help handler
@router.message(F.text.lower() == "помощь")
async def help(message: Message, state: FSMContext):
    HELP_TEXT = """

    <b>Инструкция по использованию бота:</b>
    1)Напишите команду <b>/start</b>
    2)Нажмите на кнопку "Парсинг магазина"
    3)Выберите магазин из предложенного списка
    4)Напишите название товара

    """
    await state.set_state(ClientState.HELP_SELECTED)
    await message.answer(HELP_TEXT)
    







