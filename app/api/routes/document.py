from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from app.schemas.document import DocumentCreate, DocumentUpdate, DocumentResponse
from app.core.auth import get_current_user
from app.db.dependencies import get_db
from app.services.document_service import DocumentService
from app.utils.validator import verify_knowledge_base, verify_document, validate_document_file
from app.services.s3_services import S3Service
from app.services.document_processor import DocumentProcessor

router = APIRouter()

## Documnt metadata CRUD routes

@router.post("/knowledge-bases/{knowledge_base_id}/documents", response_model=DocumentResponse)
def create_document_document_route(
    doc_data : DocumentCreate,
    knowledge_base_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):  
    doc_service = DocumentService(
        db = db,
        s3_service=S3Service(),
        document_processor=DocumentProcessor(db)
    )

    verify_knowledge_base(
        db,
        knowledge_base_id,
        current_user.id
    )

    document = doc_service.create_document(
        knowledge_base_id = knowledge_base_id,
        name = doc_data.name,
        file_type = doc_data.file_type
    )   

    return document

@router.get("/knowledge-bases/{knowledge_base_id}/documents", response_model=list[DocumentResponse])
def get_all_documents_route(
    knowledge_base_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    doc_service = DocumentService(
        db = db,
        s3_service=S3Service(),
        document_processor=DocumentProcessor(db)
    )

    verify_knowledge_base(
        db,
        knowledge_base_id,
        current_user.id
    )

    documents = doc_service.get_all_documents(knowledge_base_id=knowledge_base_id)

    return documents

@router.get("/knowledge-bases/{knowledge_base_id}/documents/{document_id}", response_model=DocumentResponse)
def get_document_route(
    document_id: int,
    knowledge_base_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    verify_knowledge_base(
        db,
        knowledge_base_id,
        current_user.id
    )

    return verify_document(
        db,
        knowledge_base_id,
        document_id
    )

@router.put("/knowledge-bases/{knowledge_base_id}/documents/{document_id}", response_model=DocumentResponse)
def update_document_route(
    doc_data: DocumentUpdate,
    document_id: int,
    knowledge_base_id: int, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    doc_service = DocumentService(
        db =db,
        s3_service=S3Service(),
        document_processor=DocumentProcessor(db)
    )

    verify_knowledge_base(
        db,
        knowledge_base_id,
        current_user.id
    )

    verify_document(
        db,
        knowledge_base_id,
        document_id
    )

    return doc_service.update_document(
        knowledge_base_id,
        document_id,
        doc_data.name
    )

@router.delete("/knowledge-bases/{knowledge_base_id}/documents/{document_id}")
def delete_document_route(
    document_id: int,
    knowledge_base_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    doc_service = DocumentService(
        db =db,
        s3_service=S3Service(),
        document_processor=DocumentProcessor(db)
    )

    verify_knowledge_base(
        db,
        knowledge_base_id,
        current_user.id
    )

    document = verify_document(
        db,
        knowledge_base_id,
        document_id
    )

    doc_service.delete_document(
        knowledge_base_id,
        document_id
    )

    return {
        "message" : f"Document {document.name} deleted successfully"
    }

## Document Upload Route

@router.post(
    "/knowledge-bases/{knowledge_base_id}/documents/{document_id}/upload",
    response_model=DocumentResponse
)
async def upload_document_route(
    knowledge_base_id: int,
    document_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    doc_service = DocumentService(
        db =db,
        s3_service=S3Service(),
        document_processor=DocumentProcessor(db)
    )

    verify_knowledge_base(db, knowledge_base_id, current_user.id)

    document = verify_document(db, knowledge_base_id,document_id)

    if document.storage_path != "/":
        raise HTTPException(
            status_code=400,
            detail="Document already has a file uploaded"
        )

    await validate_document_file(file)

    return doc_service.upload_document(
        knowledge_base_id, document_id, current_user.id, file
    )