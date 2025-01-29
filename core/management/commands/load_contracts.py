# -*- coding: utf-8 -*-
"""
Created on Wed Jan 29 12:16:43 2025

@author: Aleksandr.Mikhailov
"""

import csv

from django.conf import settings
from django.core.management.base import BaseCommand

from procurement.models import Contract


class Command(BaseCommand):

    PATH_DATA = 'data'

    FILE_NAME = 'procurement_contract.csv'

    FIELD_NAMES = ['number', 'buyer_id', 'seller_id']

    PATH = settings.BASE_DIR.joinpath(PATH_DATA)

    help = 'Populates DB with Contracts Data'

    def handle(self, *args, **options):
        with open(self.PATH.joinpath(self.FILE_NAME), encoding='utf8') as file:
            reader = csv.DictReader(file, fieldnames=self.FIELD_NAMES)
            Contract.objects.bulk_create(Contract(**_) for _ in reader)

        self.stdout.write(
            self.style.SUCCESS('Successfully Populated DB with Contracts Data')
        )
