from sqlalchemy import Column, String, Integer
from app.models.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer,primary_key=True)
    name = Column(String)
    email = Column(String, unique=True, nullable = False)
    password = Column(String, nullable=False)
