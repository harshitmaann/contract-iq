from app.rag.embedding_service import create_embedding


def embed_chunks(
    db,
    chunk_records
):

    for chunk in chunk_records:

        embedding = create_embedding(
            chunk.content
        )

        chunk.embedding = embedding

    db.commit()