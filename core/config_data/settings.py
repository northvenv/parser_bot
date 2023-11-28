from environs import Env
from dataclasses import dataclass

@dataclass
class Bot:
    token: str             
    admin_id: list[int]   

@dataclass
class DatabaseConfig:
    db_port: str
    db_host: str       
    db_user: str       
    db_password: str  
    database: str     

@dataclass
class RedisConfig:
    redis_host: str
    redis_port: int
    redis_db: int
    redis_password: str

@dataclass
class Config:
    bot: Bot
    db: DatabaseConfig
    redis: RedisConfig

def get_settings(path: str):
    env = Env()
    env.read_env(path)

    return Config(
        bot=Bot(
            token=env.str('BOT_TOKEN'),
            admin_id=env.int('ADMIN_ID')
        ),
        db=DatabaseConfig(
        database=env.str('DATABASE'),
        db_host=env.str('DB_HOST'),
        db_user=env.str('DB_USER'),
        db_password=env.str('DB_PASSWORD'),
        db_port=env.int('DB_PORT')
        ), 
        redis=RedisConfig(
            redis_host=env.str('REDIS_HOST'), 
            redis_port=env.int('REDIS_PORT'),
            redis_db=env.int('REDIS_DB'), 
            redis_password=env.str('REDIS_PASSWORD')
        )   
    )




