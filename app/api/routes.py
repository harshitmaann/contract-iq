from fastapi import APIRouter
from fastapi import UploadFile
from fastapi import File
from fastapi import Depends

from sqlalchemy.orm import Session

from app.db.session import get_db

from app.rag.pdf_processor import extract_pdf_text
from app.rag.document_service import create_document
from app.rag.chunking import create_chunks
from app.rag.chunk_service import save_chunks
from app.rag.vector_service import embed_chunks
from app.models.search_request import SearchRequest
from app.rag.search_service import search_chunks
from app.models.ask_request import AskRequest
from app.rag.llm_service import generate_answer

router = APIRouter()


@router.post("/upload")
async def upload_pdf(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    pdf_bytes = await file.read()

    result = extract_pdf_text(pdf_bytes)

    document = create_document(
        db=db,
        filename=file.filename,
        pages=result["pages"],
        characters=len(result["text"])
    )

    chunks = create_chunks(
        result["text"]
    )

    chunk_records = save_chunks(
        db=db,
        document_id=document.id,
        chunks=chunks
    )

    embed_chunks(
        db=db,
        chunk_records=chunk_records
    )

    return {
        "document_id": document.id,
        "filename": document.filename,
        "pages": document.page_count,
        "characters": document.character_count,
        "chunks_created": len(chunks),
        "embeddings_created": len(chunk_records)
    }

@router.post("/search")
def search(
    request: SearchRequest,
    db: Session = Depends(get_db)
):

    results = search_chunks(
        db=db,
        question=request.question
    )

    return {
        "question": request.question,
        "results": [
            row.content
            for row in results
        ]
    }
@router.post("/ask")
def ask(
    request: AskRequest,
    db: Session = Depends(get_db)
):

    results = search_chunks(
        db=db,
        question=request.question
    )

    chunks = [
        row.content
        for row in results
    ]

    answer = generate_answer(
        request.question,
        chunks
    )

    return {
        "question": request.question,
        "answer": answer
    }