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
            id,
            content
        FROM chunks
        ORDER BY embedding <=> :embedding
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