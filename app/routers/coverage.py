from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import crud, deps, schemas

router = APIRouter(prefix='/coverage', tags=['coverage'])


@router.get('/', response_model=list[schemas.CoverageRead])
def list_coverage(db: Session = Depends(deps.get_db)):
    return crud.get_all_coverage(db)


@router.post('/', response_model=schemas.CoverageCreate)
def create_coverage(
    data: schemas.CoverageCreate,
    db: Session = Depends(deps.get_db)
):
    return crud.create_coverage(db, data)


@router.get('/{coverage_id}', response_model=schemas.CoverageRead)
def get_coverage(coverage_id: int, db: Session = Depends(deps.get_db)):
    obj = crud.get_coverage(db, coverage_id)
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Coverage not found'
        )
    return obj
