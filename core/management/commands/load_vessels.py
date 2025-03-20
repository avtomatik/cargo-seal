# -*- coding: utf-8 -*-
"""
Created on Wed Jan 15 17:42:06 2025

@author: Aleksandr.Mikhailov
"""

import csv

from django.conf import settings
from django.core.management.base import BaseCommand

from vessels.models import Vessel


class Command(BaseCommand):

    PATH_DATA = 'data'

    FILE_NAME = 'vessels_vessel.csv'

    FIELD_NAMES = ['name', 'imo', 'built_on']

    PATH = settings.BASE_DIR.joinpath(PATH_DATA)

    help = 'Populates DB with Vessels Data'

    def handle(self, *args, **options):

        with self.PATH.joinpath(self.FILE_NAME).open(encoding='utf8') as file:
            reader = csv.DictReader(file, fieldnames=self.FIELD_NAMES)
            next(reader)
            Vessel.objects.bulk_create(Vessel(**_) for _ in reader)

        self.stdout.write(
            self.style.SUCCESS('Successfully Populated DB with Vessels Data')
        )
