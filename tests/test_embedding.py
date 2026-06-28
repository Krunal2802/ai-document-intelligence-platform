from app.utils.embedding_utils import generate_embeddings
from app.services.rag_service import retrieve_relevant_chunks_from_knowledge_base
from app.db.database import SessionLocal

## -----------------------------------
## document embeddings

# embedding = generate_embeddings(
#     "Payment should be made within 30 days"
# )
# print(len(embedding))

## -----------------------------------
## question embeddings

# question = "Who is the trustee?"
# embedding = generate_embeddings(question)
# print(len(embedding))

## -----------------------------------
# find similar embeddings

db = SessionLocal()

try:
    question = "What are the skills Krunal have?"
    # question_embedding = generate_embeddings(question)

    similar_chunks = retrieve_relevant_chunks_from_knowledge_base(
        db=db,
        knowledge_base_id=1,
        query = question,
        top_k=2
    )

    for chunk in similar_chunks:
        print("=" * 50)
        print(chunk.chunk_index)
        print(chunk.chunk_text)

finally:
    db.close()