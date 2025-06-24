from sqlalchemy.orm import Session

from . import models, schemas


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
