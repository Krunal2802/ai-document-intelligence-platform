from fastapi import UploadFile
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.document import Document, DocumentStatus
from app.services.s3_services import S3Service
from app.utils.file_utils import get_page_count
from app.services.document_processor import DocumentProcessor

class DocumentService:

    def __init__(
        self, 
        db: Session,
        s3_service: S3Service,
        document_processor: DocumentProcessor
    ):
        self.db = db
        self.s3_service = s3_service
        self.document_processor = document_processor

    def create_document(
        self,
        knowledge_base_id: int, 
        name: str,
        file_type: str
    ):
        document = Document(
            knowledge_base_id = knowledge_base_id,
            name = name,
            file_type = file_type,
            storage_path = "/",
            page_count = None,
            status = DocumentStatus.DRAFT
        )

        self.db.add(document)
        self.db.commit()
        self.db.refresh(document)

        return document

    def get_all_documents(
        self,
        knowledge_base_id: int
    ):
        """
        documents for only particular knowledge base
        """
        documents = self.db.execute(
            select(Document).filter_by(
                knowledge_base_id = knowledge_base_id
            )
        ).scalars().all()

        return documents

    def get_document_by_id(
        self,
        knowledge_base_id: int,
        document_id: int
    ):
        """ 
        get_document_by_id -> by document_id 
        but we also make sure, that document is for particular knowledge base.
        """
        document = self.db.execute(
            select(Document).filter_by(
                id = document_id,
                knowledge_base_id = knowledge_base_id
            )
        ).scalar_one_or_none()

        if document is None:
            return None

        return document

    def update_document(
        self,
        knowledge_base_id: int,
        document_id: int,
        name: str | None = None,
    ):
        document = self.get_document_by_id(
            knowledge_base_id = knowledge_base_id,
            document_id = document_id
        )

        if document is None:
            return None

        if name is not None:
            document.name = name

        self.db.commit()
        self.db.refresh(document)

        return document

    def delete_document(
        self,
        knowledge_base_id: int,
        document_id: int
    ):

        document = self.get_document_by_id(
            knowledge_base_id = knowledge_base_id,
            document_id = document_id
        )

        if document is None:
            return None

        if document.storage_path != "/":
            self.s3_service.delete_file_from_s3(document.storage_path)

        self.db.delete(document)
        self.db.commit()

        return document

    ## Upload Document - File
    def upload_document(
        self,
        knowledge_base_id: int, 
        document_id: int,
        user_id: int, 
        file: UploadFile
    ):

        document = self.get_document_by_id(knowledge_base_id, document_id)

        if document is None:
            return None

        page_count = get_page_count(file)

        file.file.seek(0)

        text = self.document_processor.extract_text(file)

        chunks = self.document_processor.chunk_text(text)

        self.document_processor.store_document_chunks_embedding(
            document_id=document.id,
            chunks=chunks
        )

        file.file.seek(0)

        s3_key = self.s3_service.generate_s3_key(
            user_id,knowledge_base_id, file.filename
        )

        self.s3_service.upload_file_to_s3(file,s3_key)

        document.storage_path = s3_key
        document.page_count = page_count
        document.status = DocumentStatus.READY

        self.db.commit()
        self.db.refresh(document)

        return document