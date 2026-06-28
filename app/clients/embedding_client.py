from openai import OpenAI
from app.core.config import settings

## currently we are using the SentenceTransformer for embeddigns only.

class EmbeddingClient:

    def __init__(self):
        self.client = OpenAI(
            api_key=settings.OPENAI_API_KEY
        )

    def generate_embeddings(self, text):
        response = self.client.embeddings.create(
            model = "text-embedding-3-small",
            input = text
        )

        return response.data[0].embedding