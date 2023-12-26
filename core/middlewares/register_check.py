from typing import Callable, Dict, Awaitable, Any

from aiogram import BaseMiddleware
from aiogram.types import Message
from sqlalchemy import select
from core.db.postgresql import User, Admin
from core.config_data.settings import get_settings
import datetime

config = get_settings('core/config_data/.env')



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
                result = await session.execute(select(Admin).where(Admin.admin_id == event.from_user.id))
                admin = result.one_or_none()
                if admin:
                    pass
                else:
                    if event.from_user.id == config.bot.admin_id:
                        admin = Admin(
                            admin_id=event.from_user.id,
                            username = event.from_user.username,
                            coins = 100,
                        )
                        session.add(admin)
                        session.commit()
                    else:
                        result = await session.execute(select(User).where(User.user_id == event.from_user.id))
                        user = result.one_or_none()
                        if user:
                            pass
                        else:
                            user = User(
                                user_id = event.from_user.id,
                                username = event.from_user.username,
                                coins = 100,
                                reg_date = datetime.date.today()
                            )
                            session.add(user)
                            session.commit()
        
        return await handler(event, data)