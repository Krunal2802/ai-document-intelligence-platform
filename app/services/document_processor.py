from fastapi import UploadFile
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.utils.file_utils import extract_pdf_file, extract_docx_file, extract_text_file
from app.utils.embedding_utils import generate_embeddings

from sqlalchemy.orm import Session
from app.models.document_chunk import DocumentChunk

class DocumentProcessor:

    def __init__(self, db: Session):
        self.db = db

    ## Text Extraction
    def extract_text(
        self, 
        file: UploadFile
    ) -> str: 
        extension = file.filename.split(".")[-1].lower()

        try: 
            if extension == 'pdf':
                return extract_pdf_file(file)
            elif extension == 'docx':
                return extract_docx_file(file)
            elif extension in {'md','txt'}:
                return extract_text_file(file)

            return ""

        finally:
            file.file.seek(0)

    ## Chunking and storing chunk in DB

    def chunk_text(
        self,
        text: str,
        chunk_size : int = 500,
        chunk_overlap : int = 100
    ) -> list[str]:
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=[
                "\n\n",
                "\n",
                ".",
                " ",
                ""
            ]
        )
        chunks = splitter.split_text(text)

        return chunks

    def store_document_chunks_embedding(
        self,
        document_id: int,
        chunks: list[str]
    ):
        document_chunks = []

        for index, chunk in enumerate(chunks):

            embedding = generate_embeddings(chunk)

            document_chunk = DocumentChunk(
                document_id=document_id,
                chunk_index=index,
                chunk_text=chunk,
                embedding=embedding
            )

            document_chunks.append(document_chunk)

        self.db.add_all(document_chunks)
        self.db.commit()

        return document_chunks