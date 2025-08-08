from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app import crud, deps, schemas
from app.constants import TEMPLATE_DIR
from app.services.coverage import generate_coverage_docx
from app.utils.coverage_transform import transform_flat_to_nested

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
    obj = crud.get_coverage(db, coverage_id)
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Coverage not found'
        )

    shipment = obj.shipment
    vessel = shipment.vessel

    coverage_date = obj.date
    imo = vessel.imo
    vessel_name = vessel.name.lower().replace(' ', '_')

    filename = f'certificate_{coverage_date}_imo_{imo}_{vessel_name}_draft.docx'

    template_path = TEMPLATE_DIR / 'certificate.docx'
    buffer = generate_coverage_docx(obj, template_path)

    return StreamingResponse(
        buffer,
        media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        headers={
            'Content-Disposition': f'attachment; filename={filename}'
        }
    )


@router.post('/draft-flat')
def draft_coverage_docx_flat(
    flat_data: schemas.CoverageDraftFlat,
    db: Session = Depends(deps.get_db)
):
    nested = transform_flat_to_nested(db, flat_data)

    nested_dict = nested.model_dump()
    nested_dict['id'] = 0

    buffer = generate_coverage_docx(
        nested_dict, TEMPLATE_DIR / 'certificate.docx')

    filename = f"certificate_{nested.date}_imo_{nested.shipment.vessel.imo}_{nested.shipment.vessel.name.lower().replace(' ', '_')}_draft.docx"

    return StreamingResponse(
        buffer,
        media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        headers={'Content-Disposition': f'attachment; filename={filename}'}
    )
