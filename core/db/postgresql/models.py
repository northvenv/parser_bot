import datetime

from sqlalchemy import Column, Integer, VARCHAR, DATE, BigInteger
from sqlalchemy.ext.declarative import declarative_base

BaseModel = declarative_base()

class User(BaseModel):
    __tablename__ = 'data_users'

    user_id = Column(BigInteger, unique=True, nullable=False, primary_key=True)
    
    username = Column(VARCHAR(64), unique=False, nullable=False)
    
    coins = Column(Integer, unique=False, nullable=True)
    
    reg_date = Column(DATE, default=datetime.date.today())
    
    upd_date = Column(DATE, onupdate=datetime.date.today())
    
    def __str__(self):
        return f'<User:{self.user_id}>'
    
class Admin(BaseModel):
    __tablename__ = 'admins'

    admin_id = Column(BigInteger, unique=True, nullable=False, primary_key=True)
    
    username = Column(VARCHAR(64), unique=False, nullable=False)
    
    coins = Column(Integer, unique=False, nullable=True)

    def __str__(self):
        return f'<Admin:{self.user_id}>'
    





