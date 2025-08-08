from decimal import Decimal

from sqlalchemy.orm import Session

from app import models, schemas


def transform_flat_to_nested(
    db: Session,
    flat: schemas.CoverageDraftFlat
) -> schemas.CoverageDraftCreate:
    """
    Transforms a flat coverage draft payload into a nested CoverageDraftCreate
    schema.
    """

    # Resolve insured
    insured_obj = db.query(models.Entity).filter_by(name=flat.insured).first()

    # Resolve vessel
    vessel_obj = db.query(models.Vessel).filter_by(imo=flat.vessel).first()

    # Resolve loadport
    loadport_name, loadport_country = flat.loadport.split(', ')
    loadport_obj = (
        db.query(models.Port)
        .filter_by(name=loadport_name.strip(), country=loadport_country.strip())
        .first()
    )

    # Resolve disport
    disport_name, disport_country = flat.disport.split(', ')
    disport_obj = (
        db.query(models.Port)
        .filter_by(name=disport_name.strip(), country=disport_country.strip())
        .first()
    )

    # Resolve operator
    first_name, last_name = flat.operator.split(' ', 1)

    # Transform bills of lading
    bills_of_lading = []
    for bl in flat.bills_of_lading:
        value = (
            Decimal(str(bl.quantity_mt)) * Decimal(str(bl.price_per_unit))
            if bl.price_per_unit is not None
            else None
        )
        bills_of_lading.append(
            schemas.BillOfLadingRead(
                number=bl.number,
                date=bl.date,
                product=bl.product,
                quantity_mt=bl.quantity_mt,
                quantity_bbl=bl.quantity_bbl or 0,
                value=value,
                ccy=bl.ccy,
            )
        )

    shipment = schemas.ShipmentRead(
        deal_number=flat.deal_number,
        insured=schemas.InsuredRead(
            name=insured_obj.name,
            address=insured_obj.address,
        ),
        vessel=schemas.VesselRead(
            name=vessel_obj.name,
            imo=vessel_obj.imo,
            date_built=vessel_obj.date_built,
        ),
        loadport=schemas.PortRead(
            name=loadport_obj.name,
            country=loadport_obj.country,
            region=loadport_obj.region,
        ),
        disport=schemas.PortRead(
            name=disport_obj.name,
            country=disport_obj.country,
            region=disport_obj.region,
        ),
        operator=schemas.OperatorRead(
            first_name=first_name,
            last_name=last_name,
        ),
        bills_of_lading=bills_of_lading,
    )

    policy_obj = db.query(models.Policy).filter_by(number=flat.policy_number).first()

    premium_value = flat.premium if flat.premium is not None else Decimal('0')

    return schemas.CoverageDraftCreate(
        shipment=shipment,
        policy=policy_obj,
        ordinary_risks_rate=flat.ordinary_risks_rate,
        war_risks_rate=flat.war_risks_rate,
        date=flat.date,
        value_margin=flat.value_margin,
        premium=premium_value,
    )
