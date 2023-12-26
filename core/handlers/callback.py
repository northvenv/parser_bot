from aiogram import Router
from aiogram.types import CallbackQuery
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from core.states import ClientState, StoreState

router = Router()
 
#inline handler
@router.callback_query(StateFilter(ClientState.PARSE_SELECTED))
async def select_store(call: CallbackQuery, state: FSMContext): 
    """
    Функция для обработки inline кнопок для выбора магазина 
    
    (Wildberries, Avito)
    """
    
    
    ans = 'Напиши подробное название товара'

    if call.data == 'wb_parse':
        await call.message.edit_text(text=ans)
        await state.set_state(StoreState.WB_SELECTED)
        
    
    if call.data == 'avito_parse':
        await call.message.edit_text(text=ans)
        await state.set_state(StoreState.AVITO_SELECTED)
        

    
















