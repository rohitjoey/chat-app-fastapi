from sqlalchemy import Column, Integer, String
from ..database import Base
from ..models import BaseClass


class User(Base, BaseClass):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String)
    email = Column(String, unique=True)
    hashed_password = Column(String)
