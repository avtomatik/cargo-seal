# -*- coding: utf-8 -*-
"""
Created on Mon Jan 27 16:31:02 2025

@author: Aleksandr.Mikhailov
"""

import csv

from django.conf import settings
from django.core.management.base import BaseCommand

from logistics.models import Location


class Command(BaseCommand):

    PATH_DATA = 'data'

    FILE_NAME = 'logistics_location.csv'

    FIELD_NAMES = ['locality', 'country']

    PATH = settings.BASE_DIR.joinpath(PATH_DATA)

    help = 'Populates DB with Locations Data'

    def handle(self, *args, **options):

        with open(self.PATH.joinpath(self.FILE_NAME), encoding='utf8') as file:
            reader = csv.DictReader(file, fieldnames=self.FIELD_NAMES)
            Location.objects.bulk_create(Location(**_) for _ in reader)

        self.stdout.write(
            self.style.SUCCESS('Successfully Populated DB with Locations Data')
        )
