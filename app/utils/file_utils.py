from fastapi import UploadFile
from PyPDF2 import PdfReader
from docx import Document as doc

def get_page_count(
    file: UploadFile
) -> int:
    extension = file.filename.split(".")[-1].lower()

    try:
        if extension == "pdf":
            reader = PdfReader(file.file)
            count = len(reader.pages)

            file.file.seek(0)

            return count

        elif extension in {"docx", "txt", "md"}:
            file.file.seek(0)
            return 1

        file.file.seek(0)
        return 1

    except Exception:
        file.file.seek(0)
        return 1

def extract_pdf_file(
    file: UploadFile
) -> str:
    reader = PdfReader(file.file)
    
    text = []

    for page in reader.pages:
        page_text = page.extract_text()
        
        if page_text:
            text.append(page_text)

    file.file.seek(0)

    return "\n".join(text)

def extract_docx_file(
    file: UploadFile 
) -> str:
    document = doc(file.file)

    text = []

    for paragraph in document.paragraphs:
        text.append(paragraph.text)

    file.file.seek(0)

    return "\n".join(text)

def extract_text_file(
    file: UploadFile
) -> str:
    text = file.file.read()

    file.file.seek(0)

    return text.decode("utf-8")