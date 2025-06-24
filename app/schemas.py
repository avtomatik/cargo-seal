from datetime import date
from decimal import Decimal
from typing import List, Optional

from pydantic import (BaseModel, Field, computed_field, field_validator,
                      model_validator)
from slugify import slugify

from app.models import DocumentCategory


class BillOfLadingBase(BaseModel):
    number: str
    date: date
    product: str
    quantity: float
    value: float


class BillOfLadingCreate(BillOfLadingBase):
    shipment_id: int


class BillOfLadingRead(BillOfLadingBase):
    id: int

    class Config:
        from_attributes = True


class CoverageBase(BaseModel):
    shipment_id: int
    policy_id: Optional[int] = None
    debit_note: str = Field(default='#', max_length=255)
    ordinary_risks_rate: Decimal = Decimal('0.0')
    war_risks_rate: Decimal = Decimal('0.0')


class CoveragePushRequest(BaseModel):
    policy_number: str
    vessel_id: int
    cargo_description: str
    insured_value: float
    issued_date: str


class CoverageCreate(CoverageBase):
    pass


class CoverageRead(BaseModel):
    shipment: 'ShipmentRead'
    ordinary_risks_rate: Decimal
    war_risks_rate: Decimal
    date: date

    @computed_field(return_type=Decimal)
    @property
    def premium(self) -> Decimal:
        return self.shipment.sum_insured * (self.ordinary_risks_rate + self.war_risks_rate)

    class Config:
        from_attributes = True


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
    name: str = Field(..., max_length=255)
    slug: Optional[str] = Field(None, max_length=128)
    address: Optional[str] = Field(None, max_length=255)

    class Config:
        str_strip_whitespace = True
        validate_assignment = True


class EntityCreate(EntityBase):
    @field_validator('slug', mode='before')
    @classmethod
    def generate_slug(cls, v, info):
        return v or slugify(info.data.get('name'))

    @field_validator('address', mode='before')
    @classmethod
    def default_address(cls, v):
        return v or 'Unknown'


class EntityRead(EntityBase):
    id: int

    class Config:
        from_attributes = True


class OperatorBase(BaseModel):
    first_name: str = Field(
        ...,
        max_length=64,
        description="Operator's first name"
    )
    last_name: str = Field(
        ...,
        max_length=64,
        description="Operator's last name"
    )

    class Config:
        str_strip_whitespace = True
        validate_assignment = True


class OperatorCreate(OperatorBase):
    pass


class OperatorRead(OperatorBase):
    id: int
    first_name: str
    last_name: str


class PolicyBase(BaseModel):
    number: str
    inception: date
    expiry: Optional[date]
    provider_id: int
    insured_id: int


class PolicyCreate(PolicyBase):
    pass


class PolicyRead(PolicyBase):
    id: int
    provider: EntityRead
    insured: EntityRead

    class Config:
        from_attributes = True


class PortBase(BaseModel):
    name: str = Field(..., max_length=64)
    country: str = Field(..., max_length=64)
    region: Optional[str] = Field(None, max_length=64)


class PortCreate(PortBase):
    pass


class PortRead(PortBase):
    id: int

    class Config:
        from_attributes = True


class ShipmentBase(BaseModel):
    deal_number: int
    insured_id: int
    vessel_id: int
    loadport_id: int
    disport_id: int
    operator_id: int
    subject_matter_insured: str
    weight_metric: float
    sum_insured: float
    ccy: Optional[str] = Field(default='USD', max_length=3)
    volume_bbl: Optional[float] = 0.0
    basis_of_valuation: Optional[float] = 0.0
    disport_eta: Optional[date] = None


class ShipmentCreate(ShipmentBase):
    pass


class ShipmentRead(ShipmentBase):
    id: int

    class Config:
        from_attributes = True


class ShipmentDetail(ShipmentRead):
    vessel: 'VesselRead'
    bills_of_lading: List['BillOfLadingRead'] = []

    class Config:
        from_attributes = True


class VesselBase(BaseModel):
    name: str
    imo: int
    date_built: date


class VesselCreate(VesselBase):
    pass


class VesselRead(VesselBase):
    id: int

    class Config:
        from_attributes = True
