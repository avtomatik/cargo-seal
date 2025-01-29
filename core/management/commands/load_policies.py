# -*- coding: utf-8 -*-
"""
Created on Wed Jan 29 12:39:27 2025

@author: Aleksandr.Mikhailov
"""

import csv

from django.conf import settings
from django.core.management.base import BaseCommand

from coverage.models import Policy


class Command(BaseCommand):

    PATH_DATA = 'data'

    FILE_NAME = 'coverage_policy.csv'

    FIELD_NAMES = [
        'number',
        'date',
        'inception',
        'expiry',
        'insured_id',
        'provider_id'
    ]

    PATH = settings.BASE_DIR.joinpath(PATH_DATA)

    help = 'Populates DB with Policies Data'

    def handle(self, *args, **options):

        with open(self.PATH.joinpath(self.FILE_NAME), encoding='utf8') as file:
            reader = csv.DictReader(file, fieldnames=self.FIELD_NAMES)
            Policy.objects.bulk_create(Policy(**_) for _ in reader)

        self.stdout.write(
            self.style.SUCCESS('Successfully Populated DB with Policies Data')
        )
