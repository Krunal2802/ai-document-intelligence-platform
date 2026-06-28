from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models.enums import DocumentStatus

from app.models.base import Base

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index = True)
    knowledge_base_id = Column(Integer, ForeignKey("knowledge_bases.id"), nullable=False)
    name = Column(String, nullable=False)
    file_type = Column(String, nullable=False)
    storage_path = Column(String, nullable=False)
    page_count = Column(Integer)
    status = Column(Enum(DocumentStatus),nullable=False, default=DocumentStatus.PROCESSING)
    created_at = Column(DateTime, default = datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default = datetime.utcnow, nullable=False)
    
    knowledge_base = relationship(
        "KnowledgeBase",
        back_populates = "documents"
    )

    chunks = relationship(
        "DocumentChunk",
        back_populates="document",
        cascade="all, delete-orphan"
    )