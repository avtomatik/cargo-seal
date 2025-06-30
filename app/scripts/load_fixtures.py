import json
from datetime import datetime

from sqlalchemy.orm import Session

from app.constants import FIXTURE_DIR
from app.database import SessionLocal
from app.models import (BillOfLading, Coverage, Document, DocumentCategory,
                        Entity, Operator, Policy, Port, Shipment, Vessel)

db: Session = SessionLocal()


def load_model_data(model, file_name):
    with open(f'{FIXTURE_DIR}/{file_name}', 'r') as f:
        items = json.load(f)

    for item in items:
        for key, value in item.items():
            if isinstance(value, str):
                try:
                    item[key] = datetime.fromisoformat(value)
                except ValueError:
                    pass
            if model == Document and key == 'category':
                item[key] = DocumentCategory(value)

        db.merge(model(**item))


load_model_data(Port, 'ports.json')
load_model_data(Vessel, 'vessels.json')
load_model_data(Entity, 'entities.json')
load_model_data(Document, 'documents.json')
load_model_data(Operator, 'operators.json')
load_model_data(Policy, 'policies.json')
load_model_data(Shipment, 'shipments.json')
load_model_data(BillOfLading, 'bills_of_lading.json')
load_model_data(Coverage, 'coverages.json')

db.commit()
db.close()
print('Fixtures loaded.')
