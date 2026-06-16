from app.db.models import Chunk


def save_chunks(
    db,
    document_id,
    chunks
):

    chunk_records = []

    for chunk_text in chunks:

        chunk = Chunk(
            document_id=document_id,
            content=chunk_text
        )

        db.add(chunk)

        chunk_records.append(chunk)

    db.commit()

    return chunk_records