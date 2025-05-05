# -*- coding: utf-8 -*-
"""
Created on Mon May  5 11:35:52 2025

@author: Aleksandr.Mikhailov
"""

from django.core.management.base import BaseCommand


class CSVImportCommand(BaseCommand):
    loader_class = None  # Set in child classes

    def handle(self, *args, **options):
        if self.loader_class is None:
            self.stderr.write('No loader class defined.')
            return

        loader = self.loader_class()
        loader.run()
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully imported {self.loader_class.__name__}'
            )
        )
