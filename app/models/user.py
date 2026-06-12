from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.orm import relationship
from app.models.base import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer,primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable = False)
    password = Column(String, nullable=False)
    role = Column(String, default="USER")
    created_at = Column(DateTime, default=datetime.utcnow)

    knowledge_bases = relationship("KnowledgeBase", back_populates="owner")