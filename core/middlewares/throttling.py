from typing import Callable, Dict, Awaitable, Any

from aiogram import BaseMiddleware
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from core.states import StoreState, ClientState

class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, state: FSMContext):
        self.state = state

    def __call__(
            self, 
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any],
    ) -> Any:
        # if self.state == StoreState.WB_SELECTED or self.state == StoreState.AVITO_SELECTED:
        # if self.state in (StoreState. WB_SELECTED, StoreState.AVITO_SELECTED):
        state = data['fsm']
        



        