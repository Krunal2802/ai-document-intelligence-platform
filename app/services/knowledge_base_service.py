from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.knowledge_base import KnowledgeBase

def create_knowledge_base(
    db: Session,
    user_id: int,
    name: str,
    description: str
):
    kb = KnowledgeBase(user_id = user_id, name = name, description = description)

    db.add(kb)
    db.commit()
    db.refresh(kb)

    return kb

def get_all_knowledge_bases(
    db: Session,
    user_id: int
):
    knowledge_bases= db.execute(
        select(KnowledgeBase).filter_by(
            user_id = user_id
        )
    ).scalars().all()

    return knowledge_bases

def get_knowledge_base_by_id(
    db: Session,
    knowledge_base_id: int,
    user_id: int
):
    kb = db.execute(
        select(KnowledgeBase).filter_by(
            id = knowledge_base_id,
            user_id = user_id
        )
    ).scalar_one_or_none()

    return kb 

def update_knowledge_base(
    db: Session,
    knowledge_base_id: int,
    user_id : int,
    name: str | None = None,
    description: str | None = None
):
    kb = get_knowledge_base_by_id(
        db = db,
        knowledge_base_id = knowledge_base_id,
        user_id = user_id
    )

    if kb is None:
        return None

    if name is not None:
        kb.name = name

    if description is not None:
        kb.description = description
    
    db.commit()
    db.refresh(kb)

    return kb

def delete_knowledge_base(
    db: Session,
    knowledge_base_id: int,
    user_id: int
):
    kb = get_knowledge_base_by_id(
        db = db,
        knowledge_base_id = knowledge_base_id,
        user_id = user_id
    )

    if kb is None:
        return None  

    db.delete(kb)
    db.commit()

    return kb