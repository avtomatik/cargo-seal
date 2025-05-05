# -*- coding: utf-8 -*-
"""
Created on Mon May  5 11:28:59 2025

@author: Aleksandr.Mikhailov
"""

import csv
from abc import ABC, abstractmethod

from django.conf import settings


class BaseCSVLoader(ABC):
    data_dir = settings.BASE_DIR / 'data'

    def __init__(self, file_name, field_names):
        self.file_path = self.data_dir / file_name
        self.field_names = field_names

    def load_data(self):
        with self.file_path.open(encoding='utf8') as file:
            reader = csv.DictReader(file, fieldnames=self.field_names)
            next(reader)  # Skip header
            return list(reader)

    @abstractmethod
    def save(self, data):
        pass

    def run(self):
        data = self.load_data()
        self.save(data)
