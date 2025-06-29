import traceback
from pathlib import Path
from tempfile import NamedTemporaryFile

from fastapi import HTTPException, UploadFile, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app import crud
from app.constants import SHEET_NAMES_EXPECTED
from app.schemas import (BillOfLadingCreate, CoverageCreate, EntityCreate,
                         OperatorCreate, PortCreate, ShipmentCreate,
                         VesselCreate)
from app.services.excel_processors import SummaryFromExcelProcessor
from app.services.excel_reader import ExcelReader
from app.utils.data_transform import standardize_dataset
from app.utils.text import parse_date

templates = Jinja2Templates(directory='templates')


def save_temp_file(file: UploadFile) -> Path:
    with NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp:
        tmp.write(file.file.read())
        return Path(tmp.name)


def validate_sheet_names(sheet_names: set[str]):
    if not SHEET_NAMES_EXPECTED.issubset(sheet_names):
        raise ValueError('Missing expected Excel sheets')


def parse_summary_and_details(path):
    reader = ExcelReader()
    sheet_names, operator_name = reader.get_details(path)
    validate_sheet_names(sheet_names)

    df_summary = (
        reader.read_sheet(path, 'declaration_form')
        .pipe(SummaryFromExcelProcessor().process)
    )

    df_details = (
        reader.read_sheet(path, 'bl_breakdown')
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
            detail=(
                'Missing required columns in Excel sheet: '
                f"{', '.join(missing_columns)}"
            )
        )

    summary = df_summary['current'].to_dict()

    return sheet_names, operator_name, df_details, summary


def create_vessel(db, summary):
    vessel_date_built = parse_date(summary['date_built']) if isinstance(
        summary['date_built'], str) else summary['date_built']

    return crud.upsert_vessel(
        db,
        vessel=VesselCreate(
            name=summary['vessel'],
            imo=summary['imo'],
            date_built=vessel_date_built
        )
    )


def create_operator(db, operator_name):
    first_name, last_name = operator_name.split()
    return crud.get_or_create_operator(
        db,
        OperatorCreate(first_name=first_name, last_name=last_name)
    )


def create_ports(db, summary):
    port_ids = {}
    for name_key, country_key in [
        ('loadport_locality', 'loadport_country'),
        ('disport_locality', 'disport_country'),
    ]:
        port = crud.upsert_port(
            db,
            PortCreate(
                name=summary[name_key],
                country=summary[country_key]
            )
        )
        port_ids[name_key] = port.id
    return port_ids


def create_entities(db, summary):
    insured_id = None
    for name_key, address_key in [
        ('insured', 'address'),
        ('counterparty', 'beneficiary_address'),
        ('surveyor_loadport', None),
        ('surveyor_disport', None),
    ]:
        name = summary[name_key]
        address = summary.get(address_key)
        entity = crud.upsert_entity_by_name(
            db,
            EntityCreate(name=name, address=address)
        )
        if name_key == 'insured':
            insured_id = entity.id
    return insured_id


def create_shipment(db, insured_id, port_ids, deal_number, vessel_id, operator_id):
    return crud.create_shipment(
        db,
        ShipmentCreate(
            deal_number=deal_number,
            insured_id=insured_id,
            vessel_id=vessel_id,
            loadport_id=port_ids['loadport_locality'],
            disport_id=port_ids['disport_locality'],
            operator_id=operator_id,
            disport_eta=None
        )
    )


def create_bills_of_lading(db, df_details, shipment_id, ccy='USD'):
    items = [
        BillOfLadingCreate(
            shipment_id=shipment_id,
            number=str(row['bl_number']),
            date=row['bl_date'].date(),
            product=row['subject_matter_insured'],
            quantity_mt=row['weight_mt_in_vacuum'],
            quantity_bbl=row.get('volume_bbl', 0.0),
            value=row['sum_insured_100_usd'],
            ccy=row.get('ccy', ccy)
        )
        for _, row in df_details.iterrows()
    ]

    crud.bulk_create_bills(db, items)


def create_coverage(db, shipment_id, basis_of_valuation):
    crud.create_coverage(
        db,
        CoverageCreate(
            shipment_id=shipment_id,
            basis_of_valuation=basis_of_valuation,
            policy_id=None
        )
    )


def process_declaration_file(file: UploadFile, db: Session) -> tuple:
    try:
        tmp_path = save_temp_file(file)
        sheet_names, operator_name, df_details, summary = parse_summary_and_details(
            tmp_path
        )

        vessel = create_vessel(db, summary)
        insured_id = create_entities(db, summary)
        port_ids = create_ports(db, summary)
        operator = create_operator(db, operator_name)
        shipment = create_shipment(
            db,
            insured_id,
            port_ids,
            summary['deal_number'],
            vessel.id,
            operator.id
        )
        create_bills_of_lading(db, df_details, shipment.id)
        create_coverage(db, shipment.id, summary['basis_of_valuation'])

        return sheet_names, operator_name, vessel

    except Exception as e:
        traceback.print_exc()
        return HTMLResponse(
            content=f'<h1>Failed to process shipment file.</h1><p>{e}</p>',
            status_code=status.HTTP_400_BAD_REQUEST
        )
