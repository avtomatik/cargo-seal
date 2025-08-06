from datetime import datetime

from sqlalchemy.orm import Session

from app.constants import CLASSES_AGREED
from app.models import Document, DocumentCategory

VALID_DOCUMENT_CATEGORIES = [
    DocumentCategory.CLASS_CERTIFICATE,
    DocumentCategory.PI_POLICY
]


def get_valid_documents_with_provider_flag(
    db: Session,
    vessel_id: int
) -> list[dict]:
    today = datetime.now().date()

    valid_documents = db.query(Document).filter(
        Document.vessel_id == vessel_id,
        Document.category.in_(VALID_DOCUMENT_CATEGORIES),
        Document.date >= today
    ).all()

    results = []
    for document in valid_documents:
        data = {
            'id': document.id,
            'filename': document.filename,
            'category': document.category,
            'provider': document.provider,
            'number': document.number,
            'date': document.date,
            'provider_agreed': (
                document.provider and document.provider.name in CLASSES_AGREED
            )
            if document.category == DocumentCategory.CLASS_CERTIFICATE
            else None
        }
        results.append(data)

    return results
