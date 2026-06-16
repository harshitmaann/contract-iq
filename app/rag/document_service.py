from app.db.models import Document


def create_document(
    db,
    filename,
    pages,
    characters
):
    document = Document(
        filename=filename,
        page_count=pages,
        character_count=characters
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    return document