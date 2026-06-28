from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.dependencies import get_db
from app.core.auth import get_current_user
from app.schemas.chat import QueryRequestKB
from app.dependencies.service import get_rag_service

router = APIRouter()

@router.post("/query-kb")
async def query_entire_knowledge_base(
    request : QueryRequestKB,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    rag_service = get_rag_service(db)

    response = rag_service.chat_with_knowledge_base(
        knowledge_base_id = request.knowledge_base_id,
        query = request.question
    )

    return response