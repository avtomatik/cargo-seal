# -*- coding: utf-8 -*-
"""
Created on Wed Jan 29 11:54:40 2025

@author: Aleksandr.Mikhailov
"""

import csv

from django.conf import settings
from django.core.management.base import BaseCommand

from logistics.models import Operator


class Command(BaseCommand):

    PATH_DATA = 'data'

    FILE_NAME = 'logistics_operator.csv'

    FIELD_NAMES = ['first_name', 'last_name']

    PATH = settings.BASE_DIR.joinpath(PATH_DATA)

    help = 'Populates DB with Operators Data'

    def handle(self, *args, **options):

        with open(self.PATH.joinpath(self.FILE_NAME), encoding='utf8') as file:
            reader = csv.DictReader(file, fieldnames=self.FIELD_NAMES)
            Operator.objects.bulk_create(Operator(**_) for _ in reader)

        self.stdout.write(
            self.style.SUCCESS('Successfully Populated DB with Operators Data')
        )
