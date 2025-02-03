from sqlalchemy import Column, Integer, Boolean
from db.basemodel import Base

class User(Base):
    __tablename__ = "users"

    tg_id = Column(Integer, primary_key=True)
    in_white_list = Column(Boolean, default=False)