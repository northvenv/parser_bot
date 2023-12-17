from typing import Callable, Dict, Awaitable, Any

from aiogram import BaseMiddleware
from aiogram.types import Message
from sqlalchemy import select
from core.db1 import User


class RegisterCheck(BaseMiddleware):
    """
    Проверка регистрации пользователя
    """

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        session_maker = data['sessionmaker']
        async with session_maker() as session:
            async with session.begin():
                result = await session.execute(select(User).where(User.user_id == event.from_user.id))
                user = result.one_or_none()
                if user:
                    pass
                else:
                    user = User(
                        user_id = event.from_user.id,
                        username = event.from_user.username,
                        coins = 100
                    )
                    session.add(user)
                    session.commit()
        
        return await handler(event, data)