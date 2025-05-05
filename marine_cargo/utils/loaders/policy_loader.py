# -*- coding: utf-8 -*-
"""
Created on Mon May  5 14:16:06 2025

@author: Aleksandr.Mikhailov
"""

from coverage.models import Policy
from marine_cargo.utils.abstract_loader import BaseCSVLoader


class PolicyLoader(BaseCSVLoader):
    def __init__(self):
        super().__init__(
            'coverage_policy.csv',
            ['number', 'inception', 'expiry', 'insured_id', 'provider_id']
        )

    def save(self, data):
        Policy.objects.bulk_create(Policy(**row) for row in data)
