import traceback
from pathlib import Path
from tempfile import NamedTemporaryFile

from fastapi import (APIRouter, Depends, File, HTTPException, Request,
                     UploadFile, status)
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.constants import SHEET_NAMES_EXPECTED
from app.services.excel_processors import SummaryFromExcelProcessor
from app.services.excel_reader import ExcelReader
from app.utils.data_transform import standardize_dataset
from app.utils.text import parse_date

from .. import crud, deps, schemas

router = APIRouter(prefix='/coverage', tags=['coverage'])


# @router.get('/', response_model=list[schemas.CoverageRead])
# def list_coverage(db: Session = Depends(deps.get_db)):
#     return crud.get_all_coverage(db)


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
async def push_coverage(
    request: Request,
    file: UploadFile = File(...),
    db: Session = Depends(deps.get_db)
):
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

        summary_processor = SummaryFromExcelProcessor()
        df_summary = (
            reader.read_sheet(tmp_path, 'declaration_form')
            .pipe(summary_processor.process)
        )
        df_details = (
            reader.read_sheet(tmp_path, 'bl_breakdown')
            .pipe(standardize_dataset)
        )

        summary = df_summary['current'].to_dict()

        vessel_name = summary['vessel']
        vessel_imo = summary['imo']
        vessel_date_built = parse_date(summary['date_built']) if isinstance(
            summary['date_built'], str) else summary['date_built']

        vessel_in = schemas.VesselCreate(
            name=vessel_name,
            imo=vessel_imo,
            date_built=vessel_date_built
        )
        vessel_db = crud.upsert_vessel(db, vessel=vessel_in)

        entity_names = [
            ('insured', 'address'),
            ('counterparty', 'beneficiary_address'),
            ('surveyor_loadport', None),
            ('surveyor_disport', None),
        ]

        for name_key, address_key in entity_names:
            name = summary[name_key]
            address = summary.get(address_key)
            entity_data = schemas.EntityCreate(name=name, address=address)
            crud.upsert_entity_by_name(db, entity_data)

        port_names = [
            ('loadport_locality', 'loadport_country'),
            ('disport_locality', 'disport_country'),
        ]

        for name_key, country_key in port_names:
            name = summary[name_key]
            country = summary[country_key]
            port_data = schemas.PortCreate(name=name, country=country)
            crud.upsert_port(db, port_data)

        first_name, last_name = operator.split()
        operator_data = schemas.OperatorCreate(
            first_name=first_name,
            last_name=last_name
        )
        crud.upsert_operator(db, operator_data)

    except Exception as e:
        traceback.print_exc()
        return HTMLResponse(
            content=f'<h1>Failed to process shipment file.</h1><p>{e}</p>',
            status_code=status.HTTP_400_BAD_REQUEST
        )

    return templates.TemplateResponse(
        'shipment_result.html',
        {'request': request, 'sheet_names': sheet_names,
            'operator': operator, 'vessel': vessel_db}
    )
