from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.services.knowledge_base_service import KnowledgeBaseService
from app.services.document_service import DocumentService

from app.services.s3_services import S3Service
from app.services.document_processor import DocumentProcessor

ALLOWED_EXTENSIONS = {"pdf","md","docx","txt"}

MAX_FILE_SIZE = 10 * 1024 * 1024 # 10 MB

def verify_knowledge_base(
    db: Session,
    knowledge_base_id: int,
    user_id: int
):

    kb_service = KnowledgeBaseService(db)

    kb = kb_service.get_knowledge_base_by_id(
        knowledge_base_id=knowledge_base_id,
        user_id=user_id
    )

    if kb is None:
        raise HTTPException(
            status_code=404,
            detail="Knowledge Base not found"
        )

    return kb

def verify_document(
    db: Session,
    knowledge_base_id: int,
    document_id: int
):

    document_service = DocumentService(
        db,
        s3_service=S3Service(),
        document_processor=DocumentProcessor(db)
    )

    document = document_service.get_document_by_id(
        knowledge_base_id=knowledge_base_id,
        document_id=document_id
    )

    if document is None:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    return document

async def validate_document_file(
    file: UploadFile
):
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Filename is missing !!"
        )

    extension = file.filename.split(".")[-1].lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail = (
                "Unsupported file type !!",
                f"Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
            )
        )

    content = await file.read()

    if len(content) == 0:
        raise HTTPException(
            status_code=400,
            detail="File is empty !!"
        )

    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail="File size exceeds 10 MB limit"
        )

    file.file.seek(0)

    return True