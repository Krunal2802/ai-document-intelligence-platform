from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.knowledge_base import KnowledgeBaseCreate, KnowledgeBaseUpdate, KnowledgeBaseResponse
from app.core.auth import get_current_user
from app.db.dependencies import get_db
from app.services.knowledge_base_service import KnowledgeBaseService
from app.utils.validator import verify_knowledge_base

router = APIRouter()

@router.post("/", response_model=KnowledgeBaseResponse)
def create_knowledge_base_route(
    kb_data: KnowledgeBaseCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    kb_service = KnowledgeBaseService(db)

    kb = kb_service.create_knowledge_base(
        user_id = current_user.id,
        name = kb_data.name,
        description = kb_data.description
    )

    return kb

@router.get("/", response_model=list[KnowledgeBaseResponse])
def get_knowledge_bases_route(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):   
    kb_service = KnowledgeBaseService(db)

    kb = kb_service.get_all_knowledge_bases(current_user.id)

    return kb

@router.get("/{knowledge_base_id}", response_model=KnowledgeBaseResponse)
def get_knowledge_base_route(
    knowledge_base_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return verify_knowledge_base(
        db,
        knowledge_base_id,
        current_user.id
    )

@router.put("/{knowledge_base_id}", response_model=KnowledgeBaseResponse)
def update_knowledge_base_route(
    kb_data: KnowledgeBaseUpdate,
    knowledge_base_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    kb_service = KnowledgeBaseService(db)

    verify_knowledge_base(
        db,
        knowledge_base_id,
        current_user.id
    )

    return kb_service.update_knowledge_base(
        knowledge_base_id, 
        current_user.id, 
        kb_data.name, 
        kb_data.description
    )

@router.delete("/{knowledge_base_id}")
def delete_knowledge_base_route(
    knowledge_base_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    kb_service = KnowledgeBaseService(db)

    kb = verify_knowledge_base(
        db,
        knowledge_base_id,
        current_user.id
    )

    kb_service.delete_knowledge_base(
        knowledge_base_id,
        current_user.id
    )

    return {
        "message": f"Knowledge Base: {kb.name} deleted successfully"
    }