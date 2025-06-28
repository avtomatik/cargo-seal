from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import crud, deps, schemas

router = APIRouter(prefix='/coverage', tags=['coverage'])


@router.get('/', response_model=list[schemas.CoverageRead])
def list_coverage(db: Session = Depends(deps.get_db)):
    return crud.get_all_coverage(db)


@router.get('/shipments/{shipment_id}', response_model=schemas.ShipmentWithTotals)
def read_shipment_with_totals(shipment_id: int, db: Session = Depends(deps.get_db)):
    result = crud.get_shipment_with_totals(db, shipment_id)
    if not result:
        raise HTTPException(status_code=404, detail='Shipment not found')
    return result


@router.get('/{coverage_id}', response_model=schemas.CoverageRead)
def get_coverage(coverage_id: int, db: Session = Depends(deps.get_db)):
    obj = crud.get_coverage(db, coverage_id)
    if not obj:
        raise HTTPException(status_code=404, detail='Coverage not found')
    return obj


@router.post('/', response_model=schemas.CoverageCreate)
def create_coverage(
    data: schemas.CoverageCreate,
    db: Session = Depends(deps.get_db)
):
    return crud.create_coverage(db, data)
