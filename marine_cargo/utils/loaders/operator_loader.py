# -*- coding: utf-8 -*-
"""
Created on Mon May  5 14:15:44 2025

@author: Aleksandr.Mikhailov
"""

from logistics.models import Operator
from marine_cargo.utils.abstract_loader import BaseCSVLoader


class OperatorLoader(BaseCSVLoader):
    def __init__(self):
        super().__init__(
            'logistics_operator.csv',
            ['first_name', 'last_name']
        )

    def save(self, data):
        Operator.objects.bulk_create(Operator(**row) for row in data)
