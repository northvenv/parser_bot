from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from .models import User, Admin
                
async def get_coins(user_id, sessionmaker: async_sessionmaker[AsyncSession]):
    async with sessionmaker() as session:
        async with session.begin():
            admin = await session.get(Admin, user_id)
            if admin:
                return admin.coins
            user = await session.get(User, user_id)
            if user:
                return user.coins
            
            
async def update_coins(user_id, sessionmaker: async_sessionmaker[AsyncSession]):
    async with sessionmaker() as session:
        async with session.begin():
            admin = await session.get(Admin, user_id)
            if admin:
                pass
            
            user = await session.get(User, user_id)
            if user:
                if user.coins > 0:
                    user.coins -= 1
            await session.commit()






