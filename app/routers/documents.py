from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.deps import get_db
from app.scripts.load_documents import load_documents

router = APIRouter(prefix='/documents', tags=['documents'])


@router.post('/load-documents')
def load_documents_from_csv(dry_run: bool = False, db: Session = Depends(get_db)):
    load_documents(dry_run=dry_run)  # uses default CSV path
    return {'status': 'completed', 'dry_run': dry_run}
