from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.dependencies import get_db

from app.clients.llm_client import LLMClient
from app.clients.embedding_client import EmbeddingClient

from app.services.rag_service import RAGService


def get_llm_client():
    return LLMClient()

def get_embedding_client():
    return EmbeddingClient()

def get_rag_service(
    db: Session = Depends(get_db)
):
    return RAGService(
        db,
        llm_client=LLMClient()
    )
