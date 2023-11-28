from aiogram import Bot, Router
from io import BytesIO
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import emoji 
from core.keyboards.inline import first_keyboard
from core.utils.dbconnect import Request
from aiogram.filters import Command, StateFilter
from core.parser.parseavito import ParseAvito
from core.utils.redis_utils import ConnectRedis, create_redis_pool
from core.utils.xlsx_utils import create_excel_file
class ClientState(StatesGroup):
    START_ORDER = State()
    FUNC_SELECTED = State()
    HELP_SELECTED = State()

class StoreState(StatesGroup):
    WB_SELECTED = State()
    OZON_SELECTED = State()
    AVITO_SELECTED = State()
    YM_SELECTED = State()


router = Router()

START_TEXT = """

Я <b>парсер</b>
И вот что я умею 

"""

@router.message(Command(commands=['start', 'run']))
async def get_start(message: Message, request: Request, state: FSMContext):
    await request.add_data(message.from_user.id, message.from_user.first_name)
    await message.answer(f'Привет, <b>{message.from_user.first_name}</b>!' + START_TEXT + emoji.emojize(':backhand_index_pointing_down:'),
                        reply_markup=first_keyboard)
    await state.set_state(ClientState.START_ORDER)
     
   
    
@router.message(StateFilter(StoreState.AVITO_SELECTED))
async def get_name_product(message: Message, bot: Bot):
    pool = create_redis_pool()
    redis = ConnectRedis(pool)
    chat_id = message.chat.id
    query = message.text
    parser = ParseAvito()
    products = parser.get_data_with_selenium(query)
    await create_excel_file(products, query)
    
    file = await redis.redis_get(f'{query}_file')
    document = FSInputFile(file, filename='avito.xlsx')
    await bot.send_document(chat_id, document)
    await redis.redis_delete(f'{query}_file')




    # chat_id = message.chat.id
    # # global func_complete
    # # if func_complete == True:
    # #     product = message.text
    # # else:
    # #     await message.answer('Не получилось спарсить товар')
    # product = message.text
    # if not product:
    #       await message.answer('Пожалуйста, укажиет название товара')
    # p_avito = ParseAvito()
    # data = await p_avito.main(product)
    # return (data, product)





