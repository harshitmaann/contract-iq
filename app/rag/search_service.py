from sqlalchemy import text

from app.rag.embedding_service import create_embedding


def search_chunks(
    db,
    question,
    limit=5
):

    embedding = create_embedding(question)

    sql = text("""
        SELECT
            c.id,
            c.document_id,
            d.filename,
            c.content
        FROM chunks c
        JOIN documents d
            ON c.document_id = d.id
        ORDER BY c.embedding <=> :embedding
        LIMIT :limit
    """)

    results = db.execute(
        sql,
        {
            "embedding": str(embedding),
            "limit": limit
        }
    )

    return results.fetchall()