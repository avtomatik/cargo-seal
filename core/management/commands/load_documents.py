# -*- coding: utf-8 -*-
"""
Created on Fri Jan 17 22:15:36 2025

@author: Aleksandr.Mikhailov
"""

import csv

from django.conf import settings
from django.core.management.base import BaseCommand

from vessels.models import Document


class Command(BaseCommand):

    PATH_DATA = 'data'

    FILE_NAME = 'vessels_document.csv'

    FIELD_NAMES = ['number', 'category', 'date', 'provider_id', 'vessel_id']

    PATH = settings.BASE_DIR.joinpath(PATH_DATA)

    help = 'Populates DB with Vessel Documents Data'

    def handle(self, *args, **options):

        with open(self.PATH.joinpath(self.FILE_NAME), encoding='utf8') as file:
            reader = csv.DictReader(file, fieldnames=self.FIELD_NAMES)
            next(reader)
            Document.objects.bulk_create(
                objs=(Document(**_) for _ in reader),
                ignore_conflicts=True
            )

        self.stdout.write(
            self.style.SUCCESS(
                'Successfully Populated DB with Vessel Documents Data')
        )
