# -*- coding: utf-8 -*-
"""
Created on Mon May  5 14:16:14 2025

@author: Aleksandr.Mikhailov
"""

from logistics.models import Shipment
from marine_cargo.utils.abstract_loader import BaseCSVLoader


class ShipmentLoader(BaseCSVLoader):
    def __init__(self):
        super().__init__(
            'logistics_shipment.csv',
            [
                'number',
                'date',
                'disport_eta',
                'volume_bbl',
                'weight_metric',
                'ccy',
                'unit',
                'subject_matter_insured',
                'contract_id',
                'disport_id',
                'loadport_id',
                'operator_id',
                'surveyor_disport_id',
                'surveyor_loadport_id',
                'sum_insured',
                'vessel_id'
            ]
        )

    def save(self, data):
        Shipment.objects.bulk_create(Shipment(**row) for row in data)
