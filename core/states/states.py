from aiogram.fsm.state import State, StatesGroup

class ClientState(StatesGroup):
    START_ORDER = State()
    PARSE_SELECTED = State()
    HELP_SELECTED = State()
    PRODUCT_WRITED = State()

class StoreState(StatesGroup):
    WB_SELECTED = State()
    AVITO_SELECTED = State()