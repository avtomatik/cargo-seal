from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from . import models, schemas


def get_entity_by_name(db: Session, name: str):
    return db.query(models.Entity).filter(models.Entity.name == name).first()


def get_entity(db: Session, entity_id: int):
    return db.query(models.Entity).filter(models.Entity.id == entity_id).first()


def get_entities(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Entity).offset(skip).limit(limit).all()


def create_entity(db: Session, entity: schemas.EntityCreate):
    entity_data = entity.model_dump()
    db_entity = models.Entity(**entity_data)
    db.add(db_entity)
    try:
        db.commit()
        db.refresh(db_entity)
        return db_entity
    except IntegrityError:
        db.rollback()
        raise


def upsert_entity_by_name(db: Session, entity: schemas.EntityCreate):
    """
    Either update an existing entity by name or create a new one.
    """
    existing = get_entity_by_name(db, entity.name)
    entity_data = entity.model_dump()

    if existing:
        for key, value in entity_data.items():
            setattr(existing, key, value)
        db.commit()
        db.refresh(existing)
        return existing
    else:
        return create_entity(db, entity)


def upsert_operator(db: Session, operator_data: schemas.OperatorCreate) -> models.Operator:
    existing_operator = (
        db.query(models.Operator)
        .filter(
            models.Operator.first_name == operator_data.first_name,
            models.Operator.last_name == operator_data.last_name,
        )
        .first()
    )

    if not existing_operator:
        new_operator = models.Operator(**operator_data.model_dump())
        db.add(new_operator)
        db.commit()
        db.refresh(new_operator)
        return new_operator


def upsert_port(db: Session, port: schemas.PortCreate) -> models.Port:
    stmt = select(models.Port).where(
        models.Port.name == port.name,
        models.Port.country == port.country
    )
    db_port = db.execute(stmt).scalar_one_or_none()

    if db_port:
        return db_port  # already exists

    # Create new port
    db_port = models.Port(name=port.name, country=port.country)
    db.add(db_port)
    db.commit()
    db.refresh(db_port)
    return db_port


def get_vessel_by_imo(db: Session, imo: int):
    return db.query(models.Vessel).filter(models.Vessel.imo == imo).one_or_none()


def upsert_vessel(db: Session, vessel: schemas.VesselCreate):
    db_obj = db.query(models.Vessel).filter(
        models.Vessel.imo == vessel.imo
    ).first()

    vessel_data = vessel.model_dump()

    if db_obj:
        for key, value in vessel_data.items():
            setattr(db_obj, key, value)
    else:
        db_obj = models.Vessel(**vessel_data)
        db.add(db_obj)

    db.commit()
    db.refresh(db_obj)
    return db_obj
