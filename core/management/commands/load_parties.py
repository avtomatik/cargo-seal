# -*- coding: utf-8 -*-
"""
Created on Fri Jan 17 17:47:51 2025

@author: Aleksandr.Mikhailov
"""

import csv

from django.conf import settings
from django.core.management.base import BaseCommand

from procurement.models import Party


class Command(BaseCommand):

    PATH_DATA = 'data'

    FILE_NAME = 'procurement_party.csv'

    FIELD_NAMES = ['name', 'address']

    PATH = settings.BASE_DIR.joinpath(PATH_DATA)

    help = 'Populates DB with Counterparties Data'

    def handle(self, *args, **options):

        with open(self.PATH.joinpath(self.FILE_NAME), encoding='utf8') as file:
            reader = csv.DictReader(file, fieldnames=self.FIELD_NAMES)
            Party.objects.bulk_create(Party(**_) for _ in reader)

        self.stdout.write(
            self.style.SUCCESS(
                'Successfully Populated DB with Counterparties Data')
        )
