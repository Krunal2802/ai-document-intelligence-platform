from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector
from datetime import datetime
from app.models.base import Base

class DocumentChunk(Base):
    __tablename__ = "document_chunk"

    id = Column(Integer, primary_key=True,index=True)
    document_id = Column(Integer, ForeignKey("documents.id"),nullable=False)
    chunk_index = Column(Integer, nullable=False)
    chunk_text = Column(String, nullable=False)
    embedding = Column(Vector(384))
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    document = relationship(
        "Document",
        back_populates="chunks"
    )