# -*- coding: utf-8 -*-
"""
Created on Mon May  5 14:56:25 2025

@author: Aleksandr.Mikhailov
"""

import json

from django.conf import settings


class UUIDDumper:
    def __init__(self, queryset, output_filename, data_dir='data'):
        self.queryset = queryset
        self.output_filename = output_filename
        self.output_path = settings.BASE_DIR / data_dir / output_filename

    def run(self):
        uuid_list = [
            str(uuid) for uuid in self.queryset.values_list('id', flat=True)
        ]

        with self.output_path.open('w') as f:
            json.dump(uuid_list, f)
