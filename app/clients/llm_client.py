from openai import OpenAI

from app.core.config import settings

class LLMClient:

    def __init__(self):
        self.client = OpenAI(
            api_key=settings.OPENAI_API_KEY
        )

    def generate_answer(
        self, 
        question: str,
        context : str
    ):
        prompt = f"""
            You are a helpful AI assistant.

            Answer the questions ONLY using the provided context.

            Do not use your own knowledge.

            If the answer is not present in the context, reply:
            "I could not find this information in the knowledge base.

            keep the answer concise and grounded in the context.

            Context:
            {context}

            Question:
            {question}

            Answer:
        """

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role":"system",
                    "content": "you are helpful AI assistant."
                },
                {
                    "role":"user",
                    "content": prompt
                }
            ]
        )

        return response.choices[0].message.content