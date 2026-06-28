from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.knowledge_base import KnowledgeBase

class KnowledgeBaseService:

    def __init__(self, db: Session):
        self.db = db

    def create_knowledge_base(
        self,
        user_id: int,
        name: str,
        description: str
    ):
        kb = KnowledgeBase(user_id = user_id, name = name, description = description)

        self.db.add(kb)
        self.db.commit()
        self.db.refresh(kb)

        return kb

    def get_all_knowledge_bases(
        self,
        user_id: int
    ):
        """
        knowledge bases for particular user
        """
        knowledge_bases= self.db.execute(
            select(KnowledgeBase).filter_by(
                user_id = user_id
            )
        ).scalars().all()

        return knowledge_bases

    def get_knowledge_base_by_id(
        self,
        knowledge_base_id: int,
        user_id: int
    ):
        """ 
        get_knowledge_base_by_id -> by knowledge_base_id 
        but we also make sure, that knowledge base is for particular user.
        """
        kb = self.db.execute(
            select(KnowledgeBase).filter_by(
                id = knowledge_base_id,
                user_id = user_id
            )
        ).scalar_one_or_none()

        if kb is None:
            return None

        return kb 

    def update_knowledge_base(
        self,
        knowledge_base_id: int,
        user_id : int,
        name: str | None = None,
        description: str | None = None
    ):
        kb = self.get_knowledge_base_by_id(
            knowledge_base_id = knowledge_base_id,
            user_id = user_id
        )

        if kb is None:
            return None

        if name is not None:
            kb.name = name

        if description is not None:
            kb.description = description
        
        self.db.commit()
        self.db.refresh(kb)

        return kb

    def delete_knowledge_base(
        self,
        knowledge_base_id: int,
        user_id: int
    ):
        kb = self.get_knowledge_base_by_id(
            knowledge_base_id = knowledge_base_id,
            user_id = user_id
        )

        if kb is None:
            return None  

        self.db.delete(kb)
        self.db.commit()

        return kb