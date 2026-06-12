from pydantic import BaseModel

class KnowledgeBaseCreate(BaseModel):
    # user_id is not needed becasue it come from the get_current_user()
    name: str
    description: str

class KnowledgeBaseUpdate(BaseModel):  
    # user_id is not needed becasue it come from the get_current_user()
    name: str | None = None
    description: str | None = None

class KnowledgeBaseResponse(BaseModel):
    # user_id is not needed becasue it come from the get_current_user()
    id: int
    name: str
    description: str

    model_config = {
        "from_attributes": True # Meaning: when fastAPI retun SQLAlchemy Object, Pydantic needs to know it should read attributes from the ORM object.
    }