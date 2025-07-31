from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.constants import TEMPLATE_DIR
from app.services.coverage import generate_coverage_docx

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


@router.get('/{coverage_id}/draft')
def draft_coverage_docx(coverage_id: int, db: Session = Depends(deps.get_db)):
    coverage = crud.get_coverage(db, coverage_id)
    if not coverage:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Coverage not found'
        )

    shipment = coverage.shipment
    vessel = shipment.vessel

    coverage_date = coverage.date
    imo = vessel.imo
    vessel_name = vessel.name.lower().replace(' ', '_')

    filename = f'certificate_{coverage_date}_imo_{imo}_{vessel_name}_draft.docx'

    template_path = TEMPLATE_DIR / 'certificate.docx'
    buffer = generate_coverage_docx(coverage, template_path)

    return StreamingResponse(
        buffer,
        media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        headers={
            'Content-Disposition': f'attachment; filename={filename}'
        }
    )
