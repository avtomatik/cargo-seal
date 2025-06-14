from datetime import date
from typing import List, Optional

from pydantic import BaseModel


class EntityBase(BaseModel):
    name: str
    slug: Optional[str] = None
    address: Optional[str] = 'Unknown'

class EntityCreate(EntityBase):
    pass

class Entity(EntityBase):
    id: int

    class Config:
        orm_mode = True


class VesselBase(BaseModel):
    name: str
    imo: int
    date_built: date

class VesselCreate(VesselBase):
    pass

class Vessel(VesselBase):
    id: int

    class Config:
        orm_mode = True


class PolicyBase(BaseModel):
    number: str
    inception: date
    expiry: Optional[date]
    provider_id: int
    insured_id: int

class PolicyCreate(PolicyBase):
    pass

class Policy(PolicyBase):
    id: int
    provider: Entity
    insured: Entity

    class Config:
        orm_mode = True


class BillOfLadingBase(BaseModel):
    number: str
    date: date
    grade: str
    quantity: float
    value: float

class BillOfLadingCreate(BillOfLadingBase):
    shipment_id: int

class BillOfLading(BillOfLadingBase):
    id: int

    class Config:
        orm_mode = True


class ShipmentBase(BaseModel):
    deal_number: int
    insured: str
    vessel_id: int
    loadport_locality: str
    loadport_country: str
    disport_locality: str
    disport_country: str
    subject_matter_insured: str
    weight_metric: float
    sum_insured: float
    ccy: Optional[str] = 'USD'
    operator: str
    volume_bbl: Optional[float] = 0.0
    basis_of_valuation: Optional[float] = 0.0
    disport_eta: date

class ShipmentCreate(ShipmentBase):
    pass

class Shipment(ShipmentBase):
    id: int
    vessel: Vessel
    bills_of_lading: List[BillOfLading] = []

    class Config:
        orm_mode = True
