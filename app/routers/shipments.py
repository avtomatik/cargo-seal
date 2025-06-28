import traceback
from pathlib import Path
from tempfile import NamedTemporaryFile

from fastapi import (APIRouter, Depends, File, HTTPException, Request,
                     UploadFile, status)
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app import crud, deps, schemas
from app.constants import SHEET_NAMES_EXPECTED
from app.services.excel_processors import SummaryFromExcelProcessor
from app.services.excel_reader import ExcelReader
from app.utils.data_transform import standardize_dataset
from app.utils.text import parse_date

router = APIRouter(prefix='/shipments', tags=['shipments'])

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

        required_columns = [
            'bl_number',
            'bl_date',
            'subject_matter_insured',
            'weight_mt_in_vacuum',
            'sum_insured_100_usd'
        ]

        missing_columns = [
            col for col in required_columns if col not in df_details.columns
        ]
        if missing_columns:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Missing required columns in Excel sheet: {', '.join(missing_columns)}"
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

            entity = crud.upsert_entity_by_name(db, entity_data)

            if name_key == 'insured':
                insured_id = entity.id

        loadport_id = None
        disport_id = None

        port_names = [
            ('loadport_locality', 'loadport_country'),
            ('disport_locality', 'disport_country'),
        ]

        for name_key, country_key in port_names:
            name = summary[name_key]
            country = summary[country_key]
            port_data = schemas.PortCreate(name=name, country=country)

            port = crud.upsert_port(db, port_data)

            if name_key == 'loadport_locality':
                loadport_id = port.id
            elif name_key == 'disport_locality':
                disport_id = port.id

        first_name, last_name = operator.split()
        operator_data = schemas.OperatorCreate(
            first_name=first_name,
            last_name=last_name
        )
        operator_obj = crud.get_or_create_operator(db, operator_data)

        shipment_data = schemas.ShipmentCreate(
            deal_number=summary['deal_number'],
            insured_id=insured_id,
            vessel_id=vessel_db.id,
            loadport_id=loadport_id,
            disport_id=disport_id,
            operator_id=operator_obj.id,
            disport_eta=None
        )

        shipment_obj = crud.create_shipment(db, shipment_data)

        bill_of_lading_items = [
            schemas.BillOfLadingCreate(
                shipment_id=shipment_obj.id,
                number=str(row['bl_number']),
                date=row['bl_date'].date(),
                product=row['subject_matter_insured'],
                quantity_mt=row['weight_mt_in_vacuum'],
                quantity_bbl=row.get('volume_bbl', 0.0),
                value=row['sum_insured_100_usd'],
                ccy=row.get('ccy', summary.get('ccy', 'USD'))
            )
            for _, row in df_details.iterrows()
        ]

        crud.bulk_create_bills(db, bill_of_lading_items)

        coverage_data = schemas.CoverageCreate(
            shipment_id=shipment_obj.id,
            basis_of_valuation=summary['basis_of_valuation'],
            policy_id=None
        )
        crud.create_coverage(db, coverage_data)

    except Exception as e:
        traceback.print_exc()
        return HTMLResponse(
            content=f'<h1>Failed to process shipment file.</h1><p>{e}</p>',
            status_code=status.HTTP_400_BAD_REQUEST
        )

    return templates.TemplateResponse(
        'shipment_result.html',
        {
            'request': request,
            'sheet_names': sheet_names,
            'operator': operator,
            'vessel': vessel_db
        }
    )
