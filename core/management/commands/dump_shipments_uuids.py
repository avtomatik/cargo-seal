# -*- coding: utf-8 -*-
"""
Created on Thu Mar 20 11:40:07 2025

@author: Aleksandr.Mikhailov
"""

from django.core.management.base import BaseCommand

from logistics.models import Shipment
from marine_cargo.utils.dumpers.uuid_dumper import UUIDDumper


class Command(BaseCommand):
    help = 'Dump UUIDs of Shipment instances'

    def handle(self, *args, **options):
        dumper = UUIDDumper(
            queryset=Shipment.objects.all(),
            output_filename='uuid_dump.json'
        )
        dumper.run()

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully dumped UUIDs to <{"uuid_dump.json"}>.'
            )
        )
