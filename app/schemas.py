import datetime
from decimal import Decimal
from typing import List, Optional

from pydantic import (BaseModel, Field, computed_field, field_validator,
                      model_validator)
from slugify import slugify

from app.models import DocumentCategory


# =============================================================================
# Nested Models
# =============================================================================
class InsuredRead(BaseModel):
    name: str
    address: str

    class Config:
        from_attributes = True


class ProviderRead(BaseModel):
    name: str
    address: str

    class Config:
        from_attributes = True


# =============================================================================
# Base Models
# =============================================================================
class BillOfLadingBase(BaseModel):
    shipment_id: int
    number: str = Field(max_length=64)
    date: datetime.date
    product: str = Field(max_length=128)
    quantity_mt: float
    quantity_bbl: Optional[float] = Field(default=None, ge=-1)
    value: float
    ccy: str = Field(default='USD', min_length=3, max_length=3)

    class Config:
        from_attributes = True


class BillOfLadingCreate(BillOfLadingBase):
    pass


class BillOfLadingRead(BaseModel):
    number: str
    date: datetime.date
    product: str
    quantity_mt: float
    quantity_bbl: Optional[float]
    value: float
    ccy: str

    class Config:
        from_attributes = True


class CoverageBase(BaseModel):
    shipment_id: int
    policy_id: Optional[int] = None
    debit_note: str = Field(default='#', max_length=255)
    ordinary_risks_rate: Decimal = Decimal('0.0')
    war_risks_rate: Decimal = Decimal('0.0')
    value_margin: Optional[float] = 0.0


class CoverageCreate(CoverageBase):
    date: datetime.date = Field(default_factory=datetime.date.today)


class CoverageRead(BaseModel):
    id: int
    shipment: 'ShipmentRead'
    policy: Optional['PolicyRead'] = None
    ordinary_risks_rate: Decimal
    war_risks_rate: Decimal
    date: datetime.date
    value_margin: float

    @computed_field(return_type=Decimal)
    @property
    def premium(self) -> Decimal:
        return Decimal(str(self.shipment.total_value_usd)) * (
            self.ordinary_risks_rate + self.war_risks_rate
        )

    class Config:
        from_attributes = True


class DocumentBase(BaseModel):
    filename: str
    category: DocumentCategory
    vessel_id: int
    provider_id: Optional[int] = None
    number: Optional[str] = None
    date: datetime.date


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


class DocumentRead(DocumentBase):
    id: int

    @computed_field
    @property
    def is_valid(self) -> bool:
        return self.date >= datetime.datetime.now().date()

    class Config:
        from_attributes = True


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
        description="Operator's First Name"
    )
    last_name: str = Field(
        ...,
        max_length=64,
        description="Operator's Last Name"
    )

    class Config:
        str_strip_whitespace = True
        validate_assignment = True


class OperatorCreate(OperatorBase):
    pass


class OperatorRead(OperatorBase):
    first_name: str
    last_name: str

    class Config:
        from_attributes = True


class PolicyBase(BaseModel):
    number: str
    inception: datetime.date
    expiry: Optional[datetime.date]
    provider_id: int
    insured_id: int


class PolicyCreate(PolicyBase):
    pass


class PolicyRead(BaseModel):
    provider: ProviderRead
    number: str
    inception: datetime.date
    expiry: datetime.date

    class Config:
        from_attributes = True


class PortBase(BaseModel):
    name: str = Field(..., max_length=64)
    country: str = Field(..., max_length=64)
    region: Optional[str] = Field(None, max_length=64)


class PortCreate(PortBase):
    pass


class PortRead(BaseModel):
    name: str
    country: str
    region: str

    @property
    def full_name(self) -> str:
        return f'{self.name}, {self.country}'

    class Config:
        from_attributes = True


class ShipmentBase(BaseModel):
    deal_number: int
    insured_id: int
    vessel_id: int
    loadport_id: int
    disport_id: int
    operator_id: int

    class Config:
        from_attributes = True


class ShipmentCreate(ShipmentBase):
    pass


class ShipmentRead(BaseModel):
    deal_number: int
    insured: InsuredRead
    vessel: 'VesselRead'
    loadport: PortRead
    disport: PortRead
    operator: OperatorRead
    bills_of_lading: List[BillOfLadingRead]

    @computed_field
    @property
    def ccy(self) -> Optional[str]:
        currencies = {b.ccy for b in self.bills_of_lading if b.ccy is not None}
        if len(currencies) == 1:
            return currencies.pop()
        elif len(currencies) == 0:
            return None
        else:
            raise NotImplementedError(
                (
                    'Multiple currencies found in bills_of_lading; '
                    'cannot determine a single ccy.'
                )
            )

    @computed_field
    @property
    def total_weight_mt(self) -> float:
        return sum((b.quantity_mt or 0.0) for b in self.bills_of_lading)

    @computed_field
    @property
    def total_volume_bbl(self) -> float:
        return sum((b.quantity_bbl or 0.0) for b in self.bills_of_lading)

    @computed_field
    @property
    def total_value_usd(self) -> float:
        return sum((b.value or 0.0) for b in self.bills_of_lading)

    @computed_field
    @property
    def product_names(self) -> Optional[str]:
        names = {b.product for b in self.bills_of_lading if b.product}
        if not names:
            return None
        return '; '.join(sorted(names))

    @computed_field
    @property
    def bills_of_lading_display(self) -> List[dict[str, str]]:
        return [self._format_bl(b) for b in self.bills_of_lading]

    def _format_bl(self, bill: BillOfLadingRead) -> dict[str, str]:
        NBSP = '\u00A0'

        num = int(bill.number) if str(bill.number).isdigit() else bill.number
        return {
            'bl_number': (
                f'Bill of Lading{NBSP}#{NBSP}{num} '
                f'dated {bill.date:%d{NBSP}%B{NBSP}%Y}'
            )
        }

    class Config:
        from_attributes = True


class VesselBase(BaseModel):
    name: str
    imo: int
    date_built: datetime.date

    @field_validator('imo')
    @classmethod
    def validate_imo(cls, value: int) -> int:
        if value < 1000000 or value > 9999999:
            raise ValueError('IMO number must be a 7-digit integer.')

        numbers = []
        temp = value
        for _ in range(7):
            temp, number = divmod(temp, 10)
            numbers.append(number)

        check_digit = numbers[0]
        calculated_check = sum(
            i * num for i, num in enumerate(numbers[1:], start=2)
        )

        if calculated_check % 10 != check_digit:
            raise ValueError('Not a valid IMO number.')

        return value

    @property
    def year_built(self) -> int:
        return self.date_built.year

    @property
    def folder_name(self) -> str:
        return f'imo_{self.imo}_{self.name.strip().lower().replace(" ", "_")}'


class VesselCreate(VesselBase):
    pass


class VesselRead(VesselBase):
    name: str
    imo: int
    date_built: datetime.date

    class Config:
        from_attributes = True


class VesselUpsert(BaseModel):
    name: str
    imo: int

    @field_validator('imo')
    @classmethod
    def validate_imo(cls, value: int) -> int:
        if value < 1000000 or value > 9999999:
            raise ValueError('IMO number must be a 7-digit integer.')

        numbers = []
        temp = value
        for _ in range(7):
            temp, number = divmod(temp, 10)
            numbers.append(number)

        check_digit = numbers[0]
        calculated_check = sum(
            i * num for i, num in enumerate(numbers[1:], start=2)
        )

        if calculated_check % 10 != check_digit:
            raise ValueError('Not a valid IMO number.')

        return value


ShipmentRead.model_rebuild()
CoverageRead.model_rebuild()
