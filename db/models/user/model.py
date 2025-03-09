from db.basemodel import Base
from sqlalchemy import Column, Integer, String, Boolean, Enum

class RoleEnum(str):
    USER = "user"
    ADMIN = "admin"
    
    
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    tg_id = Column(Integer, unique=True, nullable=True)
    tg_name = Column(String(32))
    email = Column(String(255), unique=True, nullable=True)
    password = Column(String(60), nullable=True)
    role = Column(String(60), nullable=False, default=RoleEnum.USER)
    in_white_list = Column(Boolean, default=False)
