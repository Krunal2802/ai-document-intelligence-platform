from pydantic import BaseModel
from app.models.enums import DocumentStatus

class DocumentCreate(BaseModel):
    name: str # not needed -> but we dont use frontend now ,so we use this
    file_type: str # not needed -> but we dont use frontend now ,so we use this

class DocumentUpdate(BaseModel):
    name: str | None = None

class DocumentResponse(BaseModel):
    id: int
    knowledge_base_id: int
    name: str
    file_type: str
    storage_path: str
    page_count: int | None = None
    status: DocumentStatus

    model_config = {
        "from_attributes" : True
    }
