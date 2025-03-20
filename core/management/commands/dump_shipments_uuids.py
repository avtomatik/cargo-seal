# -*- coding: utf-8 -*-
"""
Created on Thu Mar 20 11:40:07 2025

@author: Aleksandr.Mikhailov
"""

import json

from django.conf import settings
from django.core.management.base import BaseCommand

from logistics.models import Shipment


class Command(BaseCommand):

    PATH_DATA = 'data'

    FILE_NAME = 'uuid_dump.json'

    PATH = settings.BASE_DIR.joinpath(PATH_DATA)

    help = 'Dump UUIDs of Shipment instances'

    def handle(self, *args, **kwargs):

        uuids = Shipment.objects.values_list('id', flat=True)

        uuid_list = [str(uuid) for uuid in uuids]

        with open(self.PATH.joinpath(self.FILE_NAME), 'w') as json_file:
            json.dump(uuid_list, json_file)

        self.stdout.write(
            self.style.SUCCESS('Successfully dumped UUIDs to uuid_dump.json')
        )
