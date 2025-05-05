# -*- coding: utf-8 -*-
"""
Created on Mon May  5 14:15:55 2025

@author: Aleksandr.Mikhailov
"""

from marine_cargo.utils.abstract_loader import BaseCSVLoader
from procurement.models import Party


class PartyLoader(BaseCSVLoader):
    def __init__(self):
        super().__init__(
            'procurement_party.csv',
            ['name', 'address']
        )

    def save(self, data):
        Party.objects.bulk_create(Party(**row) for row in data)
