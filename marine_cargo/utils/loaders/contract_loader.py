# -*- coding: utf-8 -*-
"""
Created on Mon May  5 14:15:03 2025

@author: Aleksandr.Mikhailov
"""

from marine_cargo.utils.abstract_loader import BaseCSVLoader
from procurement.models import Contract


class ContractLoader(BaseCSVLoader):
    def __init__(self):
        super().__init__(
            'procurement_contract.csv',
            ['number', 'buyer_id', 'seller_id']
        )

    def save(self, data):
        Contract.objects.bulk_create(Contract(**row) for row in data)
