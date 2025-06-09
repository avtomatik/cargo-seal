import re
from typing import Any, Dict

import pandas as pd
from core.services import DateService, clean_string

from pydantic_models.extractors import FieldExtractor
from pydantic_models.logistics import (BillOfLading, ShipmentDataModel,
                                       ShipmentMeta)
from pydantic_models.shared import Surveyor
from pydantic_models.utils import parse_date, sort_and_concat
from pydantic_models.vessels import VesselModel


class ShipmentBuilder:
    def __init__(self, cleaned_data: Dict[str, Any]):
        self.data = cleaned_data

    def build(self) -> ShipmentDataModel:
        vessel = VesselModel(
            name=self.data.pop('vessel'),
            imo=self.data.pop('imo'),
            date=self.data.pop('date_built').date()
        )

        bills_of_lading = [
            BillOfLading(number=num, date=dt)
            for num, dt in zip(
                self.data.pop('bl_numbers'),
                self.data.pop('bl_dates')
            )
        ]

        meta = ShipmentMeta(
            counterparty=self.data.pop('counterparty'),
            contract_number=self.data.pop('contract_number'),
            surveyor_loadport=self.data.pop('surveyor_loadport'),
            surveyor_disport=self.data.pop('surveyor_disport')
        )

        return ShipmentDataModel(
            vessel=vessel,
            bills_of_lading=bills_of_lading,
            meta=meta,
            quantity_gross_kg=self.data.get('weight_metric', 0.0) * 1000,
            **self.data
        )


class ShipmentFactory:
    def __init__(self, extractor: FieldExtractor):
        self.extractor = extractor

    def create(
        self,
        df_summary: pd.DataFrame,
        df_details: pd.DataFrame,
        operator: str
    ) -> ShipmentDataModel:
        summary = df_summary['current'].to_dict()
        cleaned_data = {
            'vessel': clean_string(summary['vessel']).strip().title(),
            'imo': int(re.match(r'^(\d+)', str(summary['imo'])).group(1)) if re.match(r'^(\d+)', str(summary['imo'])) else -1,
            'date_built': parse_date(summary['date_built']) if isinstance(summary['date_built'], str) else summary['date_built'],
            'loadport_locality': summary['loadport_locality'],
            'loadport_country': summary['loadport_country'],
            'disport_locality': summary['disport_locality'],
            'disport_country': summary['disport_country'],
            'bl_numbers': df_details['bl_number'].astype(str).tolist(),
            'bl_dates': pd.to_datetime(df_details['bl_date']).dt.date.tolist(),
            'weight_metric': self.extractor._sum_with_fallback(df_details, 'weight_mt_in_vacuum', 'quantity_gross_kgs', lambda x: x / 1000),
            'sum_insured': float(summary.get('sum_insured', 0.0)),
            'ccy': summary.get('ccy', 'USD'),
            'operator': operator,
            'volume_bbl': self.extractor._sum_with_fallback(df_details, 'volume_bbl', 'quantity_net_kgs', lambda x: x / 1000),
            'basis_of_valuation': float(summary.get('basis_of_valuation', 0.0)),
            'disport_eta': DateService.resolve_eta(),
            'counterparty': summary.get('counterparty', 'Unknown'),
            'contract_number': summary.get('contract_number', 'Unknown'),
            'insured': clean_string(summary['insured']).title(),
            'subject_matter_insured': sort_and_concat(df_details['subject_matter_insured'].astype(str).tolist()),
            'surveyor_loadport': Surveyor.parse(summary.get('surveyor_loadport')),
            'surveyor_disport': Surveyor.parse(summary.get('surveyor_disport')),
            'deal_number': int(re.match(r'^(\d+)', str(summary['deal_number'])).group(1)) if re.match(r'^(\d+)', str(summary['deal_number'])) else -1
        }

        return ShipmentBuilder(cleaned_data).build()
