from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine as _create_async_engine

from core.config_data.settings import get_settings

def create_async_engine(url: URL):
    return _create_async_engine(url=url, echo=True, pool_pre_ping=True)

def create_sessionmaker(engine: AsyncEngine):
    return async_sessionmaker(bind=engine, class_=AsyncSession)

def get_session_maker():
     
    config = get_settings('core/config_data/.env')

    postgres_url = URL.create(
            drivername = 'postgresql+asyncpg', 
            username = config.db.db_user, 
            password = config.db.db_password, 
            database = config.db.database,
            host = config.db.db_host, 
            port = config.db.db_port,
        )

    async_engine = create_async_engine(postgres_url)
    session_maker = create_sessionmaker(async_engine)
    
    return session_maker









