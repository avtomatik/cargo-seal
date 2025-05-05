# -*- coding: utf-8 -*-
"""
Created on Mon May  5 14:15:36 2025

@author: Aleksandr.Mikhailov
"""

from logistics.models import Location
from marine_cargo.utils.abstract_loader import BaseCSVLoader


class LocationLoader(BaseCSVLoader):
    def __init__(self):
        super().__init__(
            'logistics_location.csv',
            ['name', 'country']
        )

    def save(self, data):
        Location.objects.bulk_create(Location(**row) for row in data)
