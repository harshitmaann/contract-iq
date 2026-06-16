from fastapi import APIRouter
from fastapi import UploadFile
from fastapi import File

from app.rag.pdf_processor import extract_pdf_text

router = APIRouter()


@router.post("/upload")
async def upload_pdf(
    file: UploadFile = File(...)
):

    pdf_bytes = await file.read()

    result = extract_pdf_text(pdf_bytes)

    return {
        "filename": file.filename,
        "pages": result["pages"],
        "characters": len(result["text"])
    }