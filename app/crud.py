from sqlalchemy.orm import Session
from . import models, schemas

def get_cargo(db: Session, cargo_id: int):
    return db.query(models.Cargo).filter(models.Cargo.id == cargo_id).first()

def create_cargo(db: Session, cargo: schemas.CargoCreate):
    db_obj = models.Cargo(**cargo.dict())
    db.add(db_obj); db.commit(); db.refresh(db_obj)
    return db_obj
