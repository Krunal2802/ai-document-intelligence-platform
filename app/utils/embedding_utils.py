## Embeddings
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

def generate_embeddings(
    text: str
) -> list[float]:
    embeddings = model.encode(
        text,
        normalize_embeddings=True
    )

    return embeddings.tolist()