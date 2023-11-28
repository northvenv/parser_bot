from aiogram import Bot, Router
from aiogram.types import CallbackQuery
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from core.keyboards.inline import parse_site_inline_kb
from core.handlers.basic import ClientState, StoreState


router = Router()

@router.callback_query(StateFilter(ClientState.START_ORDER))#state = ClientState.START_ORDER)
async def select_func(call: CallbackQuery, bot: Bot, state: FSMContext):
    if call.data == 'parse_store':
        await call.message.answer('Выбери сайт из предложенного списка', 
                                  reply_markup=parse_site_inline_kb)
        await call.answer()
        await state.set_state(ClientState.FUNC_SELECTED)
    
    if call.data == 'help':
        await call.message.answer('С чем я могу помочь?')
        await call.answer()
        await state.set_state(ClientState.HELP_SELECTED)
 
@router.callback_query(StateFilter(ClientState.FUNC_SELECTED))#state = ClientState.FUNC_SELECTED)   
async def select_store(call: CallbackQuery, bot: Bot, state: FSMContext): 
    ans = 'Напиши подробное название товара'

    if call.data == 'ozon_parse':
        await call.message.answer(text = ans)
        await call.answer()
        await state.set_state(StoreState.OZON_SELECTED)
    
    if call.data == 'wb_parse':
        await call.message.answer(text = ans)
        await call.answer()
        await state.set_state(StoreState.WB_SELECTED)
    
    if call.data == 'ym_parse':
        await call.message.answer(text = ans)
        await call.answer()
        await state.set_state(StoreState.YM_SELECTED)
    
    if call.data == 'avito_parse':
        await call.message.answer(text = ans)
        await call.answer()
        await state.set_state(StoreState.AVITO_SELECTED)

    
















