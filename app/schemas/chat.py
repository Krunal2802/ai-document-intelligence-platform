from pydantic import BaseModel

class QueryRequestKB(BaseModel):
    knowledge_base_id: int
    question: str