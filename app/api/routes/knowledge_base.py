from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.knowledge_base import KnowledgeBaseCreate, KnowledgeBaseUpdate, KnowledgeBaseResponse
from app.core.auth import get_current_user
from app.db.dependencies import get_db
from app.services.knowledge_base_service import create_knowledge_base, get_knowledge_base_by_id, get_all_knowledge_bases, update_knowledge_base, delete_knowledge_base

router = APIRouter()

@router.post("/", response_model=KnowledgeBaseResponse)
def create_knowledge_base_route(
    kb_data: KnowledgeBaseCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    kb = create_knowledge_base(
        db = db,
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
    return get_all_knowledge_bases(db,current_user.id)

@router.get("/{knowledge_base_id}/", response_model=KnowledgeBaseResponse)
def get_knowledge_base_route(
    knowledge_base_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    kb = get_knowledge_base_by_id(db, knowledge_base_id, current_user.id)

    if kb is None:
        raise HTTPException(
            status_code=404,
            detail="Knowledge Base not found"
        )

    return kb

@router.put("/{knowledge_base_id}/", response_model=KnowledgeBaseResponse)
def update_knowledge_base_route(
    kb_data: KnowledgeBaseUpdate,
    knowledge_base_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    kb = update_knowledge_base(db, knowledge_base_id, current_user.id, kb_data.name, kb_data.description)

    if kb is None:
        raise HTTPException(
            status_code=404,
            detail="Knowledge Base not found"
        )

    return kb

@router.delete("/{knowledge_base_id}/")
def delete_knowledge_base_route(
    knowledge_base_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    result = delete_knowledge_base(db, knowledge_base_id, current_user.id)

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Knowledge Base not found"
        ) 

    return {
        "message": "Knowledge Base deleted successfully"
    }