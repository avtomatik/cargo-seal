# -*- coding: utf-8 -*-
"""
Created on Wed Jan 29 14:13:17 2025

@author: Aleksandr.Mikhailov
"""

import csv

from django.conf import settings
from django.core.management.base import BaseCommand

from coverage.models import Coverage


class Command(BaseCommand):

    PATH_DATA = 'data'

    FILE_NAME = 'coverage_coverage.csv'

    FIELD_NAMES = [
        'debit_note',
        'date',
        'ordinary_risks_rate',
        'war_risks_rate',
        'policy_id',
        'shipment_id',
    ]

    PATH = settings.BASE_DIR.joinpath(PATH_DATA)

    help = 'Populates DB with Coverage Data'

    def handle(self, *args, **options):

        with open(self.PATH.joinpath(self.FILE_NAME), encoding='utf8') as file:
            reader = csv.DictReader(file, fieldnames=self.FIELD_NAMES)
            next(reader)
            Coverage.objects.bulk_create(Coverage(**_) for _ in reader)

        self.stdout.write(
            self.style.SUCCESS('Successfully Populated DB with Coverage Data')
        )
