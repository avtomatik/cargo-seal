from pathlib import Path

from celery import Celery

from app.database import SessionLocal
from app.services import declaration

celery = Celery(
    'app',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0',
)


@celery.task
def process_shipment_task(file_path_str: str):
    file_path = Path(file_path_str)
    db = SessionLocal()
    try:
        declaration.process_declaration_file(file_path, db)
        if file_path.exists():
            file_path.unlink()
    except Exception as e:
        raise e
    finally:
        db.close()
