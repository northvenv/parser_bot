from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from .models import User
from sqlalchemy import select

async def register_user(user_id, username, coins, sessionmaker: async_sessionmaker[AsyncSession]):
     async with sessionmaker() as session:
        async with session.begin():
            result = await session.execute(select(User).where(User.user_id == user_id))
            user = result.one_or_none()
            if user:
                pass
            else:
                user = User(
                    user_id = user_id,
                    username = username,
                    coins = coins
                )
                await session.add(user)
                await session.commit()
                
async def get_coins(user_id, sessionmaker: async_sessionmaker[AsyncSession]):
    async with sessionmaker() as session:
        async with session.begin():
            user = await session.get(User, user_id)
            if user:
                return user.coins
            
            
async def update_coins(user_id, sessionmaker: async_sessionmaker[AsyncSession]):
    async with sessionmaker() as session:
        async with session.begin():
            user = await session.get(User, user_id)
            if user:
                user.coins -= 1
            await session.commit()






