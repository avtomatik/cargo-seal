from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, schemas, deps

router = APIRouter(prefix='/coverage', tags=['coverage'])

@router.get('/', response_model=list[schemas.Coverage])
def list_coverage(db: Session = Depends(deps.get_db)):
    return crud.get_all_coverage(db)

@router.get('/{coverage_id}', response_model=schemas.Coverage)
def get_coverage(coverage_id: int, db: Session = Depends(deps.get_db)):
    obj = crud.get_coverage(db, coverage_id)
    if not obj:
        raise HTTPException(status_code=404, detail='Coverage not found')
    return obj

@router.post('/', response_model=schemas.Coverage)
def create_coverage(data: schemas.CoverageCreate, db: Session = Depends(deps.get_db)):
    return crud.create_coverage(db, data)
