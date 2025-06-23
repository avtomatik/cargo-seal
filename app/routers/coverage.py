from pathlib import Path
from tempfile import NamedTemporaryFile

from fastapi import (APIRouter, Depends, File, HTTPException, Request,
                     UploadFile, status)
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.constants import SHEET_NAMES_EXPECTED
from app.services.excel_reader import ExcelReader

from .. import crud, deps, schemas

router = APIRouter(prefix='/coverage', tags=['coverage'])


@router.get('/', response_model=list[schemas.CoverageRead])
def list_coverage(db: Session = Depends(deps.get_db)):
    return crud.get_all_coverage(db)


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


templates = Jinja2Templates(directory='templates')


@router.post('/push', response_class=HTMLResponse)
async def push_coverage(request: Request, file: UploadFile = File(...)):
    """
    Push Declaration to Database Handler (HTML view)
    """
    if not file:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='No file provided'
        )

    with NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp:
        tmp.write(await file.read())
        tmp_path = Path(tmp.name)

    reader = ExcelReader()
    try:
        sheet_names, operator = reader.get_details(tmp_path)

        if not SHEET_NAMES_EXPECTED.issubset(sheet_names):
            return templates.TemplateResponse(
                'missing_sheets.html',
                {
                    'request': request,
                    'filename': file.filename,
                    'sheet_names': sheet_names,
                },
                status_code=status.HTTP_400_BAD_REQUEST
            )

    except Exception:
        return HTMLResponse(
            content='<h1>Failed to process shipment file.</h1>',
            status_code=status.HTTP_400_BAD_REQUEST
        )

    return templates.TemplateResponse(
        'shipment_result.html',
        {'request': request, 'sheet_names': sheet_names, 'operator': operator}
    )
