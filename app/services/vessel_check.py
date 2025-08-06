from datetime import datetime

from sqlalchemy.orm import Session

from app.constants import CLASSES_AGREED
from app.models import Document, DocumentCategory

VALID_DOCUMENT_CATEGORIES = [
    DocumentCategory.CLASS_CERTIFICATE,
    DocumentCategory.PI_POLICY
]


def get_valid_documents_with_provider_flag(db: Session, vessel_id: int) -> list[dict]:
    today = datetime.now().date()

    valid_documents = db.query(Document).filter(
        Document.vessel_id == vessel_id,
        Document.category.in_(VALID_DOCUMENT_CATEGORIES),
        Document.date >= today
    ).all()

    results = []
    for doc in valid_documents:
        doc_data = {
            'id': doc.id,
            'filename': doc.filename,
            'category': doc.category,
            'provider': doc.provider,
            'number': doc.number,
            'date': doc.date,
            'provider_agreed': (doc.provider and doc.provider.name in CLASSES_AGREED)
            if doc.category == DocumentCategory.CLASS_CERTIFICATE
            else None
        }
        results.append(doc_data)

    return results
