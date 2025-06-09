import datetime
import json
from pathlib import Path
from typing import List, Optional, Union

from core.services import DateService
from pydantic import BaseModel, Field, PrivateAttr

from pydantic_models.shared import Surveyor
from pydantic_models.vessels import VesselModel


class BillOfLading(BaseModel):
    number: Union[str, int]
    date: datetime.date
    # grade: str
    # quantity: float
    # value: float

    def format_bl_number(self):
        num = int(self.number) if isinstance(
            self.number, (int, float)
        ) else self.number
        return {
            'bl_number': f'Bill of Lading #\xa0{num} dated {self.date:%d\xa0%B\xa0%Y}'
        }

    @classmethod
    def format_bl_list(cls, bills_of_lading: List['BillOfLading']) -> List[dict]:
        return [bill.format_bl_number() for bill in bills_of_lading]


class PortMappingService:
    def __init__(self, path: Path):
        self.path = path
        self._mapping: dict[str, str] = {}

    def get_region(self, port: Optional[str]) -> Optional[str]:
        if not self._mapping:
            with self.path.open(encoding='utf-8') as f:
                self._mapping = json.load(f)
        return self._mapping.get(port)


class Port(BaseModel):
    locality: str
    country: str
    _mapping_service: PortMappingService = PrivateAttr()

    def __init__(self, **data):
        super().__init__(**data)
        FILE_NAME = 'map_logistics_locations.json'
        self._mapping_service = PortMappingService(
            ROOT_DIR / 'src' / 'config' / FILE_NAME
        )

    @property
    def name(self) -> str:
        return f'{self.locality}, {self.country}'

    @property
    def region(self) -> Optional[str]:
        return self._mapping_service.get_region(self.name)


class ShipmentMeta(BaseModel):
    counterparty: str = 'Unknown'
    contract_number: str = 'Unknown'
    surveyor_loadport: 'Surveyor' = Surveyor.CLB_RU
    surveyor_disport: 'Surveyor' = Surveyor.SGSN_CH


class ShipmentDataModel(BaseModel):
    deal_number: int
    insured: str
    vessel: 'VesselModel'
    loadport_locality: str
    loadport_country: str
    disport_locality: str
    disport_country: str
    subject_matter_insured: str
    bills_of_lading: List[BillOfLading]
    weight_metric: float
    sum_insured: float
    ccy: str = 'USD'
    operator: str
    volume_bbl: float = 0.0
    basis_of_valuation: float = 0.0
    disport_eta: datetime.date = Field(
        default_factory=lambda: DateService.get_date(40)
    )
    meta: ShipmentMeta

    @property
    def quantity_gross_kg(self) -> Optional[float]:
        return self.weight_metric / 1000 if self.weight_metric else None

    @property
    def loadport(self) -> Port:
        return Port(locality=self.loadport_locality, country=self.loadport_country)

    @property
    def disport(self) -> Port:
        return Port(locality=self.disport_locality, country=self.disport_country)

    def flatten(self) -> dict:
        return {
            'deal_number': self.deal_number,
            'insured': self.insured,
            'vessel': getattr(self.vessel, 'name', 'Unknown'),
            'imo': getattr(self.vessel, 'imo', -1),
            'date_built': getattr(self.vessel, 'date', None),
            'loadport': self.loadport.name,
            'disport': self.disport.name,
            'load_region': self.loadport.region,
            'disc_region': self.disport.region,
            'subject_matter_insured': self.subject_matter_insured,
            'bl_number': self.bills_of_lading[0].number if self.bills_of_lading else None,
            'bl_date': self.bills_of_lading[0].date if self.bills_of_lading else None,
            'sum_insured': self.sum_insured,
            'ccy': self.ccy,
            'operator': self.operator,
            'volume_bbl': self.volume_bbl,
            'gross_weight_kg': self.quantity_gross_kg,
            'basis_of_valuation': self.basis_of_valuation,
            'counterparty': self.meta.counterparty,
            'contract_number': self.meta.contract_number,
            'surveyor_loadport': self.meta.surveyor_loadport.value,
            'surveyor_disport': self.meta.surveyor_disport.value,
        }
