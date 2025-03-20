# -*- coding: utf-8 -*-
"""
Created on Wed Jan 29 14:13:17 2025

@author: Aleksandr.Mikhailov
"""

import csv
import json

from django.conf import settings
from django.core.management.base import BaseCommand

from coverage.models import Coverage


class Command(BaseCommand):

    PATH_DATA = 'data'

    FILE_NAME_CSV = 'coverage_coverage.csv'

    FILE_NAME_JSON = 'uuid_dump.json'

    FIELD_NAME = 'shipment_id'

    FIELD_NAMES = [
        'debit_note',
        'date',
        'ordinary_risks_rate',
        'war_risks_rate',
        'policy_id',
        FIELD_NAME,  # Excessive; May Be Dropped
    ]

    PATH = settings.BASE_DIR.joinpath(PATH_DATA)

    help = 'Populates DB with Coverage Data'

    def handle(self, *args, **options):

        with self.PATH.joinpath(self.FILE_NAME_JSON).open() as file:
            uuid_strings = json.load(file)

        with self.PATH.joinpath(self.FILE_NAME_CSV).open(encoding='utf8') as file:
            reader = csv.DictReader(file, fieldnames=self.FIELD_NAMES)
            next(reader)

            coverage_data = [
                entry.update({self.FIELD_NAME: uuid_string}) or entry
                for entry, uuid_string in zip(reader, uuid_strings)
            ]

            Coverage.objects.bulk_create(Coverage(**_) for _ in coverage_data)

        self.stdout.write(
            self.style.SUCCESS('Successfully Populated DB with Coverage Data')
        )
