# -*- coding: utf-8 -*-
"""
Created on Mon May  5 11:38:13 2025

@author: Aleksandr.Mikhailov
"""

from marine_cargo.utils.abstract_loader import BaseCSVLoader
from vessels.models import Vessel


class VesselLoader(BaseCSVLoader):
    def __init__(self):
        super().__init__(
            'vessels_vessel.csv',
            ['name', 'imo', 'built_on']
        )

    def save(self, data):
        Vessel.objects.bulk_create(Vessel(**row) for row in data)
