from sqlalchemy.orm import Session
from app.models.document import Document
from app.models.document_chunk import DocumentChunk
from app.utils.embedding_utils import generate_embeddings
from app.clients.llm_client import LLMClient

class RAGService:

    def __init__(
        self, 
        db: Session,
        llm_client = LLMClient
    ):
        self.db = db
        self.llm_client = llm_client
        ## currently we are using the SentenceTransformer for embeddigns only.

    def retrieve_relevant_chunks_from_knowledge_base(
        self,
        knowledge_base_id: int,
        query: str,
        top_k: int = 5
    ):  

        query_embedding = generate_embeddings(query)

        similar_chunks = (
            self.db.query(
                DocumentChunk,
                DocumentChunk.embedding.cosine_distance(query_embedding).label("distance")
            )
            .join(Document)
            .filter(
                Document.knowledge_base_id == knowledge_base_id
            )
            .order_by(
                DocumentChunk.embedding.cosine_distance(
                    query_embedding
                )
            )
            .limit(top_k)
            .all()
        )

        return [
            {
                "document_id": chunk.document_id,
                "distance": float(distance),
                "chunk_index": chunk.chunk_index,
                "chunk_text": chunk.chunk_text
            }
            for chunk, distance in similar_chunks
        ]

    def build_context(
        self,
        chunks: list[str]
    ):
        return "\n\n".join(
            chunk["chunk_text"] for chunk in chunks
        )

    def chat_with_knowledge_base(
        self,
        knowledge_base_id: int, 
        query: str
    ):
        chunks = self.retrieve_relevant_chunks_from_knowledge_base(
            knowledge_base_id=knowledge_base_id,
            query=query
        )   

        if not chunks:
            return {
                "question": query,
                "answer": "No relevant information found in the knowledge base.",
                "sources": []
            }

        context = self.build_context(chunks=chunks)

        answer = self.llm_client.generate_answer(
            question=query, 
            context=context
        )

        return {
            "question": query,
            "answer": answer,
            "sources": chunks
        }