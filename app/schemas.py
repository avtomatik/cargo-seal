from datetime import date
from decimal import Decimal
from typing import List, Optional

from pydantic import BaseModel, Field, model_validator

from app.models import DocumentCategory


class CoverageBase(BaseModel):
    shipment_id: int
    policy_id: Optional[int] = None
    debit_note: str = Field(default='#', max_length=255)
    ordinary_risks_rate: Decimal = Decimal('0.0')
    war_risks_rate: Decimal = Decimal('0.0')


class CoverageCreate(CoverageBase):
    pass  # add validation for creation if needed


class CoverageRead(CoverageBase):
    date: date
    premium: Decimal

    class Config:
        from_attributes = True  # Enables ORM model compatibility for response


class DocumentBase(BaseModel):
    filename: str
    category: DocumentCategory
    vessel_id: int
    provider_id: Optional[int] = None
    number: Optional[str] = None
    date: date


class DocumentCreate(DocumentBase):
    @model_validator(mode='after')
    def validate_required_fields(cls, model):
        if model.category != DocumentCategory.Q88:
            if model.provider_id is None:
                raise ValueError(
                    'provider_id is required unless category is Q88'
                )
            if not model.number:
                raise ValueError('number is required unless category is Q88')
        return model


class EntityBase(BaseModel):
    name: str
    slug: Optional[str] = None
    address: Optional[str] = 'Unknown'


class EntityCreate(EntityBase):
    pass


class Entity(EntityBase):
    id: int

    class Config:
        from_attributes = True


class VesselBase(BaseModel):
    name: str
    imo: int
    date_built: date


class VesselCreate(VesselBase):
    pass


class Vessel(VesselBase):
    id: int

    class Config:
        from_attributes = True


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
        from_attributes = True


class BillOfLadingBase(BaseModel):
    number: str
    date: date
    product: str
    quantity: float
    value: float


class BillOfLadingCreate(BillOfLadingBase):
    shipment_id: int


class BillOfLading(BillOfLadingBase):
    id: int

    class Config:
        from_attributes = True


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
        from_attributes = True


class CoveragePushRequest(BaseModel):
    policy_number: str
    vessel_id: int
    cargo_description: str
    insured_value: float
    issued_date: str  # or `datetime` if you parse it
