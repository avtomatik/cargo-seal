# -*- coding: utf-8 -*-
"""
Created on Mon May  5 14:15:20 2025

@author: Aleksandr.Mikhailov
"""

import csv
import json

from django.conf import settings

from coverage.models import Coverage
from marine_cargo.utils.abstract_loader import BaseCSVLoader


class CoverageLoader(BaseCSVLoader):
    def __init__(self):
        super().__init__(
            file_name='coverage_coverage.csv',
            field_names=[
                'debit_note',
                'date',
                'ordinary_risks_rate',
                'war_risks_rate',
                'policy_id',
                'shipment_id'  # placeholder, will be replaced with UUID from JSON
            ]
        )
        self.json_file_name = 'uuid_dump.json'

    def load_data(self):
        json_path = settings.BASE_DIR / 'data' / self.json_file_name
        with json_path.open() as json_file:
            uuid_list = json.load(json_file)

        with self.file_path.open(encoding='utf8') as file:
            reader = csv.DictReader(file, fieldnames=self.field_names)
            next(reader)  # skip header

            return [
                {**row, 'shipment_id': uuid}
                for row, uuid in zip(reader, uuid_list)
            ]

    def save(self, data):
        Coverage.objects.bulk_create(Coverage(**row) for row in data)
