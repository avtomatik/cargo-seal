from datetime import date

from sqlalchemy.orm import Session

from app import models
from app.constants import CLASSES_AGREED


def check_vessel_documents(db: Session, vessel_id: int) -> dict:
    vessel = db.query(models.Vessel).filter(
        models.Vessel.id == vessel_id
    ).first()
    if not vessel:
        raise ValueError(f'Vessel with ID {vessel_id} not found.')

    results = {
        'vessel_id': vessel_id,
        'invalid_documents': [],
        'class_certificate_valid': False,
    }

    today = date.today()
    documents = db.query(models.Document).filter(
        models.Document.vessel_id == vessel_id
    ).all()

    for doc in documents:
        if doc.date and doc.date > today:
            results['invalid_documents'].append({
                'id': doc.id,
                'type': doc.type,
                'date': doc.date.isoformat(),
            })

        if doc.type == models.DocumentCategory.CLASS_CERTIFICATE:
            if doc.value in CLASSES_AGREED:
                results['class_certificate_valid'] = True

    return results
