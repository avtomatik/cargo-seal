# -*- coding: utf-8 -*-
"""
Created on Mon May  5 14:15:28 2025

@author: Aleksandr.Mikhailov
"""

from marine_cargo.utils.abstract_loader import BaseCSVLoader
from vessels.models import Document


class DocumentLoader(BaseCSVLoader):
    def __init__(self):
        super().__init__(
            'vessels_document.csv',
            ['number', 'category', 'date', 'provider_id', 'vessel_id']
        )

    def save(self, data):
        Document.objects.bulk_create(
            (Document(**row) for row in data),
            ignore_conflicts=True
        )
